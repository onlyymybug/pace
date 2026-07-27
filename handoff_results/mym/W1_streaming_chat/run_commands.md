# W1 运行说明

## 1. 环境要求

- Android 设备能够通过 `adb` 访问。
- 使用能够运行 ExecuTorch Llama 且可导入 `pytorch_tokenizers` 的 Python 环境。
- 设备目录 `/data/local/tmp/<主机用户名>/executorch/static_llm/` 中已有：

```text
qnn_llama_runner
hybrid_llama_qnn.pte
tokenizer.json
tokenizer_config.json
```

- 主机端 PTE 目录中也存在 `hybrid_llama_qnn.pte`。

## 2. 修改配置

运行前编辑：

```text
/code/run_w1_streaming_config.json
```

| 配置字段                            | 说明                                                      |
| ----------------------------------- | --------------------------------------------------------- |
| `paths.repo_root`                 | 其他相对路径的解析根目录                                  |
| `paths.handoff_root`              | 输出根目录，应指向`final/handoff_results`               |
| `paths.samples_jsonl`             | W1 样本文件`final/code/data/w1_streaming_samples.jsonl` |
| `paths.tokenizer_path`            | 主机端`tokenizer.json`                                  |
| `paths.tokenizer_config_path`     | 主机端`tokenizer_config.json`                           |
| `paths.pre_gen_pte`               | 主机端预生成 PTE 所在目录                                 |
| `runtime.device`                  | `adb devices` 显示的设备 serial                         |
| `runtime.soc_model`               | 目标 SoC；本实验为`SM8750`                              |
| `experiment.performance_configs`  | 要运行的 HTP 性能模式                                     |
| `experiment.target_output_tokens` | 目标输出 token budget                                     |
| `experiment.repeats`              | 每个 prompt/mode 的重复次数                               |

提交配置默认适配 `final/` 与 `executorch/` 位于同一项目根目录的布局。移动目录或模型产物后，再按实际位置修改 `paths.*`。

## 3. 检查设备

```bash
adb devices
adb -s <device_serial> shell 'test -x /data/local/tmp/<主机用户名>/executorch/static_llm/qnn_llama_runner'
adb -s <device_serial> shell 'test -e /data/local/tmp/<主机用户名>/executorch/static_llm/hybrid_llama_qnn.pte'
```

两条 `test` 命令返回状态 0 后再开始实验。

## 4. 运行

在项目根目录使用 ExecuTorch 的 Python 解释器运行：

```bash
<executorch_python> /code/run_w1_streaming.py
```

当前工作区示例：

```bash
executorch/.venv/bin/python /code/run_w1_streaming.py
```

脚本会遍历 `performance_configs`、全部 W1 样本和 `repeats`，不需要逐个样本手工调用 runner。

## 5. 输出

当 `paths.handoff_root` 指向 `final/handoff_results` 时，输出目录为：

```text
/handoff_results/mym/W1_streaming_chat/
```

运行会生成或更新 `raw_logs.csv`、`summary_metrics.csv`、`thermal_summary_metrics.csv`、`energy_batches.csv`、`failure_cases.md`、`raw_runner_logs/` 和 `runner_outputs/`。

CSV 使用增量追加。正式复跑应设置新的输出目录或先备份现有结果，避免新旧记录混合。
