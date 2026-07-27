## 运行说明

请参考run_commands.md.

# W2 文件说明

| 文件或目录 | 说明 |
| --- | --- |
| `raw_logs.csv` | 每个 reasoning 样本、mode、budget 和 deadline 的原始指标 |
| `summary_metrics.csv` | 按 mode、budget 和 deadline 汇总的正确率、错误与延迟 |
| `thermal_summary_metrics.csv` | 按 mode 和 reasoning budget 汇总的温度指标 |
| `energy_batches.csv` | 每个 mode/budget 物理批次的整机电池测量 |
| `failure_cases.md` | Parse error、wrong answer 和 deadline miss 的逐行记录 |
| `run_commands.md` | W2 运行说明 |
| `one_page_memo.md` | W2 实验备忘录 |
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
| `target_output_tokens`, `reasoning_budget_tokens` | 目标输出 budget 和 reasoning budget；本实验中二者相同 |
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
| `task_success` | 本 deadline 行是否正确且按时完成 |
| `deadline_ms` | 当前展开行使用的 deadline，单位毫秒 |
| `progress_satisfied` | 是否得到 deadline 内正确答案 |
| `error_type` | `parse_error`、`wrong_answer`、`deadline_miss`、runtime error 或 `none` |
| `notes` | 测量和运行补充信息 |
| `answer`, `gold_answer` | Parser 提取答案和标准答案 |
| `answer_correct` | 提取答案是否与 gold 等价 |
| `correct_under_deadline` | 答案正确且 e2e 不超过 deadline |
| `output_truncated` | 输出是否因达到 token budget 截断 |
| `energy_per_correct_answer_j` | 行级留空字段；汇总值在 `summary_metrics.csv` 中计算 |

### `summary_metrics.csv`

| 字段 | 说明 |
| --- | --- |
| `runtime`, `model`, `backend` | 汇总组的 runtime、模型和后端 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `reasoning_budget_tokens`, `deadline_ms` | Reasoning budget 和 deadline |
| `num_rows`, `num_unique_runs` | 组内行数和唯一物理 run 数 |
| `parse_error_truncated_count` | 截断输出中的 parse error 数 |
| `parse_error_untruncated_count` | 未截断输出中的 parse error 数 |
| `wrong_answer_count` | 成功解析但答案错误的行数 |
| `deadline_miss_count` | 答案正确但超时的行数 |
| `other_errors_count` | 不属于上述类别的错误数 |
| `runtime_success_rate` | 物理推理成功完成的比例 |
| `answer_correct_rate` | 不考虑 deadline 的答案正确率 |
| `correct_under_deadline_rate` | Deadline 内答案正确率 |
| `e2e_mean_ms`, `e2e_p50_ms`, `e2e_p95_ms` | 端到端延迟的均值、p50 和 p95 |
| `decode_latency_mean_ms` | Decode latency 均值 |
| `actual_output_tokens_mean` | 实际输出 token 数均值 |
| `e2e_output_tokens_per_second_mean` | `actual_output_tokens / e2e_latency` 的组内均值；包含 TTFT，不与 W1 的逐 token visible speed 混用 |
| `energy_per_correct_answer_j` | 对应物理批次 gross energy 除以 deadline 内正确答案数 |

### `thermal_summary_metrics.csv`

| 字段 | 说明 |
| --- | --- |
| `task_group`, `runtime`, `model`, `backend` | 任务和运行环境分组 |
| `performance_mode` | 性能模式简称 |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名 |
| `reasoning_budget_tokens` | 当前汇总组的 reasoning budget |
| `num_rows` | 组内包含 deadline 展开的原始行数 |
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
| `physical_budget_tokens` | 批次实际运行的 reasoning budget |
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
