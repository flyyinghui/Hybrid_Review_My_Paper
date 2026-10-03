# 正文诚实化 vs Lean 代码语义脱节（paper-vs-lean semantic drift）

## 审查维度

终审核对时，**不能只核对「声明计数」**（axiom/theorem/opaque 数量是否一致），还要核对「**正文公式语义 vs Lean 代码定义**」是否一致。最常见且最危险的是：**正文已诚实修正/标注，但 Lean 代码仍保留旧错误语义**——此时声明计数完全对齐、编译 0 sorry，但论文声称「Lean 验证了正文」是假的（正文说 A，Lean 写的是 B）。

## 案例（SL(6,C) V18 终审，2026-09-20）

5 代理终审（technical 4.5 / lean_specialist 3.5 / publication 3.5，一致 NOT READY）发现 3 个「编译通过但数学错」的硬错误，全部是正文已诚实化、Lean 代码未同步：

1. **ouCov 因子 2**：正文 §IV.C 已写正确 `C_t = D/ℓ + (C₀−D/ℓ)e^{−2ℓt}`，但 Lean `def ouCov (ell D C0 t) := (C0 − D/ell) * exp(−ell*t) + D/ell` 仍是指数 −ℓt（应为 −2ℓt）。残差 ℓ(C−D/ℓ)≠0；反例 ℓ=D=1,C₀=2,t=0 时导数 −1，CGICE-2 要求 −2。
2. **metzler 稳态比例写反**：稳态向量 [v,u]（B=v, D=u），正确 DM/重子比 = D/B = **u/v**，注释写成 v/u。
3. **PF 主特征值伪装谱定理**：正文已诚实标注「5.47 是 Planck 观测输入 Ω_c/Ω_b≈5.44」，但 Lean `axiom perron_frobenius_dominant_eigen : … → DominantEigenvalue M = 5.47` 仍把观测输入当主特征值——保守 Metzler 生成元（列和为零）谱界为 0，主特征值不可能为 5.47。属「校准伪装成推导」。

## 检测方法

1. 逐条提取正文的数值公式（尤其带 `[honest-axiom]`/`[P]`/「calibrated」/「withdrawn」标记的），grep Lean 里对应 def/axiom 定义，比对**语义**（不是字面一致，而是数学值是否同一）。
2. 重点查「正文已诚实化/修正，但 Lean 代码未同步」的双向脱节——正文写 −2ℓt 但 Lean 写 −ℓt；正文说「观测输入」但 Lean 写成「谱定理结论」。
3. 编译通过（0 sorry / 0 error）≠ 数学正确。三个错误全部编译通过。grep 关键数值（`-2 * ell`、`u/v`、`targetRatio`）确认正文的修正是否真的落到了代码。

## 修复原则

正文的诚实标注**必须传导到 Lean 代码**，不能只改正文文字：
- 硬算术错（因子/比例/符号）→ 直接改 Lean def 的数值（如 `exp(−ell*t)` → `exp(−2*ell*t)`）。
- 观测输入伪装成谱定理 → 删公理，改 `def targetRatio : ℝ := 547/100`（诚实常量），删下游包装定理 + 孤立 opaque。
- 隐含假设未披露（正定性缺失）→ 在 def/定理注释里显式披露反例 + 限定条件（如「限制到紧实形式 su(6) 用 ⟨X,Y⟩=−Re tr(XY)」）。

改完重新统计声明计数（116→114 axiom 等）并同步论文附录 A 的自报数字。
