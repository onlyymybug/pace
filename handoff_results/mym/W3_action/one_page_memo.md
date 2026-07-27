# W3 One-page memo：Action / Function Calling

## 1. 实验设计

- Runtime / model：Android SM8750 真机，ExecuTorch + Qualcomm QNN HTP，Qwen2.5-3B-Instruct，temperature 0，hybrid，prefill AR 128。
- Dataset / samples：30 个自建 `tiny_schema_v2` 单步 function-calling 样例，覆盖 12 类 action、严格参数集合与 JSON 类型。
- Configs / repeats：Burst、Balanced、LowPowerSaver，96-token budget；每个 sample/mode 1 次物理 repeat，共 90 次生成。每次展开 2/5/10 s 三个 deadline，`raw_logs.csv` 共 270 行。

## 2. 验证指标

- Latency：e2e、decode latency、e2e output tokens/s、time-to-valid-action，均可用。
- Success：action 与 gold action/arguments 精确匹配得到 `action_correct`，再结合 deadline 得到 `correct_under_deadline`。
- Validity：严格验证单一 JSON、固定 `action`/`arguments` envelope、action schema、参数集合和 JSON 原生类型；`action_valid` 与语义正确分开，均可用。
- Energy：三个 mode 各有一个电池批次，可比较 gross energy/run 趋势；不是单 action、模型或 NPU 独立能耗。

## 3. 重点结果

| Mode          | Action valid / correct | Time-to-valid p50 / p95 | 2 s / 5 s / 10 s correct | Gross energy/run |
| ------------- | ---------------------: | ----------------------: | -----------------------: | ---------------: |
| Burst         |        73.33% / 36.67% |         1.582 / 2.425 s | 33.33% / 36.67% / 36.67% |         17.394 J |
| Balanced      |        73.33% / 36.67% |         2.471 / 3.871 s |  10.0% / 36.67% / 36.67% |         14.548 J |
| LowPowerSaver |        73.33% / 36.67% |         5.226 / 8.161 s |      0% / 20.0% / 36.67% |         15.464 J |

2 s deadline 需要 Burst；5 s 起 Balanced 已达到与 Burst 相同的任务成功率，gross energy/run 低 16.4%。三个 mode 输出内容相同，说明加速只能让已有正确 action 更早到达，不能修复模型质量；在本次批次测量中，Balanced 同时具有更低的整机 gross energy/run。

## 4. 失败情况

- Parser：1/30 输出连续两个 JSON 并含额外字符，严格解析失败。
- Timeout：2 s 下 11 个语义正确 action 中，Burst/Balanced/LowPowerSaver 分别有 10/3/0 个及时到达；5 s 下为 11/11/6。
- Wrong answer/action：19 个内容错误包括选错 action 4 个、参数值错误 9 个；典型问题是混淆日历/闹钟/计时器、忽略用户最后修正、时间或单位换算错误。
- Invalid action：仅 22/30 structurally valid；5 个主要类型/字段问题包括 boolean/integer 被写成字符串或生成额外字段。结构无效与语义错误存在交叉。
- Runtime：三个 mode 的 runtime success 都是 100%，没有 QNN runner failure。

## 5. 可信结论与 fallback sanity

可信的是当前真机和 30 个固定样例上的 JSON/schema validity、精确 action correctness、time-to-valid 与 deadline 排序；全部来自 `executorch_qnn`，没有混入 fallback。

Balanced 在 5 s 达到 sufficient speed、Burst 在 2 s 更优由逐样本 timing 直接支持。

能耗仅是批次趋势，每个 mode 只有 1 个能耗批次；数据又是自建 tiny schema、精确文本匹配较严格，因此对真实工具生态和其他模型的泛化仍是 sanity。

## 6. 如果再给一周，我会优先做什么

模型正确率偏低，需要放宽一些答案解析标准。

系统实验上扩大 schema 与样本、每 mode 至少 3 repeats、随机执行顺序。

## 7. 需要注意的问题

- `raw_logs.csv` 的 `energy_j` 全部为 `NA`，因为能耗按性能模式的物理批次测量；实际批次能耗记录在 `energy_batches.csv`。
- `task_success`、`progress_satisfied` 和 `correct_under_deadline` 在 W3 中含义相同，均表示 action 正确且在 deadline 内形成；同时保留三个字段是为了兼容任务书的公共 raw-log schema。
- W3 的 `schema_error` 专指 function-call 顶层外壳错误：合法 JSON 的顶层不是 object、缺少/多出 `action` 或 `arguments`，或这两个字段的类型不符合要求。参数字段、参数类型和参数值问题归入 `wrong_argument`；当前数据没有顶层外壳错误，因此 `schema_error_rate=0`。
- `e2e_output_tokens_per_second_mean` 按 `actual_output_tokens / e2e_latency` 计算，包含 TTFT，不等同于 W1 根据逐 token timestamp 计算的 visible tokens/s。
- 模型是 Qwen2.5-3B-Instruct；`Qwen2_5_1_5BQuantRecipe` 是被 3B 配置复用的量化 recipe 类名，不表示本实验使用了 1.5B 模型。
- `device_id` 保存的是易变化的 ADB `IP:port`，用于定位当次连接，不是稳定的物理设备 serial。
