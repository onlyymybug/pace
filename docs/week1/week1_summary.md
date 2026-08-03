# 第一周工作总结

## 1. 已完成工作

1. 完成了实验环境的配置。确认了手机的 ABI、SoC、HTP 版本和可用存储空间，配置了 ExecuTorch、Qualcomm QNN 动态库及模型运行目录；同时打通 WSL 通过 Windows ADB server（端口 5037）访问 USB 手机的流程，并对模型、runner、backend 和 tokenizer 的本地及手机端文件进行了校验。
2. 生成了 Qwen2.5-3B 和 BitNet-1.5B 的 PTE 文件及各自对应的 runner。两套模型均采用 Hybrid-1024 配置，并分别完成了 tokenizer、量化参数、QNN backend 和运行参数的配套验证。Qwen 使用 QNN 2.37 对应运行时，BitNet 当前使用与其 PTE 匹配的旧版 QNN 运行时。
3. 尝试生成同一个 runner 运行两个模型，但暂时没有成功。Qwen 和 BitNet 在 decoder 类型、模型输入元数据、tokenizer、量化参数及 QNN/ExecuTorch 构建版本方面存在差异。当前 QNN 2.37 runner 可以运行 Qwen，但运行 upstream BitNet PTE 时会因 `kv_cache_dtype was not detected from method inputs` 退出。因此正式实验仍使用各自匹配的 PTE、runner 和 backend，未将不兼容组合纳入结果。
4. 完成两个模型在 W1、W2、W3 数据集上的一次完整基线，共 132 次推理：W1 每模型 6 条，W2 和 W3 每模型各 30 条。132 次 runner 调用返回码均为 0，生成文本中未发现 Unicode replacement character。
5. 将实际使用的实验代码按模型整理到 `code/qwen/` 和 `code/bitnet/`；结果统一整理为 `results/w1|w2|w3/<model>/`，每组保留原始 runner 日志、runner 输出和 `summary_metrics.csv`。

## 2. 实验配置

| 项目 | Qwen | BitNet |
| --- | --- | --- |
| 模型 | Qwen2.5-3B-Instruct Hybrid-1024 | BitNet-1.5B Hybrid-1024 |
| 后端 | ExecuTorch + QNN HTP | ExecuTorch + QNN HTP |
| QNN 版本 | 2.37.0 | 模型对应的 2.28.0 运行时 |
| KV 更新 | ShiftPointer | ShiftPointer |
| 推理模式 | `eval_mode=1`，temperature=0 | `eval_mode=1`，temperature=0 |
| 最大序列长度 | 1024 | 1024 |
| W1/W2/W3 输出预算 | 512 / 128 / 96 | 512 / 128 / 96 |

W2 和 W3 根据实际 prompt token 数动态设置 `seq_len`，使输出预算能够在 1024 的最大总序列长度内执行。BitNet 使用手机 runner 的 token 计数校准表，减少主机 tokenizer 估算与 runner 实际计数之间的偏差。

## 3. 基线结果

表中的 E2E 是模型加载完成后的单次推理阶段耗时，不含模型加载。

### 3.1 W1 Streaming Chat

W1 没有正式质量评分器，因此只报告性能和运行状态。

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 6/6 | 未评分 | 56.50 ms | 18.509 s | 20.873 tok/s | 384.50 |
| Qwen | 6/6 | 未评分 | 93.17 ms | 22.280 s | 21.726 tok/s | 481.83 |

### 3.2 W2 Reasoning

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 30/30 | 1/30（3.3%） | 292.40 ms | 6.173 s | 20.969 tok/s | 123.27 |
| Qwen | 30/30 | 8/30（26.7%） | 129.07 ms | 6.090 s | 21.306 tok/s | 127.00 |

W2 的 deadline 统计如下，括号内为在 deadline 内完成且答案正确的数量。

| 模型 | 5 s | 10 s | 20 s | 30 s |
| --- | ---: | ---: | ---: | ---: |
| BitNet | 3/30（0） | 30/30（1） | 30/30（1） | 30/30（1） |
| Qwen | 0/30（0） | 30/30（8） | 30/30（8） | 30/30（8） |

### 3.3 W3 Action

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 30/30 | 4/30（13.3%） | 1642.40 ms | 3.489 s | 20.692 tok/s | 38.50 |
| Qwen | 30/30 | 0/30（0%） | 471.07 ms | 4.951 s | 21.207 tok/s | 95.00 |

W3 的 deadline 统计如下，括号内为在 deadline 内完成且 action 正确的数量。

| 模型 | 2 s | 5 s | 10 s |
| --- | ---: | ---: | ---: |
| BitNet | 0/30（0） | 26/30（4） | 30/30（4） |
| Qwen | 0/30（0） | 28/30（0） | 30/30（0） |

## 4. 结果分析

- **运行稳定性：** 两套匹配的模型/运行时组合均能完整执行三组数据，没有 runner 崩溃。Qwen 每次均成功恢复 4 个 QNN shard；BitNet 的旧 runner 日志格式不同，只显示缓存 delegate handle，不能据此逐 shard 计数，但所有样本均正常完成。
- **生成性能：** 两个模型的平均 decode 速度都约为 21 tok/s，Qwen 略高。TTFT 随 prompt 长度和任务模板变化明显，不能只用跨任务平均值判断模型优劣。
- **W1：** Qwen 平均生成长度更长，5/6 样本接近预算上限；BitNet 更常提前结束。因此 W1 的 E2E 差异主要受实际生成 token 数影响，不能直接解释为 BitNet 整体更快。仍需增加内容质量和重复率评估。
- **W2：** Qwen 的答案正确率高于 BitNet，但 26.7% 仍然较低。主要失败是模型没有严格输出指定的最终答案标记；BitNet 有 28/30 条缺少可解析答案标记，Qwen 有 22/30 条缺少标记。
- **W3：** 当前瓶颈主要是严格 JSON 协议遵循。BitNet 有 20 条 parse error，另有 3 条参数错误和 3 条 action 类型错误；Qwen 30 条均被严格解析器判为 parse error，常见现象是先输出 JSON，随后继续给解释、第二个 JSON 或下一轮内容。该结果说明模型能够生成内容，但尚不能稳定满足“只返回一个 JSON 对象”的执行要求。

## 5. 当前限制

1. 当前两套可用 runner 都不输出逐 token timestamp，因此只能得到 runner 直接报告的 TTFT、prefill/decode 速度和阶段级 E2E；暂时无法真实计算 TBT p50/p95、stall ratio 或 W3 的 time-to-valid-action。
2. runner 不提供可控的 `--htp_performance_mode` 参数，所以尚未完成 Always Max、Balanced、Low Power Saver 三种 QNN performance mode 的有效 A/B 对照。当前数据只能标记为默认模式。
3. 本轮完整对比通过 USB ADB 执行，手机处于充电状态，没有获得可信的放电能量数据；系统接口也未确认能单独暴露 NPU/HTP 功耗。因此结果中没有能耗指标。
4. 本轮没有按统一的基线温度、采样频率和冷却条件采集温度，故没有生成 `thermal_summary_metrics.csv`，也不对热稳定性作结论。
5. 当前是每个样本一次运行的功能性基线，尚未进行多轮重复、随机顺序和置信区间统计。

## 6. 下一步计划

- 先补齐可复现的温度采样：仅覆盖推理窗口，并统一推理前基线温度和冷却条件。
- 使用无线 ADB 配合外置 USB 功率计测整机功耗，记录空闲基线和推理能量；在无法得到 HTP rail 数据时明确将指标标为整机能耗。
- 为 runner 增加或获得逐 token timestamp 能力，再计算 W1 的 TBT/stall 和 W3 的 time-to-valid-action。
- 确认支持 HTP performance mode 的 runner/API 后，补做三种模式的重复实验。
- 加入 Llama-3.1-8B，生成适用于当前手机平台的 PTE 和配套 runner，并在相同的 W1/W2/W3 配置下与 Qwen2.5-3B、BitNet-1.5B 进行对比。
- 改进 W2 的答案抽取与 W3 的 JSON 截止策略，但同时保留严格评分，分别报告“原始协议正确率”和“首个 JSON 可执行率”。
- 每个配置至少重复 3 次，报告均值、离散程度以及 deadline 下的正确率。

## 7. 产物位置

- 实验代码：`code/qwen/`、`code/bitnet/`
- 数据集：`code/data/`
- W1 结果：`results/w1/qwen/`、`results/w1/bitnet/`
- W2 结果：`results/w2/qwen/`、`results/w2/bitnet/`
- W3 结果：`results/w3/qwen/`、`results/w3/bitnet/`

总体上，第一周已经完成了端侧 QNN 实验链路和两模型三任务的可运行基线。当前最需要补齐的是可控性能模式、规范化热测量和可信能耗测量。
