# 双 LLM 审查模式：v4-pro 深度推理 + v4-flash 撰写报告

用户显式指令「采用 deepseek-v4-pro 推理，deepseek-v4-flash 撰写审查报告的双 LLM 模式」的执行配方。2026-09-20 验证（V19↔CGICE 基准动力学遵循度终审，最终 7.2/10）。

## 何时使用

- 用户要求「双 LLM 模式」「v4-pro 推理 + v4-flash 撰写」「v4-pro(最大 token)推理」
- 跨论文审查需要「深度数学推理」与「结构化报告撰写」分离（推理层 vs 撰写层）
- 与「5 代理并行 deepseek-flash」不同：双 LLM 是**单推理 + 单撰写**的两段串行，速度更快（~5 分钟），深度靠 v4-pro 的 thinking 轨迹，而非多代理交叉验证

## 模型名与 API 配置（2026-09-13 权威）

- 仅两个有效模型名：`deepseek-v4-pro` 和 `deepseek-flash`（`deepseek-chat` 已废弃）
- v4-pro：thinking 默认开；`max_tokens=32768, temperature=0.0, timeout=900`
- v4-flash：**必须** `extra_body={"thinking": {"type": "disabled"}}` 否则 content 空；`max_tokens=32768, temperature=0.2, timeout=600`
- OpenAI SDK，`base_url="https://api.deepseek.com"`

## v4-pro 返回结构（关键陷阱）

v4-pro thinking 模式会同时返回两个字段：

| 字段 | 本会话实测 | 含义 |
|---|---|---|
| `message.content` | 7523 chars | **蒸馏后的结构化答案**（遵循你 prompt 的输出格式） |
| `message.reasoning_content` | 57576 chars | 原始思考轨迹 |

**选择规则**：`content if content.strip() else reasoning_content`。
- content 非空 = v4-pro 已按你的格式输出结构化分析，直接用 content（本会话 content=7523 非空，正确选 content）。
- 仅当 content 为空（长生成时偶发）才回退 reasoning_content。
- 不要盲目用 reasoning_content 取代 content —— reasoning_content 是未蒸馏的思考过程，可能含冗余/自我修正/未定论，而 content 是收敛后的结论。

## 时序（本会话实测）

- v4-pro：28K char prompt，302s（CPU 空闲 = 等待 API 返回，属正常 thinking 阶段，非挂死）
- v4-flash：8.4K char prompt（v4-pro 的 content + 撰写指令），17s
- 总 ~5.5 分钟

**v4-pro 可靠性边界**：28K char（<50K 安全区）可靠 ~300s。CPU 0.5% + 0:01 累计 CPU 时间 = 网络等待，不是挂死；等待 300-360s 再判定超时。与 `references/v4pro-multi-paper-cross-review.md` 的 <50K 安全区一致。

## 执行脚本结构（scripts 级模板）

1. 读目标论文 + 母框架论文，用 `extract_sections(text, start_pat, end_pat)` 正则切片（摘要/三阶段/结论/关键方程），**每节 trim 到 3000-6000 chars**，控制总 prompt <50K。
2. 机器实测 Lean 声明统计（剥嵌套块注释 + 行首锚定计数），并入 prompt。
3. **推理 prompt（v4-pro）**：任务 + 母框架基准方程 + 子论文核心节 + Lean 统计 + 「输出结构化分析」的明确要求（三阶段判定矩阵/推导核验/深化建议/数值重算）。
4. **撰写 prompt（v4-flash）**：v4-pro 的 content（截到 ~40K）+ 「据此撰写终审报告」+ 严格 7 节结构模板（总体结论/判定矩阵/推导核验/P0-P3 清单/证据链建议/物理诠释建议/评分投稿）。
5. 每步输出立即写文件（`.part` 或独立文件），防超时丢失；最终报告复制到论文目录。

## 判定矩阵输出要求（跨论文动力学遵循度）

对每个因果箭头判 follows/partial/language_only（不是对整篇判单一值）。本会话 V19 结果：11 条箭头 = 7 follows（守恒/耗散/代数骨架层）+ 3 partial（物理语义生成层）+ 1 partial/language_only（KL→DE）。区分两正交维度：内部一致性 vs 跨论文动力学遵循度。
