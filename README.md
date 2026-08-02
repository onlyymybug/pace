# PACE：手机端 QNN 大模型推理实验

本仓库用于在 Android 手机上运行 ExecuTorch + Qualcomm QNN Hybrid PTE，并评估不同模型在三类端侧任务上的性能与输出质量。目前包含 Qwen2.5-3B 和 BitNet-1.5B 两套独立实验流程。

当前测试设备为 OPPO PLQ110，SoC 为 Snapdragon 8 Elite（SM8750），HTP v79，ABI 为 arm64-v8a。模型文件、runner 和 QNN 动态库体积较大，不保存在本仓库中；代码通过配置引用本机 bundle，并使用 ADB 调用手机上已部署的运行环境。

## 任务

| 任务 | 内容 | 输出预算 | 主要指标 |
| --- | --- | ---: | --- |
| W1 Streaming Chat | 长文本聊天生成 | 512 tokens | TTFT、E2E、decode tok/s、生成长度 |
| W2 Reasoning | 数学推理与最终答案抽取 | 128 tokens | 正确率、TTFT、E2E、deadline |
| W3 Action | 根据请求生成结构化 action JSON | 96 tokens | action 正确率、格式错误、deadline |

## 目录结构

```text
pace/
├── code/
│   ├── data/                 # W1、W2、W3 JSONL 数据集
│   ├── qwen/                 # Qwen 配置、运行脚本和评分代码
│   └── bitnet/               # BitNet 配置、部署、运行和评分代码
├── docs/week1/               # 第一周总结
├── manifests/                # 模型与 runtime 支持情况
├── results/
│   ├── w1/{qwen,bitnet}/
│   ├── w2/{qwen,bitnet}/
│   └── w3/{qwen,bitnet}/     # 日志、runner 输出和汇总 CSV
├── pace_task.pdf             # PACE 任务说明
└── T-MAN.pdf                 # 相关论文
```

每个正式结果目录包含：

- `raw_runner_logs/`：runner 的完整标准输出和错误日志；
- `runner_outputs/`：生成文本、速度文件及实际运行命令；
- `summary_metrics.csv`：从真实 runner 输出解析出的样本级指标。

当前 runner 不提供逐 token timestamp，也不能控制三种 HTP performance mode。本轮结果没有经过统一条件下的温度和功耗测量，因此仓库中不生成虚构或不可验证的对应字段。详细状态见 [第一周总结](docs/week1/week1_summary.md)。

