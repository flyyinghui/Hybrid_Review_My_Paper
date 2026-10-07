# 定义性重述 dressed as derivation：当论文自己的定理证明"任意"时

## 模式（5/5 审稿人一致判 P0 的案例）

论文在 A 处声称「X 是从结构 Y *导出*的」，但在 B 处（往往是它自己的命题）已经证明「X 是*任意选择*的 / 不唯一的」。这两者逻辑矛盾，审稿人会一针见血指出，且这是**最致命**的一类过度声称——不是措辞问题，是论文内部自相矛盾。

## 检测信号（三条同时命中即 P0）

1. 论文声称「X 是从结构 Y 导出的 / X 由 Y 决定」。
2. 论文自己的某个定理（或显而易见的事实）证明「X 是定义 / 选择 / 约定，不唯一」。
3. 关键量是 divisor / 归一化 / equipartition / 等分这类**约定性的"分母"**，而非被迫的常数。

## 案例（光速分界面 c²=3，第三轮终审实录）

论文声称「c² = λ∥/λ⊥ = 3 从 SU(1,5) 谱结构导出」，并把定理 `c_squared_eq_spectral_ratio` 标 [T]。

但论文自己的 **Prop.1 已经证明「r∥/r⊥ = d 对任意非零 d 都成立」**（比值是任意选择的）。

审稿人原话（R2 领域专家）：
> "The step λ⊥ = λ∥/rank(A3) is a **definition**, not a derivation. The manuscript's own Prop.1 proved that r∥/r⊥ = d for *any* chosen d — the same logic applies here: λ⊥ = λ∥/3 is a *choice*, and c² = 3 is a *consequence of that choice*. The new module adds the *label* 'rank(A3)' to the divisor, but the divisor is still chosen."

即：给 divisor 贴上「rank(A₃)」的群论标签，但 divisor 仍是被选择的——「标签」不改变「选择」的性质。

## 修复模式（诚实降级，不要试图"证明 3 是被迫的"）

1. **[T] → [M]/[O]**：把声称"导出"的定理标签降级为 matched input 或 open bridge。
2. **"derived" → "arithmetic identity from the choice"**：明确写「值 3 是 equipartition choice λ⊥=λ∥/3 的算术恒等式，*not* derived from the SU(1,5) structure, which — as Proposition 1 shows — does not select the divisor」。
3. **摘要/Eq(1) 去掉"结论"地位**：`spectral light speed c²=3` → `spectral ratio λ∥/λ⊥=3`；框式 Eq 把 c*²=3 从"结论"改为「c* fixed by the effective metric」。
4. **Lean 定理重命名**：`c_squared_eq_spectral_ratio` → `spectral_ratio_is_three`，注释写明「ARITHMETIC identity (a restatement of the existing spectral_rate_ratio), NOT a derivation of a light speed; the value 3 follows from the definitions, an equipartition CHOICE」。

## 根本诊断（可复用）

**要"导出" X，必须证明 X 是"被迫的"（forced by the structure），而非"任意选择的"（chosen）。** 如果论文自己证明了"任意"，那"导出"就不可能成立——除非引入一个新的 [M] 输入（如 SO(3) 空间各向同性对称性），但那样只是把矛盾从「任意 divisor」转移到「新的对称性假设」，审稿人大概率仍判 PARTIAL。

判定标准：grep 论文里有没有「for any / arbitrary / any nonzero d / any chosen」这类任意性声明，再 grep 有没有「derived / determined by / follows from the structure」这类导出声明。两者出现在同一个量上 = P0。

## 关联

- `lean-tautology-and-false-fix-detection.md`（定义性重言式，unfold 后只剩恒等式）
- `honesty-downgrade-paradox.md`（诚实降级反而降分——本例是它的极端版：不降级就是自相矛盾的 P0）
- `parameterization-disguised-as-dynamical-closure.md`（参数化伪装成动力学闭合）
