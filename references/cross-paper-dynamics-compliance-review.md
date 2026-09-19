# 跨论文动力学遵循度审查：存在性参数化 vs 动力学闭合 · 语言借用 vs 方程遵循

以母框架动力方程（如 CGICE 四方程）为基准审查子论文（如 V18 三阶段）时，两条独立于既有 B3「校准伪装成推导」/ B4「状态升级」的检测维度。2026-09-19 V18↔CGICE 跨论文终审验证，5 代理一致。

## Pattern 1 — 存在性参数化 ≠ 动力学闭合（existence parameterization ≠ dynamical closure）

**触发信号**：论文引入一个自由参数/分支比来「闭合」一个数值矛盾（如 0.46% vs 8.59% 的 18.7× 张力），并配套一个 Lean 真定理声称「同时闭合两个观测量」。

**检测三问**：
1. 参数定义式是否把**待解释的观测量本身**写进了分子？—— `f_DE = 0.682/((47/547)·148.036)` 中的 0.682 就是 Ω_DE 观测值。用观测值反解参数再声称参数「预测」观测值 = 反向工程。
2. 定理证的是「∃ 参数使恒等式成立」还是「参数由动力学唯一确定」？—— 存在性定理在数学上平凡：**任何目标值都能靠调节一个自由参数达到**。真物理闭合应从分支物理（Γ_b/Γ_trans + PBH 蒸发粒子种类）**导出**参数值，而非反解。
3. 分级表（K/C/A/P/O）是否登记了该参数？—— 未登记 = 与「net predictive degree = 0」自评矛盾。

**判定**：命中第 1 或第 2 问 = P0 反向工程（即便 Lean 代数 0 sorry、norm_num 真证）；命中第 3 问 = P1。

**修复模板**（三处同步）：
- 叙述层：删「covariant mass-transfer dynamic」→「EXISTENCE-level phenomenological branching ratio [P]」；「RESOLVED」→「PARAMETERIZED (not dynamically resolved)」
- 分级表：登记 f_DE 为 [P]（fixed BY Ω_DE, reverse-engineered; dynamical origin [O]）
- 明确区分「代数存在性」vs「动力学闭合」：定理证存在性，动力学导出标 [O]

**关键洞察**：这类缺陷的 Lean 证明是**干净的**（0 sorry），问题**纯粹在叙述层**。修复不动 Lean，只改 md 的叙述措辞 + 分级表登记。审稿人一致认可代数正确性，否决的是「存在自由参数吸收观测量」被叙述成「动力学机制」。

## Pattern 2 — 语言借用 vs 方程遵循（language borrowing vs equation following）

**触发信号**：子论文的三阶段/多机制声称「遵循」母框架的动力方程，但每个因果箭头的推导链需要逐一核对。

**检测方法**：把子论文每个因果箭头（如 localization→inflation、OT→time、KL→DE）逐条问「这是母方程（CGICE-1 Langevin / CGICE-2 Lyapunov / CGICE-3 Casimir / CGICE-4 KL 耗散）的**直接推论**，还是 honest-axiom / model-building postulate / [P] 校准？」。三值判定：`follows`（方程直接推出）/ `partial`（部分引用）/ `language_only`（只借语言无方程级映射）。

**2026-09-19 案例**：V18 Phase II（OT→时间→CDM 结晶）被判 5/5 `language_only`——Monge L¹ 成本 ≠ Brenier-McCann 平方成本，「transport ray = macroscopic time」是 postulate，与 CGICE-3 Casimir 守恒**无任何方程级映射**。

**连带检测**：子论文自述「four equations form a closed dynamical system」但同一段承认「`CGICE_System` 是 function/parameter 字段记录，无约束强制四方程成立」——这种「声称闭合 + 自我承认未闭合」是残留过度声称，与母框架 §4.5「四方程不闭合宇宙学反馈回路」自相矛盾。修复：改「conditional benchmark」。

## Pattern 3 — 双维度评分区分（internal consistency vs dynamics compliance）

同一篇论文可能：
- **内部一致性**评分高（公理/定理/参数自洽 + 0 sorry）—— V18 四轮审稿 4.7→6.5
- **跨论文动力学遵循度**评分低（三阶段因果箭头未由母方程驱动）—— V18↔CGICE 终审 4.80

**报告必须显式区分两个维度**，否则用户会困惑「为什么同一篇从 6.5 掉到 4.8」。两个维度衡量的东西不同：内部一致性 = 论文自身的自洽性；动力学遵循度 = 论文机制是否真正由母框架方程驱动（而非语言借用）。

## 正面判定（勿误伤）

跨论文参数对齐本身是**正面成果**：V18 与 CGICE 在 η_k=36/35（C_A=h^∨=6 约定）、g_TC 双值（2.60 vs 1.8395）、三谱对象区分（35/≥29/35/3）上基本一致——这是本轮唯一确认的对齐成果。审查报告应同时列出「对齐项」与「借用项」，不要只报缺陷。
