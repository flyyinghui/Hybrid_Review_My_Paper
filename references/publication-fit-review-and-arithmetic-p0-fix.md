# 投稿适配性终审 + 「编译通过但数学错误」硬算术错误修复（V18 → Foundations of Physics，2026-09-20）

## 一、投稿适配性终审的 5 代理配置（区别于标准 5 代理）

当用户要求「评估是否适合投稿某期刊」时，5 代理应替换为**含 publication-strategist 的配置**，而非标准 consistency/logic/technical/writing/bibliography：

| 代理 | 任务 | 关键输入 |
|---|---|---|
| consistency | MD-Lean 统计核验 + 跨章节数值/结论一致性 + 证据等级（K/C/A/P/O）前后矛盾 | 论文全文 + 机器级统计 |
| technical | 逐条**独立重算** P0 硬错误的算术 + 判断正文/Lean 是否已修复 | P0 清单 + 论文全文 |
| logic | 逻辑闭环 + 诚实性（状态升级、校准伪装、语言借用 vs 方程遵循） | P0 清单 + 论文全文 |
| lean_specialist | 公理依赖审计（多少是真研究公理 vs 零内容/占位/数值断言）+ 包装定理占比 + 0 sorry 真实性 | Lean 公理名清单 + 定理名清单 |
| **publication** | **期刊格式合规 + 科学门槛 + 投稿建议（READY/MAJOR/NOT READY）** | 期刊作者指南 + P0/P1 清单 |

### Foundations of Physics（Springer）格式核查清单（具体数字）

- 摘要 150–250 词；关键词 **4–6 个**（超 6 个即不合规）；最多**三级十进制标题**（`III.D′` 带撇号变体非标准，须改为 `III.E`）
- **必须提供 .tex 源文件 + 编译 PDF**（Markdown 直接投稿会被技术审查退回；Pandoc 标记 `[§III.B]{.mark}` 非标准 LaTeX）
- **AI 辅助披露**（Springer 2023 起强制，Acknowledgments 或独立声明段）
- 该刊对 honest-axiom 方法**容忍度最高**，但仍要求「明确物理内容」——净预测度≈0 时核心价值须重定位为「组织观测量」而非「独立预测」

### 投稿终审的机器级验证（先于 LLM 审稿）

1. 独立复现 `lake build`（确认论文自报 "SUCCESS, N jobs" 真实；注意 `export HOME=/root` 否则 lake 内部 `$HOME/.local/bin/env` 报错但无害）
2. 声明计数（剥离嵌套块注释 + 行注释后，行首锚定，处理分行 `@[honest_axiom]` 装饰器 + 区分 `noncomputable def` vs `noncomputable section`）
3. 把二审报告 + 既往审稿的 P0/P1 清单提炼为对抗性上下文注入每个代理，要求逐条判 `fixed/remain/partial`（禁止重新凭空评审）

---

## 二、三类「编译通过但数学错误」硬算术错误修复模式

> **元教训：Lean 编译通过 ≠ 数学正确。0 sorry 是源码卫生条件，不能替代命题语义审查。** 下述三类错误全部 `lake build SUCCESS`，却是语义级硬错误。

### 类型 1：因子/系数错误 + 正文与形式化双向脱节（ouCov 因子 2）

- **症状**：正文公式正确（`C_t = D/ℓ + (C₀−D/ℓ)e^{−2ℓt}`），但 Lean `def ouCov := ... * Real.exp (-ell * t)` 指数少因子 2。
- **本质**：诚实化只落在**正文文字层**，未传导到 **Lean 代码层**——这是终审发现的最危险错误类型（论文声称 Lean 验证了正文，但 Lean 定义与正文公式矛盾）。
- **检测**：逐条对比正文公式 vs Lean def 的系数/指数/符号；代入反例（ℓ=D=1, C₀=2, t=0 导数 −1 vs 方程要求 −2）。
- **修复**：改 Lean def + 编译验证 + 补 `_deriv` 定理验证 `C' = −2ℓC + 2D`（`ouCov_initial`/`ouCov_stationary` 用 `simp [ouCov]` 对任意指数都成立，改指数后无需改证明体）。

### 类型 2：比例/方向写反（metzler 稳态比例 v/u vs u/v）

- **症状**：注释写「稳态 DM/重子比 = v/u」，但稳态向量 `![v,u]`（B=v, D=u）故 D/B = **u/v**。
- **检测**：用具体数值代入验证（u=2, v=1 → 稳态 (B,D)=(1,2) → D/B=2=u/v）。
- **修复**：改注释 + **显式标注分量顺序**（`（B=v, D=u）`），消除歧义。

### 类型 3：观测输入伪装成谱定理（PF 主特征值 = 5.47）

- **症状**：`axiom perron_frobenius_dominant_eigen : MetzlerPositiveCone M → DominantEigenvalue M = 5.47`。但**保守 Metzler 生成元（列和为零）谱界为 0**，主特征值不可能为 5.47。5.47 是 Planck 观测输入（Ω_c/Ω_b≈5.44）。
- **本质**：「校准伪装成推导」的**谱定理变体**——把观测输入包装成谱定理结论。注释里即使已诚实标注「5.47 是观测输入」，**公理声明本身仍把 5.47 当谱定理**，诚实标注未传导到声明语义。
- **修复**（删除公理链，最小侵入）：
  1. 删除 `perron_frobenius_dominant_eigen` + 依赖它的 `dominant_eigen_closure` 公理
  2. 删除调用它们的包装定理 `baryon_dark_matter_ratio_evolution_closure`（先 grep 确认**无下游引用**）
  3. 删除随之孤立的 opaque（`strat5_DominantEigenvalue`/`strat5_BaryonDMRatioClosure`，零引用后）
  4. 新增诚实常量 `def targetRatio : ℝ := 547/100`（标注 [P] 观测输入，NOT 谱定理）

---

## 三、修复后的同步协议

1. **grep 残留引用**：删除声明后 grep 全部被删名字，须 0 残留（无悬空引用）。本次 5 个名字（2 公理 + 1 定理 + 2 opaque）全部 0 残留。
2. **编译验证**：`cp 6D_*.lean Spacetime_*.lean && rm -f .lake/.../Spacetime_*.olean && lake build`（lakefile roots 数字开头模块名须用 Spacetime_ 前缀；`export HOME=/root`）。本次 8725 jobs 通过，jobs 数与删除前后一致。
3. **同步论文 MD 附录 A 统计**：删除后重跑声明计数，每个声明类型重新核对。本次 116→114 axiom（104→98 honest + 16 phenomenological）、174→173 theorem、73→71 opaque、125→126 def（89→90 plain）。同时把正文「among the 104 [honest-axiom]」同步为 98。
4. **验证无残留**：grep 论文 MD 旧数字（116 axiom / 104 honest / 174 theorem 等）须 0 残留，新数字须命中。

### 网络中断时的进度保存协议

- 三个硬错误修复已 `patch` 落盘后，若编译需暂停：`process kill` 编译进程 → 确认 0 残留 lake 进程 → `cp` 修复后文件为 `.bak_p0fix_<date>` → 写进度快照 MD（含已完成修复表 + 恢复后编译命令模板 + 待同步的论文 MD 统计）。快照里明确「本地 lake build 不依赖网络」。
