---
name: ars-awa-hybrid-review
description: >-
  Integrated academic paper review pipeline combining ARS (Academic Research Skills)
  full 10-stage workflow with AWA (Academic Writing Agents) granular parallel review
  at writing and revision stages. ARS provides structural pipeline management, integrity
  verification, and formal peer review. AWA injects 12-specialist-agent parallel review
  at Stage 2 (Writing) and Stage 4 (Revision) for fine-grained quality improvement.
  Triggers: hybrid review, ARS+AWA pipeline, integrated paper review, full review pipeline.
version: "1.3.0"
model: deepseek-flash
tags: [academic-writing, peer-review, pipeline, multi-agent, hybrid, frame-audit, prose-lint, bootloops]
depends_on:
  - academic-pipeline
  - academic-writing-agents
  - academic-paper-reviewer
---

# ARS + AWA Hybrid Review Pipeline v1.3

Integrated academic paper review pipeline: **ARS backbone** (structural management + formal peer review) × **AWA injection** (granular quality review at writing/revision stages) × **BootLoops frame-audit** (implicature + prose-honesty + number-discipline pre-audit, v1.3).

```
ARS RESEARCH → WRITE +[AWA Review]→ INTEGRITY → FORMAL REVIEW → REVISE +[AWA Review]→ RE-REVIEW → FINALIZE
```

## Design Rationale

| Layer | Tool | Role |
|:--|:--|:--|
| **Backbone** | ARS `academic-pipeline` | 10-stage state machine, integrity gates, two-stage peer review, format output |
| **Injection 1** | AWA Stage 2a | After draft complete → 5-7 reviewer agents in parallel → granular prose/structure/math/consistency feedback → incorporate before integrity check |
| **Injection 2** | AWA Stage 4a | After revision complete → 3-5 reviewer agents on changed sections → verify fixes + catch new issues → incorporate before re-review |
| **Formal Gate** | ARS Stage 3 | 5-person panel (EIC + R1/R2/R3 + Devil's Advocate), editorial decision, revision roadmap |

## Hybrid Pipeline (13 Stages)

```
Stage 0:  FRAME PRE-AUDIT   [BootLoops referee-sim: implicature audit] ← NEW v1.3
Stage 1:  RESEARCH          [ARS deep-research]
Stage 2:  WRITE             [ARS academic-paper full mode]
Stage 2a: AWA WRITE REVIEW  [AWA: 5-7 reviewer agents parallel]  ← INJECTION 1
Stage 2b: INCORPORATE       [apply AWA findings → revise draft]
Stage 2.5: INTEGRITY        [ARS integrity_verification_agent]
Stage 3:  FORMAL REVIEW     [ARS academic-paper-reviewer: 5-person panel]
Stage 4:  REVISE            [ARS academic-paper revision mode]
Stage 4a: AWA REV REVIEW    [AWA: 3-5 reviewer agents on changed sections] ← INJECTION 2
Stage 4b: INCORPORATE       [apply AWA findings → finalize revision]
Stage 3': RE-REVIEW         [ARS verification review]
Stage 5:  FINALIZE          [ARS format-convert]
Stage 6:  PROCESS SUMMARY   [ARS process record]
```

**Stage 0（框架预审，v1.3 新增）**：任何 5-agent 事实审稿（Stage 2a/3/4a）之前，必须先跑一轮 `referee-sim` implicature 审计——审计「读者会得出什么结论」而非「句子是否真实」。事实核查（fact-checking）与框架核查（frame-checking）是两种正交审计，抓的失败互不重叠。Stage 0 抓 6 类事实核查必然漏掉的失败：摘要防火墙（body 诚实 abstract 干净）、未读答案（答案在正文但反对者早在摘要形成印象）、hedge-blur（修复削弱所有 claim 而非 scope 一次）、缺失受众（借用的方法/数据集社区没拿到审计行）、新颖性-正确性混淆（只答一轴）、友好读者/strawman（模拟审稿继承作者框架）。完整流程见 `references/referee-sim-frame-pre-audit.md`。

## Trigger Keywords

- "深化开放桥" / "把开放桥往前推" / "advance open bridge" / "trivial 构造伪装推进" / "循环定义调 codim" / "recover c 循环代入" — triggers OPEN-BRIDGE DEEPENING HONESTY TRAPS: 作者做形式化证明「深化开放桥」时，警惕三个陷阱——①循环定义（把 codim 调成匹配值再证明）②校准伪装（引入自由参数设为观测值再「恢复」）③状态升级（trivial 构造标记为 [T] 定理）。作者侧自检五问 + 检测信号见 `references/open-bridge-deepening-honesty-traps.md`。

- "框架预审" / "读者会得出什么结论" / "implicature" / "摘要防火墙" / "audience enumeration" / "缺失受众" / "referee-sim" / "frame audit" — triggers FRAME PRE-AUDIT (Stage 0, v1.3): 在 5-agent 事实审稿前跑 `referee-sim` implicature 审计——枚举受众（含 incumbent + borrowed-authority）→ 每受众两轴（correctness+novelty）→ steelman 三测试（sting/knowledge/lead）→ 验证答案在反对者阅读路径上 → 摘要单独冷读最后审 → 最小 scope 编辑（禁 hedge-blur）→ 裁决表。抓 6 类事实核查漏掉的失败（摘要防火墙/未读答案/hedge-blur/缺失受众/新颖性-正确性混淆/友好读者）。See `references/referee-sim-frame-pre-audit.md`.

- "诚实性tell" / "数字呈现矛盾" / "舍入方向" / "情态词是数字" / "number discipline" / "捏造精确性" / "封闭区间舍入" — triggers HONESTY TELLS (B6) + NUMBER DISCIPLINE (N): B6 六条句子级诚实性 tell（捏造精确性/重要性通胀/出处错误/结果过度声称/自信模糊/封闭区间引号完整性）+ N 十三条数字呈现机械矛盾（舍入方向/减法一致/显示平局/二代舍入/情态词/标识符双向）。See `references/prose-lint-honesty-number-discipline.md`.

- "审查员说数值矛盾/算术错误" / "多个审稿人一致判算术错" / "5 agent 全部误判" / "摘要歧义导致集体误读" — triggers REVIEWER ARITHMETIC FALSE-POSITIVE VERIFICATION: independently recompute the flagged arithmetic BEFORE relaying it as P0; check whether a garbled/ambiguous sentence splices two SEPARATE chains (0.46%→Ω_DE vs 5.00→5.47 case); re-derive convention-dependent values (T_F index, normalization) yourself — agents make convention errors (b₀=12 case). See `references/reviewer-arithmetic-false-positive-verification.md`.

- "转换表算术" / "修复引入新错误" / "fix introduces new defect" / "正根数" / "combinatorial count" / "维度不闭合误报" — triggers FIX-INTRODUCES-NEW-DEFECT + COMBINATORIAL-COUNT FALSE-POSITIVE: (a) 修复新增的转换表/归一化表每个格子须按声明恒等式逐格验证（`3(B−L)=3·q_{B₆}` 案例 N_R 列 −3/2 应为 −3，×2 因子错）；(b) 审稿人报"维度不闭合/重数错"时先自算组合量（Aₙ 正根 = n(n+1)/2，A₅=15 非 5，dim=5+15·2=35 闭合）。See `references/fix-introduces-new-defect-conversion-table-arithmetic.md`.

- "计数不一致" / "定理名不一致" / "grönwall vs gr" / "审稿代理被清单误导" / "technical 代理符号算错" / "点积对称性" — triggers LEAN-INVENTORY-REGEX + SYMBOL-ERROR FALSE-POSITIVE: when a reviewer reports a count/name/sign mismatch, FIRST grep the source file to verify the reviewer-quoted value actually exists AND check whether the intermediate Lean-theorem inventory fed to reviewers was truncated by a `[A-Za-z0-9_]` regex (Unicode identifiers ξ/ö get truncated → phantom count/name mismatches). Also re-derive dot-product symmetry (∫∇ξ·j = ∫j·∇ξ) yourself — technical agents make sign errors. See `references/reviewer-false-positive-lean-regex-and-symbol-errors.md`.

- "两份修改建议哪个更有优势" / "对比评价修改方案" / "从数学基础完备性/定理推导严密性/阐释自洽性评估" / "给融合修改意见" / "competing proposal evaluation" — triggers COMPETING-PROPOSAL COMPARATIVE EVALUATION: 先识别两份提案的「性质」（激进重构派 vs 严格条件派），再按三维度（数学基础完备性/定理推导严密性/阐释自洽性）打分，判据核心=证据层级诚实性（[S]是否真编译、所谓推导是否循环校准、范畴错误是否被抓）。融合输出=严格条件派的诚实框架作脊柱 + 激进派的正确数值纠错作补丁 + 降格过度声称。含 8 条决定性技术检查清单（能量非电荷/Wasserstein对称不能产生箭头/SM单态无反常/诱导引力系数(1/6−ξ_conf)共形耦合处为零/ CW系数是超迹非计数/ M_R=sqrt(G⁻¹)=普朗克质量混淆/ 反例构造决定性）。See `references/competing-proposal-evaluation.md`.\n\n- "hybrid review my paper"
- "适不适合投 X 期刊" / "评估是否适合投稿 Foundations of Physics" / "venue-fit" / "投稿适配性终审" — triggers VENUE-FIT PUBLICATION-STRATEGIST REVIEW: 5 代理换为 consistency+technical+logic+lean_specialist+publication-strategist；publication 代理按期刊格式合规清单（摘要 150-250 词 / 关键词 4-6 个 / 三级十进制标题 / .tex 源 / AI 披露）+ 科学门槛（至少一个真实动力学工作包）判 READY / MAJOR REVISION / NOT READY。注意「诚实性 vs 技术严谨性分裂」（诚实标注未同步到 Lean 代码层）。See `references/venue-fit-publication-strategist-review.md`.
- "投稿适配性终审" / "评估是否适合投稿" / "评估适不适合投某期刊" / "journal fit" / "Foundations of Physics 适配性" — triggers PUBLICATION VENUE-FIT FINAL REVIEW: 5 代理替换为 consistency/technical/logic/lean_specialist/**publication-strategist**（核查期刊格式：摘要词数/关键词数/章节层级/.tex 源/AI 披露 + 科学门槛 + READY/MAJOR/NOT READY 建议）。See `references/publication-fit-review-and-arithmetic-p0-fix.md`.
- "编译通过但数学错误" / "ouCov 因子2" / "metzler 比例写反" / "观测输入伪装成谱定理" / "诚实化双向脱节" / "正文公式正确但 Lean 定义错误" — triggers ARITHMETIC-P0-FIX: 三类硬算术错误（因子2/比例方向写反/谱定理伪装）+ 正文文字层诚实化 vs Lean 代码层脱节检测 + 删除公理链后 grep 残留/编译/同步附录 A 统计协议。See `references/publication-fit-review-and-arithmetic-p0-fix.md`.
- "MD-Lean 一致性" / "核查论文md和lean的计数" / "验证md和lean一致性" / "幻影引用机器验证" — triggers MD-LEAN CONSISTENCY MACHINE VERIFICATION: 先机器验证（grep 交叉核对计数/定理名/数值，剥离注释后行首锚定）再 LLM 审稿；传给审稿人的定理名清单必须完整（截断=假阳性）；计数漂移（插新定理后附录 A 未同步）检测。See `references/md-lean-consistency-machine-verification.md`.
- "编译状态表述遗漏" / "改了编译状态但审稿报矛盾" / "pending local build 残留" / "声明计数改了但别处没同步" — triggers COMPILATION-STATUS-CLAIM SYNC: 修改"编译状态/编译通过/0 sorry/声明计数"类元声明时，必须 grep 全文所有残留关键词（pending/not claimed/not asserted/compilation status/final compilation/not been compiled）一次性改干净——这些表述分散在摘要、§1 标签表、各章节 Lean 验证段、附录 A、Materials 段，容易遗漏（V19 案例：改 §1+附录 A 漏 §9.2，被 consistency 代理报 P0 内部矛盾）。See `references/compilation-status-claim-sync.md`.
- "ARS + AWA pipeline"
- "integrated paper review"
- "full review pipeline with writing quality"
- "comprehensive paper review"
- "比较本文与...学术贡献度" / "compare contribution to existing literature"
- "contributions comparison" / "contribution benchmarking"
- "创新性工作" / "innovation assessment" / "从创新性角度" — triggers INNOVATION-FOCUSED review mode with 6-domain benchmarking
- "compare five versions" / "multi-version comparison" / "V{N} V{M} V{K} comparison" — triggers FIVE-VERSION COMPARATIVE REVIEW with 2 dimension-specialized agents (logic+math, testability+evolution). See `references/five-version-comparative-review.md`.
- "cross-check GW consistency" / "compare GW peaks" / "两篇论文GW表述" — triggers CROSS-PAPER GW CONSISTENCY AUDIT across papers sharing SL(6,C) foundation. See `references/cross-paper-gw-consistency-audit.md`.
- "频率比当温度比" / "等效温度算错" / "hf/kB 换算" / "多版本数值残留" / "旧频率比 10² 残留" — triggers two V17-era patterns: (a) frequency↔temperature ratio confusion (f-ratio mislabeled as T-ratio via hf/k_B, 3.44K vs 21.6K case) → see `references/math-calculation-accuracy-review.md` §10; (b) multi-version-fix numerical residue (one section FIX-annotated but sibling sections still use old values → internal self-contradiction) + "母框架已诚实标注不闭合但论文正文仍称闭合" overclaim. See `references/triple-gw-v17-review-record.md`.
- "公式序号重排" / "字母后缀公式乱序" / "9a 9b 9c 夹在连续编号" / "equation renumbering" / "tag 编号不连续" — triggers EQUATION RENUMBERING: 审稿意见整合在 §X 主体后插新子节，新子节公式用父公式后缀编号（9a/9b/9c、12a/12b/12c）导致乱序；修复=按出现顺序连续重编号，正文引用用精确上下文替换（禁用全局正则，会误伤 SL(6)/SU(6)/U(1) 群符号数字、参考文献年份 (1973)、函数值 P(0)/Q(0)）。含 def 计数 noncomputable 陷阱 + A₅ 正根数 15 审稿误判案例。See `references/equation-renumbering-alphabetical-suffix.md`.

- "表述层无限循环" / "P2/P3 修不完" / "7.5 分收尾" / "还要不要跑下一轮复审" — triggers PROSE-LAYER INFINITE-LOOP JUDGMENT: 四轮复审后 P0/P1 连续清零、五维度 ≥7.0、核心卖点(0公理/0sorry/真编译/黄金门控)从未被击穿、新发现全是 P2/P3 表述层 → 应收尾(生成交付版+更新memory)，不要再跑第 5 轮（P2/P3 每轮都能挑出新瑕疵，会无限递归）。含复审执行配方(deepseek-flash 串行+增量落盘+逐条fixed/remain/partial)、审稿人误判纠正(restricted-root 正根数 15≠5)、归一化转换表算术连带错误。See `references/prose-layer-infinite-loop-judgment.md`。

- "启动Hybrid-review-my-paper技能" / "采用deepseek-v4-pro(最大tokens)推理" / "三篇论文相互推导结论的一致性" — triggers V4-PRO MULTI-PAPER CROSS-REVIEW.

- "公式序号重排" / "字母后缀乱序" / "公式编号连续化" / "多轮复审收尾" / "文献精化无限循环" / "复审收敛判断" / "转换表算术错误" / "多归一化转换表" / "归一化转换表逐行验算" — triggers ITERATIVE-REVIEW-CONVERGENCE & MD-CLEANUP: 四轮复审收敛规律(6.2→7.1→7.3→7.5，每轮新发现 severity 递减 P0→P1→P2/P3) + 收尾判断标准(评分≥7.0 且 5 维度均衡 + P0/P1 连续两轮清零 + 核心卖点未被击穿 = 不再追 P2/P3) + 公式字母后缀→连续编号重排(先 \tag 按出现顺序映射，再正文引用用精确上下文字符串替换，避开群符号 SL(6)/SU(6)/U(1)/年份/函数值 P(0)) + 多归一化转换表逐行独立验算(3(B−L)=3q_{B_6} 每行核对，N_R −3/2→−3 案例)。See `references/iterative-review-convergence-and-md-cleanup.md`.

- "编译状态矛盾" / "多处未编译残留" / "正文声称编译通过但附录说未编译" / "compilation status inconsistency" / "grep 未编译变体" — triggers COMPILATION-STATUS CONSISTENCY: 手稿被外部进程（sibling subagent）扩展后，编译状态在正文多处残留"未编译"（has not been compiled / was not compiled / uncompiled / No Lean compilation / No compilation performed / not executed here / compilation status must be checked），与编译成功事实矛盾，五代理审查中 consistency+writing+logic 三代理会同时报 P0。用 `grep -niE "compil|uncompiled|not executed"` 一次抓全变体统一更新。见 references/compilation-status-consistency.md。

- "编译状态表述多处同步" / "pending 残留" / "编译通过但正文仍写待编译" / "一处说 pending 一处说 0 errors" — triggers COMPILATION-STATUS HONESTY SYNC: 编译状态诚实性表述分布在多处（§1 标签表 / 具体定理节正文 / 附录 A 核查段），更新为"已编译"时必须 grep 全部变体（pending/not claimed/not asserted/final compilation status/stopped after elaboration/...）并逐处替换，否则内部自相矛盾被 consistency-checker 抓 P0。See `references/compilation-status-honesty-sync-multi-location.md`.

- "deepseek-v4-pro推理，deepseek-v4-flash撰写" / "双LLM模式" / "v4-pro推理 + v4-flash撰写报告" — triggers DUAL-LLM REVIEW MODE: v4-pro thinking 深度推理 → 提取 content（非空则用 content，空则回退 reasoning_content）→ v4-flash(thinking=disabled) 撰写结构化终审报告。两段串行 ~5.5 分钟（v4-pro 28K/302s + v4-flash 8K/17s）。See `references/dual-llm-v4pro-reason-v4flash-write.md`.

- "三阶段是否遵循CGICE方程" / "语言借用vs方程遵循" / "动力学遵循度" / "以CGICE基准审查" / "子论文是否由母框架方程驱动" — triggers CGICE-BASELINE PHASE-COMPLIANCE REVIEW: 跨论文审查维度，区分「语言借用(language borrowing)」vs「方程遵循(equation following)」，三阶段各判 follows/partial/language_only。标志性红旗「closed dynamical system replacing ΛCDM」+ 诚实标注与过强措辞并存。See `references/cgice-baseline-phase-compliance-review.md`。

- "逻辑自洽性" / "物理现象关联性" / "删除或精简不相关" / "前后论述矛盾" / "relevance-trim" — triggers LOGIC-CONSISTENCY + RELEVANCE-TRIM REVIEW: 5 代理（consistency/relevance/logic/redundancy/cross_check）聚焦逻辑自洽性+物理关联性+精简，识别混入的旁支内容（场论层/现象学层内容、修订日志、已 superseded 残留），输出 delete/simplify/keep 建议；删除时从后往前且 end 索引不越界（防误删下一标题）、删附录后重编号+修悬空引用。See `references/relevance-trim-review.md`。

- "逻辑自洽性" / "物理关联性" / "精简不相关内容" / "删除旁支" / "附录重编号" — triggers RELEVANCE-TRIM: 5 代理 consistency/relevance/logic/redundancy/cross_check 复审，识别与主线不相关的旁支（场论层/现象学层内容混入几何层）给 delete/simplify/keep 建议，含删除范围 [start,end) 多删标题陷阱、附录重编号+悬空引用修复。See `references/relevance-trim-and-appendix-renumber.md`.

- "参考文献核验" / "核验参考文献" / "幻影引用" / "孤儿引用" / "reference verification" — triggers REFERENCE-LIST MACHINE VERIFICATION: 正则提取正文 [N] 引用 vs 列表条目，排除数学区间（κ∈[10,100] 误报）与双横线范围引用（[1--5]），输出幻影/孤儿/编号连续三类判定。See `references/reference-list-machine-verification.md`.

- "复审" / "re-review" / "带前轮P0清单复审" / "对抗性对照复审" / "逐条判定fixed/remain/partial" — triggers RE-REVIEW WITH ADVERSARIAL DEFECT-LIST INJECTION: 串行 5 代理直调 `deepseek-flash`（thinking=disabled）复审修订稿，前轮 P0–P3 清单作为对抗性上下文，要求每缺陷输出 fixed/remain/partial 判定，汇总为 已修复/未修复/部分修复 + 本轮新发现。完整执行配方（模型名、JSON 契约、~16-20s/代理串行、聚合规则、Lean 注释剥离计数）见 `references/rereview-adversarial-defect-list-execution.md`。

- \"评分收敛\" / \"P2/P3 无限递归\" / \"复审何时收尾\" / \"四轮复审轨迹\" — triggers REVIEW SCORE CONVERGENCE: 多轮复审的评分轨迹（6.2→7.1→7.3→7.5）、P0/P1 清零后 P2/P3 每轮重新出现的无限递归现象，以及收尾判据（评分跨越接受线 + P0/P1 连续清零 + 核心卖点稳固 + 五维度均衡 → 建议收尾而非无限修表述层）。见 `references/review-score-convergence-and-p2p3-infinite-recursion.md`。

- "P2/P3无限循环" / "复审收敛" / "评分稳定但每轮都有新P2/P3" / "要不要继续修表述层" — triggers REVIEW-CONVERGENCE-STOPPING RULE: 当 P0/P1 连续两轮清零 + 评分稳定跨越接受线（~7.0，Foundations of Physics）+ 核心卖点（0 公理/0 sorry/真编译/#print axioms 黄金门控）多轮审查从未被击穿时，剩余的 P2/P3 是**表述/文献精化的无限递归**——每轮审稿人都能挑出新瑕疵（[N] 缺作者年份、NuFit 版本号、摘要边界句措辞、E_{6w} 定义、表格分隔符），评分提升递减（7.3→7.5 仅 +0.2），且 P3 数量会从 11 膨胀到 31。此时应**主动建议收尾**（生成交付版 + 更新 memory），而非继续"修 P2/P3 → 再审 → 又发现新 P2/P3"的死循环。判据：P0/P1=0 且 `#print axioms` 干净且核心推导链未被击穿 → 收尾。V64 四轮实测：6.2→7.1→7.3→7.5，第 4 轮五维度全 7.5 且 bibliography 从 6.5 跃升 7.5，之后停止。
- "分支比解耦" / "存在性定理" / "existence proof" / "引入参数闭合两个观测量" / "反向工程自由参数" / "covariant mass-transfer dynamic" — triggers EXISTENCE-PROOF-REVERSE-ENGINEERING DETECTION: 当作者/审稿人提议「引入参数 X 同时闭合两个观测量」时，检查 X 的定义式是否把观测值写进分子（f_DE = 0.682/(...) 中的 0.682 即待解释的 Ω_DE）；∃-存在性定理在数学上平凡（任何目标值都可被一个自由参数吸收），存在性 ≠ 动力学闭合；清洁的 0-sorry 代数证明不能拯救物理过度声称。另含 smoke-test 断言陷阱（`assert 'OK' in smoke` 失败，deepseek-flash 不原样回显，应 `assert smoke` 非空）。见 `references/existence-proof-reverse-engineering-detection.md`。

- "清除历史版本残留" / "参考文献重建" / "公理计数统一" / "投稿前清理 md+lean" / "把关键公式标注序号" — triggers PREPRINT-SUBMISSION CLEANUP: 投稿前清理完整方法论——历史版本残留清除（[Vxx correction]/WITHDRAWN/日期戳/审查记录段落，含小写 withdrawn 保留、附录误删恢复）、参考文献重建（范围引用展开/幻影 vs 孤儿/作者名补编号）、公理计数统一（多重矛盾口径→实测）、纯文本 md 公式编号（字母后缀乱序→连续重排的精确替换法见 references/equation-renumbering-letter-suffix-to-sequential.md）、lean 注释清理 + 活跃代码完整性验证。See `references/preprint-submission-cleanup.md`. 三类痕迹精确分类（历史版本/修改时间/修改错误）+ 删工作日志留诚实声明(withdrawn/not an active declaration)的判断原则 + str.replace 改写句子产生重复的陷阱（new_string 带入原文后续内容，Cosmic Noon 案例）：`references/revision-mark-cleanup-rewrite-duplication.md`.

- "删除修正过去版本内容的论述" / "按PRD体例重构" / "精简版本修正论述" / "优化科技论文文字" / "投稿前清理" — triggers VERSION-COMMENTARY STRIP + PRD RECONSTRUCTION: the pre-review cleanup workflow — strip [V17 FIX]/[WITHDRAWN]/date-stamps/cross-refs/honest-axiom notes, resolve the contradictions the commentary was masking (fossilized-GW vs withdrawn DM=GW, dual numeric values), rebuild to standard PRD skeleton, THEN run the 5-agent review. See `references/version-commentary-strip-prd-reconstruction.md`. Single API call with 8-axis matrix + 5-section output. Use when user explicitly requests v4-pro or cross-paper consistency audit across 3+ papers. See `references/v4pro-multi-paper-cross-review.md`.
- "系列论文审查" / "统一框架文档" / "母框架" / "跨论文参数不一致" / "同一系列多篇论文" — triggers UMBRELLA-FRAMEWORK PREREQUISITE: 审查共享同一理论框架的系列论文前，必须先查找并加载母框架文档，否则会把框架内角色分工（UV/IR 跑动两端、双分量谱隙、双实形式）误判为跨论文 P0 矛盾。另含 v4-flash 幻觉论文编号 + 审计脚本嵌套块注释 sorry 假阳性两个陷阱。See `references/multi-paper-umbrella-framework-prerequisite.md`.
- "表演性诚实" / "honest-axiom 是注释不是属性" / "公理计数矛盾" / "revision 只是加标签" — triggers PERFORMATIVE-HONESTY DETECTION: check whether claimed `@[honest_axiom]`/`@[phenomenological]` attributes are REAL Lean attributes or commented-out text, recount axiom/line stats against the actual file, verify circularity wasn't just migrated axiom→def. See `references/performative-honesty-detection.md`.

- "诚实化只落在正文" / "正文已诚实但Lean未同步" / "body-Lean divergence" / "honestification asymmetry" / "正文写-2ℓt但Lean仍-ℓt" / "保守Metzler谱界" / "迹配对不正定" — triggers HONESTIFICATION-ASYMMETRY DETECTION: 当诚实性评分(7.5)≈技术/形式化评分(3.5-4.5)的2倍时，诚实化只落在正文文字层、未传导到Lean代码层。检测：正文每处"已修正"值，grep Lean的旧值（如正文 e^{-2ℓt} vs Lean exp(-ell*t)）。附带可复用数学事实：保守Metzler生成元(列和为零)谱界=0(主特征值≠5.47)；B=Re tr(XY)在sl(6,C)上不正定(须限su(6)用⟨X,Y⟩=-Re tr(XY))。See `references/honestification-asymmetry-body-vs-lean.md`.

- "权威Lean声明计数" / "axiom数不一致" / "附录计数vs实测" / "def vs noncomputable def" / "grep行首计数" / "108 axiom vs 110" — triggers LEAN-DECLARATION-COUNT AUTHORITATIVE METHOD: use line-anchored `grep -cE '^\s*axiom\s'` (NOT `grep -c "^axiom "` which undercounts indented, NOT Python regex which overcounts decoration) as ground truth; def total splits into plain def + noncomputable def (126 = 86 + 40); align appendix self-reported count for EVERY declaration type (structure/class drift too). See `references/lean-declaration-count-authoritative-method.md`.
- "0 axiom是文本统计还是内核验证" / "文本计数≠lake build" / "声称0 axiom但编译失败" / "AI生成Lean证明未编译" / "lake build验证0 axiom" — triggers TEXT-COUNT VS KERNEL-VERIFICATION: a text-level "0 axiom / 0 sorry / N theorem" (strip nested block comments + line-anchored grep) matching the paper's Appendix A self-report is NOT kernel verification — `lake build` may still fail with dozens of tactic-level proof-body errors (field_simp/ring/linarith/simpa not closing, whnf heartbeat timeout, Type mismatch, metavariable, unknown-constant cascade). The paper's honest "not compiled" claim is accurate but means the formalization is UNVERIFIED until `lake build` passes; `#print axioms` also requires a successful compile. Full error→theorem mapping methodology + V19 case (30 errors / 20 theorems) in `mathlib-offline-build/references/lake-build-verification-vs-text-count.md`.
- "把所有假等式公理改成def" / "假实数等式axiom改def" / "axiom改def修复" / "log值假等式" — triggers FALSE-EQUALITY-AXIOM→DEF REPAIR: 孤立公理（grep 名字 1 次=零引用）+ 假等式（十进制近似当精确）→ 改 `def 名 : ℝ := 数值`（保留数值、消除假声明），而非删除；含幻影占位声明诚实标注、编译验证、计数一致性核对。See `references/false-equality-axiom-to-def-repair.md`.
- "编译通过但数学错误" / "正文写对但Lean没同步" / "公理伪装谱定理" / "隐含假设未披露" / "历史方程残留" / "投稿适配性终审" / "评估是否适合投稿某期刊" / "5代理终审" — triggers PAPER-LEAN P0 HARD-ERROR FIX PATTERNS: 五类「编译通过但数学错误」的 P0 修复（正文-Lean 双向脱节 / 公理伪装谱定理→targetRatio def / 比例方向写反 / 隐含假设未披露→注释诚实披露不删定理 / 历史方程残留→基准对齐+历史版本标注）+ 5 代理投稿适配性终审配方（consistency/technical/logic/lean_specialist/publication 角色分工 + 编译独立复现 + 诚实性 vs 技术严谨性分裂诊断）。See `references/paper-lean-p0-hard-error-fix-patterns.md`.
- "axiom签名引用的类型零定义却编译通过" / "grep 类型名只出现1次" / "#check 模块外 unknown identifier 但 lake build 成功" / "autoImplicit 幻影" / "签名里 UndefinedType" — triggers LEAN AUTOIMPLICIT PHANTOM-TYPE DETECTION: Lean 4 `autoImplicit`（默认开）把 axiom 签名里的未知类型标识符静默当作隐式绑定变量，`lake build` 成功但该类型全文件零定义。检测三步：grep 类型名计数=1 → 模块外 `#check` 报 unknown identifier → 最小复现确认 autoImplicit 机制。判定=「签名类型计数1 + 模块外#check失败 + lake build成功」。修复=删除悬空 axiom（死代码）。比已知「theorem 证明体引用未定义名直接编译失败」更隐蔽。See `references/lean-autoimplicit-phantom-type-reference.md`.
- "axiom 签名含未定义类型" / "phantom axiom signature" / "编译通过但符号零定义" / "autoImplicit" — triggers LEAN-AUTOIMPLICIT-PHANTOM-AXIOM: Lean 4 `autoImplicit` 把 axiom 签名中未定义的标识符当作隐式自动绑定变量（编译通过、无数学内容、零引用死代码）。检测三步：grep 符号名计数==1 → 模块外 `#check` 报 unknown identifier → 最小文件复现编译通过。见 `references/lean-autoimplicit-phantom-axiom-signature.md`。

- "根据最新手稿修改Response" / "同步回应文件" / "Response_to_Reviewers 过时" / "手稿↔回应一致性" — triggers PAPER-RESPONSE-SYNC: 手稿迭代后把 Response 文件里过时声明（标题/模型名/参数/章节号/术语方向）同步到最新手稿。以手稿为准（术语方向可能反转审稿人建议），审稿人原话不改，run 级替换保留格式，补入最新结论数字。见 `references/paper-response-to-reviewers-sync.md`。

- "换名复发" / "零内容公理又出现" / "relabeled recurrence" / "孤立公理" / "isolated axiom" / "≈偷换成=" — triggers RELABELED-RECURRENCE + ISOLATED-AXIOM AUDIT: after a prior review claimed "zero-content axioms removed", re-audit the NEW axiom list for the same defect class under new impressive names (e.g. `a_t3_harish_chandra_lower_bound : (35:ℝ)≤35`); run reference-count audit to flag isolated axioms (declared but never referenced = fake or filler); recompute every numeric-assertion axiom against Python precise values to catch "≈ written as =". See `references/relabeled-axiom-recurrence-and-isolated-audit.md`.
- "把假设升级为推导" / "参数化假设升级为第一性原理" / "status escalation" / "re-label Ansatz as derivation" / "第一性原理推导过度声称" — triggers STATUS-ESCALATION OVERCLAIM DETECTION: check whether a quantity was re-labeled from [PARAMETERIZATION hypothesis]/Ansatz to "first-principles derivation"/"rigorous theorem" without a genuine derivation chain (case: Seeley-DeWitt heat-kernel a₁ → anomalous dimension η_k projection is an unproven Ansatz; formula η_k=C₂(adj)·h^∨/dim(M) not in FRG literature; anomalous dimension is a dynamical quantity not a pure group invariant). See `references/status-escalation-overclaim-detection.md`.

- "分支比解耦" / "branching ratio decoupling" / "引入参数闭合数值矛盾" / "existence theorem vs dynamical closure" / "代数存在性 ≠ 动力学闭合" / "反向工程自由参数" / "parameterization disguised as dynamical closure" — triggers PARAMETERIZATION-DISGUISED-AS-DYNAMICAL-CLOSURE DETECTION: when a paper introduces a branching-ratio/coupling/fraction parameter to "close" a numerical tension AND the parameter is defined using the observed value itself (reverse-engineered), the resulting "∃ parameter" theorem is trivially true (any target value is hit by a free parameter) and must be labeled [P] phenomenological — NOT narrated as "covariant mass-transfer dynamic"/"dynamical mechanism". Honestification is text-only (label [P] + register in K/C/A/P/O table + "PARAMETERIZED not RESOLVED" + mark dynamical derivation [O]); the Lean existence proof itself is fine and stays untouched. See `references/parameterization-disguised-as-dynamical-closure.md`.
- "对所有具体数学计算结论是否准确给出评审" / "数学计算准确性专项" / "论述自洽性+数学推导完备性终审" — triggers MATH-CLAIM INDEPENDENT VERIFICATION: 逐条提取数值断言→Python 独立重算→五类判定；套用 4 判据识别反向工程（参数=观测值反推 / 循环公理对 / 表演性声明 / 零内容公理）。See `references/math-claim-independent-verification.md`.
- "评估审稿意见是否正确" / "根据母框架物理动机评估" / "审稿说混用/矛盾，但真的是矛盾吗" — triggers FRAMEWORK-PHASE REVERSAL: when a review flags "object A/B mixing" as a contradiction requiring unification, first check whether the PARENT framework assigns A/B as two ENDPOINTS/PHASES of an evolution (UV↔IR, dual real forms). If so, the correct fix is explicit role division + transition map (Wick rotation / real-section locking), NOT "unify to one". Multi-model consensus on the wrong fix is still wrong — arbitrate against the theory's own physical motivation. See `references/reviewer-contradiction-vs-framework-phases.md`.
- "多论文联合审查" / "统一框架" / "系列论文" / "审查 CGICE+V17+V63+V16" / "消除四篇论文之间的不自洽" — triggers PARENT-FRAMEWORK REVIEW PREREQUISITE: before jointly reviewing a set of papers sharing a master/unified framework, LOAD the parent framework doc FIRST (e.g. SL6C_Unified_Geometric_Dynamics_Framework.md) and extract its "already-resolved mechanism list" (dual spectral gap, UV/IR running, real-form role division). Otherwise you will misjudge framework-resolved mechanisms as cross-paper P0 contradictions. Three-way re-adjudication: framework-resolved (→ annotation clarification) / genuine error (→ delete) / needs honest label. See `references/parent-framework-review-prerequisite.md`.

- "分支比闭合矛盾" / "存在性定理吸收观测量" / "反向工程自由参数" / "语言借用还是方程遵循" / "三阶段遵循CGICE吗" / "跨论文动力学遵循度" / "内部一致性 vs 动力学遵循度" — triggers CROSS-PAPER DYNAMICS-COMPLIANCE REVIEW: three dimensions — (1) 存在性参数化≠动力学闭合（参数定义式把待解释观测量写进分子反解=反向工程，即便 Lean 代数 0 sorry；存在性定理平凡=任何目标值可被一个自由参数吸收）；(2) 语言借用 vs 方程遵循（子论文每个因果箭头逐条判 follows/partial/language_only，是否母方程直接推论）；(3) 双维度评分区分（内部一致性 6.5 ≠ 跨论文动力学遵循度 4.8，报告须显式区分两个维度）。See `references/cross-paper-dynamics-compliance-review.md`.
- "η_k 是 72/35 还是 36/35" / "异常维度归一化" / "g_TC 是 FRG 定点还是 D1 耦合" / "三个谱对象" / "λ_∥ vs λ₁ vs λ_⊥ 混同" / "SL6C 参数对齐" — triggers SL6C PARAMETER ALIGNMENT: 重构/审查 SL(6,C) 系列时，η_k 权威值 = 36/35（Hermitian 约定 C_A=h^∨=6，NOT 72/35=Killing 约定）；g_TC 双值区分（FRG 定点 g*≈1.8395=12π²/35 vs D1 瞬子耦合 2.60=24π²/35，"2.60 不是 FRG 定点"）；三谱对象区分（λ_∥=35 自由 Laplacian 谱底 / λ₁≥29 Witten 隙 / λ_⊥=35/3 独立匹配输入，绝不混同）。See `references/sl6c-parameter-alignment-v18-cgice-20260917.md`（含 V18 公理架构 A-F、定理状态表、Lean 计数 80/151/43/113）。
- "整合四篇论文到统一框架" / "同步框架文档统计表" / "把框架文档对齐到论文最新状态" / "框架文档 Lean 统计表过时" — triggers FRAMEWORK-DOC SYNC: 独立实测每个 Lean 文件的活跃声明数（含 `@[...]` 装饰器前缀的正则），对账"论文自报 vs 实测"，区分版本漂移/复核一致/口径差异，用整行锚定精确替换（禁止全局裸数字替换），密度列随行数重算。See `references/paper-self-reported-vs-measured-framework-sync.md`.
- "多论文评分表" / "幻觉论文编号" / "漏掉某篇论文" — PITFALL: v4-flash generating a multi-paper score table HALLUCINATES paper labels (real case: dropped CGICE V9.1, invented a non-existent "V18", mislabeled each paper's role). Fix: in the review prompt, enumerate every paper by exact name + role + key params (e.g. "1. CGICE V9.1 = dynamics core, 73 axioms; 2. V17 = geometry base..."), and require the score table to cover EXACTLY those N names. Verify the table has N rows before saving.
- "对所有具体数学计算结论是否准确给出评审" / "数学计算结论准确性" / "数值是否算对" / "verify all numerical/calculation conclusions" — triggers MATH-CALCULATION-ACCURACY REVIEW: extract every numerical claim (incl. table cells + Lean numeric-assertion comments), independently recompute each (Python precise calc + hand algebra), classify into ✅arithmetic-correct / 🔴P0 calc-error / 🟠P1 internal-inconsistency / 🟡P2 statement. Core insight: definitional arithmetic (τ, α reciprocity, ln values, powers) is almost always right; numbers carrying physical predictions (N_e, g_TC flow, Landau pole, μ_crit, |ρ|², H₀t₀) are where errors cluster. See `references/math-calculation-accuracy-review.md`.
- "import 属性文件缺失" / "@[honest_axiom] 但注册文件不存在" / "表演性诚实 v2" / "import HonestAttr" / "红移公式反推" / "f = f₀·e^(-N_e)" / "指数衰减差数量级" — triggers IMPORT-GHOST-ATTRIBUTE + REDSHIFT-REVERSE-CHECK: (a) 表演性诚实新变体——@[honest_axiom] 从注释升级为活跃属性 + 头加 `import HonestAttr`，但 HonestAttr.lean 注册文件不存在→无法编译+属性未注册；三步检测(grep import→find 注册文件→编译验证)。(b) 指数红移公式 f_obs=f₀·e^(-N_e) 的独立重算 + 反推 N_e=ln(f₀/f_obs) 对比论文声称值，差数量级即"校准伪装成推导+算术错误"。See `references/import-ghost-attribute-and-redshift-reverse-check.md`.
- "维度不闭合" / "multiplicity 维度账" / "restricted root multiplicity" / "对称空间维数" / "正根数" — triggers SYMMETRIC-SPACE DIMENSION FALSE-POSITIVE: 审稿人声称维度不闭合时，先独立重算 dim = rank + 正根数×multiplicity（A_n 正根数 = n(n+1)/2，不是 rank；SL(6,C)/SU(6) = 5 + 15×2 = 35 闭合）。See `references/symmetric-space-dimension-false-positive.md`.

- "多个审稿人同时报告数值矛盾" / "agent 集体误判" / "摘要数值矛盾" / "独立核验 agent 数值发现" / "数值 agent 重算错了" — triggers AGENT-FALSE-POSITIVE + INDEPENDENT-VERIFICATION: 当多个评审 agent 同时报告同一"数值矛盾/计算错误"时，先独立重算算术 + 检查语法歧义（冒号/分号把两条独立链拼接），再检查 agent 自己的重算是否有惯例错误（Dirac/Weyl 费米子 4/3 vs 2/3 系数、T_F=1/2 基本表示因子、Killing 度规归一化），最后才定性 P0。案例：V17 摘要 "5.00→5.47: 0.46%..." 被 5 agent 集体误读为算术矛盾，实际 0.46%×148≈0.68≈Ω_DE 是独立自洽链。合成报告必须附"agent 误判纠正"表。See `references/agent-false-positive-independent-verification.md`.

- "10^N 数量级矛盾" / "差 10²⁴" / "单位转换漏算" / "漏了 ℏ/c/k_B 转换" / "固定点因子漏 1/2" / "论文正确但审稿人算错" — triggers UNIT-CONVERSION & PREFACTOR FALSE-POSITIVE: 当审稿人报告"差 10²⁴ 倍"或"固定点算错"时，先 grep 论文是否已显式写了单位转换句（ℏ=6.582×10⁻²⁵ GeV·s 等）并自行代入转换因子；固定点类先独立重算（β(g)=ηg/2 的 1/2 因子极易漏）；两审稿人对同一量给出互相矛盾的数值时，必有一方错，自行重推仲裁。另含跨论文推导度机器量化法（grep 两 Lean 文件 `^(theorem|lemma)` 名集合→交集=转录/follows、差集=新增/language_only、未转录=透明度缺口）。See `references/reviewer-unit-conversion-and-prefactor-false-positives.md`.

- "正文已修正但Lean未同步" / "双向脱节" / "正文诚实化 vs Lean语义脱节" / "编译通过但数学错" / "硬算术错误" / "正文自报公式与Lean定义不一致" / "观测输入伪装成谱定理" / "迹配对不正定" — triggers BODY-VS-LEAN DESYNC + HARD ARITHMETIC FIX: 终审时对照正文自报公式与 Lean 实际定义（ouCov 指数、观测输入 vs 谱定理、正定性隐含假设），修复须双向同步（正文 + Lean 定义/注释）。三例硬算术错误（ouCov 因子2、metzler 比例 v/u→u/v、PF 公理伪装谱定理→targetRatio def）完整修复 recipe 见 `references/body-vs-lean-desync-and-hard-arithmetic-fixes.md`。

## 核心检测规则 (Core Detection Rules) — v1.1 新增

> **使用说明**：以下 5 组检测规则为强制检查项。每个 reviewer agent 在输出 findings 前，必须先跑完对应类别的 checklist；未跑 checklist 的 finding 视为无效。所有规则均**只增强、不删除**原有 pipeline 行为。

### 规则组 A：公理自洽性检测 (Axiom Self-Consistency)

**触发条件**：论文含 `axiom` / `postulate` / `assumption` / `定义式` / Lean/Coq/Isabelle 代码块 / "我们假设" / "我们定义"。

**A1. 可证 False 检测 (Provably-False Axiom)**
- 对每条公理/假设，尝试在标准数学语义下构造反例或直接代入数值验证。
- 若公理形如 `x = c`（c 为具体数值），用高精度独立重算 c（Python `mpmath` / `sympy`），偏差 > 1e-6 相对误差即判 **P0**。
- 若公理形如 `P → Q`，检查是否存在已知 P 为真而 Q 为假的实例；存在即 **P0**。
- 若公理断言不等式 `a ≤ b`，代入数值验证；若 `a > b` 则 **P0**（例：`(35:ℝ) ≤ 35` 若写成 `≤ 34` 即假）。

**A2. 循环定义检测 (Circular Definition)**
- 构建公理依赖图（谁引用谁）。检测长度 ≥ 2 的有向环。
- 若环内所有节点均为 `axiom`/`def` 且无外部锚点（无经验输入、无独立定理支撑），判 **P0 循环公理对**。
- 特别警惕：`A := f(B)` 且 `B := g(A)` 且 f∘g = id 的伪装形式——这是"用定义互相证明"。

**A3. 假实数等式检测 (False Real-Equality)**
- 任何形如 `def x : ℝ := 3.14159` 或 `axiom h : π = 3.14159` 的十进制近似当精确值，判 **P0**。
- 修复建议：改为 `def x : ℝ := Real.pi` 或显式标注 `≈` 并降级为 `def`（非 `axiom`）。
- 若论文正文写 `=` 但附录写 `≈`，判 **P1 内部不一致**。

**A4. 空壳桩检测 (`:= True` / `:= trivial` / `sorry` 桩)**
- grep 所有 `axiom .* : True`、`:= trivial`、`:= by sorry`、`:= by admit`。
- 每个空壳桩单独计数；若空壳桩数量 > 论文声称的"核心定理数"的 20%，判 **P0 表演性形式化**。
- 检查 `sorry` 是否被嵌套在块注释中——嵌套块注释内的 `sorry` 是**假阳性**，不计入（见 `references/multi-paper-umbrella-framework-prerequisite.md`）。

**A5. 孤立公理检测 (Isolated Axiom)**
- 对每条公理名做引用计数（grep 名字出现次数）。出现 1 次（仅声明处）= 零引用 = **P1 填充性公理**。
- 若孤立公理同时满足 A1（可证 False）或 A3（假等式），升级为 **P0**。
- 警惕"换名复发"：上一轮审查删除的缺陷公理，以新名字重新出现（见 `references/relabeled-axiom-recurrence-and-isolated-audit.md`）。

**A6. 公理计数一致性**
- 论文声称"共 N 条公理"→ 实际 grep 计数必须 = N。
- 声称"已移除零内容公理"→ 重新审计新公理列表，检查同类缺陷是否换名保留。
- 计数不符判 **P1**；若差异涉及核心定理判 **P0**。

---

### 规则组 B：诚实性检测 (Honesty & Integrity)

**触发条件**：论文含 `@[honest_axiom]` / `@[phenomenological]` / "严格推导" / "第一性原理" / "rigorous" / "theorem" / 引用文献 / 校准参数。

**B1. 表演性诚实检测 (Performative Honesty)**
- 检查声称的 `@[honest_axiom]` / `@[phenomenological]` 属性是否为**真实 Lean 属性**（在 Lean 中可被 `#check` 识别）还是**注释掉的文本**。
- 若属性仅存在于注释/文档字符串中，判 **P0 表演性诚实**。
- 重新计数 axiom/line 统计，与论文正文声称的数字对比；不符判 **P0**。
- 检查循环性是否只是从 `axiom` 迁移到 `def`（换汤不换药）——若 `def` 仍依赖循环链，判 **P0**。

**B2. 幻影引用检测 (Phantom Citation)**
- 对每条引用 `[N]`，检查参考文献列表是否存在对应条目。
- 对每条参考文献，检查 DOI/arXiv 编号是否可解析（若工具可用）。
- 幻影引用（正文引用但列表无）判 **P0**；列表有但正文未引用判 **P2**。
- 警惕 v4-flash 幻觉论文编号（见 `references/multi-paper-umbrella-framework-prerequisite.md`）。

**B3. 校准伪装成推导检测 (Calibration-Disguised-as-Derivation)**
- 检查每个"推导得到"的数值：其上游是否有独立的第一性原理链条，还是反向从观测值反推参数。
- 4 判据识别反向工程：
  1. 参数值 = 观测值（到小数点后多位）= 疑似反推
  2. 循环公理对（A 定义 B，B 定义 A）
  3. 表演性声明（"严格证明"但无证明代码/步骤）
  4. 零内容公理（`x = x` 形式）
- 命中 ≥ 2 判据判 **P0 校准伪装**。

**B4. 状态升级过度声称检测 (Status-Escalation Overclaim)**
- 检查是否有量从 `[PARAMETERIZATION hypothesis]` / `Ansatz` 被重新标记为 "first-principles derivation" / "rigorous theorem" 而无真实推导链。
- 案例：Seeley-DeWitt heat-kernel a₁ → anomalous dimension η_k 投影是未证 Ansatz；公式 `η_k = C₂(adj)·h^∨/dim(M)` 不在 FRG 文献中；anomalous dimension 是动力学量而非纯群不变量。
- 无推导链的升级判 **P0**；推导链不完整判 **P1**。
- 见 `references/status-escalation-overclaim-detection.md`。

**B5. 母框架诚实标注 vs 正文过度声称**
- 若母框架已诚实标注"不闭合"，但论文正文仍称"闭合"，判 **P0 内部矛盾**。
- 检查"已撤回"的声明（如 DM=GW）是否在正文残留（见 `references/triple-gw-v17-review-record.md`）。

**B6. 诚实性 tells 细目（BootLoops prose-lint E，v1.3 新增）**
- 规则组 B1–B5 聚焦公理/引用/校准层面的诚实性；B6 补**句子级/数字呈现级**的诚实性 tell。逐条 grep，命中即记录，不用眼扫。
- **B6.1 捏造精确性**：编数字/计数/日期当数据。只用有真实来源的量；估计值显式标"估计"或删。宁可要更小但已核实的 claim，不要更大但臆测的。
- **B6.2 重要性通胀**：声称某事"被需要"/"比实际更重要"。只声称真实——"at the frontier of what is computable"（可计算前沿），非"what the field needs"（领域所需）。
- **B6.3 出处错误**：错标谁构建/撰写/发现。对照真实 repo/论文核验，不靠记忆。
- **B6.4 结果过度声称**：把 partial/未验证结果 round up 成"done"。报告真实状态；绝不暗示通过了没通过的检查。
- **B6.5 自信模糊**：把有争议/近似的事实（"a first"/记录/日期）平铺直叙。要么 pin 来源，要么精确 hedge，绝不模糊。
- **B6.6 封闭区间/引号完整性**（最易漏）：(a) 认证区间**向外**舍入——下端点向下、上端点向上，认证下界只能向下舍；(b) 引号需逐字收据——fair paraphrase 加引号=出处错误；(c) error-bound/residual 摘要只能**保守方向**舍入（1.06×10⁻⁷ 的 agreement 不是"10⁻⁷"），逐条 trace 数量级摘要回源值并查舍入方向。
- 详细 checklist 见 `references/prose-lint-honesty-number-discipline.md`。

---

### 规则组 C：跨章节一致性检测 (Cross-Section Consistency)

**触发条件**：论文有多章节 / 多版本 / 多附录 / 系列论文。

**C1. 多版本数值残留检测 (Multi-Version Numerical Residue)**
- 对每个关键数值，grep 全文所有出现位置，检查是否一致。
- 若某节已标注 `[V17 FIX]` 但兄弟节仍用旧值，判 **P0 内部自相矛盾**。
- 警惕"旧频率比 10² 残留"（见 `references/triple-gw-v17-review-record.md`）。

**C2. 计数矛盾检测 (Count Contradiction)**
- 论文声称的定理数/公理数/引理数/公式数 → 实际计数必须一致。
- 声称"共 N 个"但实际列出 M ≠ N，判 **P1**；若涉及核心贡献判 **P0**。

**C3. 维度错误检测 (Dimensional Error)**
- 对每个物理量，检查量纲：`[L]`、`[T]`、`[M]`、无量纲。
- 等式两边量纲必须一致；不一致判 **P0**。
- 特别检查：频率 vs 温度（`hf/k_B` 换算）、能量 vs 质量、长度 vs 时间。

**C4. 物理量混淆检测 (Physical-Quantity Confusion)**
- 频率比当温度比（`f-ratio` 误标为 `T-ratio`，经 `hf/k_B` 换算，3.44K vs 21.6K 案例）判 **P0**。
- 检查所有"比"、"率"、"系数"的分子分母定义是否前后一致。
- 见 `references/math-calculation-accuracy-review.md` §10。

**C5. 跨论文参数不一致检测**
- 系列论文共享同一理论框架时，参数值/符号/约定必须一致。
- 不一致判 **P1**；若导致结论矛盾判 **P0**。
- **前置条件**：审查系列论文前必须先查找并加载母框架文档，否则会把框架内角色分工（UV/IR 跑动两端、双分量谱隙、双实形式）误判为跨论文 P0 矛盾（见 `references/multi-paper-umbrella-framework-prerequisite.md`）。

**C6. 框架相位反转检测 (Framework-Phase Reversal)**
- 当审稿意见标记"对象 A/B 混用"为矛盾要求统一时，先检查母框架是否将 A/B 分配为演化的两个**端点/相位**（UV↔IR、dual real forms）。
- 若是，正确修复是显式角色划分 + 过渡映射（Wick rotation / real-section locking），**不是**统一。
- 误判为矛盾判 **P1 审稿误判**。

---

### 规则组 D：Severity 分级标准 (P0–P3)

> **原则**：P0 = 阻断级（阻断发表/阻断 pipeline 推进）；P1 = 重大（需修订但非阻断）；P2 = 中等（建议修订）；P3 = 轻微（文字/格式）。

**P0（阻断级）— 任一命中即阻断**
- 可证 False 的公理/定理（A1）
- 循环定义/循环公理对（A2）
- 假实数等式当精确值（A3）
- 空壳桩占比 > 20%（A4）
- 孤立公理 + 可证 False 或假等式（A5 升级）
- 公理计数不符且涉及核心定理（A6 升级）
- 表演性诚实（B1）
- 幻影引用（B2）
- 校准伪装成推导（B3，命中 ≥ 2 判据）
- 状态升级无推导链（B4）
- 母框架诚实标注 vs 正文过度声称（B5）
- 多版本数值残留导致自相矛盾（C1）
- 维度错误（C3）
- 物理量混淆（C4）
- 跨论文参数不一致导致结论矛盾（C5 升级）

**P1（重大）**
- 内部不一致（`=` vs `≈`）（A3 降级）
- 孤立公理（零引用，未命中 A1/A3）（A5）
- 公理计数不符（未涉及核心定理）（A6）
- 推导链不完整的状态升级（B4 降级）
- 计数矛盾（未涉及核心贡献）（C2）
- 跨论文参数不一致（未导致结论矛盾）（C5）
- 审稿误判（框架相位反转）（C6）

**P2（中等）**
- 参考文献列表有但正文未引用（B2 降级）
- 符号/约定不统一但不影响结论
- 图表编号错乱
- 术语不一致

**P3（轻微）**
- 拼写/语法/标点
- 格式/排版
- 引用风格不统一

**Severity 升级规则**：
- 同一缺陷在多个章节重复出现 → 升级一级
- 缺陷涉及核心定理/主结论 → 升级一级
- 缺陷被作者明确声称"已修复"但实际未修复 → 升级一级

**Severity 降级规则**：
- 缺陷位于附录/补充材料且不影响主结论 → 降级一级
- 缺陷为已知约定（如 `≈` 显式标注）→ 降级一级

---

### 规则组 E：审查员算术假阳性验证 (Reviewer Arithmetic False-Positive Verification)

**触发条件**：审查员报告"数值矛盾"/"算术错误"/"多个审稿人一致判算术错"/"5 agent 全部误判"/"摘要歧义导致集体误读"。

**E1. 独立重算优先**
- 在将审查员的算术 finding 作为 P0 转达前，**必须**独立重算被标记的算术。
- 用 Python `mpmath` / `sympy` 高精度重算，不依赖审查员给出的中间值。

**E2. 摘要歧义检测**
- 检查被标记的句子是否因措辞歧义**拼接了两条独立链**（例：`0.46%→Ω_DE` vs `5.00→5.47` 案例）。
- 若是，判 **P1 表述歧义**（非 P0 算术错），修复建议为拆分句子。

**E3. 约定依赖值重算**
- 对约定依赖的值（T_F index、normalization）自行重算。
- 审查员会犯约定错误（`b₀=12` 案例）；不盲信。
- 见 `references/reviewer-arithmetic-false-positive-verification.md`。

---

- "公理自洽性" / "可证False" / "循环定义" / "假实数等式" / "空壳桩" / ":=True" / "sorry桩" — triggers AXIOM SELF-CONSISTENCY AUDIT (规则组 A): 逐条公理跑 A1–A6 checklist（可证 False / 循环定义 / 假实数等式 / 空壳桩 / 孤立公理 / 计数一致性）。See `references/axiom-self-consistency-audit.md`.
- "诚实性" / "表演性诚实" / "幻影引用" / "校准伪装成推导" / "状态升级" — triggers HONESTY & INTEGRITY AUDIT (规则组 B): 跑 B1–B5 checklist（表演性诚实 / 幻影引用 / 校准伪装 / 状态升级 / 母框架诚实标注）。See `references/honesty-integrity-audit.md`.
- "跨章节一致性" / "多版本数值残留" / "计数矛盾" / "维度错误" / "物理量混淆" — triggers CROSS-SECTION CONSISTENCY AUDIT (规则组 C): 跑 C1–C6 checklist（多版本残留 / 计数矛盾 / 维度错误 / 物理量混淆 / 跨论文参数 / 框架相位反转）。See `references/cross-section-consistency-audit.md`.
- "severity 分级" / "P0 阻断" / "严重度判定" / "分级标准" — triggers SEVERITY CLASSIFICATION (规则组 D): 按 P0–P3 标准判定，套用升级/降级规则。
- "审查员算术假阳性" / "集体误读" / "约定错误" — triggers REVIEWER ARITHMETIC FALSE-POSITIVE VERIFICATION (规则组 E): 独立重算优先，摘要歧义检测，约定依赖值重算。

- "正文诚实化 vs Lean 代码语义脱节" / "正文已修正但Lean未同步" / "编译通过但数学错" / "ouCov 因子2" / "paper-vs-lean semantic drift" — triggers PAPER-VS-LEAN SEMANTIC DRIFT: 终审核对不能只核对声明计数，还要核对正文公式语义 vs Lean 代码定义是否一致；正文已诚实化/修正但 Lean 代码未同步是最危险的脱节（编译 0 sorry 但数学错）。三个硬算术错误案例（ouCov 因子2、metzler 比例 u/v、PF 主特征值伪装谱定理）见 `references/paper-vs-lean-semantic-drift.md`。

---

### 规则组 F：三 Refinement Agents 检查项（ScientistTwo Table 7）— v1.2 新增

> Table 7 实证：三个 refinement agent（spec 合规 + 引用核查 + 方法-代码对齐）**全开**才 49/49 通过四项审计；关掉任意一个即出现引用幻觉（19/1840）或方法-代码错位（38/49）。
> **F1/F2/F3 三项在每次审稿中默认全开，不得单独关闭**；若因工具限制跳过某项，必须在报告中标 `F_x: SKIPPED(reason)` 并降级 gate 结论。

---

#### F1 — Spec 合规审计（Anti-Reward-Hacking）

**检查目标**：每条 finding 及其对应的论文 claim，是否满足论文**自己声明的规范/约束**，以及是否满足本次审稿任务声明的 rubric。

**检测动作**
1. 抽出论文中显式声明的规范集：`axioms / assumptions / 约束条件 / 不变量 / claimed scope(域、维数、能量区间) / rubric 条款`
2. 对每条 finding 的 `claim_at_issue` 逐条对照，判定三类状态：
   - `compliant`：claim 在声明范围内且被证据支撑
   - `reward-hacking`：**表面合规但实质绕过**——典型形态：①悄悄加入未被声明的辅助假设；②把结论缩到无意义的退化情形来换取成立；③用「在适当条件下」等无限定词替代真实条件；④改符号/改定义使约束字面满足
   - `violation`：claim 直接越过声明范围（如未声明适用范围却外推到整个参数空间）
3. 命中 `reward-hacking` 或 `violation` → 记为 **P0/P1**，并写出「被绕过的那条规范」原文

**输出字段**：`finding_id / declared_spec / status(compliant|reward-hacking|violation) / bypassed_spec_quote / severity`

**假阳性防范**：作者**显式声明并证明**的额外假设不算 hacking；仅当假设被隐藏、或声明后未给依据时才算。

---

#### F2 — 引用核查（Live-Search 逐条验证）

**检查目标**：升级现有 `bibliography-auditor`——**从「内部自洽核查」升级为「外部真实性核查」**。内部一致性（正文编号=文献表编号、引用格式统一）**不构成通过**。

**检测动作**
1. 提取**全部**参考文献条目（含正文中出现的所有 work）
2. 对**每一条**执行 live web search（arXiv / DOI / 期刊页 / 出版社页 / Semantic Scholar）逐条核验四要素：
   - 存在性（该文献真实存在）
   - 元数据匹配：标题、全部作者（含顺序）、年份、venue、卷期页
   - 标识符有效：DOI 可解析 / arXiv ID 指向该标题 / 否则说明来源
   - 具体引用位置的可支持性：该文献是否真的支持正文中引它时的那句话（防「存在但被误用/张冠李戴」）
3. 状态分级：
   - `verified`：四要素全匹配
   - `metadata-mismatch`：存在但标题/作者/年份/venue 有偏差 → **P0**（须修正或删除）
   - `unsupported-citation`：文献存在但**不支持**所引论断 → **P0**
   - `hallucinated`：live-search 查无此文献（或 ID 指向不同论文）→ **P0 + 一票否决**，禁止 PASS
4. 每条核查必须附**可复现证据**：查询串、命中的原始 URL/DOI、抓取日期。无证据的 `verified` 视为未核查。

**输出字段**：`ref_key / claimed_metadata / search_query / found_url_or_doi / status / severity / evidence_locations`

**执行约束**：无网络或搜索受限时，**不得**默认标记 `verified`，一律标 `unverified` 并在 gate 报告中降级（引文审核未完成 ⇒ 不得给出 PASS）。

---

#### F3 — 方法-代码/形式化对齐审计

**检查目标**：论文的方法描述必须与 **Lean / 代码 / 脚本实现** 逐条对齐。**禁止「论文声称 X 但代码里没有 X」**。

**检测动作**
1. 从论文 Methods / 形式化章节抽出**原子级主张清单**（每条 = 一个可判真假的实现陈述），例如：
   - 「Z₂ 等变 K 理论替代 Atiyah-Bott」
   - 「数值使用 4 阶 Runge-Kutta，步长 h=1e-3」
   - 「该不变量在 D=2 情形退化为 Chern 数」
2. 在 Lean/代码中**定位对应实现**，逐条给出：
   - `aligned`：代码中有对应实现且语义一致（附 `文件:行号` 或定理名）
   - `partial`：部分实现（如只在特例分支 / 只对某维度 / 被 `:=True` stub 或 `sorry` 占位）→ **P0/P1**，必须披露
   - `missing`：论文声称但实现中**完全不存在** → **P0 一票否决**，禁止 PASS
   - `extra`：实现中存在而论文未描述的关键机制（可能影响可复现性）→ **P2**，建议补写
3. 检查**参数/常量一致性**：论文数值表 ↔ 代码默认参数（步长、截断维度、容差、随机种子）
4. 检查**stub/占位披露完整性**：`sorry`、`:=True`、硬编码返回值、跳过分支必须在论文中显式披露（参照 Pitfall 5: `:=True` Stub Disclosure）

**输出字段**：`claim_id / claim_quote / code_anchor(file:line|theorem) / status(aligned|partial|missing|extra) / severity / disclosure_needed`

**执行约束**：无法访问实现文件时，标 `F3: BLOCKED(no_code_access)`，并在 gate 报告中标注「方法-代码对齐未验证」——不得凭论文自述推定 `aligned`。

---

#### 规则组 F 汇总输出（并入 Finding Output Format）

```
[F1] finding_id | status | bypassed_spec_quote | severity
[F2] ref_key | status(verified|metadata-mismatch|unsupported|hallucinated) | evidence_url | severity
[F3] claim_id | status(aligned|partial|missing|extra) | code_anchor | severity
F-Table7 通过判定: 三项全开且无 P0 → PASS; 任一项 SKIPPED/BLOCKED 或存在 P0 → 不得 PASS
```

**与流程的接口**：F1/F2/F3 在 Stage 2a/4a 审稿阶段执行；其结果同时作为 `## Quality Gates` 一票否决项与 `## Rebuttal Agent 闭环协议` R1 任务卡的输入源。

### 规则组 N：数字呈现一致性检测 (Number Discipline) — v1.3 新增

> **来源**：BootLoops `prose-lint` N 段（13 条）。核心原则：**每个数字出现在多个表面（正文 / 表格 / 图注 / 图标签 / 摘要），每一对表面都是一个静默矛盾位点**。这些是机械类矛盾，sweep 它们，不信任眼睛。规则组 N 与规则组 C（跨章节一致）互补——C 抓"值变了没同步"，N 抓"值没变但呈现方式制造了矛盾"。

- **N1 舍入方向**：测量到的数字/精度计数**绝不向上舍**——实测 23.85 位打印 23 非 24。achievement 数字永远朝更弱 claim 舍。
- **N2 减法一致呈现**：读者会相减的数字必须一致舍入——41.2 和 3.9 支持"37 位 gap"；独立 floor 成 41、3 后打印算术为假（38）。分解和同理：舍入列必须重组出舍入总和。
- **N3 每个 N/N 和 N-of-M 带单位**："812/812 exact"——是条目/列/行/成员？计数名词来自不同表面则错，直到对照源定义核对。
- **N4 显示平局**：值正好落在舍入平局（141/400=0.3525）在 float 格式（35.2）与 half-up 显示（35.3）打印不同——生成标签与正文静默分歧。显示标签从整数计数用精确 half-up 十进制算术算，绝不从 float。
- **N5 二代舍入**：已舍入值的比/差（0.172/0.126→1.37）≠ 未舍入计算（1.362）。逐字引源记录的数值；绝不"纠正"可引用记录。z-score/比"不能从显示输入重算"可能是从未舍入值精确算的——说明哪个约定算的。
- **N6 分解不求和→命名边界**：打印的部分凑不齐打印的总和，通常是一次分析里两个不同边界（按日期切的窗口、按不同方案赋的标签），不是过期数字。找到边界错配并说明，不 nudges 数字逼和。
- **N7 非嵌套分母**：两个过滤器可差一个 NET 计数（4201 kept vs 4178 kept，overlap 3900）："23 fewer"为真，"23 removed"为假。写任何子集从句前先查嵌套。
- **N8 反直觉方向数字带机制从句**：正确数字朝"错"方向动（样本翻倍功率反降）读作 typo。核实后，在每个打印处附半句机制。
- **N9 两个真数字一个假括号**：两个统计共享一个括号（"p=0.005；高于均值十五个标准差"）诱导读者合成两个都不支持的 claim。各自命名 provenance，或分开。
- **N10 情态词是数字的一部分**："the estimate can be 1.08 times the bound" 压缩成 "is 1.08 times" 把可能性变判定。压缩/重述 claim 时查情态（can-be/is/must-be）与查数字同样仔细。
- **N11 一符号一对象**：对易冲突字母做符号普查——同一字母一节作系数、一节作曲/矩阵/半径会误导追踪它的读者（同论点两义最糟）。改名较廉价实例并 sweep。词同理：同一术语技术义+普通义同段出现→首次出现 gloss 或改名。
- **N12 claim-bearing 连接散文**：关系从句静默附加可核查事实（"their best-fit model carries 的趋势"）——一致性 pass 必须覆盖数字周围的连接散文，不只数字本身。
- **N13 标识符完整性双向**：看似正确的标识符可能错、看似错的可能对——注册机构迁移前缀，带陌生前缀的 DOI 可能是真的、"canonical" 形式反而不再解析。归一化到熟悉形式前必须 resolve 两个候选；奇数者获胜时留 dated do-not-fix 注释。裸整数出现在该引用的位置可能是 citation-command misfire（numeric-style \citealp 输出"(cf. 9)"）——查书目渲染后再怀疑手打数字。
- 完整 13 条 checklist 见 `references/prose-lint-honesty-number-discipline.md`。

## 输出格式 (Finding Output Format) — v1.1 新增

每个 finding 必须包含以下字段，缺一不可：

```
[ID]        唯一编号（如 A1-001）
[类别]      规则组 A/B/C/D/E
[规则]      具体规则编号（如 A1 可证 False）
[严重度]    P0 / P1 / P2 / P3
[位置]      章节/行号/公式编号
[证据]      独立重算结果 / 引用计数 / 量纲检查 / grep 输出
[描述]      缺陷描述
[修复建议]  具体可操作修复
[置信度]    high / medium / low（low 置信度需标注为"待验证"）
```

**证据门槛**：无 `[证据]` 字段的 finding 视为无效，不得进入最终报告。
**置信度门槛**：`low` 置信度 finding 不计入 P0，最高 P1。

---

## How It Works

### Stage 2a: AWA Write Review Injection

After ARS Stage 2 (WRITE) completes with a full paper draft:

**Step 1 — Load AWA**: Load `academic-writing-agents` skill and `principles/academic-writing.md` (30 principles).

**Step 2 — Present deployment plan**:
```
## AWA Write Review — Deployment Plan

Draft complete: [N] pages, [M] references, [K] figures

Deploying 5 agents in parallel:
├── consistency-checker → Terminology, cross-refs, structural coherence
├── logic-reviewer      → Argument flow, transitions, narrative arc
├── technical-reviewer  → Math notation, methodology, result validity
├── writing-reviewer    → Prose clarity, conciseness, academic tone
└── bibliography-auditor → Bib completeness, arXiv updates, venue consistency

Each agent reads the full draft. Expected output: prioritized issue lists.
Proceed? (y/n/add agents)
```

**Step 3 — Deploy**: Use `delegate_task` with `tasks` array (max 3 per batch, 2 batches for 5 agents).

**Step 4 — Synthesize**: Merge findings → Critical/Important/Minor → present to user.

**Step 5 — User decides**: Which issues to fix before Stage 2.5 integrity check.

### Stage 4a: AWA Revision Review Injection

After ARS Stage 4 (REVISE) completes:

**Step 1 — Identify changed sections**: Compare revised draft vs original draft.

**Step 2 — Deploy 3 agents** (lighter than Stage 2a):
```
├── consistency-checker → Verify fixes + cross-refs on changed sections
├── writing-reviewer    → Check revision prose quality
└── technical-reviewer  → Verify technical corrections
```

**Step 3 — Synthesize**: Verify that ARS review concerns were actually addressed, flag any new issues introduced by revision.

**Step 4 — User decides**: Which residual issues to fix before Stage 3' re-review.

## AWA Agent Deployment Patterns

### Full Draft Review (Stage 2a)

```
Batch 1 (parallel):
  delegate_task(tasks=[
    {goal: "consistency-checker: Review terminology, cross-refs, figure-text alignment in [FILE]",
     context: "Read [FILE]. Load principles A1,A3,D3,D7. Report Critical/Important/Minor issues with line references.",
     toolsets: ["terminal", "file"]},
    {goal: "logic-reviewer: Review argument flow, transitions, narrative arc in [FILE]",
     context: "Read [FILE]. Load principles A2,A4,A5,A6,A7. Check GPS rhythm, paragraph closers, claim-first exposition.",
     toolsets: ["terminal", "file"]},
    {goal: "technical-reviewer: Check math notation, methodology, citations in [FILE]",
     context: "Read [FILE]. Load principles C1,C2,C3,E1,E2. Verify all equations explained, all named entities cited.",
     toolsets: ["terminal", "file"]},
  ])

Batch 2 (parallel):
  delegate_task(tasks=[
    {goal: "writing-reviewer: Review prose clarity, conciseness, tone in [FILE]",
     context: "Read [FILE]. Load principles B1-B8. Flag AI-tell markers, negation-contrast, colloquial terms.",
     toolsets: ["terminal", "file"]},
    {goal: "bibliography-auditor: Audit bib completeness, arXiv updates, venue consistency",
     context: "Read [FILE]. Load principles E1,E2,E3. Check every citation exists, no arXiv-only when published version exists.",
     toolsets: ["terminal", "file"]},
  ])
```

### Revision Review (Stage 4a)

```
Batch 1 (parallel, 3 agents):
  delegate_task(tasks=[
    {goal: "consistency-checker: Verify fixes on changed sections [FILES]. Check no new cross-ref breaks.",
     context: "Read [FILES]. Compare against prior review findings. Load principles A1,A3. Flag: fixes not applied, new issues.",
     toolsets: ["terminal", "file"]},
    {goal: "writing-reviewer: Review revised prose in [FILES]. Check revision quality.",
     context: "Read [FILES]. Load principles B1-B8. Flag: prose regression, unfixed issues from prior review.",
     toolsets: ["terminal", "file"]},
    {goal: "technical-reviewer: Verify technical corrections in [FILES].",
     context: "Read [FILES]. Check all math/citation fixes from ARS reviewer concerns applied correctly. Flag regressions.",
     toolsets: ["terminal", "file"]},
  ])
```

## Synthesis Report Format

```markdown
## Hybrid Review — Stage [2a/4a] AWA Injection Report

### ARS Stage [2/4] Summary
- Draft: [N] pages, [M] references, [K] figures
- ARS self-assessment: [score if available]

### AWA Parallel Review Findings

#### Critical ([N] items)
1. **[Agent]** [Principle] [FILE:LINE] — Description → Suggested fix

#### Important ([N] items)
...

#### Minor ([N] items)
...

### Patterns
- [Cross-agent recurring themes]

### Comparison: AWA vs ARS Self-Assessment
- ARS found: [N] issues
- AWA found: [N] additional issues (not caught by ARS internal review)
- Overlap: [N] issues (both caught)

### Recommended Actions Before Next Stage
1. [Highest priority]
2. ...

### User Decision
- [ ] Fix all Critical + Important → proceed
- [ ] Fix Critical only → proceed (Important deferred)
- [ ] Bypass AWA findings → proceed directly
```

## Rebuttal Agent 闭环协议 — v1.2 新增

> 来源：ScientistTwo (arXiv:2609.19644) §3.5 Rebuttal Agent。把用户此前**隐式**做法（V38→V64 每轮审稿驱动证明升级，如「Z₂ 等变 K 理论替代 Atiyah-Bott」）固化为命名流程 + 阈值门控。
> **核心纪律：Rebuttal 不是改文字，是针对审稿意见生成新证据。**

### 触发条件

| 条件 | 动作 |
|:--|:--|
| 综合分 **≥ 8/10** | 不触发，直接进 Quality Gates 投递判定 |
| 综合分 **6–8/10** | **触发本闭环**，`max_rounds=2` |
| 综合分 **< 6/10** | 不走本闭环，走 idea-level 深度重建（见 `## Quality Gates`） |
| 存在未消解的 **P0**（如引用幻觉、方法-代码错位、算术假阳性未过验证） | 无论分数高低，**强制触发**第 1 轮 |

**范围限定（与 text-level 分流对齐）**：本闭环只处理 **idea-level** 意见（需要新证明 / 新数值验证 / 新图 / 新附录 才能回应）。纯 text-level 意见（排版、措辞、符号统一、DOCX 结构）不进 Rebuttal Coder，直接走 Stage 4a 修订路径。混淆二者是本协议最常见的误用。

### 三阶段流程（每个 round）

**阶段 R1 — Rebuttal Planner（意见 → 任务）**
- 输入：上一轮完整审稿报告的全部 finding（P0–P3）
- 对**每条 idea-level finding** 产出一个可执行的「补充分析/实验任务」，而非一段辩解文字
- 任务卡必须含字段：`finding_id` / `severity(P0–P3)` / `claim_at_issue`(论文原句) / `required_evidence` / `acceptance_test`(怎样算被回应) / `level(text|idea)`
- 映射约定：理论物理论文的「补充实验」= **新生成一段 Lean 证明 / 数值验证 / 新图 / 新附录**；不得以「已在下文说明」式文字敷衍
- 任务清单需按 severity 排序，P0 任务全部为**阻塞项**，未完成不得进入 R3

**阶段 R2 — Rebuttal Coder（执行任务）**
- 逐条执行 R1 任务卡，产出**可核查的产物**：Lean 文件/定理片段、数值脚本与输出、新图源文件、新附录 Markdown
- 每个产物必须带可复现信息：命令、输入、输出摘要（哈希或数值）
- 若某任务执行后发现 claim 本身不成立 → **不伪造证据**，标记 `unresolvable` 并升级为 idea-level 重建候选（进 R4 回退保护判定），绝不用「软化措辞」替代
- 禁止 reward-hacking：不得通过缩小 claim 范围、加限定词、改符号定义的方式让 `acceptance_test` 表面通过（对照规则组 B 诚实性检测、规则组 F1）

**阶段 R3 — Paper Enhancer（回填正文）**
- 把 R2 产物**回填进论文正文**：改 narrative claims、更新表格/图/附录编号、同步摘要与结论中的数值
- 回填后必须重跑**跨章节一致性检测（规则组 C）**：新证据引入的数值/符号/术语需全文一致
- 更新 `Diff Log`：每个改动条目记录 `{finding_id, 原句, 新句, 证据位置}`

**阶段 R4 — 全量重审（强制，每 round 结束必做）**
- **必须重跑完整 12-stage 审稿 pipeline，不得只验局部修复**
- 理由：局部验证会漏掉跨章节一致性与引用连带影响（Pitfall 12/13/15 的直接教训）
- 输出：新一轮综合分 + 完整 finding 列表（旧 finding 复现状态 + 新 finding）
- 判定：分数 ≥ 8/10 → 退出闭环；否则 `round += 1`，若 `round > max_rounds(=2)` → 退出并转 idea-level 重建判定

### 闭环调度表

| Round | 增幅期望（Table 5 实证） | 退出条件 |
|:--|:--|:--|
| 0（无答辩） | 基线 5.2/10，接收率 46.9% | — |
| 1 | **6.9/10，79.6%（增幅最大）** | ≥8/10 或 P0 全清且无 idea-level 阻塞项 |
| 2 | 7.6/10，93.9%（**边际递减**） | ≥8/10；否则停止，转 idea-level |

**`max_rounds=2` 是经验最优**：1 轮吃掉主要增益，第 2 轮边际收益显著下降；继续加轮次只增加成本与「为改而改」风险。若用户显式要求第 3 轮，需在报告中标注 `[超出经验最优轮次]` 并说明理由。

### 回退保护（Rollback Guard，强制）

idea-level 重建（含 `unresolvable` 升级项与 <6/10 判定项）必须遵守**严格更优才替换**：

1. **先快照**：重建前记录当前最优版本的 `版本号 + 文件哈希 + 该版本综合分`（写作 `best_known`）
2. **重建**：在**独立分支/副本**上做深度重建（回到假设层，改公理/框架，而非补丁）
3. **A/B 全量审稿**：对重建版跑完整 pipeline（同一批 agent、同一 rubric），得到新综合分
4. **判定**：
   - 新分 **严格 >** `best_known` 分 → 接受替换，更新 `best_known`
   - 新分 **≤** `best_known` 分 → **丢弃重建版，回退到 `best_known`**（回退过程需可一键复现：从快照哈希还原）
5. **记录**：无论接受或回退，都在报告 `Patterns` 段落写明 `{重建假设, 新分, 旧分, 决策}`；回退不得静默发生

禁止：以「新版看起来更完整」为由跳过 A/B 计分；禁止在回退后继续保留重建版的局部片段（避免半成品污染）。

### 与既有章节的接口

- **规则组 D（Severity）**：每条 finding 增补 `level: text|idea` 列；只有 `idea` 进 R1
- **规则组 E（算术假阳性验证）**：Rebuttal Coder 产出的任何新数值，必须过规则组 E 后方可回填
- **规则组 F（三 refinement agents）**：R3 回填后、R4 重审前，先跑 F1/F2/F3 自检
- **Quality Gates**：本协议的退出分即 Quality Gates 的输入分，二者共用同一评分口径

## Quality Gates

| Gate | Tool | Blocking? |
|:--|:--|:--|
| Stage 2a AWA findings | AWA reviewers | **Advisory** — user decides what to fix |
| Stage 2.5 Integrity | ARS integrity_verification_agent | **MANDATORY** — must PASS |
| Stage 3 Formal Review | ARS 5-person panel | **MANDATORY** — decision required |
| Stage 4a AWA findings | AWA reviewers | **Advisory** — user decides |
| Stage 4.5 Final Integrity | ARS integrity_verification_agent | **MANDATORY** — zero issues |

### 数值接受门槛 (Numerical Acceptance Gates) — v1.2 新增

> v1.2 追加：把 ScientistTwo Table 5 的分数门槛落为**显式数值 gate**，取代 v1.1 的定性描述。所有 gate 的判定输入 = 最近一次**全量审稿**（12-stage pipeline）的综合分，禁止用局部验证分或自评分替代。

### 门槛与动作（唯一权威表）

| 综合分 | 判定 | 强制动作 | 下一步入口 |
|:--|:--|:--|:--|
| **≥ 8/10** | **PASS — 可投** | 结清报告：`Synthesis Report` + `Patterns` + `Recommended Actions`；确认无未消解 P0 | 投递 / 用户终审（可选 held-out 终审：Ollama qwq:32b 或独立 rubric） |
| **6 – 8/10** | **REVISE — 走 Rebuttal 闭环** | 进入 `## Rebuttal Agent 闭环协议`，`max_rounds=2`；先出 R1 任务卡清单再动手 | 闭环退出后重跑本 gate |
| **< 6/10** | **REJECT — 走 idea-level 深度重建** | 停止文字层修补；回到假设层重建（改公理/框架/证明策略），并启用 Reback 回退保护 | 重建版跑全量审稿 → 与 `best_known` A/B 比 → 严格更优才替换 |

### 一票否决项（与分数无关，任一存在即不得 PASS）

| 否决项 | 依据 | 处理 |
|:--|:--|:--|
| 引用幻觉（参考文献经 live-search 不存在 / 元数据不符） | 规则组 F2 | 强制进 Rebuttal 闭环，P0 阻塞 |
| 方法-代码错位（论文声称 X、Lean/代码无 X） | 规则组 F3 | 同上；若无法补实现 → 改 claim，改后重跑全量审稿 |
| 未过规则组 E 的算术/数值结论 | 规则组 E | 剔除或改写该 claim 后重审 |
| 存在被静默忽略的 P0 finding | Pitfall 11/12/13/15 | 补齐回应后重审 |

### Gate 执行纪律

1. **分数口径统一**：gate 分数与 Rebuttal 闭环退出分必须来自**同一次全量审稿**；不得混用不同轮次的分段结果
2. **不可用「接近过线」通融**：7.9 与 8.0 走不同路径，不做四舍五入上调
3. **每次 gate 判定留痕**：`{轮次, 综合分, 各 P0–P3 计数, gate 判定, 触发的动作}`
4. **版本新鲜度前置检查**：跑 gate 前先确认 agent 读到的文件版本 = 用户指定版本（Pitfall 15 / Pitfall 13），陈旧文件导致的分偏差不作数
5. **超轮次例外**：`max_rounds=2` 用尽仍落在 6–8 → 按 <6 处理（转 idea-level），不再加轮次
6. **高风险单一模型偏差**：若综合分仅由 v4-pro/v4-flash 单模型给出且落在 7–8 边界区间，建议补一道 held-out 终审再定 PASS/REVISE（历史上存在「v4-pro 单独审计 9/10 实际 2/10」的失准记录）

## Innovation-Correctness Gap Analysis (NEW v1.1)

When a paper shows divergent innovation and correctness scores (e.g., innovation 5.2 vs correctness 3.4), run a **meta-review** asking: "What correctness improvements would most elevate this innovation?" The gap reveals that the conceptual framework is strong but the mathematical execution lags. See `references/innovation-correctness-gap-analysis.md` for the 5-specialist meta-review protocol (proof gaps, D1 closure, gamma closure, axiom burden, improvement roadmap).

### Progressive Honesty and Score Trajectory

Making a paper MORE honest can REDUCE scores. This is NOT a regression — it reflects accurate assessment replacing inflated overclaim scores. See `proof-paper-cross-ref-revision/references/progressive-honesty-score-paradox.md`.

## Reference Files (NEW in v1.1)
### ScientistTwo (arXiv:2609.19644) → 可移植机制 ← NEWEST
ScientistTwo 论文的四个可移植机制（Rebuttal 闭环 / CoE 四维审计 / Meta-Review 分流 / held-out 评审器）+ Table 5/7 实证数据 + P0-P4 整合优先级。见 `references/scientisttwo-review-mechanisms.md`。

| `references/reference-list-verification.md` | **⭐ NEW — 参考文献核验脚本模式** — phantom/orphan 检测 + `[1--5]` 双横线范围引用展开 + 数学区间 `[10,100]` 误报排除。投稿前必查（2026-09-19） |

| `references/date-stamp-revision-trace-cleanup.md` | **⭐ NEW — 投稿前清理历史版本/时间信息** — 日期戳 `[Xxx, 2026-09-12]`/修订历史 "earlier value"/内部文档引用 "review report"/大写强调 NOT/DISTINCT 五类残留 + patch 工具 `\tag`→`\\tag` 双反斜杠陷阱，含统一检查命令 (2026-09-15) |

| `references/lean-unicode-identifier-reviewer-false-positive.md` | **⭐ NEW — Lean Unicode 标识符提取陷阱致审稿误报** — 正则 `[A-Za-z0-9_]` 截断 `sum_ξ_indicator_s`→`sum_`、`grönwall`→`gr`，致审稿代理误报计数/定理名不一致；甄别规则=先 grep 原始文件行级计数，不信提取清单 (2026-09-15) |


| `references/multi-value-parameter-tracing.md` | **⭐ NEW — 多值常数溯源** — 同一物理常数跨论文/多章节出现多值时的反推法：每个值代入定义式反解其依赖的另一参数，暴露循环定义。g_TC 四值(2.60/1.50/0.5/2.83)各自对应 λ_KLS=35/3、35、无来源、g_TC²=8。连带发现 |ρ|² 归一化 17.5 vs 35、λ_KLS=35/3 非紧流形谱隙错误。跨论文审查先做"常数取值-反推依赖"8轴矩阵 (2026-08-29) |

| `references/nested-block-comment-sorry-false-positive.md` | **⭐ NEW — 嵌套块注释假阳性** — proof_consistency_audit.py 的 `re.sub(r'/-.*?-/','',flags=re.S)` 非贪婪无法处理 Lean 嵌套 `/-.../-...-/`，致注释内 "0 sorry" 字样漏到 active 列表误判 BLOCK。中微子 V63 案例：4 处 sorry 全是声明文字，实际 0 active sorry。修复用行级状态机跟踪嵌套深度；判定前必须 grep -n 逐行看上下文 (2026-08-29) |
| `references/framework-stats-sync-counting-methodology.md` | **⭐ NEW — 框架文件统计同步口径** — 把四论文 Lean 统计同步进统一框架文件时的口径统一：①装饰声明 `@[...] axiom` 被朴素正则漏掉（GW-V19 47 vs 论文 48）②先剥嵌套块注释再计数③论文自报数≠实测活跃数（V17 自报 65/42 vs 实测 62/48）④批量替换禁裸数字、用 Python+命中计数。含四论文 2026-09-11 权威统计表 (2026-09-11) |

| `references/lean-tautology-and-false-fix-detection.md` | **⭐ NEW — Lean 证明深度审计** — 块注释/docstring 导致 sorry 假阳性（grep 必须先剥 `/-...-/` 再滤 `--`）；def-baked 重言式公理检测（`axiom X : name=value` 且 name 已 `def name:=value` → name=name 零内容）；假修正检测（论文"fix"本身可能是错的，H₀t₀ 0.9484 假修正案例）；公理计数膨胀分解（占位/重言式/数值断言/真公设）；跨文档过称vs诚实张力。CGICE V9 FOP 终审 2026-08-23 |

| File | Description |
|------|-------------|
| `references/false-proposition-axiom-detection.md` | **⭐ NEW — 假公理三型检测** — 假命题公理(∀量化写错可证False)/假实数等式公理(exp精确值不等,norm_num盲区)/零内容公理(1=1命名成定理)。CGICE V9.1 终审 2026-08-19 |
| `references/v4pro-multi-paper-cross-review.md` | **⭐ NEW — v4-pro Multi-Paper Cross-Review** — 6-step protocol for 3+ paper cross-review with v4-pro: extraction→prompt build (<50K chars)→v4-pro API (max_tokens=32768)→8-axis matrix→5-section output. ~160s. (2026-08-07) |
| `references/axiom-consistency-audit-patterns.md` | **⭐ NEW — 公理体系自洽性审计** — 8 模式：可证 False(爆炸原理)/矛盾迁移/表演性诚实(@[honest_axiom]注释文本)/公理计数失守/公理重述当证明/非紧空间离散谱错误/流形标量占位/声称verified但定理不存在 + Lean最小文件编译复现矛盾技术 (2026-08-16) |
| `references/multi-paper-v4flash-thinking-review.md` | **⭐ NEW — Multi-paper V4-Flash Thinking Review** — Single-API-call alternative for 3+ paper cross-review. ~4 min, 48K reasoning. (2026-08-06) |
| `references/cross-paper-gw-consistency-audit.md` | **⭐ NEW — Cross-paper GW consistency audit** — 8-axis checklist for SL(6,C) trilogy, 3 common failure patterns, V63→V17 case study (2026-08-06) |
| `references/section-alignment-v4pro-docx.md` | **⭐ NEW — Section realignment workflow** — v4-pro rewrite + DOCX insertion for diverged papers, pitfall catalog (2026-08-06) |
| `references/v14-to-v16-iterative-fix-pipeline.md` | **⭐ NEW — V14→V15→V16 三版迭代修复** — regression引入检测、header-code漂移、尺度不匹配、双轨同步协议 (2026-08-06) |
| `references/cross-paper-consistency-review-protocol.md` | **⭐ NEW — 跨论文一致性审查协议** — V63 vs V16对比审查、六步对齐方法、4项关键陷阱 (2026-08-06) |
| `references/iterative-fix-regression-detection.md` | **⭐ NEW — 迭代修复回归检测** — 4类回归模式：Bourgain头注释陷阱、Stale定理旧值、观测比较漂移、尺度不匹配 (2026-08-06) |
| `references/bourgain-header-claim-trap.md` | **⭐ NEW — Bourgain头注释陷阱** — 头声称已修但代码未删的检测模式 (2026-08-06) |
| `references/v14-review-fix-pipeline.md` | V14 Review-to-Fix Pipeline — Lean审计→双轨修复→交叉核查 (2026-08-06) |
| `references/lean-axiom-consistency-audit.md` | **⭐ NEW — Lean 公理自洽性审计** — 编译 `False` 证明来验证公理不一致、表演性诚实（注释掉的 @[honest_axiom]）、矛盾迁移（"修"引入新矛盾）、公理计数矛盾、幽灵定理声称（"fully verified" 但 .lean 无此定理）。CGICE V9.1 案例：3 agent 审出"可证 False"的致命缺陷 (2026-08-16) |
| `references/fake-axiom-removal-honest-declaration.md` | **⭐ NEW — 假公理删除→诚实声明→形式化方案** — 假公理三类型（假命题/假实数等式/零内容）、孤立公理 grep 验证、删除后补诚实声明、生成分级形式化可行性方案。CGICE V9.1 案例：删 4 条公理 66→62（2026-08-19）|
| `references/lean-false-axiom-patterns.md` | **⭐ NEW — Lean 假公理审计四模式** — ①假命题全称量化（∀ 写错范围可证 False，spec_gap_bound 案例）②零内容公理（1×1=1 命名深刻定理）③量级对但精确值错的假实数等式（exp(-280.7)≠10⁻¹²²）④孤立公理删除评估（grep 零引用→删除不影响编译）。含删除影响判定 + active sorry 注释过滤陷阱 (2026-08-19) |
| `references/math-claim-independent-verification.md` | **⭐ NEW — 数学计算结论独立验证 + 循环论证检测** — 逐条提取数值断言→Python 独立重算→五类判定；"定义数 vs 论断数"启发式；4 判据识别反向工程（参数=观测值反推/循环公理对/表演性声明/零内容公理）；假实数等式公理检测（Lean norm_num 盲区，exp/sqrt 等式可假 101 量级）；复审前 pre-flight 版本膨胀检测 (2026-08-18) |
| `references/three-agent-paper-lean-review.md` | **NEW — 三代理并行论文+Lean审阅** — 效率替代方案(3代理vs5+1)，含对抗性上下文注入、5种检测模式（2026-08-06） |
| `references/lean-arithmetic-audit-patterns.md` | **NEW — Lean算术审计模式** — norm_num假阳性、DOF计数溢出、定理=恒等展开、Bourgain替换为假代数、0 sorries+不可编译代码（2026-08-06） |
| `references/math-calculation-verification-patterns.md` | **⭐ NEW — 论文数学计算结论独立审查** — 5类错误模式(维度vs标度指数混淆/RG方程解因子2不自洽/Landau极点符号/内积归一化依赖/临界标度缺因子)+归一化声明三文件落地+报告问题解决后调整（2026-08-18） |
| `references/three-version-comparative-review.md` | **NEW — Three-Version Comparative Review** — 3 dimension-specialized agents (logic+math+testability), progressive honesty paradox, V13 warning case (2026-07-28) |
| `references/adversarial-context-sequential-review.md` | **NEW** — Multi-round review with prior findings as mandatory audit context |
| `references/innovation-focused-review-mode.md` | **NEW** — Innovation-only assessment with percentile rankings vs top papers |
| `references/innovation-correctness-gap-analysis.md` | **NEW** — Meta-review protocol: 5 specialists diagnose how to close the gap |
| `references/incremental-review-score-tracking.md` | **NEW** — Multi-version score tracking: V5→V6→V7, Δ<0.5 = cosmetic fixes, inject prior P0 as adversarial context |
| `references/comparative-three-version-review.md` | **NEW** — Comparative 3-version review: 3 parallel agents (consistency/math/testability), honesty-testability paradox detection (2026-07-28) |
| `references/brain-memory-knowledge-framework-synthesis.md` | **NEW** — Brain+memory→comprehensive MD: multi-source retrieval, 6-section structure, LaTeX+ASCII diagrams (2026-07-28) |
| `references/docx-translation-image-embedding-fix.md` | **NEW** — DOCX translation image loss fix: 5-step ZIP-level protocol to re-embed images after python-docx rebuild (2026-08-03) |
| `references/comparative-two-paper-review.md` | **NEW** — Comparative 2-paper review: 5 agents in 2 batches for cross-paper consistency, rigor, testability, publication strategy, and mutual learning assessment (2026-08-01) |
| `references/dual-path-theory-comparative-roadmap.md` | **NEW** — Dual-path theoretical framework comparative analysis+roadmap: 5-stage pipeline (load foundation→gather evidence→deep reasoning with v4-flash thinking→synthesis→deliver), 6-dimension scoring, cross-pollination mapping, moduli space contradiction detection (2026-08-04) |
| `references/paper-plus-lean-final-review.md` | **NEW** — Paper+Lean 6-agent final review: parallel deploy of consistency+logic+technical+writing+bibliography+lean-specialist. Multi-dimensional scoring, Deng-Hani framework compliance, prioritized P0-P3 fix checklist (2026-07-30) |
| `references/revision-landing-check-pattern.md` | **NEW** — Revision landing check: automated scan against prior review P0-P3 checklist, fix/partial/unfixed/new-issue classification, Lean stats conflict detection, residual version artifact scan (2026-07-30) |
| `references/v63-p0fix-final-review-pattern.md` | **NEW** — V63 P0Fix two-stage review: 26-check audit → 5-agent panel (2026-08-04) |

### V22→V25 Neutrino Condensation Paper (2026-07-06)

**Full multi-tier revision pipeline:**

```
Stage 2a (5 agents, 71 findings)
  → P0-P6 blocking fixes (provenance, no-free-params, falsifiability, citations, SB arithmetic)
  → P7-P10 quality fixes (AI markers, transitions, self-praise, g_TC dual role)
  → Stage 4a (3 agents, 4 residual issues found)
  → R1-R4 immediate fixes
  → Stage 3 formal panel (5 reviewers, PRD Major Revision)
  → R1-R6 editorial decision revisions
```

Key lessons:
1. **Tiered implementation**: P0-P4 are blocking → P5-P6 are technical → P7+ are prose. Fix in priority order, cross-audit after each tier.
2. **Stage 4a catches regressions**: 4 issues survived P0-P10 that only the verification review caught (R1 "no free parameters" in Abstract, R2 same in Introduction, R3 Σm_ν inconsistency, R4 ghost [cite] placeholders).
3. **Three-stage postulate → hypothesis repositioning**: definitional identity → bridging postulate (Stage 1, P21) → phenomenological hypothesis (Stage 2, P26). Triggered when formal peer review identifies the postulate as carrying the entire predictive weight. Full protocol in `proof-paper-cross-ref-revision/references/v24-v25-editorial-decision-revisions.md`.

### V20a Neutrino Condensation Paper (2026-07-05)
Full pipeline executed: 5 agents deployed, 12 Critical issues found and fixed, Stage 2.5 passed. See `proof-paper-cross-ref-revision/references/awa-hybrid-review-findings-v20.md` for full findings.

### Key Execution Lessons

1. **Bibliography is always the worst.** Every paper's reference list needs full audit — missing entries, wrong citation numbers, and duplicates are near-universal.
2. **Two competing axiom/numbering tables are a red flag.** Legacy tables must be labeled or removed.
3. **Dependency graphs fossilize predictably.** Always check range claims (A1–AN, L1–LN) against current reality.
4. **√2 convention splits are common in seesaw papers.** Check §1 vs §2.5 vs §3 for consistency.
5. **AWA catches what ARS misses.** In the V20a execution, ARS structural audits found 0/24 of the issues that AWA's parallel agent review discovered.

1. **AWA is advisory, ARS is blocking.** AWA provides granular quality feedback; ARS enforces structural/integrity gates.
2. **User always drives.** AWA review findings are presented with priorities; user chooses what to fix.
3. **Maximum 3 agents per delegate_task batch.** For 5+ agents, split into two parallel batches.
4. **Each AWA agent prompt must include**: file paths, principle categories (A-F), expected output format (Critical/Important/Minor with line references).
5. **Stage 2a deploys 5-7 agents** (full review). **Stage 4a deploys 3 agents** (lighter verification).
6. **Fix small AWA findings directly** (use `patch`/`write_file`). Deploy AWA action agents (prose-polisher) only for complex rewrites.
7. **Track AWA-ARS divergence.** When AWA catches issues ARS missed (bibliography collapse, narrative breaks, convention splits), note the pattern for pipeline improvement. See `references/awa-ars-divergence.md`.

## Verified Runs

| `references/comprehensive-rewrite-fix-pipeline.md` | **⭐ NEW — Comprehensive DeepSeek Rewrite for Bulk P0 Fixes** — 6-step protocol for applying 10+ P0 fixes in a single API call (64s vs 30min manual). CGICE V7→V8 case study. (2026-08-11) |

### CGICE V9→V10 R2 Review + Comprehensive Fix (2026-08-11) ← NEWEST

Eighteenth verified run. Second-round review of CGICE V9 found that prior "P0 fixes" were header notes appended without changing body text — the paper simultaneously made contradictory claims. 5-agent panel scored 2/10 consistency. V10 applied 9 REAL fixes via comprehensive DeepSeek rewrite (82s) + Lean surgical correction. v4-pro confirmed 9/10. Key pattern: header-only fixes ARE NOT fixes. See `references/cgice-v9-r2-header-only-fix-pattern.md`.

Seventeenth verified run. CGICE V7 paper with 12 P0 + 8 P1 issues from hybrid review. Used comprehensive DeepSeek rewrite protocol: classified fixes → built 12-item fix instruction with exact replacement text for §2.7 → single v4-flash API call (64.3s) → v4-pro audit (7/10). 10/12 P0 FIXED, 2 PARTIAL. Key pattern: replaced iterative patch with one-shot rewrite — dramatically faster and more consistent. Full protocol: `references/comprehensive-rewrite-fix-pipeline.md`.

### CGICE V7→V9 Multi-Round Evolution (2026-08-11) ← NEWEST

Eighteenth verified run. Three-round pipeline: V7(3.3, 12 P0)→comprehensive rewrite(64s)→V8(7.0)→P1 fixes→V9. Critical discovery: v4-pro single audit scored V9 9/10, but 5-agent panel found 4.7/10 with 8 undetected P0 issues. Added Pitfall 18 (v4-pro over-generosity) + `references/comprehensive-rewrite-fix-pipeline.md` + `references/cgice-v7-v9-evolution-case-study.md`. Full protocol in the case study reference.

### V63+V17+V16 Three-Paper Cross-Review with v4-pro (2026-08-07)

Sixteenth verified run. User explicitly requested "deepseek-v4-pro(最大tokens)推理" for 3-paper + 3-Lean cross-review. Prompt 47K chars, response 7,841 chars in 159.5s. 8-axis consistency matrix + 5-section output. Scores: V63=2/10, V17=3/10, V16=4/10 — all NOT READY.

Key findings: V63 internal g_TC contradiction (2.60 vs 0.5), V17 H₀ circularity + DM DOF ad-hoc construction (75≠70), V16 10⁸× dilution factor requires unobservable t_freeze. Cross-paper: DM mechanism conflict (neutrino condensate vs GW energy), GW frequency conflict, g_TC value conflict.

**v4-pro safe operating window confirmed**: v4-pro works reliably for prompts <50K chars with max_tokens=32768. Above 120K chars still hangs. Pattern and extraction methodology codified as `references/v4pro-multi-paper-cross-review.md`.

### Triple GW V5→V6→V7 (2026-07-25) ← NEW

Thirteenth verified run. Three consecutive reviews in single session with adversarial context injection. Scores: 1.3→1.4→1.7. Four P0 issues persisted across all versions, triggering the P0-persistence-across-versions detection rule. Key finding: surgical fixes cannot resolve framework-insufficient P0s — GW production from SL(6,C) geometry has no known derivation. See `references/triple-gw-v5-v6-v7-reviews.md` and `references/p0-persistence-across-versions.md`.

### Triple GW V11 — Formal Verification Trap (2026-07-25) ← NEWEST

Fourteenth verified run. V11 added Bakry-Émery explicit tactic proof, Bourgain slicing formalization, Ricci flow theorem (Lean 811 lines, 28 theorems, 0 sorries). **Score unchanged from V7: 1.7/10**. Demonstrates the "formal verification trap" — Lean proof upgrades do not improve review scores when the underlying physical derivation chain is broken. Five reviewers unanimously identified the same P0 issues as V7. Deeper mathematical errors (Ricci sign error, false axiom `ln(35/33)=160`) were later discovered by v4-pro deep analysis.

**Key lesson**: When 5-agent review scores stagnate despite formal proof upgrades, deploy single v4-pro deep mathematical analysis (Anthropic SDK, max_tokens=16384) to identify whether P0 issues are symptoms of mathematical impossibilities. See `references/triple-gw-v11-hybrid-review-record.md`.

### CDM Topological Kink Paper (2026-07-07)

Fourth verified run — 76-paragraph physics paper claiming to prove CDM:visible = 5:1 via SL(6,C) geometric crystallization. 5 agents in 2 batches. Scores: Consistency 3/10, Logic 2/10, Technical 2/10, Writing 6/10, Bibliography 3/10. Overall **3.2/10 — NOT READY**.

6 P0 showstoppers discovered:
1. Rank=90 in 70×70 matrix (mathematical impossibility)
2. 5:1 ratio hardcoded as axiom A5, not derived
3. Lean proof is empty shell (8 `exact trivial`, 5 `admit`, 31 undefined identifiers)
4. OllamaLens TEXTUAL_COOCCURRENCE is categorical error (LLM co-occurrence ≠ mathematical validation)
5. Reference [9] fabricated co-authorship (Eldan not co-author of cited paper)
6. KLS inequality misapplied to infinite-dimensional moduli space

Recommended path: downgrade from "formal proof" to "formalized conjecture" → target *Physics Letters B*. Full findings: `references/cdm-hybrid-review-20260707.md`.
Third real-world hybrid review — ~24,300 words, V38 final before PRD submission. 5 agents in 2 batches, all deployed in parallel. Scores: Consistency 5/10, Logic 6/10, Technical 3/10, Writing 3/10, Bibliography 2/10. Overall **3.8/10 — NOT READY for PRD**.

Key findings (6 P0 showstoppers):
1. SL(6,C)/SU(6) dimension error (26→35)
2. Self-identical ratio comparison after global 2.32→2.56 replacement (P52)
3. Citation numbering system collapse (~30% wrong)
4. Axiom catalog mismatch: body A1-A24 vs appendix A1-A28 (P53)
5. `:=True` stubs surviving in A6/A16/A28 despite claims of "zero stubs"
6. √2 convention untracked: Lean y_ν=0.50 vs paper y_ν=0.71 (41% discrepancy)

Submission recommendation: **Not ready for PRD.** Consider Physics Letters B (shorter, single-idea focus) or EPJC (higher tolerance for interdisciplinary methods). PRD requires higher writing and citation rigor. A full rewrite (abstract <250 words, CGICE→appendix, AI tools→supplement, ~12,000 word target) would be needed for PRD submission.

Agent deployment pattern refined:
```python
delegate_task(tasks=[
    {"goal": "consistency-checker: ...", "toolsets": ["terminal","file"]},
    {"goal": "logic-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "technical-reviewer: ...", "toolsets": ["terminal","file"]},
])  # Batch 1: 3 agents (structure + logic + math)
delegate_task(tasks=[
    {"goal": "writing-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "bibliography-auditor: ...", "toolsets": ["terminal","file"]},
])  # Batch 2: 2 agents (prose + refs)
```
Each agent reads the full paper from `/tmp/v38_paper.txt` + appendix from `/tmp/v38_appendix.txt`. Scores aggregated into 5-dimension radar with submission recommendation. 5 agents in 2 batches found **71 issues** (26 Critical / 22 Important / 23 Minor). Key findings: λ_KLS provenance misattributed to Klartag & Lehec (they prove positivity, not numerical value 11.7), "no free parameters" contradicted by internal admissions, "maximally falsifiable" for unmeasurable M_R ≈ 10¹⁴ GeV, bibliography system broken (duplicate [28], ghost [14], 11 uncited refs), §2.2.3→§2.3 zero transition. Prose score 5/10. Synthesized into P0-P6 prioritized fix list. See `references/v22-v23-hybrid-review-p0-p6-fix.md`.

### V56 Neutrino Condensation Paper — Final Hybrid Review + Contribution Comparison (2026-07-23)

Eleventh verified run. 6-agent panel. Unanimous REJECT at 3.0/10.

**Twelfth verified run — V55→V56 FOLLOW-UP REVIEW WITH ADVERSARIAL CONTEXT (2026-07-23)**:
User required V56 review to build on V55 findings. 6 agents received full V55 P0/P1 defect list as mandatory audit context. 5/6 MAJOR_REVISION, 1/6 REJECT, 3.9/10 (+0.8 from V55's 3.1). New pitfalls discovered: JSON unparseable from embedded quotes in detailed_comments (P0), .format() brace conflict with LaTeX (P0). Full pattern: `references/v56-vs-v55-followup-review-pattern.md`.

### V55 Neutrino Condensation Paper — Full Hybrid Review + C3-C6/C1-C2 Fix Pipeline (2026-07-22)

Tenth verified run. 5 rounds over 2 days: 3.1→4.3→5.5. EPJC recommendation. CN translation delivered. **New: Contribution Comparison Review mode** (3 domain experts: neutrino theory + cosmology + publication strategy) for benchmarking against literature. Triggers: "比较学术贡献度" / "compare contribution". See `references/v55-full-review-20260722.md`.

10 P0 showstoppers (initial):
1. Version chain break: paper V55 vs Lean V53 (2 versions behind)
2. Lean L379 compile error: `A_CS_QUANT]` illegal character `]`
3. g_TC² dual values: header ≈6.748 vs T_gTC_value proves 6.768 (0.3% diff)
4. D1 is definitional identity, not derivation
5. Dual-path "cross-validation" is an algebraic loop (shared |ρ|²=35 origin)
6. D1 epistemic status swings between 7+ contradictory labels (proved/conditional/postulate/conjecture)
7. Predictive degree drifts between −1 and −2 across sections
8. 23 references missing ([42]-[64]), numbering jump from 41→58
9. Abstract 384 words (limit 250) + contains LLM pipeline meta-info
10. |ρ|²=35 possible confusion with dim(SU(6))=35

**Venue recommendation**: NOT PRD/PRL. Target **Foundations of Physics** (highest tolerance for honest-axiom approach) or **Physics Letters B** (short format forces tightening).

### Pitfall 11: Follow-Up Review WITHOUT Prior Context — User Rejection (P0)

When running a review of V{N+1} after V{N} has already been reviewed, the user EXPECTS reviewers to build upon the prior review findings. Running without injecting the prior P0/P1 issue list causes rejection.

**Mandatory**: Load prior review → extract ALL P0/P1 IDs → inject as 【前次评审历史】 block → require "v55_issues_fixed" / "v55_issues_remain" in JSON output → include fix-status table in report.

### Pitfall 8: DOCX Extraction Loop Overwrites Target File (P0, 2026-07-22)

When iterating over multiple DOCX files in a directory to extract text to a single `/tmp/output.txt`, the LAST file in the loop silently overwrites all previous extractions. The consistency-checker and logic-reviewer received only §2.2 (13K chars) instead of the full 199K-char paper because `Section_22_Restructured_V55.docx` was processed last.

**Detection**: Compare extracted file size against expected. If `wc -c /tmp/output.txt` < 50K for a 60-page paper, the extraction was overwritten.

**Fix**: Either (a) filter to a single target file: `if 'EN_V55.docx' in f and 'Modifications' not in f and 'Section' not in f`, or (b) write each extraction to a uniquely-named file.

**Symptom**: Reviewers report "only §2.2 available" when the full paper was provided.

Sixth verified run — V51 paper + Lean with full Floquet-Equivariant framework. 5 agents in 2 batches. Key finding: the MD→DOCX+Lean upgrade pipeline successfully transformed the reviewer's Chinese markdown into a 55-OMML DOCX section + 11 new Lean axioms with zero conversion warnings. The cross-audit discovered 85/9/29 ground truth counts that were inconsistent across 4 DOCX files (old: 82/7/10). Fixed via XML-level bulk replacement without losing OMML formulas.

### V63 Neutrino → V17 Triple-GW Cross-Paper Alignment (2026-08-06) ← NEW

Fifteenth verified run. Cross-paper consistency audit between V63 neutrino condensation paper Section V and V16 triple GW paper. Deployed single consistency agent with 8-axis comparison matrix. **Score: 3.0/10 — CRITICAL inconsistencies found.**

Key findings:
1. GW peak count: V63=2 peaks, V16=3 peaks — DIVERGENT
2. GW frequencies: V63 (10⁻⁸/10⁻² Hz) vs V16 (4.5×10¹¹/1.71/10⁻⁹ Hz) — CONFLICT
3. H₀ status: V63 labeled as "derived", V16 corrected to [honest-axiom] — CONFLICT
4. V63 internal math: S₃/T formula claimed ≈35 but computes to ≈929
5. Missing honest-axiom declarations in V63 throughout Section V

Resolution: deepseek-v4-pro generated corrected Section V + Appendix E.5-E.6 text aligned to V16 ground truth. python-docx paragraph-level replacement in V63 DOCX → V63_V17.docx. 31 paragraphs changed across Section V, Appendix E, and cross-references in §§VII.C.

**Pattern codified as `references/cross-paper-consistency-review-protocol.md`** — six-step alignment protocol with 4 key pitfalls.

Seventh verified run — single-section focused evaluation using deepseek-v4-pro (max_tokens=16384, temp=0.0). Compared paper's Bakry-Émery curvature approach (§2.3.3) vs reviewer's Monge-Kantorovich optimal transport suggestion for deriving λ_KLS ≈ 11.7. **Finding**: Bakry-Émery formula is mathematically fabricated (2.35/10) — λ_KLS = λ₀·dim/(dim+2λ₀) appears in no published literature, the correct SL(6,ℂ)/SU(6) spectral gap is λ₁ = 35 not 35/3, and applying convex-body KLS to symmetric-space Laplacian is a category error. Monge-Kantorovich is rigorous (6.40/10) but can only give asymptotic bounds, not the precise numerical value. **Recommendation**: Acknowledge λ_KLS as phenomenological parameter, remove fabricated derivation, adopt optimal transport for qualitative support. Full evaluation in `proof-paper-cross-ref-revision/references/kls-method-comparison-v4pro.md`.

### Reviewer-Proposal Incremental Review (2026-07-17, ninth verified run)

When a reviewer MD proposes math upgrades to specific sections, do NOT run the full 5-agent
review. Use the targeted 3-specialist protocol: extract current section FIRST (proposal may
duplicate existing text), inject prior verdicts + known P0 issues as adversarial context,
check MathCode INDEX for formalization infrastructure (0 hits = honest-axiom-only chain),
deliver verdict MD to paper directory. Detected in run 9: fabrication resurrection under a
new theorem name, stale Lean stats (V50 numbers quoted against V52 file), 80% duplication
masquerading as increment. Full protocol: `references/reviewer-proposal-incremental-review.md`.

### Incremental-Value Review of Reviewer-Proposed Content (2026-07-17)

Ninth verified run — evaluating whether a reviewer MD improves specific paper sections (V52 §2.3.1–2.3.3) and whether it upgrades a postulate to a theorem. Pattern additions:

1. **Score TWO axes, not one**: correctness AND increment-vs-current-text. Reviewer content can be simultaneously correct and worthless — MD stages duplicating existing V52 text scored 8.5/10 correctness but 1.5/10 increment. Extract the CURRENT paper section (python-docx paragraph slice between heading anchors) and feed it alongside the reviewer MD so agents can diff.
2. **Adversarial context injection**: prepend all prior verdicts (fabrication rulings, P0 lists, actual Lean stats) to every agent prompt. This makes agents cross-check instead of re-litigating, and catches "new packaging of a judged-fabricated formula" (the λ₀/d equipartition claim was caught precisely because the prior λ₀·dim/(dim+2λ₀) ruling was in context).
3. **Specialists by claim domain** (3 agents mapped to the MD's claim clusters) beats 5 generic reviewers for single-section evaluation; embed known counterexamples in the targeted questions (e.g. Bobkov 2003 projection monotonicity, Gaussian marginal counterexample).
4. **Watch for stale statistics in reviewer MDs**: the 20260717 MD cited Lean stats from two versions back (54/82 axioms vs actual V52 9 axioms). Always verify reviewer-quoted file stats against current files before accepting their framing.
5. **Author self-flagged caveats go into the adversarial context** ("已知作者自警" item) — a subsequent 5-agent review then independently confirms or dismisses them, giving the caveat a verdict instead of leaving it hanging (the ρ∈F flag was confirmed fatal by 2/5 agents).



### Pitfall 7: Bibliography-Auditor 优化 (2026-07-16)

✅ **已解决**：四方案对比（Baseline / Few-shot / Manual / Two-stage），**Few-shot（3个真实审计案例注入）胜出**——零 JSON 破损，真实论文命中 21 条（Baseline 为 0）。SkillOpt ReflACT 不适用于结构化 JSON 输出场景（5 epoch 净改善 0）。详见 `references/bibliography-auditor-optimization.md`。

### Pitfall 9: DOCX Rebuild Corruption — Paper Text Silently Degraded (2026-07-25)

When a DOCX is rebuilt via raw XML manipulation (e.g., `str.replace()` on `word/document.xml`), the resulting file may pass ZIP integrity checks AND open in Word but contain drastically reduced text. **Symptom**: extracted paper text returns 494 chars from a file that should have 47,000+ chars. **Root cause**: XML-level modifications can corrupt OOXML structure in ways `zipfile.testzip()` doesn't catch — ZIP valid, XML semantics destroyed.

**Mandatory pre-deployment check:**
```python
paper_text = extract_docx(path)
assert len(paper_text) > 5000, f"DOCX may be corrupted: only {len(paper_text)} chars"
```

**Prevention**: Prefer python-docx paragraph-level edits over raw XML manipulation.


### Pitfall: Interrupted delegate_task May Have Completed (Pitfall 6, 2026-07-15)

When `delegate_task` is interrupted by a session boundary or timeout (status='interrupted'), the subagent may have actually completed all file modifications before being killed. The `tool_trace` at the end of the result is the key signal — count the actual tool calls executed. If you see `write_file` or `terminal` commands with file paths in the trace, CHECK those files before re-running. A re-run will find "0 citations inserted" because the work was already done.

**Detection pattern**: `status: "interrupted"` + tool_trace shows many completed operations + verification finds the expected state.

**Fix**: Always run a verification pass after an interrupted delegate_task before deciding to re-run. The verification will either confirm completion or show exactly what's missing, allowing a targeted fix instead of a full redo.

### Pattern: Adversarial-Context Injection (2026-07-17, verified runs 9-10)

When reviewing material that has REVIEW HISTORY (prior verdicts, fabrication rulings, known
P0 lists, author self-warnings), prepend an 【对抗性历史上下文】 block to every reviewer
prompt and instruct "评审时必须逐条对照". Include: (a) prior fabrication/REJECT rulings with
scores, (b) unresolved P0 lists, (c) known counterexamples (e.g. Bobkov 2003 projection),
(d) scoring baselines from sibling routes ("Ratner=1.5, DH=4.0 — score relative to these"),
(e) the author's own pre-flagged caveats as explicit audit questions. Effects observed:
reviewers directly cross-referenced history, detected "new packaging of previously-judged
fabrication", confirmed the pre-flagged ρ∈F caveat as fatal, and produced calibrated
relative scores instead of free-floating ones.

### Pattern: Incremental-Value Review of a Reviewer MD (run 9, 2026-07-17)

When the user asks "does this reviewer MD improve section X?", do NOT review the MD in
isolation — extract the CURRENT manuscript section text first (python-docx, locate heading
boundaries e.g. 2.3.1→2.3.4) and feed BOTH to each reviewer with the explicit question
"what does the MD add that the manuscript does not already contain?" Frequent outcome:
the MD largely duplicates existing text (V52 case: stages 1-3 scored 1.5/10 incremental
despite 8.5/10 correctness) — correctness and increment are separate axes; score both.
Also check MD factual staleness against current artifacts (the 20260717 MD cited V50-era
Lean stats 54/82 vs actual V52 9 axioms).

### Pattern: Adversarial-Context Injection Review (2026-07-17, verified ×2)

When reviewing a NEW derivation/reviewer-proposal in a domain with prior review history, inject an explicit 【对抗性历史上下文】 block into every reviewer prompt containing:
1. Prior verdicts with scores (e.g. "旧公式 λ₀·dim/(dim+2λ₀) 被判捏造 2.35/10")
2. Known fatal issues from earlier rounds (P0 lists) the new material must be checked against
3. **Score baselines**: "Ratner路线1.5/10, DH路线4/10 — 若优于两者需给出高于4的分数并论证"
4. **Author self-flagged caveats** as mandatory audit items ("已知作者自警(须重点审查): ...")

Effects observed: reviewers calibrate scores against the baselines instead of drifting; pre-flagged caveats get explicitly adjudicated (the ρ∈F caveat was confirmed fatal by both EIC and R1); "new packaging of an old fabrication" gets caught (R2: "均分定理新版不应高于旧版1.8/10"). Without the context block, reviewers routinely miss that a proposal recycles a previously-rejected argument under new terminology.

Cost profile: 3-5 agents × deepseek-chat temp=0.0 max_tokens=8192 ≈ 30-65s each, sequential OK for ≤5 agents (total <5 min). Save each reviewer to `/tmp/<tag>_<name>.part` immediately.

### Pattern: v4-pro Single-Section Evaluation

When a reviewer challenges a specific mathematical derivation:
1. Extract the challenged section from paper DOCX → plain text
2. Extract the reviewer's suggested alternative from MD → plain text
3. Run brain recall for bridging concepts
4. Use `deepseek-chat` (NOT v4-pro — timing issues) with `max_tokens=16384, temperature=0.0`
5. Structure prompt with 5 weighted criteria (self-consistency 25%, framework alignment 25%, rigor 20%, heuristic 15%, acceptability 15%)
6. Output scored table + detailed analysis + actionable recommendation

### V51 Neutrino Condensation Paper — Full Hybrid Review + P0 Fix Pipeline (2026-07-15)

Eighth verified run — V51 paper, 155K chars, 474 paragraphs. 5 agents in 2 batches. Scores: Consistency 3/10, Logic 4/10, Technical 3/10, Writing 6.5/10, Bibliography 2/10. Overall **3.7/10 — REJECT**.

6 P0 showstoppers:
1. Lean proof stats completely fabricated (claimed 85/15/33 → actual 17/9/7)
2. Predictive degree self-contradiction (−1 in abstract, −2 in body)
3. λ_KLS = 35/3 uses unexplained factor of 3 (|ρ|²=35 derived, but 35/3 used)
4. 7 ghost citations [58]-[64] + fabricated ref [17] + commentary as [14]
5. |ρ|² normalization split: body=35, Appendix F=35/2
6. κ calibration circularity (claimed "m_τ" but actually calibrates to m_₃)

**Post-review fix pipeline**: All 6 P0 + P1-1 fixed in single session via 3-phase pipeline:
- Phase 1: Mechanical XML text replacements (59-66 changes/file across 4 DOCX)
- Phase 2a: Structural insertion (λ_KLS honest-scope disclosure paragraph in §2.3.3)
- Phase 2b: Bibliography rebuild (8 new refs [42]-[49], 3 removals, 1 journal fix)
- Phase 3: Python cross-audit verifying all fixes consistent across 4 DOCX + 1 Lean

Key lesson: **NTFS DOCX write corruption** — writing ZIP files directly to `/mnt/c/...` produces `BadZipFile`. Always write to `/tmp/` first, then copy back. See `proof-paper-cross-ref-revision/references/v51-p0-rapid-fix-pipeline.md`.

### V50 Neutrino Condensation Paper (2026-07-13)

Fifth verified run — V50 paper, 160K chars. 5 agents + Lean specialist. 3.6/10 — REJECT. Top findings: λ_KLS formula self-created, KO⁻³⁵(pt)=0, tautological verification, 17 :=True stubs. Full: `references/v50-neutrino-review-20260713.md`.

## Pitfalls

### Pitfall 12: Version-Scope Discipline — Review the Requested Version, Not Its Transition (P0, 2026-08-06)

When the user says "review V14", review V14 **as-is**. Do NOT:
- Compare V14 against V15 fixes or analyze whether V15 changes landed
- Critique the V14→V15 transition pipeline
- Spend paragraphs proving that "V15 fixes weren't applied"

If the file has a V15 header but is named V14, just note the naming oddity in one sentence and move on. The user wants a review of the **content**, not a meta-analysis of the version history. The correction signal is clear: "没有让审阅V15啊" — the user named the version they want. Stick to it.

### Pitfall 13: Check Version Staleness Before Offering Fixes (P0, 2026-08-06)

When the user mentions a version number but the pipeline has already progressed further (e.g., "V14" when V16 exists), do NOT offer to fix the old version. Check what the latest version is in the directory first. Signal: "嗯不需要了，现在都V16版本了".

### 1. DeepSeek JSON Unparseable — detailed_comments with Embedded Quotes (P0)

When `detailed_comments` contains quoted phrases (e.g., `the "derived" value`), the generated JSON is unparseable by `json.loads()`. Two of six reviewers in the V56 session produced valid JSON that failed parsing. **Recovery**: Use regex field extraction (`re.search(r'"score":\s*([\d.]+)', text)`) instead of `json.loads()`. **Prevention**: Add to prompt: "Escape ALL double-quotes in detailed_comments as backslash-escaped."

### 2. Python .format() Brace Conflict with Paper Text (P0)

When paper text contains LaTeX math with curly braces (`\mathbb{C}`, `\{X\}`), using `str.format()` to inject paper text into a prompt template breaks with `KeyError`. **Fix**: Use `str.replace("__TOKEN__", value)` instead of `.format()`. Never use `.format()` with untrusted paper text.


### Pitfall 19: "P0 Fix Header Notes" — AI Rewrites Add Disclaimers Instead of Changing Text (2026-08-11)

When DeepSeek rewrites a paper to apply fixes, it often appends banner notes (e.g., `[V9.1 P0 FIXES: ...]`) to headers and adds inline notes like `N_e = 161 is a calibration result` but LEAVES the original overclaim text unchanged in the body. The result: a paper that simultaneously says "prediction" in 5 locations and "calibration" in 1 banner note. The CGICE R2 review found 8/8 "fixes" from R1 were only partially applied — banner notes existed but body text was untouched.

**Detection**: After every rewrite pass, grep for the OLD text patterns. If `grep -c "within an order of magnitude"` > 0 after the fix was supposed to remove it, the rewrite failed. DO NOT trust the banner notes.

**Key signal**: A paper header containing `[V9.1 P0 FIXES 2026-08-11]` with a list of claimed fixes is a RED FLAG — it means the AI writer appended a fix manifest rather than fixing the actual text. Fix manifests in headers should be treated as TODO lists, not as evidence of completion.

**Fix approach**: In the rewrite prompt, explicitly say "Do NOT add header notes or banner disclaimers. Change the ACTUAL body text. The fix must survive a grep for the old text returning zero."

v4-pro single-API-call audits consistently score papers 2-5 points HIGHER than 5-agent adversarial panels. CGICE V9 case: v4-pro scored 9/10; 5-agent panel found 4.7/10 with 8 P0 issues (phantom predictions, Lean algebra bug, Λ_CC contradiction, RG arithmetic error). The single audit missed all of these.

**Root cause**: v4-pro reads linearly and trusts framing. Multi-agent panels with adversarial context + specialized roles (consistency/logic/math/writing/bibliography) produce cross-verification that catches inconsistencies no single reader would.

**Rule**: v4-pro single = DIRECTIONAL CHECK only. Always follow with ≥3-agent panel for gate decision.

**Detection signal**: If v4-pro gives ≥8/10 but no "CRITICAL" findings → re-audit with multi-agent panel.

### Pitfall 15: Stale-File Re-review — Agents Silently Read the OLD Version (P0, 2026-08-23)

When re-reviewing a MODIFIED paper/Lean, agents pointed at `/tmp` files with wrong/nonexistent
names silently fall back to STALE copies left by earlier tasks (translation/extraction), producing
findings that contradict the current files (e.g. agent says "A5 present" when your grep of the
current file says "A5 deleted"). Detection: agent's reported line counts ≠ current `wc -l`.
Fix: re-copy the current files + verify line counts + tell each agent the expected count before
deploying. Full recipe: `references/stale-file-version-mismatch.md`.


### Pitfall 14: v4-pro 全尺寸挂死 + v4-flash Content 空 (2026-08-07)

v4-pro 对 5.5K chars 的 prompt 也会挂死——0% CPU、6+ 分钟无响应。旧假设"仅 >120K 挂死"不成立。**v4-pro 对所有审查任务不可靠**。

**替代**: 深度推理用 v4-flash thinking。但可能 token 耗尽致 `content=""`(71K reasoning/0 content)。从 `reasoning_content` 提取结论回退。

**决策树**: 短 prompt→v4-flash thinking | 中长→v4-flash+thinking=disabled | 任何长度+v4-pro→❌

**执行方式（5 代理终审，2026-08-23 验证）**: 用 terminal + Python 脚本直调 v4-flash API（OpenAI SDK, `extra_body={"thinking": {"type": "disabled"}}`, `max_tokens=8192`, `temperature=0.0`, `timeout=600`, background + notify_on_complete），**不用 delegate_task**——delegate_task 子代理继承主 model（主 agent 是 v4-pro 时子代理也 v4-pro 挂死），且 delegate_task 无 model 参数可覆盖。串行执行（DeepSeek 速率限制，5 代理 ~8 分钟），每个审稿人输出立即写 `/tmp/<name>.part` 防超时丢失。对抗性上下文注入已知 P0 清单，要求 JSON 输出 `known_p0_verdicts` 字段逐条判 `fixed/remain/partial`（而非重新凭空评审）。

DeepSeek v4-pro has a sharp reliability cliff around prompt size:

| Zone | Prompt Size | Behavior | Recommendation |
|------|------------|----------|----------------|
| **Safe** | <50K chars | Reliable, ~160s, deep math reasoning | ✅ Use for cross-paper reviews |
| **Risky** | 50-100K chars | May hang intermittently | ⚠️ Test first, have v4-flash fallback |
| **Unsafe** | >120K chars | Silently hangs (no error, no timeout) | ❌ Use v4-flash instead |

**Symptoms of hang**: Zero stdout for >300s, process killed with exit code 143, report file not created.

**When user explicitly requests v4-pro**: Limit prompt to <50K chars by extracting only key sections (abstract + core derivations + conclusions + Lean stats + numerical claims). Do NOT include full paper text. For papers >100K chars, use the extraction pattern in `references/v4pro-multi-paper-cross-review.md`.

### 2. Process Kill Before File Write — Incremental Save

When running 5-agent review via `terminal(background=true, timeout=600)`, the timeout may kill the process AFTER all API calls complete but BEFORE the final `open().write()` saves the compiled report. All review text is lost.

**Fix**: Write each reviewer's output to a separate `.part` file IMMEDIATELY:

```python
with open(f'/tmp/review_{name}.part', 'w') as f:
    f.write(content)
```

Final compilation reads `.part` files — idempotent and recoverable even if killed mid-compile.

### 4. Lean Stats Regex Trap (V50, 2026-07-13)

When counting `axiom`, `theorem`, `sorry` in Lean files for review purposes, simple regex/grep matches comments and header strings. Example: `grep -c 'sorry' proof.lean` returned 9, but all 9 were in header comments saying "0 sorry". The actual active sorry count was 0. Similarly, `grep -c 'axiom'` returned 237 when the real count was 80.

**Fix**: Use Python regex that (a) strips block comments `/- ... -/` AND docstring comments `/--` FIRST via `re.sub(r'/-.*?-/', '', lean, flags=re.DOTALL)`, THEN (b) drops lines starting with `--`. Naive `grep -v '/-'` fails on multi-line block comments — a `/-` on line 213 closing `-/` on line 215 leaves the intervening `Removed previous sorry` and `/-- ... (0 sorry) ...` docstring words counted as ACTIVE sorries (false-positive `sorry=2` when true count is 0; verified CGICE V9 FOP 2026-08-23). **Any non-zero sorry/admit/`:= True`/`by trivial` count must be confirmed with `grep -n 'sorry'` line context before reporting a P0.** See also `references/lean-audit-detection-refinements.md` for the companion detection rules (def-baked tautological axioms, placeholder-inflated axiom counts), and `references/lean-nested-block-comment-sorry-pitfall.md` for the NESTED block-comment false-positive mechanism (non-greedy `re.sub(r'/-.*?-/',...)` leaks inner comment body into active lines).

**Nested-block-comment false positive (2026-08-29)**: the stripper `re.sub(r'/-.*?-/', '', lean, flags=re.S)` uses NON-GREEDY `.*?`, so a NESTED `/-` inside a block comment terminates the match at the first `-/` and the inner `/-`/`-/` pair unpairs — block-comment interior lines leak into the "active" list and their `sorry` words get miscounted (Neutrino V63: reported `sorry=4`, true 0). Detection: a "sorry" line whose neighbors are English prose ("✓ ZERO SORRY:", "0 active sorry keywords"). **Also: active-sorry counted into `stats` but never appended to `blocks` makes the audit gate silent on the #1 defect** — a proof with `sorry` returns `gate=PASS`. Every `stats[...]` key must have a corresponding gate path. Full recipe + the g_TC four-value trace (2.60⟺λ_KLS=35/3, 1.50⟺λ_KLS=35, 0.5=no source) and the non-compact-space spectral-gap error: see `references/lean-stats-traps-and-multivalue-coupling-diagnosis.md`.

### 5. :=True Stub Disclosure (V50, 2026-07-13)

In Lean, `:= True` is syntactically distinct from `sorry` — it typechecks as a complete proof. But for verification purposes, it's equivalent to a hidden sorry (empty proof body). Papers that claim "zero sorry" must also disclose the `:= True` stub count. V50 had 17 stubs undisclosed.

When running hybrid review via `execute_code`, the 300s hard timeout is insufficient for 5 sequential API calls. Always use `terminal(background=true, notify_on_complete=true)` with timeout≥600s, or split into separate foreground calls.
