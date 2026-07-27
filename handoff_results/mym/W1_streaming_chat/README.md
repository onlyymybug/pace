## 运行说明

请参考run_commands.md.

## W1 文件说明

| 文件或目录                      | 说明                                                     |
| ------------------------------- | -------------------------------------------------------- |
| `raw_logs.csv`                | 每次 streaming 物理运行的原始指标与元数据                |
| `summary_metrics.csv`         | 按 runtime、model、mode 和 dataset 汇总的 streaming 指标 |
| `thermal_summary_metrics.csv` | 按性能模式汇总的 skin/NPU 温度与 thermal status          |
| `energy_batches.csv`          | 按性能模式记录的整机电池批次测量                         |
| `failure_cases.md`            | token timing 不可信或未满足平均阅读阈值的运行            |
| `run_commands.md`             | W1 运行说明                                              |
| `one_page_memo.md`            | W1 实验备忘录                                            |
| `raw_runner_logs/`            | QNN runner 原始日志                                      |
| `runner_outputs/`             | 生成文本、inference speed 和逐 token timestamp           |

## CSV 字段说明

### `raw_logs.csv`

| 字段                                                  | 说明                                                                   |
| ----------------------------------------------------- | ---------------------------------------------------------------------- |
| `run_id`                                            | 单次运行标识                                                           |
| `timestamp_start`, `timestamp_end`                | 运行开始与结束的 ISO 时间                                              |
| `assignee`, `task_group`                          | 执行人和任务组                                                         |
| `device_id`                                         | ADB 设备标识                                                           |
| `runtime`, `model`, `quantization`, `backend` | Runtime、模型、量化配置和执行后端                                      |
| `performance_mode`                                  | 实验使用的性能模式简称                                                 |
| `htp_performance_mode`                              | QNN HTP 性能模式数值                                                   |
| `htp_performance_mode_name`                         | QNN HTP 性能模式枚举名                                                 |
| `strategy`                                          | model mode、prefill、sequence length、budget 和 temperature 的组合描述 |
| `dataset`, `sample_id`, `repeat_id`             | 数据集、样本和重复编号                                                 |
| `prompt_tokens`                                     | 输入 prompt token 数                                                   |
| `target_output_tokens`                              | 目标输出 token budget                                                  |
| `actual_output_tokens`                              | 实际生成 token 数                                                      |
| `ttft_ms`                                           | Time to first token，单位毫秒                                          |
| `decode_latency_ms`                                 | Decode 阶段耗时，单位毫秒                                              |
| `tpot_ms`                                           | 平均每个输出 token 的耗时，单位毫秒                                    |
| `e2e_latency_ms`                                    | 不含模型加载的端到端耗时，单位毫秒                                     |
| `energy_batch_id`                                   | 关联`energy_batches.csv` 的批次标识                                  |
| `energy_j`                                          | 单行能耗；批次测量时为`NA`                                           |
| `start_temp_c`, `end_temp_c`                      | 运行前后 skin 温度，单位摄氏度                                         |
| `start_npu_temp_c`, `end_npu_temp_c`              | 运行前后 NPU/type9 温度，单位摄氏度                                    |
| `thermal_status`                                    | 运行端点观测到的最高 Android thermal status                            |
| `task_success`                                      | 本行是否具有可信 token timing                                          |
| `deadline_ms`                                       | W1 未设置 deadline，值为`NA`                                         |
| `progress_satisfied`                                | p95 TBT 是否满足平均阅读阈值                                           |
| `error_type`                                        | 运行、输出或 timing 错误类型；无错误为`none`                         |
| `notes`                                             | prompt、测量来源、归档路径和温度传感器等补充信息                       |
| `tbt_p50_ms`, `tbt_p95_ms`                        | 相邻可见 token 间隔的 p50 和 p95，单位毫秒                             |
| `stall_ratio`                                       | 超过 stall 阈值的 token 间隔占比                                       |
| `visible_tokens_per_second`                         | 按逐 token timestamp 计算的可见输出速度                                |

### `summary_metrics.csv`

| 字段                                                             | 说明                                             |
| ---------------------------------------------------------------- | ------------------------------------------------ |
| `runtime`, `model`, `backend`                              | 汇总组的 runtime、模型和后端                     |
| `performance_mode`                                             | 性能模式简称                                     |
| `htp_performance_mode`, `htp_performance_mode_name`          | HTP 模式数值和枚举名                             |
| `dataset`, `target_output_tokens`                            | 数据集和目标 token budget                        |
| `num_rows`, `num_unique_runs`                                | 组内行数和唯一 run 数                            |
| `task_success_rate`                                            | `task_success=true` 的比例                     |
| `progress_satisfied_rate`                                      | 达到平均阅读阈值的比例                           |
| `ttft_mean_ms`, `ttft_p50_ms`, `ttft_p95_ms`               | TTFT 的均值、p50 和 p95                          |
| `e2e_mean_ms`, `e2e_p50_ms`, `e2e_p95_ms`                  | 端到端延迟的均值、p50 和 p95                     |
| `decode_latency_mean_ms`                                       | Decode latency 均值                              |
| `actual_output_tokens_mean`                                    | 实际输出 token 数均值                            |
| `visible_tokens_per_second_mean`                               | 可见 tokens/s 均值                               |
| `tbt_p50_mean_ms`, `tbt_p95_mean_ms`                         | 各运行 TBT p50/p95 的组内均值                    |
| `stall_ratio_mean`                                             | Stall ratio 均值                                 |
| `pass_4_8_tps_rate`, `pass_6_tps_rate`, `pass_10_tps_rate` | 分别通过 4.8、6、10 tokens/s 对应 TBT 阈值的比例 |

### `thermal_summary_metrics.csv`

| 字段                                                    | 说明                             |
| ------------------------------------------------------- | -------------------------------- |
| `task_group`, `runtime`, `model`, `backend`     | 任务和运行环境分组               |
| `performance_mode`                                    | 性能模式简称                     |
| `htp_performance_mode`, `htp_performance_mode_name` | HTP 模式数值和枚举名             |
| `num_rows`                                            | 组内原始 CSV 行数                |
| `num_unique_physical_runs`                            | 去除 deadline 展开后的物理运行数 |
| `num_measured_physical_runs`                          | 具有完整温度端点的物理运行数     |
| `start_temp_mean_c`, `end_temp_mean_c`              | Skin 起始与结束温度均值          |
| `skin_temp_delta_mean_c`                              | Skin 温升均值                    |
| `max_observed_skin_temp_c`                            | 观测到的最高 skin 温度           |
| `start_npu_temp_mean_c`, `end_npu_temp_mean_c`      | NPU 起始与结束温度均值           |
| `npu_temp_delta_mean_c`                               | NPU 温升均值                     |
| `max_observed_npu_temp_c`                             | 观测到的最高 NPU 温度            |
| `max_thermal_status`                                  | 组内最高 Android thermal status  |

### `energy_batches.csv`

| 字段                                                              | 说明                                                         |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| `energy_batch_id`                                               | 能耗批次标识                                                 |
| `timestamp_start`, `timestamp_end`                            | 批次开始与结束时间                                           |
| `assignee`, `task_group`, `device_id`                       | 执行人、任务组和设备                                         |
| `runtime`, `model`, `quantization`, `backend`             | Runtime、模型、量化配置和后端                                |
| `performance_mode`                                              | 性能模式简称                                                 |
| `htp_performance_mode`, `htp_performance_mode_name`           | HTP 模式数值和枚举名                                         |
| `physical_budget_tokens`                                        | 批次实际执行的输出 token budget                              |
| `budget_execution_mode`                                         | Budget 的执行方式                                            |
| `num_physical_runs`                                             | 批次中的物理运行次数                                         |
| `start_counter_uah`, `end_counter_uah`, `delta_counter_uah` | 电池 charge counter 的起点、终点和差值，单位 uAh             |
| `start_voltage_mv`, `end_voltage_mv`, `average_voltage_mv`  | 起始、结束和端点平均电压，单位 mV                            |
| `duration_s`                                                    | 批次持续时间，单位秒                                         |
| `gross_energy_j`                                                | 由 charge counter 差值和平均电压估算的整机批次能耗，单位焦耳 |
| `average_power_w`                                               | `gross_energy_j / duration_s`，单位瓦                      |
| `energy_per_physical_run_j`                                     | 批次能耗除以物理运行数，单位焦耳                             |
| `counter_step_uah`                                              | 电池计数器最小步长假设，单位 uAh                             |
| `counter_ticks`                                                 | 本批次跨越的计数器步数                                       |
| `minimum_counter_ticks`                                         | 判定可报告所需的最少步数                                     |
| `valid_for_reporting`                                           | 批次是否达到报告门槛                                         |
| `measurement_status`                                            | 测量状态或无效原因                                           |
| `notes`                                                         | 测量范围、电压聚合和单行能耗口径说明                         |
