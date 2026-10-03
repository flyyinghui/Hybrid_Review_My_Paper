# referee-sim Stage 0 实测 yield — V64 中微子论文（2026-10-02）

> 首次在真实论文上跑 Stage 0 框架预审的记录。核心产出：**框架级 vs 事实级 finding 的区分方法**，以及 **"诚实标注本身成为过度声称" 的元模式**。这两点是 referee-sim 相对规则组 A–F 的独特价值所在。

---

## 一、可复用的执行配方

1. **选论文**：优先选「最成熟、最诚实化」的一篇——它已经过事实核查的穷尽迭代，referee-sim 能抓到的东西才真正是"事实核查漏掉的"。
2. **枚举受众**（referee-sim 步骤 1）：incumbent（借用其机制的社区）+ 每个 borrowed-authority 社区 + practitioner。本文 5 个受众：seesaw 社区(incumbent) / 中微子唯象学家 / 宇宙学家 / 形式理论家 / 0νββ 实验家(practitioner)。
3. **生成反对意见**：用 deepseek-flash（thinking disabled, temperature=0.3, max_tokens=1500），每个受众一个 prompt。prompt 里必须写死 steelman 三要求——「博学但不同情」「点出该社区知道而论文忽略的 prior result / 标准对照 / 基准」「不继承作者框架，不因论文已诚实标注而网开一面」。**5 受众 × 2 轴串行 ≈ 3.5 分钟**。
4. **steelman 三测试**：sting（照它行动需一次编辑吗？）/ knowledge（点出 prior result 了吗？）/ lead（是该社区第一个会问的吗？）。
5. **答案位置验证**：caveat 在摘要**末尾**、标题**干净**、答案在 §X 末尾 = "未读答案"/"摘要防火墙"，印象已在标题+摘要第一句形成。
6. **裁决表**：audience / axis / objection / answered-where-or-NOT / severity。

---

## 二、核心区分：框架级 vs 事实级 finding

这是 referee-sim yield 的量化关键。10 个钢化反对意见分成两类：

**框架级（implicature）** — referee-sim 独有，规则组 A–F 的事实核查**必然放过**：
- 判据 = "读者从标题+摘要第一句会**得出什么结论**"，不是"句子是否真实/已标注"。
- 事实核查的判据是"句子是否真实/已标注"——所以论文处处标注 conditional/A-3D/phenomenological 时，事实核查判"已诚实标注"而放过；框架核查判"但标题和摘要第一句让读者相信了相反的东西"。

**事实级（方法对齐/数值映射）** — 规则组 F3/C 也能抓，但 referee-sim 用受众视角表述得更尖锐：
- 无 prior-result 逐项对照、无 Δm²/Σm_ν 映射、无 bubble nucleation/washout 计算、无参数窗口。

**实测比例**：10 个反对 → 框架级 4 个 / 事实级 6 个；severity HIGH 7 / MEDIUM 3。

---

## 三、最重要的元模式：诚实标注本身成为过度声称

V64 案例暴露的深层问题（可复用到任何"诚实化"论文）：

> 论文把 "conditional / honest premise A-3D / phenomenological matching definition" 当作诚实标注——这是对的（相对早期"几何确定 M_R"的过度声称是巨大进步）。但**框架核查**揭示：当 "conditional" 被推到极致（所有输入都是自由参数），在 practitioner（实验家）视角下它不再是诚实，而是**不可证伪**。论文从未回应这个元问题。

**诚实化的下一步不是"更多 conditional"，而是"给出一个能证伪的定量锚点"。**

检测信号：论文某类关键词的密度异常高——"conditional / remain to be calculated / not established / phenomenological matching / honest premise"——且这些词**只在正文/摘要末尾**出现、**标题和摘要第一句干净**。这是"摘要防火墙 + 诚实标注元问题"的组合信号。

---

## 四、验证结论与诚实边界

- yield 为正且独特（4 个框架级 finding 规则组 A–F 抓不到）——证明 Stage 0 是正交审计维度。
- steelman 通过（10 个反对都点出具体 prior result：AKLR 阈值修正 / Davidson-Ibarra / Coleman-Callan O(3) bounce / Cline-Kainulainen-Scott / Dolan-Jackiw daisy / IBM-2·QRPA·EDF NME）。
- fresh-context 有效（deepseek-flash 独立生成，直接挑战"conditional 是诚实"的定位）。

**诚实边界**：
- 未做对照组（同篇跑规则组 A–F 看能否抓到这 4 个框架级 finding），"必然放过"基于两套规则文本语义分析，非 A/B 实测。
- "事实级"与规则组 F3 的边界模糊，分类有主观成分。
- 反对意见由 deepseek-flash 生成，可能继承 deepseek 家族盲点。

**校准方向**（下一步）：把框架级 finding 反向投给作者，区分"该修的真实缺陷" vs "practitioner 视角合理但可辩护的选择"——校准 referee-sim 的假阳性率，防止把"conditional 这种诚实措辞"过度解读为缺陷。
