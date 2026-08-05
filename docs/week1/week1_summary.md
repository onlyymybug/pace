# 第一周工作总结

## 1. 已完成工作

1. **完成了实验环境的配置。** 确认了手机的 ABI、SoC、HTP 版本和可用存储空间，配置了 ExecuTorch、Qualcomm QNN 动态库、模型运行目录和 ADB 连接。当前实验通过 WSL 调用 Windows ADB server（端口 5037）访问手机，并对本地与手机端的模型、runner、backend 和 tokenizer 做了文件检查。
2. **生成了 Qwen2.5-3B 和 BitNet-1.5B 的 PTE 文件及各自对应的 runner。** 两个模型均生成了最大总序列长度为 1024 的 Hybrid PTE，并分别验证了 tokenizer、量化参数、runner、QNN backend 和手机端动态库的配套关系。Qwen 当前使用 QNN 2.37 运行时，BitNet 使用与现有 PTE 匹配的 QNN 2.28 运行时。
3. **尝试生成同一个 runner 运行两个模型，但暂时没有成功。** Qwen 和 BitNet 在 decoder 类型、模型输入元数据、KV cache 信息、tokenizer、量化参数和 QNN/ExecuTorch 构建版本上存在差异。QNN 2.37 runner 能运行 Qwen，但加载 upstream BitNet PTE 时会因 `kv_cache_dtype was not detected from method inputs` 退出。这个结果说明当前 PTE 与统一 runner 的接口还未对齐，不能仅替换模型路径实现共用。因此正式实验仍采用两套相互匹配的 PTE、runner 和 backend。
4. **完成了两模型、三数据集的功能性基线实验。** Qwen 和 BitNet 分别运行 W1、W2、W3：W1 每个模型 6 条，W2 和 W3 每个模型各 30 条，共 132 次推理。所有正式实验的 runner 返回码均为 0，未发现 Unicode replacement character。
5. **整理了可复用代码和真实实验结果。** 实验代码按模型放在 `code/qwen/` 和 `code/bitnet/`，数据集放在 `code/data/`；正式结果按 `results/w1|w2|w3/<model>/` 保存，只保留实际产生的 runner 日志、runner 输出和 `summary_metrics.csv`。

## 2. 实验平台与统一设置

### 2.1 硬件与软件环境

| 项目 | 设置 |
| --- | --- |
| 手机 | OPPO PLQ110 |
| SoC | Snapdragon 8 Elite / SM8750 |
| HTP | v79 |
| 系统与 ABI | Android 16，arm64-v8a |
| 推理框架 | ExecuTorch + Qualcomm QNN HTP |
| 连接方式 | WSL 调用 Windows ADB server，USB 连接手机 |

选择同一台手机运行两个模型，是为了控制 SoC、内存、系统版本等硬件变量。USB ADB 在第一周主要用于保证长时间批量实验的连接稳定性；这一选择适合先验证功能，但会影响电池能耗测量，因此本轮未报告能耗结论。

### 2.2 模型设置

| 设置 | Qwen2.5-3B | BitNet-1.5B | 选择原因 |
| --- | --- | --- | --- |
| PTE 模式 | Hybrid | Hybrid | 同时使用 prompt processor 和 token generator，适合端侧自回归生成 |
| 最大总序列长度 | 1024 | 1024 | 保证 prompt 与输出预算能够放入同一个序列上限，并统一比较范围 |
| `eval_mode` | 1 | 1 | 使用当前 PTE 和 runner 验证过的推理模式 |
| KV updater | ShiftPointer | ShiftPointer | 与生成 PTE 时的 KV cache 更新方式保持一致 |
| temperature | 0 | 0 | 关闭采样随机性，使第一轮基线可重复并便于逐样本比较 |
| prefill AR length | 128 | 32 | 采用各自 PTE 构建时固定并验证过的配置，不强行跨模型修改 |
| QNN runtime | 2.37 | 2.28 | 每个 PTE 使用与其构建版本匹配且已验证可运行的 runner/backend |

Qwen 运行时显式设置 `QNN_OP_PACKAGE_PATHS=""`，原因是匹配版本的 backend 在变量未设置时会尝试默认 T-MAN 路径；本实验不需要 T-MAN op package。两套模型没有混用 tokenizer、量化参数、PTE 或 backend。

### 2.3 测量口径

- **TTFT：** 从推理开始到第一个 token 的时间，由 runner 的 PyTorchObserver 阶段记录解析得到。
- **E2E：** 模型加载完成后的单次推理耗时，不包含模型加载时间。
- **Decode speed：** runner 报告的 token generation 速度。
- **正确率：** W2 比较解析后的最终答案；W3 使用严格 JSON/action schema 校验。
- **Deadline：** 根据上述 E2E 判断样本是否在规定时间内完成，并同时统计 deadline 内完成且正确的样本数。

本轮每个样本只运行一次，目的是先验证整条执行、解析和评分链路，而不是形成具有置信区间的最终性能结论。

## 3. 已进行的实验及结果

### 3.1 模型与 runtime 兼容性实验

首先分别用对应 runner 加载 Qwen 和 BitNet PTE，再尝试用新的 QNN 2.37 runner 加载两种模型。

- Qwen PTE 与 QNN 2.37 runner/backend 配套时可以正常加载、恢复 4 个 QNN shard 并生成连贯文本。
- BitNet PTE 与原有 QNN 2.28 runner/backend 配套时可以完成 W1、W2 和 W3。
- 新 QNN 2.37 runner 加载 upstream BitNet PTE 时返回 134，并报告缺少 `kv_cache_dtype` 输入元数据。

**结论：** 两个模型都能在手机上运行，但当前只能使用各自对应的 runtime。统一 runner 失败发生在模型加载/接口识别阶段，不是数据集、prompt 或量化 scale/offset 引起的，因此没有通过随意修改量化参数或重新导出模型来解决。

### 3.2 W1 Streaming Chat

**实验设置：** 每个模型运行 6 条聊天 prompt；输出预算为 512 tokens；temperature 为 0；动态设置总 `seq_len`，使其能够容纳实际 prompt 和输出预算。

**选择原因：** 512-token 预算用于观察较长回复下的首 token 延迟、持续生成速度、提前 EOS 和接近序列上限时的行为。W1 没有标准答案，因此本轮不计算正确率，只报告运行和性能数据。

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 6/6 | 未评分 | 56.50 ms | 18.509 s | 20.873 tok/s | 384.50 |
| Qwen | 6/6 | 未评分 | 93.17 ms | 22.280 s | 21.726 tok/s | 481.83 |

**结论：** 两个模型的 decode 速度接近，Qwen 略高。BitNet 的平均 TTFT 更低，但更常提前结束；Qwen 生成更长，5/6 个样本接近预算上限。因此不能只根据 E2E 判断 BitNet 整体更快，因为两者实际生成 token 数不同。W1 目前只能说明推理链路和长文本生成可用，不能说明哪一个模型的回答质量更好。

### 3.3 W2 Reasoning

**实验设置：** 每个模型运行 30 道推理题；reasoning budget 为 128 tokens；temperature 为 0；deadline 为 5、10、20、30 秒。总 `seq_len` 根据 prompt token 数和 128-token 预算动态设置。BitNet 使用手机 runner 的 prompt token 校准表，修正主机 tokenizer 估算与 runner 实际计数之间的偏差。

**选择原因：** 128 tokens 是本轮规定的 reasoning budget，用于限制端侧推理开销并比较 deadline 下的有效正确率。动态 `seq_len` 可以确保 128 是输出预算，而不是把 prompt 与输出合计误当成 128。最终答案使用固定标记解析，是为了让评分自动化且可复核。

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 30/30 | 1/30（3.3%） | 292.40 ms | 6.173 s | 20.969 tok/s | 123.27 |
| Qwen | 30/30 | 8/30（26.7%） | 129.07 ms | 6.090 s | 21.306 tok/s | 127.00 |

括号内为在 deadline 内完成且答案正确的数量。

| 模型 | 5 s | 10 s | 20 s | 30 s |
| --- | ---: | ---: | ---: | ---: |
| BitNet | 3/30（0） | 30/30（1） | 30/30（1） | 30/30（1） |
| Qwen | 0/30（0） | 30/30（8） | 30/30（8） | 30/30（8） |

**结论：** 两个模型均能稳定完成全部题目，但正确率明显不同，Qwen 高于 BitNet。主要失败不全是算错：BitNet 有 28/30 条、Qwen 有 22/30 条没有生成评分器要求的最终答案标记，导致无法解析。10 秒及以上 deadline 对本轮样本已足够宽松，下一步更需要改善答案格式遵循和推理质量，而不是单纯放宽 deadline。

### 3.4 W3 Action

**实验设置：** 每个模型运行 30 条 action 请求；action budget 为 96 tokens；temperature 为 0；deadline 为 2、5、10 秒。prompt 中包含完整 action schema，输出使用严格解析器，要求只返回一个 JSON 对象，action 名称、参数集合、参数类型和值都必须正确。

**选择原因：** W3 面向可执行的手机操作，格式错误的内容不能直接交给下游系统，所以正式指标采用严格评分，而不是只判断输出中是否出现过一个看似正确的 JSON。96-token 预算用于限制 action 生成成本，同时足以容纳目标 JSON。

| 模型 | 成功运行 | 正确率 | 平均 TTFT | 平均 E2E | 平均 decode | 平均生成 tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BitNet | 30/30 | 4/30（13.3%） | 1642.40 ms | 3.489 s | 20.692 tok/s | 38.50 |
| Qwen | 30/30 | 0/30（0%） | 471.07 ms | 4.951 s | 21.207 tok/s | 95.00 |

括号内为在 deadline 内完成且 action 正确的数量。

| 模型 | 2 s | 5 s | 10 s |
| --- | ---: | ---: | ---: |
| BitNet | 0/30（0） | 26/30（4） | 30/30（4） |
| Qwen | 0/30（0） | 28/30（0） | 30/30（0） |

**结论：** 当前主要瓶颈是输出协议遵循，而不是 runner 稳定性。BitNet 有 20 条 parse error、3 条参数错误和 3 条 action 类型错误；Qwen 的 30 条输出均被严格解析器判为 parse error。Qwen 常先生成一个 JSON，随后继续输出解释、第二个 JSON 或下一轮内容，因而在“只能返回一个 JSON”的严格规则下失败。5 秒 deadline 已覆盖大多数样本，但只有格式和语义同时正确的结果才具有实际执行价值。

## 4. 总体结论

1. 手机端 ExecuTorch + QNN 推理链路已经打通，两套匹配的模型/runtime 组合能够稳定完成三类数据集。
2. 两个模型平均 decode 速度均约为 21 tok/s，性能差异小于输出长度、prompt 长度和格式遵循造成的任务差异。
3. Qwen 在 W2 上的正确率高于 BitNet；W3 中两者都需要改进结构化输出，Qwen 尤其需要在生成首个完整 JSON 后立即停止。
4. 当前数据是功能性单次基线，适合确认系统可运行和定位主要问题，不足以作为不同模型能效、热稳定性或统计性能优劣的最终结论。
5. 一个 runner 运行两个模型的目标尚未实现。现有证据指向 PTE 输入元数据和构建版本兼容问题，而不是简单的命令行参数问题。

## 5. 未完成内容与原因分类

| 未完成内容 | 原因性质 | 原因与说明 |
| --- | --- | --- |
| 逐 token timestamp、TBT p50/p95、stall ratio | 客观技术原因 | 当前两个可用 runner 都不输出逐 token 时间，必须修改或重建 runner，或获得带时间戳能力的 runtime。 |
| 三种 HTP performance mode 对照 | 客观技术原因 | runner 没有可控的 `--htp_performance_mode` 接口，当前版本只能记录默认模式，计划使用更新版本尝试。 |
| NPU/HTP 独立能耗 | 客观技术原因 | Android 接口未暴露经过验证的 HTP 独立 power rail，且电池计数器粒度较粗。现阶段最多测量整机能耗，不能声称得到 NPU 独立功耗。 |
| 本轮整机能耗结果 | 混合原因 | 为保证批量实验稳定性使用了 USB ADB，手机处于供电或充电状态。USB 供电影响放电计数是客观限制；第一周优先完成功能基线、未改用无线 ADB 和外置功率计则是实验安排上的主观选择。 |
| 统一条件的温度结果 | 主观实验安排 | 正式批次没有执行基线温度、推理窗口采样和冷却控制。手机能够读取温度，但本轮优先处理模型/runtime 兼容和全量跑通，因此未纳入正式流程。 |
| 多次重复和置信区间 | 主观实验安排 | 每个样本目前只运行一次。第一周将功能验证置于统计稳定性之前，后续至少重复 3 次并随机化运行顺序。 |
| W1 自动质量评分 | 混合原因 | 当前 W1 数据没有标准答案或已确认的质量评分器，这是数据方面的客观限制；仍可设计人工评分、重复率和一致性指标，但第一周尚未实施。 |
| Llama-3.1-8B 对照 | 主观范围安排 | 尚未生成和验证对应 PTE/runtime。第一周先完成 Qwen 与 BitNet 基线，Llama 纳入下一阶段。 |

## 6. 下一步计划

1. 加入 Llama-3.1-8B，生成适用于 SM8750/HTP v79 的 PTE 和配套 runner，并在相同 W1/W2/W3 设置下与 Qwen2.5-3B、BitNet-1.5B 对比。
2. 调查 BitNet PTE 的 `kv_cache_dtype` 元数据和 ExecuTorch/QNN 构建差异，继续验证统一 runner 的可行性。
3. 先把温度采样加入正式脚本，只在推理窗口采样，并统一基线温度、冷却条件和采样周期。
4. 使用无线 ADB减少数据线干扰，配合外置 USB 功率计记录整机输入功率、空闲基线和推理能量；结果明确标注为整机能耗，而不是 NPU 独立能耗。
5. 获得或构建支持逐 token timestamp 和 HTP performance mode 的 runner，再补做 TBT/stall 以及 Always Max、Balanced、Low Power Saver 对照。
6. 每个配置至少重复 3 次并随机化模型/任务顺序，报告均值、离散程度和 deadline 内正确率。
7. W2 同时报告“内容答案正确率”和“严格格式正确率”；W3 保留严格评分，并增加“首个 JSON 可解析率”作为诊断指标，但不以宽松指标替代正式正确率。

## 7. 产物位置

- 实验代码：`code/qwen/`、`code/bitnet/`
- 数据集：`code/data/`
- W1 结果：`results/w1/qwen/`、`results/w1/bitnet/`
- W2 结果：`results/w2/qwen/`、`results/w2/bitnet/`
- W3 结果：`results/w3/qwen/`、`results/w3/bitnet/`
