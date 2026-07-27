# W3 运行说明

## 1. 环境要求

- Android 设备能够通过 `adb` 访问。
- 使用能够运行 ExecuTorch Llama 且可导入 `pytorch_tokenizers` 的 Python 环境。
- 设备目录 `/data/local/tmp/<主机用户名>/executorch/static_llm/` 中已有 `qnn_llama_runner`、`hybrid_llama_qnn.pte`、`tokenizer.json` 和 `tokenizer_config.json`。
- 主机端 PTE 目录中也存在 `hybrid_llama_qnn.pte`。

## 2. 修改配置

运行前编辑：

```text
/code/run_w3_action_config.json
```

| 配置字段                                                  | 说明                                                   |
| --------------------------------------------------------- | ------------------------------------------------------ |
| `paths.repo_root`                                       | 其他相对路径的解析根目录                               |
| `paths.handoff_root`                                    | 输出根目录，应指向`final/handoff_results`            |
| `paths.samples_jsonl`                                   | W3 样本文件`final/code/data/w3_action_samples.jsonl` |
| `paths.tokenizer_path`, `paths.tokenizer_config_path` | 主机端 tokenizer 文件                                  |
| `paths.pre_gen_pte`                                     | 主机端预生成 PTE 所在目录                              |
| `runtime.device`                                        | `adb devices` 显示的设备 serial                      |
| `runtime.soc_model`                                     | 目标 SoC；本实验为`SM8750`                           |
| `experiment.performance_configs`                        | 要运行的 HTP 性能模式                                  |
| `experiment.action_budget_tokens`                       | Action 输出 token budget                               |
| `experiment.deadlines_ms`                               | Deadline 列表                                          |
| `experiment.repeats`                                    | 每个 sample/mode 的物理重复次数                        |
| `experiment.action_schema`                              | Validator 使用的 action 和参数类型定义                 |

复现已提交实验时使用三种 mode、96-token budget、2/5/10 秒 deadline 和 1 次 repeat。提交配置默认适配 `final/` 与 `executorch/` 位于同一项目根目录的布局；移动目录或模型产物后，再按实际位置修改 `paths.*`。

## 3. 检查设备

```bash
adb devices
adb -s <device_serial> shell 'test -x /data/local/tmp/<主机用户名>/executorch/static_llm/qnn_llama_runner'
adb -s <device_serial> shell 'test -e /data/local/tmp/<主机用户名>/executorch/static_llm/hybrid_llama_qnn.pte'
```

## 4. 运行

```bash
<executorch_python> /code/run_w3_action.py
```

当前工作区示例：

```bash
executorch/.venv/bin/python /code/run_w3_action.py
```

脚本对每个 sample/mode 执行一次物理生成，使用严格 JSON/schema validator 处理输出，并为同一生成展开多个 deadline 行。

## 5. 输出

当 `paths.handoff_root` 指向 `final/handoff_results` 时，输出目录为：

```text
/handoff_results/mym/W3_action/
```

运行会生成或更新 `raw_logs.csv`、`summary_metrics.csv`、`thermal_summary_metrics.csv`、`energy_batches.csv`、`failure_cases.md`、`raw_runner_logs/` 和 `runner_outputs/`。

CSV 使用增量追加。完整复跑应设置新的输出目录或先备份已有结果，避免重复统计。
