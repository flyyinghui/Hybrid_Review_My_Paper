# ScientistTwo (arXiv:2609.19644) → Hybrid-Review 可移植机制

Google Cloud AI Research 的全自主科研 agent（**不是审稿工具**）。107 个 ICLR/ICML/NeurIPS 任务中 80.4% 超过人类 SOTA，平均 +25.2%。对 hybrid-review 的真正增量在**机制层**（答辩闭环 + 元审稿分流），而非审稿本身——现有 5-agent 并行审稿 + P0-P3 分级已强于它的单点 Peer-Reviewer。

## 四个可移植机制（按价值排序）

### 1. Rebuttal Agent 闭环（§3.5）— 最高价值
审稿分数 < 阈值（8/10）→ **不直接改文字**，而是：
1. **Rebuttal Planner** 把每条审稿意见转成一个「补充分析/实验任务」
2. **Rebuttal Coder** 执行该任务（理论物理论文 = 新生成一段 Lean 证明 / 数值验证 / 新图 / 新附录）
3. **Paper Enhancer** 把结果回填进正文（改 narrative claims + 更新表格图）
4. 再评审 → 循环直到过线或达 max_rounds

用户现在**隐式**这么做（V38→V64 每轮审稿驱动证明升级，如「Z₂ 等变 K 理论替代 Atiyah-Bott」），但未固化成命名的 Rebuttal Agent + 阈值门控。映射关系：「补充实验」= 针对意见生成新证明/验证，而非文字编辑。

### 2. CoE Integrity Audit 四维（Table 7）
| ScientistTwo 四维 | hybrid-review 对应 | 现状 |
|:--|:--|:--|
| ① Score 可复现性 | 数值结果验证（P195） | 已覆盖 |
| ② 规范合规（无 reward hacking） | 不过度声称（规则组 B） | 已覆盖 |
| ③ 参考文献验证（幻觉引用） | bibliography-auditor | ⚠️ 缺「搜索增强 live-search 逐条核查」，目前只查内部一致性 |
| ④ 方法-代码对齐 | 论文 ↔ Lean 对齐（cross-ref 核心） | 已覆盖 |

**可增量吸收的只有 ③**：升级 bibliography-auditor 为 live web search 逐条验证引用真实性，而非仅内部自洽。

### 3. Meta-Review 分流（§3.6）— text-level vs idea-level
元审稿人对「稿子+审稿意见」终判 accept/reject。**reject 时不是改文字，而是深度想法精炼**——回到假设层重建，验证严格更优才替换，否则丢弃回退到上一个最好版本。

映射：把每条 P0/P1 显式标 `text-level / idea-level`，idea-level 才走深度重建（带回退保护）。这正好把「审稿发现环论证→重写证明」与「审稿发现排版→改 DOCX」两类路由显式分开。

### 4. Held-out 评审器（防 in-distribution 偏差）
ScholarPeer = in-distribution（训练期即用于精炼），Stanford Agentic Reviewer = held-out（开发全程未见）。两个都报分才有说服力。

映射：hybrid-review 用 DeepSeek（v4-flash/v4-pro）**同时也是生成模型**，存在 in-distribution 偏差（记忆里已有「v4-pro 单独审计 9/10 实际 2/10」教训）。→ 加一道 held-out 终审：换独立模型（台式机 Ollama qwq:32b）或独立 rubric 做最终 sanity gate。

## 实证数据（直接引用）

- **Table 5（答辩轮次 vs 分数）**：无答辩 5.2/46.9% 接收 → 1 轮 6.9/79.6%（**增幅最大**）→ 2 轮 7.6/93.9%（边际递减）。且改进**泛化到 held-out**（Stanford 49%→73.5%）。→ **默认 max_rounds=2 是经验最优**。
- **Table 7（三维 refinement agents 缺一不可）**：三个 refinement agent（spec 合规 + 引用核查 + 方法-代码对齐）全开才 49/49 通过四项审计；关任意一个即出现引用幻觉（19/1840）或方法-代码错位（38/49）。

## 明确不移植
- §3.1–3.3 想法生成/实验执行（面向 ML 研究，非审稿）
- coding agent 后端（Claude Code / Antigravity）
- 成本分析（$3765/篇、2.5 天）

## 整合优先级（P0–P4）
- **P0**：新增 Rebuttal Agent 闭环协议（max_rounds=2）+ 显式数值接受门槛改写「Quality Gates」
- **P1**：Meta-Review 分流（规则组 D 补 text-level/idea-level 列）+ bibliography-auditor 搜索增强
- **P2**：held-out 终审（Ollama qwq:32b 或独立 rubric）
- **P3**：迭代前沿扩展思路（可选，用户已在做版本连续迭代）
