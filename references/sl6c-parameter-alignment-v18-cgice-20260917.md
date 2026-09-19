# SL(6,C) 参数对齐权威值（V18 + CGICE v10 对齐，2026-09-17）

跨论文审查/重构 SL(6,C) 系列（V18 三大时空相 / CGICE v10 / V63 中微子 / GW-V19 三峰）时，以下为两份最新手稿一致采用的**权威参数值**。旧框架（SL6C_Unified_Geometric_Dynamics_Framework.md）此前有三处关键错误，2026-09-17 已修正。审稿或重构时以本表为准，勿沿用旧值。

## 1. η_k 异常维度 —— 归一化约定（P0 级修正）

η_k 的数值取决于生成元归一化约定，这是最容易犯错的参数：

| 约定 | C_A 值 | η_k | 生成元条件 |
|------|:--:|:--:|------|
| **Hermitian/物理约定**（权威） | C_A = h^∨ = **6** | **36/35 ≈ 1.029** | Tr(T^aT^b)=δ^ab/2 |
| Killing-form/数学约定（废弃） | C₂(adj) = **12** | 72/35 ≈ 2.057 | Tr(T̃^aT̃^b)=δ^ab（T̃=√2T 重标定） |

- **CGICE v10 §7.3 与 V18 §III.D′ 一致采用 η_k = 36/35**（C_A = h^∨ = 6，NOT 12）。
- 旧框架的 η_k = 72/35（C₂(adj)=12）是 Killing-form 约定，**已废弃**。
- 重标定生成元（T̃=√2T）时必须一致变换耦合与 β 函数，不可只改 Casimir 单值。
- 检测信号：看到 η_k=72/35 即为旧值；72/35 = 2×36/35，差恰好 2 倍（归一化约定差异）。

## 2. g_TC 双值区分（P0 级修正）

旧框架把 g_TC=2.60 误标为"FRG IR 定点"。正确区分两个不同的 g_TC：

| 量 | 值 | 公式 | 来源 | 状态 |
|---|:--:|---|---|:--:|
| **FRG 定点** | g\* ≈ **1.8395** | (g\*)² = 4π²\|η_k\|/b₀ = **12π²/35 ≈ 3.38** | η_k=36/35 + b₀=12 | 条件定理（η_k Ansatz） |
| **D1 瞬子/谱耦合** | g_TC ≈ **2.60** | g_TC² = 8π²/λ_⊥ = **24π²/35 ≈ 6.77** | D1 桥（分母 λ_⊥=35/3） | 公理 [D1] |

- **V18 §III.D′ 原文**："g_TC ≈ 2.60 (the FRG fixed point is instead g\* ≈ 1.8395)"——**2.60 不是 FRG 定点**。
- 两值差 √2 倍（24/12=2），源于 D1 桥用 λ_⊥=35/3 作分母 vs FRG 用 η_k=36/35。
- g_TC(UV)=0.5 是裸 GUT 耦合 [postulate]；微扰单圈 Landau 极点 ~3.7×10⁴ GeV（红外方向）。
- 0.5 → 2.60 需非微扰增强 ~5×（g_TC 线性）~27×（g_TC² 二次），微扰单圈流达不到 FRG 定点。

## 3. 三个谱对象（P0 级修正）

旧框架"一刀切 λ_KLS=35"掩盖了三个本质不同的谱对象，**绝不能混同**：

| 谱对象 | 符号 | 值 | 数学来源 | 状态 |
|---|---|:--:|------|:--:|
| 自由 Laplacian 谱底 | λ_∥ | **35** | ‖ρ_res‖²=70/c, c=2（限制根重数 2 + 对偶度规归一化） | 归一化结果 [F] |
| Witten 谱隙 | λ₁(L_μ) | **≥ 29** | Bakry-Émery CD(29,∞): Hess V ≥ 35g + Ric ≥ −6g (c=2, D=1) | 条件性 [条件定理] |
| 横向率 | λ_⊥ | **35/3 ≈ 11.667** | 3D 各向同性均分 λ_∥/3 | 独立匹配输入 [M, A-3D] |

- **V18 §III.B 警告**：`29`（条件性 BE 下界）与 `35/3`（横向匹配输入）**属不同算子/子空间**——3D OU 过程单坐标 gap 是 ℓ，不是 ℓ/3。λ_⊥=λ_∥/3 的"除 3"是各向同性空间均分假设（postulate），非谱几何推导；仅 λ_∥=35 是严格谱几何值。
- CGICE v10 §2.3 标度恒等式：扩散隙 δ_L = (β/4)·δ_W(2/β, V)，非未缩放的 Witten 隙。
- √3 = √(λ_∥/λ_⊥) 是两预设输入 35 与 35/3 的算术推论（派生常数），与测度桥接因子 ξ=√π·η_Cartan 分属不同物理层面（谱几何 vs 测度论），数值接近（1.732 vs 1.7701）是巧合。

## 4. V18 公理架构 + 定理状态 + Lean 计数（对齐参考）

**公理架构 A–F 六类 29 条**（V18 附录 A，取代旧版 A1-A12 12 条）：
- A. 几何基础 5 条（A1 Cartan 分解 / A2 Witten Laplacian / A3 KLS 谱隙 / A4 Bakry-Émery CD / A5 Bourgain 切片）
- B. 动力基础 3 条（B1 CGICE 4-SDE / B2 FRG-Wetterich k=3/35 / B3 Monge OT）
- C. 分析基础 2 条（C1 Atiyah-Singer 指标 / C2 CGICE→CGWB 桥接）
- D. 桥接 3 条（D1 g_TC²=8π²/λ_⊥=24π²/35 / D2 Cartan-Gauge-Weinberg / D3 Monge 时间双用）
- E. 宇宙学 3 条（E1 三相涌现 / E2 GW 三峰 Ω_GW·h²≈2.5×10⁻⁹ / E3 CDM:baryon=5:1）
- F. 领域特定 13 条

**定理状态表**（V18 附录 A 权威）：T_WITTEN(λ₁≥29)=CONDITIONAL / T_KLS_GAP(λ_⊥=35/3)=INPUT / T_E_FOLD(N_e≈80.59)=OPEN / T_MONGE=MODEL-BUILDING / T_DM_RATIO(5:1)=ANSATZ / T_ATIYAH_SINGER(g_TC²∝ind/λ_⊥)=CONJECTURED / T_GW_SPACING=CONJECTURED / RG_POSITIVITY=PROVED。

**Lean 声明计数**（V18 附录 A 官方，comment-stripped ACTIVE）：**80 axioms + 151 theorems + 43 lemmas + 113 definitions + 30 opaque + 1 abbrev + 3 classes + 12 structures**，0 sorry / 0 admit / 0 trivial / 0 True 桩。3 个剩余证明义务（Eldan-Chen / linear SPDE / Hepp-tree）为 `[honest-axiom]` + `[Mathlib-open]` 声明。

## 5. 诚实性边界（V18 终审 5.6/10 Major Revision，2026-09-17）

- Ω_GW = Ω_DM **已撤回**（V18 附录 A：无 TT 各向异性应力/谱形/关联长度/探测器响应推导）
- 5:1 是 **P/postulate**（拓扑均分，非推导）；黑洞嬗变链不闭合（0.35%×148≈0.518≠0.682）
- 450 GHz / 1.71 Hz 是**基准参数 P**（非群维数唯一推论，峰位由源参数决定）
- V18 的 4 项 P0 待修：§III.D′ 标题"Explicit Heat-Kernel Derivation"与正文"η_k 是群论 Ansatz"矛盾、Hess(V_eff)≥35g 从 Poisson 推导属类型错误（应改 conjecture）、w₀ 三值未统一（−1/−0.73/[−0.80,−0.65]）、axiom 计数正文 80 vs 实测 84
- CGICE v10 的 3 项 P1：KL decay 术语滑移、Bakry-Émery 归一化（δ_L≥a−6D 仅 D=1 对）、c=2 与 δ/2 factor-2 桥接未推导

## 关联参考

- `multi-value-parameter-tracing.md` —— g_TC 四值溯源（2.60/1.50/0.5/2.83 各自对应 λ_KLS=35/3、35、无来源、g_TC²=8）
- `status-escalation-overclaim-detection.md` —— η_k=C₂(adj)·h^∨/dim(M) 是群论 Ansatz 非推导
- `parent-framework-review-prerequisite.md` —— 母框架角色分工（UV/IR、双实形式）
