# 负结果定理 vs "导出"声称的自相矛盾（审稿驱动的诚实降级）

## 触发场景

论文声称从某个结构"导出"了一个特定数值（如 `c² = λ∥/λ⊥ = 3`），但论文自己在另一处有一个**负结果定理**证明这个数值是**任意选择**的（如 `Prop.1: r∥/r⊥ = d 对任意 d 成立`）。审稿人（尤其 R4 魔鬼代言人）会一眼识破这个自相矛盾，判为 P0「定义性重述，非导出」。

## 真实案例（LightSpeed_Phase_Boundary，2026-10-04 第三轮终审）

**声称**：`c² = λ∥/λ⊥ = 3` 是「从 SL(6,ℂ) 谱结构导出」，F6 标 [T]。

**矛盾**：论文自己的 **Prop.1** 已证明「r∥/r⊥ = d 对任意 divisor d 成立」（比值是任意选择）。新增的 `transverse_gap_eq_par_over_rank_A3` 定理只是把 divisor 贴上「rank(A₃)=3」的标签，但 divisor **仍然是被选择的**。审稿人原话：

> "The step λ⊥ = λ∥/rank(A3) is a *definition*, not a derivation... The new module adds the *label* 'rank(A3)' to the divisor, but the divisor is still chosen."

**根因**：λ⊥ = λ∥/3 的「3」是**选择**（equipartition 约定），不是 SU(1,5) 结构**被迫**的。除非引入 SO(3) 空间各向同性对称性（又一个新的 [M] 输入），否则「3」永远无法从谱结构导出。

## 修复（诚实降级，一轮内完成）

1. **F6 标签 [T] → [M]**：明确「λ∥/λ⊥=3 是从 equipartition CHOICE 推出的算术恒等式，非从 SU(1,5) 结构导出，正如 Prop.1 所示 divisor 不被选择」。
2. **Eq.(1) 降级**：`c*²=λ∥/λ⊥=3` → `sharp local speed c* fixed by the effective metric`（c* 是度量参数，非导出）。
3. **摘要去「光速」**：`a spectral light speed c²=3` → `a spectral ratio λ∥/λ⊥=3`（「light speed」是过度声称）。
4. **Lean 侧重命名**：`c_squared_eq_spectral_ratio` → `spectral_ratio_is_three`，注释明确「算术恒等式，非光速导出」。

## 检测信号（复审时必查）

- 论文声称「导出」特定数值 X，但 grep 发现论文有负结果定理证明 X 是「任意」/「自由」/「不被选择」的。
- 新增定理的陈述与已有负结果定理**逻辑矛盾**（一个说「导出」，一个说「任意」）。
- 标签 [T] 打在一个实质上是「定义 + 算术」的陈述上，而非「定理」。

## 通用教训

任何声称「导出特定数值」的声明，提交前必须先检查论文是否已有「该数值是任意选择」的负结果。若两者并存，**必须诚实降级**（把「导出」改为「选择/约定」），否则审稿人会用论文自己的负结果定理反驳——这是最难辩解的 P0。

## 关联：标签系统 [M] 过载 → 拆分 [M]/[A]/[O]

同一轮审稿（MINOR→ACCEPT 要求）还指出标签 [M] 过载，混用了三种语义，要求拆分：

- **[T]** = Lean 形式化定理（kernel-checked）
- **[M]** = matched input（显式物理假设：dictionary、real-form 选择）
- **[A]** = analytical under stated hypotheses（解析步骤，非机器检查，如 on-shell dispersion exclusion）
- **[O]** = open bridge（未形式化、未导出，如 τ 的物理驱动、λ∥↔时间对应）

标签定义必须放在 §I 显式声明四类，并在每个 Proposition 标题行加 inline 标签（如 `**Proposition 10 — on-shell exclusion [A].**`）。审稿人明确要求「split [M] into [M]/[A]/[O]」作为 MINOR→ACCEPT 的第一项。
