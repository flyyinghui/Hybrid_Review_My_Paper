# 正文诚实化 vs Lean 语义脱节 + 硬算术错误修复

2026-09-20 V18 论文终审 + P0 修复实录。核心元发现：**多轮修订把正文改诚实了，但 Lean 代码没同步**，导致「诚实性 7.5/10 vs 技术严谨性 3.5-4.5/10」的分裂。

## 一、元模式：正文 vs Lean 双向脱节（诚实化未双向落地）

**症状**：终审 5 代理一致判 NOT READY，但诚实性维度（预测度≈0、三峰撤回、λ_⊥=35/3 标独立输入、PhaseCgiceBridge 标「语言借用」）做得很好。矛盾在于——**正文文字层的诚实标注没传导到 Lean 代码层的 axiom 定义/证明体**。

**检测**：终审时必须对照「正文自报的公式/数值」与「Lean 里实际的定义/公理」，不能只信正文的自报统计。具体三例：

| 维度 | 正文（已诚实化） | Lean（未同步） | 判定 |
|---|---|---|---|
| ouCov 指数 | §IV.C 写 `e^{−2ℓt}` | def 写 `exp(-ell*t)` | P0 双向脱节 |
| 5.47 来源 | 承认「观测输入 Ω_c/Ω_b≈5.44」 | `perron_frobenius_dominant_eigen` 公理把它当谱定理 | P0 校准伪装 |
| Casimir | 声称「provable theorem」 | `trace_pairing` 非正定，不能推 ‖j‖² 守恒 | P0 过度声称 |

**修复原则**：诚实化必须是**双向**的——正文改一句，Lean 的对应 axiom 定义/注释必须同步改；反之亦然。否则终审会同时抓到「正文诚实」和「代码矛盾」两个对立的信号。

## 二、三个硬算术错误（编译通过 + 0 sorry 但数学错）

这三例都 `lake build` 通过、0 sorry，但数学错误。印证「0 sorry 是源码卫生条件，不能替代命题语义审查」。

### P0-1 ouCov 因子 2（正文已对、Lean 错）

- 错误：`def ouCov (ell D C0 t) := (C0 - D/ell) * exp(-ell*t) + D/ell`，指数应为 `-2*ell*t`（CGICE-2 要求 C'=-2ℓC+2D）
- 残差 ℓ(C−D/ℓ)≠0；反例 ℓ=D=1,C₀=2,t=0 导数 −1，方程要求 −2
- 修复：`exp(-2 * ell * t)`。`ouCov_initial`/`ouCov_stationary` 的 `simp [ouCov]` 证明体对任意指数都成立（t=0 时 exp=1、C₀=D/ℓ 时系数=0），改指数后**不需改证明体**

### P0-2 metzler 稳态比例写反（注释错）

- 错误：注释写「稳态 DM/重子比 = v/u」
- 正确：稳态向量 ![v,u]（B=v, D=u），DM/重子比 = D/B = **u/v**
- 修复：改注释 + 显式标注「B=v, D=u」。证明体（M·[v,u]=0）不涉及比例方向，不改

### P0-3 PF 公理伪装谱定理（数学不可能，删公理改 def）

- 错误：`axiom perron_frobenius_dominant_eigen : MetzlerPositiveCone M → DominantEigenvalue M = 5.47`
- 数学事实：列和为零的保守 Metzler 生成元谱界为 0，主特征值**不可能**为 5.47
- 修复：删除该公理 + 依赖它的 `dominant_eigen_closure` 公理 + `baryon_dark_matter_ratio_evolution_closure` 包装定理 + 两个孤立 opaque，新增 `def targetRatio : ℝ := 547/100`（诚实观测输入常量）
- 前置检查：`grep -n <公理名>` 确认下游引用（本例 3 个声明互引、无其他下游，删除干净）

## 三、P0-9 迹配对不正定（隐含假设 → 诚实披露）

- `trace_pairing B(X,Y)=Re tr(XY)` 的 ad-不变性是**真定理**（trace_mul_cycle），但在整个 𝔰𝔩(6,ℂ) 上**不正定**：H=diag(1,-1,0,0,0,0) 得 B(H,H)=2>0，K=iH 得 B(K,K)=−2<0，E₁₂ 得 0
- 正文曾声称「Casimir conservation is a provable theorem rather than an honest-axiom」——这是**过度声称**，因为 B 非正定，不能单独推出 Casimir 标量 ‖j‖² 守恒
- 修复（注释层诚实披露，不改代码语义）：①trace_pairing 注释加「非正定，正定内积需限制 𝔰𝔲(6) 用 ⟨X,Y⟩=−Re tr(XY)」②trace_pairing_ad_invariant 注释改为「只证 ad-不变性，不证正定性，Casimir 守恒整体仍是 honest-axiom」③正文 III.C 同步改为诚实披露

## 四、P0-7 CGICE 方程基准对齐（旧方程残留 → 标注历史版本）

- PhaseCgiceBridge 的 opaque 注释把 CGICE-3 写成拓扑荷源项 `Q̇_CS=g∫Tr(F∧F)/8π²−γQ_CS`、CGICE-4 写成循环熵 `∮dS_info=0`，但 CGICE v10 §4 基准是：CGICE-3 = 紧李代数伴随输运 `j̇=−g[a,j]` Casimir 守恒；CGICE-4 = 固定 μ 下 `KL′=−D∫p‖∇log(p/μ)‖²`
- 修复：①opaque 注释改为 v10 基准方程 ②文件里其他旧方程残留（历史块注释、honest-axiom 注释）加 `[NOTE: HISTORICAL V11 formulation, NOT CGICE v10 baseline]` 标注，不删除（保留历史上下文）
- grep 残留检查：`grep -nE "Q_CS/dτ|dS_info|拓扑荷守恒|信息循环闭合"` 应定位到所有旧方程，逐一加标注

## 五、修复后声明计数同步（论文 MD 附录 A）

删除/新增声明后，论文 MD 附录 A 的自报统计必须同步：

| 操作 | 计数变化 |
|---|---|
| 删 2 axiom | axiom 116→114（honest 100→98） |
| 删 1 theorem | theorem 174→173 |
| 删 2 opaque | opaque 73→71 |
| 加 1 def | def 125→126（90 plain + 36 noncomputable） |

同步后 `grep -nE "116 axiom|104 honest|174 theorem|73 opaque|89 plain" 论文.md` 应无残留旧数字。注意 honest_axiom 计数口径：装饰器 `@[honest_axiom]` 分行写时，朴素 `grep -c "@\[honest_axiom\] axiom"` 会漏（只匹配同行），需分行+同行都统计；phenomenological 标记同理（16 个），论文常漏披露这一档。
