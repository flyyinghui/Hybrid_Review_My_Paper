# BootLoops 对 Hybrid-Review 审稿技能的增量评估

> 评估对象：`ars-awa-hybrid-review`（v1.2.0）—— 用户口语触发词「Hybrid-review-my-paper」对应的 5 专家混合审稿管线。
> 对照素材：BootLoops 1.0 全部 12 个协议 skills（`scientific-discovery-proof/references/bootloops-12-protocols-archive.md` 全文归档）。
> 评估日期：2026-10-02。

---

## 一句话结论

BootLoops 对审稿技能的**最大增量只有一个新维度**——`referee-sim`（框架/implicature 审计：读者会「得出什么结论」，而非「句子是否真实」）；`prose-lint` 的诚实性 tells（E）与数字纪律（N）是规则组 B/E 的精细化补充；其余协议要么是哲学强化，要么与审稿无关。**落地优先级：referee-sim ≫ prose-lint E/N > independence-bookkeeping 原则 > 其余可选。**

---

## 一、现状盘点：hybrid-review 已经很强

v1.2.0 已集成的检测能力（规则组 A–F + Quality Gates）：

| 能力 | 对应规则 | 覆盖维度 |
|---|---|---|
| 公理自洽（可证 False / 循环定义 / 假等式 / 空壳桩 / 孤立 / 计数） | A1–A6 | 数学正确性 |
| 诚实性（表演性诚实 / 幻影引用 / 校准伪装 / 状态升级 / 母框架标注） | B1–B5 | 诚实性 |
| 跨章节一致（多版本残留 / 计数矛盾 / 维度 / 物理量混淆 / 跨论文 / 相位反转） | C1–C6 | 一致性 |
| P0–P3 分级 + 升级/降级 | D | 严重度 |
| 审查员算术假阳性验证（独立重算 / 摘要歧义 / 约定依赖） | E1–E3 | 反误判 |
| 三 Refinement Agents（Spec 合规 / live-search 引用 / 方法-代码对齐） | F1–F3 | 溯源对齐 |
| 数值接受门槛 + 一票否决 | Quality Gates | 门控 |

**结论**：事实核查、一致性、诚实性标注、引用真实性、方法-代码对齐——这五条轴 hybrid-review 已经覆盖得很深。BootLoops 的 `ref-check`、`acceptance-gate`、`constant-recognition` 在这些轴上是**重复**而非新增。

---

## 二、12 协议逐项增量对照

| BootLoops 协议 | 对审稿技能的增量 | 判定 |
|---|---|---|
| **referee-sim** | **框架/implicature 审计 —— 全新维度**（hybrid-review 完全没有） | ⭐⭐⭐ 高增量 |
| **prose-lint**（E 诚实性 + N 数字纪律） | 规则组 B/E 的精细化（6 诚实性 tell + 13 数字机械矛盾） | ⭐⭐ 中增量 |
| **lit-review** | 新颖性审计的「可证伪彻底性 + 双向引用链」——F2 的部分补充 | ⭐ 低增量 |
| **independence-bookkeeping** | audit 独立性原则（模型盲点双向传染）——gate 纪律第 6 条的概念根基 | ⭐ 低增量（哲学强化） |
| **prove-protocol** | 强制结构多样性（generate/audit 用不同模型）——同上 | ⭐ 低增量（哲学强化） |
| **acceptance-gate** | 「done」的哲学：独立路线复现到 N 位 + 正对照——Quality Gates 的概念强化 | ⭐ 低增量（哲学强化） |
| **ref-check** | 民间传说错误陷阱（DOI 前缀迁移、\citealp 数字 misfire）——F2 的小补充 | ○ 微增量 |
| constant-recognition | 属 sibling 技能 `scientific-discovery-proof` Stage 1.5，不属审稿 | ✗ 无增量 |
| planted-truth | 同上（Stage 1.5a 已落地） | ✗ 无增量 |
| timing-discipline | 「自己做数值科学」的纪律，非「审别人的稿」 | ✗ 无增量 |
| reading-contract | 文档阅读工具纪律，非审稿 | ✗ 无增量 |
| tool-stewardship | 工具库管理，非审稿 | ✗ 无增量 |

---

## 三、最高价值增量详解（3 项）

### 1. `referee-sim` —— 框架 linter（唯一全新维度）

**核心洞见**：事实核查（fact-checking）与框架核查（frame-checking）是两种不同的审计。hybrid-review 的规则组 A–F 全是前者（逐句真值 + 计数一致 + 引用真实）；`referee-sim` 审计的是** implicature —— 每种读者会「相信什么」**。

**hybrid-review 抓不到、referee-sim 能抓的 6 个失败模式**（全部在 SL(6)C 四论文反复出现过）：

| 失败模式 | 含义 | 对应 SL(6)C 案例 |
|---|---|---|
| **摘要防火墙** | body 全诚实，abstract 干净无 caveat | V17 摘要无 conjecture 标签，正文却诚实标注「不闭合」 |
| **未读答案** | 答案在正文，但反对者在摘要就形成印象 | 预测度 +1/+2/+3 的修正藏在 §7，摘要仍声称「导出」 |
| **hedge-blur** | 修复时削弱所有 claim 而非 scope 一次 | 「统一」→「组织」→「对应」的渐进模糊 |
| **缺失受众** | 借用的方法/数据集社区没拿到审计行 | 中微子论文借 seesaw 机制，却未审「incumbent = 标准 seesaw 社区」 |
| **新颖性-正确性混淆** | 只答一轴 | 论文证明一切却不言明「比标准 seesaw 新在哪」 |
| **友好读者/strawman** | 模拟审稿继承作者框架，只提已答的弱反对 | 5-agent 用同一 v4-flash 生成=同盲点 |

**关键操作**：受众枚举（含 incumbent + borrowed-authority）→ 每受众两轴（correctness + novelty）→ steelman 三测试（sting / knowledge / lead）→ 验证答案在反对者的阅读路径上 → 摘要单独冷读最后审 → 最小 scope 编辑（禁 hedge-blur）→ 裁决表。

**落地位置**：作为 hybrid-review 新增 **Stage 0（框架预审）**，在任何 5-agent 事实审稿之前跑。因为它是唯一能抓「摘要防火墙」的维度——而摘要正是审稿人/投稿人第一眼形成印象的地方。

---

### 2. `prose-lint` E + N —— 诚实性与数字纪律的精细化

**E（诚实性 tells，6 条）→ 规则组 B 新增 B6**：
- E1 捏造精确性（编数字/计数/日期当数据）
- E2 重要性通胀（「field needs」vs「computable frontier」）
- E3 出处错误（张冠李戴）
- E4 结果过度声称（partial 结果 round up 到 done）
- E5 自信模糊（「a first」不 pin 来源）
- **E6 封闭区间/引号完整性**：认证区间 outward 舍入；引号需逐字收据；error-bound 只能保守舍入

**N（数字纪律，13 条）→ 新增规则组 N**：
- N1 舍入方向（23.85 打 23 不打 24）
- N2 减法一致性（41.2 − 3.9 = 37 位，floor 后 41−3=38 位即假）
- N4 显示平局（141/400 = 0.3525 float 打 35.2 / half-up 打 35.3）
- N5 二代舍入（0.172/0.126 → 1.37 vs 未舍入 1.362）
- **N10 情态词是数字的一部分**（「can be 1.08×」压缩成「is 1.08×」）
- N13 标识符完整性（DOI 前缀迁移，不归一化到熟悉形式）

**增量判定**：hybrid-review 规则组 B 目前聚焦「公理/引用/校准」层面的诚实性，**缺的是句子级/数字呈现级的机械矛盾**。E6 与 N10 尤其关键——它们直接抓「过度声称」的语言学机制（情态词、舍入方向），这正是 SL(6)C 论文「诚实降级」过程中反复出现的问题。

**落地位置**：作为规则组 B 的 B6（诚实性 tells）与新增规则组 N（数字呈现一致性），并入每个 reviewer 的强制 checklist。

---

### 3. `independence-bookkeeping` + `prove-protocol` —— audit 独立性的哲学根基

**核心原则**：喂过拟合的 oracle 永远不能认证结果。

**对应 hybrid-review 的真实缺口**：审稿 agent 用 v4-flash，被审论文也是 v4-flash 生成 → **同一模型的盲点双向传染**（referee-sim 称之为「author-context contamination」的审查版）。

**hybrid-review 已隐约意识到**（gate 执行纪律第 6 条：「若综合分仅由 v4-pro/v4-flash 单模型给出且落在 7–8 边界，建议补 held-out 终审」），但未系统化。

**系统化方案**（来自 prove-protocol 的「强制结构多样性」）：
- generate（论文/证明）与 audit（审稿）**必须用不同模型或不同结构**
- held-out 终审用独立 rubric（如 Ollama qwq:32b）
- 记录每个 oracle 喂过什么，禁止它认证自己的产物

**落地位置**：把 gate 执行纪律第 6 条从「建议」升级为「强制」——落在 6–8 分边界时，held-out 终审（不同模型）是**必须**而非可选。

---

## 四、落地优先级与建议

| 优先级 | 协议 | 落地动作 | 成本 |
|---|---|---|---|
| **P0** | referee-sim | 新增 Stage 0 框架预审（implicature 审计 + 受众枚举 + steelman + 摘要冷读） | 中（新文档 + 1 个 agent pass） |
| **P1** | prose-lint E/N | 规则组 B 加 B6 + 新增规则组 N（13 数字纪律 + 6 诚实性 tell） | 低（checklist 扩展） |
| **P2** | independence-bookkeeping 原则 | gate 纪律第 6 条升级为强制 held-out 终审（不同模型） | 低（改一段文字） |
| P3 | ref-check / lit-review | F2 补民间传说陷阱 checklist；新颖性审计加可证伪彻底性 | 低（可选） |
| — | acceptance-gate | Quality Gates 的哲学已覆盖，仅吸收「正对照证明检查会失败」原则 | 不落地 |
| — | constant-recognition / planted-truth | 已落地在 sibling 技能 `scientific-discovery-proof` Stage 1.5 | 已完成 |

**一句话**：referee-sim 是唯一值得作为「新维度」落地的；prose-lint E/N 是值得「并入 checklist」的精细化；其余是哲学强化，不改变管线结构。

---

## 五、诚实边界

- 本评估基于两套技能的**文本对照**，未在真实论文上做「有/无 referee-sim」的 A/B 对照实验。referee-sim 的实际 yield（能多抓几个 HIGH 级 finding）需用一篇 SL(6)C 论文实测验证。
- prose-lint N 的 13 条数字纪律，部分是 hybrid-review 规则组 C（跨章节一致）已有能力的「语言学化重述」——不是全新，是把「矛盾」细化为「机械矛盾」的具体形态。
- independence-bookkeeping 的「不同模型」落地，受限于当前只有 deepseek-flash / deepseek-v4-pro 两档可用；真正的结构独立性（如换 GPT/Claude）目前不可得。
