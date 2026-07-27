# W2 运行说明

## 1. 环境要求

- Android 设备能够通过 `adb` 访问。
- 使用能够运行 ExecuTorch Llama 且可导入 `pytorch_tokenizers` 的 Python 环境。
- 设备目录 `/data/local/tmp/<主机用户名>/executorch/static_llm/` 中已有 `qnn_llama_runner`、`hybrid_llama_qnn.pte`、`tokenizer.json` 和 `tokenizer_config.json`。
- 主机端 PTE 目录中也存在 `hybrid_llama_qnn.pte`。

## 2. 修改配置

运行前编辑：

```text
/code/run_w2_reasoning_config.json
```

| 配置字段                                                  | 说明                                                      |
| --------------------------------------------------------- | --------------------------------------------------------- |
| `paths.repo_root`                                       | 其他相对路径的解析根目录                                  |
| `paths.handoff_root`                                    | 输出根目录，应指向`final/handoff_results`               |
| `paths.samples_jsonl`                                   | W2 样本文件`final/code/data/w2_reasoning_samples.jsonl` |
| `paths.tokenizer_path`, `paths.tokenizer_config_path` | 主机端 tokenizer 文件                                     |
| `paths.pre_gen_pte`                                     | 主机端预生成 PTE 所在目录                                 |
| `runtime.device`                                        | `adb devices` 显示的设备 serial                         |
| `runtime.soc_model`                                     | 目标 SoC；本实验为`SM8750`                              |
| `experiment.performance_configs`                        | 要运行的 HTP 性能模式                                     |
| `experiment.reasoning_budgets`                          | Output budget 列表                                        |
| `experiment.deadlines_ms`                               | Deadline 列表                                             |
| `experiment.repeats`                                    | 每个 sample/mode/budget 的物理重复次数                    |

提交 JSON 是最后一次分批运行时使用的子集。复现完整实验矩阵时，将配置改为三种 mode、三个 budget 和四个 deadline：

```json
"performance_configs": [
  {
    "name": "always_max",
    "htp_performance_mode": 2,
    "htp_performance_mode_name": "kHtpBurst"
  },
  {
    "name": "balanced",
    "htp_performance_mode": 8,
    "htp_performance_mode_name": "kHtpBalanced"
  },
  {
    "name": "low_saver",
    "htp_performance_mode": 5,
    "htp_performance_mode_name": "kHtpLowPowerSaver"
  }
],
"reasoning_budgets": [128, 256, 512],
"deadlines_ms": [5000, 10000, 20000, 30000],
"repeats": 1
```

提交配置默认适配 `final/` 与 `executorch/` 位于同一项目根目录的布局。移动目录或模型产物后，再按实际位置修改 `paths.*`。

## 3. 检查设备

```bash
adb devices
adb -s <device_serial> shell 'test -x /data/local/tmp/<主机用户名>/executorch/static_llm/qnn_llama_runner'
adb -s <device_serial> shell 'test -e /data/local/tmp/<主机用户名>/executorch/static_llm/hybrid_llama_qnn.pte'
```

## 4. 运行

```bash
<executorch_python> /code/run_w2_reasoning.py
```

当前工作区示例：

```bash
executorch/.venv/bin/python /code/run_w2_reasoning.py
```

脚本对每个 sample/mode/budget 执行一次物理生成，再为同一输出展开多个 deadline 行；不需要为每个 deadline 重复运行模型。

## 5. 输出

当 `paths.handoff_root` 指向 `final/handoff_results` 时，输出目录为：

```text
/handoff_results/mym/W2_reasoning/
```

运行会生成或更新 `raw_logs.csv`、`summary_metrics.csv`、`thermal_summary_metrics.csv`、`energy_batches.csv`、`failure_cases.md`、`raw_runner_logs/` 和 `runner_outputs/`。

CSV 使用增量追加。完整复跑应设置新的输出目录或先备份已有结果，避免重复统计。
