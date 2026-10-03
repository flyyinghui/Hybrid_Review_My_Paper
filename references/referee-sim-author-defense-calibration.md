# referee-sim 作者辩护校准（Stage 0 实测 pitfall）

> 来源：2026-10-02 在 `Unified_Neutrino_Condensation_V64.md` 上的首轮 Stage 0 实测。
> 定位：referee-sim 框架预审的**必经校准步骤**——finding 不能直接当 HIGH 用。

---

## 核心教训（一句话）

**referee-sim 的价值在「生成最强标准反对」，不在「给出正确 severity」。** 每轮 Stage 0 产出的 finding 都必须过一遍「作者辩护」——steelman 作者的最强立场，区分真实缺陷 / 部分真实 / 可辩护（假阳性），校准 severity 后才进入最终报告。否则会把假阳性当 P0、把措辞优化当阻断。

---

## 假阳性 vs 真实缺陷的判别信号（实测提炼）

| 信号 | 判定 | 对应 referee-sim 机制 |
|---|---|---|
| 反对指向一个文档**已在显眼位置**（独立章节标题 / 摘要中段 / 加粗段落）干净作答的问题 | **假阳性（strawman）** | sting test："If the document as written already answers the objection cleanly, you have probably written a weak one" |
| 反对指向作者**从未回应的元问题**（而非"已标注但位置不对"的 caveat） | **真实缺陷** | 这是框架级 finding 的唯一可靠信号 |
| 反对是"标题/摘要的措辞张力"（一个词可消） | 轻微/部分真实 | 措辞可优化，非阻断，HIGH 降 MEDIUM/LOW |
| 反对是"conditional/参数化"的元问题（缺一个可证伪锚点） | **真实缺陷** | 补锚点，非改措辞 |

**关键区分**：假阳性 = 文档已答但反对者没读到；真实缺陷 = 文档从未答且该答。前者是 referee-sim 的误报，后者才是它的价值。

---

## 实测数据（V64 单篇，1 轮执行）

| finding | 判定 | 修订后 severity |
|---|---|---|
| 标题 Condensation + 摘要第一句 construct interface | 部分真实 | HIGH → MEDIUM |
| conditional 推到极致 = 不可证伪 | **真实缺陷** | 保持 HIGH |
| 几何"做"什么功 implicature | 可辩护（假阳性） | 撤回 |
| Kinetic Triggers 因果 implicature | 轻微真实 | HIGH → LOW |

**precision = 1 真实 + 1 部分 + 1 轻微 + 1 假阳性。**

核心价值：那 1 个真实缺陷（"conditional 不可证伪"的 practitioner 元问题）是规则组 A–F 必然放过的，证明了 Stage 0 的独特价值。但那 1 个假阳性（"几何做功"）也证明 referee-sim 会过度解读——V64 已用 §2.2「What root arithmetic and projections cannot select」独立章节干净作答。

---

## 作者辩护流程（5 步）

1. **对每个 finding，steelman 作者最强立场**——作者为什么这样措辞？标题 "for X" 是研究对象命名还是既成事实声称？"construct" 的宾语是框架还是现象？
2. **跑 sting test**——文档是否已在显眼位置（独立章节标题 / 摘要中段 / 加粗段落）干净作答？是 → 假阳性，撤回或降级。
3. **区分两类**：措辞可优化（一个词可消）vs 元问题未回应（"conditional 到极致是否=不可证伪"）。
4. **校准 severity**——通常 HIGH 要降级或撤回；只有"过作者辩护仍为真实缺陷"的 finding 保持 HIGH。
5. **诚实标注利益冲突**——代拟辩护（agent 代作者）有利益冲突（agent 既执行 referee-sim 又辩护），真正的辩护应由作者本人做。

---

## 落地到 Stage 0 的纪律

1. **Stage 0 输出分两栏**：referee-sim finding（原 severity）+ 作者辩护校准（修订后 severity）。
2. **只有「过作者辩护仍为真实缺陷」的 finding 才进入 HIGH**，其余降级或撤回。
3. **假阳性也是产出**——它验证了 sting test 在起作用，不是浪费。记录"撤回原因=文档已在 X 处作答"。
4. **作者辩护由作者本人做最优**；agent 代拟时必须在报告里标注"代拟，有利益冲突"。

---

## 与 referee-sim 主流程的关系

- `referee-sim-frame-pre-audit.md` 是**生成反对意见**的七步流程。
- 本文件是**校准 severity** 的必经后续步骤——两者合起来才是完整的 Stage 0。
- 顺序：referee-sim 七步（生成）→ 作者辩护五步（校准）→ 裁决表（合并后）。
