# W1 One-page memo：Streaming Chat / QA

## 1. 实验设计

- Runtime / model：Android SM8750 真机，ExecuTorch + Qualcomm QNN HTP，Qwen2.5-3B-Instruct，temperature 0，hybrid，prefill AR 128。
- Dataset / samples：6 个手写 chat/QA prompts，目标 budget 512 tokens，允许模型提前 EOS。
- Configs / repeats：Burst、Balanced、LowPowerSaver；每个 prompt/mode 计划重复 3 次，共 54 条物理运行记录。

## 2. 验证指标

- Latency：TTFT、e2e、runner 直接记录的逐 token timestamp、p50/p95 TBT、stall ratio、visible tokens/s，均可用。
- Success：按 p95 TBT 是否通过 208/167/100 ms（约 4.8/6/10 tokens/s）三档阅读阈值，均可用。
- Validity：W1 不涉及结构化 action validity；以 token timing 是否完整可信作为日志有效性检查。
- Energy：批次级整机电池能耗可用于初步 mode 比较；不是单次请求或 NPU 独立能耗。Thermal 为 skin/NPU 端点趋势。

## 3. 重点结果

| Mode          |     TTFT | p95 TBT / visible tps | 阈值通过率（4.8/6/10） | Gross energy/run |
| ------------- | -------: | --------------------: | ---------------------: | ---------------: |
| Burst         | 122.7 ms |       44.2 ms / 24.56 |     100% / 100% / 100% |          198.1 J |
| Balanced      | 187.2 ms |       68.7 ms / 14.76 |     100% / 100% / 100% |          130.1 J |
| LowPowerSaver | 399.2 ms |       147.6 ms / 6.98 |       100% / 100% / 0% |          122.6 J |

Balanced 已覆盖最高的 10 tokens/s 档位，Burst 的额外速度没有带来新的任务阈值收益。Balanced 的 gross energy/run 比 Burst 低 34.3%；若只要求 4.8–6 tokens/s，LowPowerSaver 也足够。

## 4. 失败情况

- Timing/stall：无 token timestamp failure，无低于平均阅读阈值的运行，三个 mode 的平均 stall ratio 均为 0。
- Runtime/data：如adb断开连接等，本次 runtime success 100%。

## 5. 可信结论与 fallback sanity

可信的是当前真机、模型和 6 个 prompt 上的 TTFT、逐 token delivery、阈值通过率与 mode 排序；结果来自 `executorch_qnn`，不是 fallback。

能耗仅为初步趋势：它们是整机批次测量，粒度很粗，无法得到细致的测量。

## 6. 如果再给一周，我会优先做什么

扩大到不同长度和语言的真实 chat prompts，加入用户开始阅读、打断生成和短回复场景；

随机化 mode 顺序排除运行先后的影响。

## 7. 需要注意的问题

- `raw_logs.csv` 的 `energy_j` 全部为 `NA`，因为能耗按性能模式的物理批次测量；实际能耗记录在 `energy_batches.csv`，不能把 `NA` 理解为零能耗。
- 模型是 Qwen2.5-3B-Instruct；`Qwen2_5_1_5BQuantRecipe` 是代码中被 3B 配置复用的量化 recipe 类名，不表示本实验使用了 1.5B 模型。
- `device_id` 保存的是易变化的 ADB `IP:port`，用于定位当次连接，不是稳定的物理设备 serial。
