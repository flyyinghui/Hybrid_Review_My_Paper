# Prior-Finding Injection in Re-Review（复审前注入前轮缺陷清单）

> 来源：V64 两轮 5-agent 终审，2026-09-26。评分 5.4 → 6.5，4 Major → 1 Major + 4 Minor。

## 核心规则（用户零容忍）

**复审必须注入前轮 P0/P1 对照清单，否则用户会明确拒绝**——"否则就推翻之前审稿意见了"。
记忆条目已记录此偏好（V56 教训），这里固化脚本级实现。

## 复审脚本必须包含三要素

1. **【前次评审历史】块**：把前轮全部 P0/P1 整理为编号清单（P0-1…P0-5, P1-1…P1-7），
   每条含「代理共识 + 具体证据（节/公式）」。注入到每个审稿人的 prompt 中。

2. **要求逐条判断**：SYSTEM 输出格式里加一行——
   ```
   ### Prior-finding resolution table
   - | Finding ID | Status (FIXED / PARTIALLY FIXED / NOT FIXED) | Evidence |
   ```

3. **reviewers 的 focus 需指向前轮缺陷**：每个代理的 focus 明确要求"验证 P0-1/P0-2… 是否
   正确执行，不过度纠正也不欠纠正"。

## 效果

- 评分从 5.4 → 6.5（+1.1），R4 从 4 → 6（+2.0，魔鬼代言人对诚实修复最敏感）。
- 5 个前轮 P0 全部 FIXED，无新推导级 P0。

## "语言 P0" vs "物理 P0" 洞察（复审后最有价值的判断）

修复物理 P0 后，剩余 P0 往往是**摘要/§1 措辞过度**，而正文已诚实。R4 原话：

> "the body is correct, the abstract is not yet aligned with it" —— 这是最好修的一类问题。

判断标准：审稿人说 "None remaining at the level of textual claim"（正文层无新 P0）
但列出 "P0-A/B/C 语言层" 时，说明只需**修辞对齐**（一两句话），无需新推导/新计算。

常见"语言 P0"模式（V64 实例）：
- 摘要 "giving S_inst≥…" 未标注 conditional（正文已标注）
- 摘要 "a CP-odd invariant … must be nonzero" 缺 "necessary"（正文已写 necessary condition）
- 摘要 0-axiom 句子有"assumption-free"风险（正文 §10.2 已澄清）
- 摘要 "mean-field gap identity" 未标注 surrogate（正文 §7 已标注）

## 复审轮次管理

- 每轮输出独立报告文件：`V64_Hybrid_Review_5agent_round{N}_YYYYMMDD.md`
- 下一轮脚本读上一轮报告，重新提取 P0/P1 清单注入（脚本化，不手抄）
- 评分单调上升 = 修复有效；若某代理评分下降需检查是否"过度纠正"（把 honest 降级过头）
