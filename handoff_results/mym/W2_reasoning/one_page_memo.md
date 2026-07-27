# W2 One-page memo：Reasoning

## 1. 实验设计

- Runtime / model：Android SM8750 真机，ExecuTorch + Qualcomm QNN HTP，Qwen2.5-3B-Instruct，temperature 0，hybrid，prefill AR 128。
- Dataset / samples：24 个 GSM8K ，6 个 Math hard 数学推理样例，要求以规范标量 final answer 结尾。
- Configs / repeats：Burst、Balanced、LowPowerSaver × 128/256/512 output budgets；每个 sample/config 1 次物理 repeat，共 270 次生成。每次生成展开 5/10/20/30 s 四个 deadline，`raw_logs.csv` 共 1080 行。

## 2. 验证指标

- Latency：e2e、decode latency、tokens/s，均可用；模型加载不计入 e2e。
- Success：严格 parser 提取最终标量，与 gold 比较 `answer_correct`，再结合 e2e 得到 `correct_under_deadline`，均可用。
- Validity：W2 不做 action schema；规范 final-answer 是否可解析是输出有效性门槛。
- Energy：按物理 mode/budget 批次测得 gross battery energy，并除以 deadline 内正确数；可做批次级 `energy_per_correct_answer_j` 比较，但不是 NPU/模型独立能耗。

## 3. 重点结果

| Deadline |       Burst 最优 | Balanced 最优 | LowPowerSaver 最优 | 任务级选择                                      |
| -------: | ---------------: | ------------: | -----------------: | ----------------------------------------------- |
|      5 s |           23.33% |         3.33% |                 0% | Burst-128：同等最高成功率下 energy/correct 最低 |
|     10 s | 60.0%（256/512） |        33.33% |              3.33% | Burst-256：111.3 J/correct                      |
|     20 s |    76.67%（512） |        63.33% |             33.33% | 若优先最高成功率，选 Burst-512                  |
|     30 s |    76.67%（512） | 76.67%（512） |             56.67% | Balanced-512：77.2 J/correct，比 Burst 低 23.7% |

离线 answer correctness 由 budget 决定：128/256/512 分别为 26.67%/60.0%/76.67%，三个 mode 内容一致。在某些情况下可以使用balanced 达到和 burst 相同的结果，并节省能耗。

## 4. 失败情况

- Parser：128/256/512 budget 分别有 21/9/2 个截断 parse error；主要因为 budget 用尽前没有输出规范 final answer。
- Timeout：短 deadline 下 Balanced/LowPowerSaver 的正确答案未及时到达；例如 10 s 最佳成功率仅 33.33%/3.33%，Burst 为 60.0%。
- Wrong answer：三个 budget 分别有 1/3/5 个完整但错误的答案；增加 budget 减少截断，却不能消除模型推理错误。
- Runtime：所有 mode/budget 的 runtime success 都是 100%，未发现 QNN runner failure。

## 5. 可信结论与 fallback sanity

可信的是当前真机与 24 个 GSM8K、6 个 MATH hard 样例上的 latency、parser、answer correctness、correct-under-deadline，以及短 deadline 用 Burst、30 s 可用 Balanced-512 的相对结论；全部来自 `executorch_qnn` 主线。

fallback sanity 如下：

Energy只支持初步趋势，因为是整机批次测量。

每配置仅 1 次物理 repeat、执行顺序未随机化。

## 6. 如果再给一周，我会优先做什么

优先复测随机 mode 顺序。

扩大 MATH hard。

## 7. 需要注意的问题

- `raw_logs.csv` 的 `energy_j` 全部为 `NA`，因为能耗按 mode/budget 物理批次测量；实际批次能耗记录在 `energy_batches.csv`。
- W2 raw CSV 的 `energy_per_correct_answer_j` 全部为 `NA`；真正的 `energy_per_correct_answer_j` 只在 `summary_metrics.csv` 中用批次 gross energy 和对应 deadline 内的正确答案数计算。
- `task_success`、`progress_satisfied` 和 `correct_under_deadline` 在 W2 中含义相同，均表示答案正确且在 deadline 内完成；同时保留三个字段是为了兼容任务书的公共 raw-log schema。
- `e2e_output_tokens_per_second_mean` 按 `actual_output_tokens / e2e_latency` 计算，包含 TTFT，不等同于 W1 根据逐 token timestamp 计算的 visible tokens/s。
- 模型是 Qwen2.5-3B-Instruct；`Qwen2_5_1_5BQuantRecipe` 是被 3B 配置复用的量化 recipe 类名，不表示本实验使用了 1.5B 模型。
- `device_id` 是易变化的 ADB `IP:port`。Always-max/Balanced 与 LowPowerSaver 使用了不同端口，因此端口不能作为物理设备身份；跨 mode 比较要求这些连接指向同一台 SM8750 设备。
