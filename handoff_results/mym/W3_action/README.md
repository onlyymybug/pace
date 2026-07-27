## 运行说明

请参考run_commands.md.

# W3 文件说明

| 文件或目录 | 说明 |
| --- | --- |
| `raw_logs.csv` | 每个 action 样本、mode 和 deadline 的原始指标及 validator 结果 |
| `summary_metrics.csv` | 按 mode 和 deadline 汇总的 valid、correct、latency 和错误率 |
| `thermal_summary_metrics.csv` | 按性能模式汇总的温度指标 |
| `energy_batches.csv` | 每个性能模式物理批次的整机电池测量 |
| `failure_cases.md` | 未在 deadline 内得到正确 action 的逐行记录 |
| `W3_model_error_summary.md` | 去除 deadline 重复后的模型内容错误归类 |
| `run_commands.md` | W3 运行说明 |
| `one_page_memo.md` | W3 实验备忘录 |
| `raw_runner_logs/` | QNN runner 原始日志 |
| `runner_outputs/` | 生成文本、inference speed 和逐 token timestamp |

## CSV 字段说明

### `raw_logs.csv`

| 字段 | 说明 |
| --- | --- |
| `run_id` | 包含 sample、mode、budget、repeat 和 deadline 的行标识 |
| `timestamp_start`, `timestamp_end` | 对应物理生成的开始与结束时间 |
| `assignee`, `task_group`, `device_id` | 执行人、任务组和设备 |
| `runtime`, `model`, `quantization`, `backend` | Runtime、模型、量化配置和后端 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `strategy` | model mode、prefill、sequence length、budget 和 temperature 的组合描述 |
| `dataset`, `sample_id`, `repeat_id` | 数据集、样本和重复编号 |
| `prompt_tokens` | 输入 prompt token 数 |
| `target_output_tokens`, `action_budget_tokens` | 目标输出 budget 和 action budget；本实验中二者相同 |
| `actual_output_tokens` | 实际生成 token 数 |
| `ttft_ms` | Time to first token，单位毫秒 |
| `decode_latency_ms` | Decode 阶段耗时，单位毫秒 |
| `tpot_ms` | 平均每个输出 token 的耗时，单位毫秒 |
| `e2e_latency_ms` | 不含模型加载的端到端耗时，单位毫秒 |
| `energy_batch_id` | 关联 `energy_batches.csv` 的批次标识 |
| `energy_j` | 单行能耗；使用批次测量时为 `NA` |
| `start_temp_c`, `end_temp_c` | 运行前后 skin 温度 |
| `start_npu_temp_c`, `end_npu_temp_c` | 运行前后 NPU/type9 温度 |
| `thermal_status` | 运行端点观测到的最高 thermal status |
| `task_success` | 本 deadline 行是否得到正确且按时的 action |
| `deadline_ms` | 当前展开行使用的 deadline |
| `progress_satisfied` | 是否在 deadline 内得到正确 action |
| `error_type` | Parse、schema、wrong action、wrong argument、deadline 或 runtime 错误 |
| `notes` | 物理 run、validator 版本和错误消息等补充信息 |
| `action_text` | 模型生成的原始 action 文本 |
| `action_name` | Parser 提取的 action 名称 |
| `action_arguments` | Parser 提取并规范化的 arguments JSON |
| `gold_action`, `gold_arguments` | 标准 action 和标准 arguments |
| `action_valid` | 输出是否满足 JSON envelope 和所选 action schema |
| `action_correct` | Action 名称及参数是否与 gold 精确匹配 |
| `action_schema_error` | 合法 JSON 是否违反 function-call 外壳：顶层不是 object、顶层缺少/多出 `action` 或 `arguments`、`action` 不是 string，或 `arguments` 不是 object；JSON parse error、参数字段/类型/值错误不计入此列 |
| `time_to_valid_action_ms` | 从运行开始到形成完整 valid action 的时间；无 valid action 时为 `NA` |
| `invalid_action_rate` | 单行 invalid 指示值，valid 为 0，invalid 为 1 |
| `valid_under_deadline` | Valid action 是否在 deadline 内形成 |
| `correct_under_deadline` | Correct action 是否在 deadline 内形成 |

### `summary_metrics.csv`

| 字段 | 说明 |
| --- | --- |
| `runtime`, `model`, `backend` | 汇总组的 runtime、模型和后端 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `dataset`, `action_budget_tokens`, `deadline_ms` | 数据集、action budget 和 deadline |
| `num_rows`, `num_unique_runs` | 组内行数和唯一物理 run 数 |
| `runtime_success_rate` | 物理推理成功完成的比例 |
| `action_valid_rate` | 输出符合 action schema 的比例 |
| `action_correct_rate` | Action 与参数匹配 gold 的比例 |
| `valid_under_deadline_rate` | Deadline 内形成 valid action 的比例 |
| `correct_under_deadline_rate` | Deadline 内形成 correct action 的比例 |
| `invalid_action_rate` | `action_valid=false` 的比例 |
| `time_to_valid_action_mean_ms`, `time_to_valid_action_p50_ms`, `time_to_valid_action_p95_ms` | Valid action 到达时间的均值、p50 和 p95 |
| `e2e_mean_ms`, `e2e_p50_ms`, `e2e_p95_ms` | 端到端延迟的均值、p50 和 p95 |
| `decode_latency_mean_ms` | Decode latency 均值 |
| `actual_output_tokens_mean` | 实际输出 token 数均值 |
| `e2e_output_tokens_per_second_mean` | `actual_output_tokens / e2e_latency` 的组内均值；包含 TTFT，不与 W1 的逐 token visible speed 混用 |
| `parse_error_rate` | 严格 JSON parse error 比例 |
| `schema_error_rate` | 合法 JSON 违反 function-call 顶层外壳的比例；定义与 raw CSV 的 `action_schema_error` 一致 |
| `wrong_action_type_rate` | Action 名称错误比例 |
| `wrong_argument_rate` | 参数集合、类型或值错误比例 |
| `deadline_miss_rate` | 内容正确但超过 deadline 的比例 |
| `runtime_error_rate` | Runtime 失败比例 |

### `thermal_summary_metrics.csv`

| 字段 | 说明 |
| --- | --- |
| `task_group`, `runtime`, `model`, `backend` | 任务和运行环境分组 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `num_rows` | 包含 deadline 展开的原始行数 |
| `num_unique_physical_runs` | 去除 deadline 展开后的物理运行数 |
| `num_measured_physical_runs` | 具有完整温度端点的物理运行数 |
| `start_temp_mean_c`, `end_temp_mean_c` | Skin 起始和结束温度均值 |
| `skin_temp_delta_mean_c` | Skin 温升均值 |
| `max_observed_skin_temp_c` | 最高 skin 温度 |
| `start_npu_temp_mean_c`, `end_npu_temp_mean_c` | NPU 起始和结束温度均值 |
| `npu_temp_delta_mean_c` | NPU 温升均值 |
| `max_observed_npu_temp_c` | 最高 NPU 温度 |
| `max_thermal_status` | 组内最高 Android thermal status |

### `energy_batches.csv`

| 字段 | 说明 |
| --- | --- |
| `energy_batch_id` | 能耗批次标识 |
| `timestamp_start`, `timestamp_end` | 批次开始与结束时间 |
| `assignee`, `task_group`, `device_id` | 执行人、任务组和设备 |
| `runtime`, `model`, `quantization`, `backend` | Runtime、模型、量化配置和后端 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `physical_budget_tokens` | 批次实际运行的 action budget |
| `budget_execution_mode` | Budget 的物理执行方式 |
| `num_physical_runs` | 批次中的物理运行次数 |
| `start_counter_uah`, `end_counter_uah`, `delta_counter_uah` | 电池 charge counter 起点、终点和差值 |
| `start_voltage_mv`, `end_voltage_mv`, `average_voltage_mv` | 起始、结束和端点平均电压 |
| `duration_s` | 批次持续时间，单位秒 |
| `gross_energy_j` | 整机批次估算能耗，单位焦耳 |
| `average_power_w` | 批次平均功率，单位瓦 |
| `energy_per_physical_run_j` | Gross energy 除以物理运行数 |
| `counter_step_uah`, `counter_ticks` | 计数器步长和批次跨越步数 |
| `minimum_counter_ticks` | 可报告批次所需的最少步数 |
| `valid_for_reporting` | 是否达到报告门槛 |
| `measurement_status` | 测量状态或无效原因 |
| `notes` | 测量范围、电压聚合和单行能耗口径说明 |
