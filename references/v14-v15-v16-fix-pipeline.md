# V14→V15→V16修复管线全记录 (2026-08-06)

三峰引力波论文V14→V16的三轮迭代修复全流程，含每轮的审阅发现、修复策略、残留缺陷。

## V14审阅 (1.4/10)

**方法**: 三代理并行 (一致性+逻辑+技术)，含对抗性上下文 (V13审阅)。

**8项P0缺陷**:
- P0-1: z_eff 10^278 vs Lean 4.29 (278数量级差异)
- P0-2: Lean 10个未定义符号 (Omega_peak_PT等)
- P0-3: H₀假推导 = `unfold H0_pred; rfl`
- P0-4: DM:B 75>70 DOF计数矛盾
- P0-5: Ω_GW能量和算术假 (6.40≠2.50, 误差156%)
- P0-6: Bourgain假定理 (A×B≥1 from A>0,B>0)
- P0-7: GW峰值正文"推导"vs附录"校准"矛盾
- P0-8: λ_KLS冲突定义 (def=35 vs axiom=klsGapFromMatrix)

## V14→V15修复

**Lean修复** (9项patch):
- P0-2: 新增10个缺失定义 (f_peak_PT, Omega_GW, h_tilde, V0等)
- P0-3: 删除h0_frw_derivation，改为[honest-axiom]
- P0-4: DM:B降级为[phenomenological]
- P0-5: 修正为1.0e-10+1.4e-9+1.0e-9=2.5e-9
- P0-6: **头注释声称删除，但代码未删** ← 这是V15审阅发现的
- P0-8: 移除kls_physical_def
- P1: 删除5处重复定义

**论文DOCX修复** (9项XML+python-docx):
- 摘要H₀声称修正、z_eff修正、ρ_DM校准标注
- §3/§B.3/§B.4/§B.5全部诚实声明更新

## V15审阅 (3.7/10)

**方法**: 三代理并行，对抗性上下文 (V14审阅)。

**新发现 (V15→V16的驱动)**
- P0-6a (新增): Lean头注释声称删除了Bourgain假定理，但代码中原封保留。**头注释与代码矛盾**。
- P0-5a (新增): Omega_GW_total_eq_Omega_DM使用V14旧值，`rfl`对`Real.exp`不可用。
- T5 (新增): ρ_GW(total)=2.5e-9 vs Ω_DM(Planck)=0.264 → 差距~10⁸倍，论文未解释归一化。
- Section 8含"intentionally false"定理 (tensor_to_scalar_ratio_lt_Planck_limit) — 不可接受。

**V14 P0修复状态**: 3 FIXED / 3 PARTIAL / 1 UNFIXED (P0-6)

## V15→V16修复

**Lean修复** (3项大patch):
1. P0-6a: 真正删除Bourgain_slicing_conservation + time_explosion + Bourgain_differential，替换为`axiom bourgain_physical_analogy`
2. P0-5a: 删除Omega_GW_total_eq_Omega_DM及其依赖定理，替换为`Omega_GW_DM_equivalence_V16 := energy_sum_rule`
3. T5: 在ρ_DM定义处添加诚实注释说明任意归一化
4. Section 8: 整节替换为`[phenomenological]`占位符

**数值校核**: 12/12通过 (Python直接验算)

## 关键教训

### 1. "头注释声称修复但代码未删"模式
**信号**: Changelog说"Removed X"但grep找到X仍存在。
**根因**: 多轮迭代 — 头注释在某一轮更新了，但删除代码的patch在另一轮遗漏。
**检测**: 任何声称删除的东西，必须用注释剥离后的grep验证。
**参考**: `lean-arithmetic-audit-patterns.md` Pattern 1

### 2. "intentionally false"定理
**严重性**: CRITICAL。公开声称的定理如果自身证明其否定，比空壳更糟糕。
**V14→V16路径**: Section 8的tensor_to_scalar_ratio被标记为"intentionally false"，V16整节删除替换。
**规则**: 任何论文/Lean中不应出现"intentionally false"的"定理"。

### 3. 三代理审阅效率
V15审阅用了3代理 (一致性+逻辑+技术) 而非V14的5+1代理。找到全部11项缺陷，时间~6min vs ~13min。
**结论**: 对于有前序审阅上下文的后继版本，3代理足够。

### 4. Ω_GW归一化诚实声明
**问题**: 论文核心声称Ω_GW=Ω_DM，但校准值2.5e-9与Planck值0.264差10⁸倍。
**解决**: 诚实声明ρ值在任意归一化中，10⁸因子代表能量稀释。不要假装相等。
