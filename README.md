## 运行说明

请参考每个任务下的 run_commands.md.

# 文件说明

| 文件或目录                                 | 说明                                 |
| ------------------------------------------ | ------------------------------------ |
| `run_commands.md`                        | W1、W2、W3 的总运行说明              |
| `code/`                                  | 实验运行、解析、验证、测量和汇总代码 |
| `code/data/`                             | W1、W2、W3 的 JSONL 输入样本         |
| `code/run_w1_streaming.py`               | W1 运行入口                          |
| `code/run_w2_reasoning.py`               | W2 运行入口                          |
| `code/run_w3_action.py`                  | W3 运行入口                          |
| `code/run_w*_config.json`                | 三类任务的运行配置                   |
| `handoff_results/mym/W1_streaming_chat/` | W1 日志、汇总、失败案例和 memo       |
| `handoff_results/mym/W2_reasoning/`      | W2 日志、汇总、失败案例和 memo       |
| `handoff_results/mym/W3_action/`         | W3 日志、汇总、失败案例和 memo       |

## CSV 字段说明

三类任务的 CSV 字段不同，逐字段说明分别位于：

- `handoff_results/mym/W1_streaming_chat/README.md`
- `handoff_results/mym/W2_reasoning/README.md`
- `handoff_results/mym/W3_action/README.md`
