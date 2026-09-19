# Lean 形式化证明审计 — 块注释假阳性 + def-baked 重言式公理 + 假修正检测

**来源**: 2026-08-23 CGICE V9 FOP 论文 + `cgice_proof_v9.lean` 终审。三代理并行（逻辑自洽性 / 数学推导完备性 / 跨文档一致性）+ 独立 Python 数值复核 + Lean 统计审计。

---

## 1. Lean 统计 grep 必须同时剥离块注释和 docstring（否则 sorry 假阳性）

只排除 `--` 行注释**不够**。`/- ... -/` 块注释和 `/--` docstring 里也常出现 "sorry"（如注释文字 "Removed previous sorry"、"/-- ... (0 sorry) ..."），导致 `grep -c sorry` 假阳性。

**正确做法（Python 精确版，先剥块注释再滤行注释）**：
```python
import re
lean = open(path, encoding='utf-8', errors='replace').read()
lean_noblock = re.sub(r'/-.*?-/', '', lean, flags=re.DOTALL)   # 先剥 /- ... -/ 块注释 + /-- docstring
lines = [l for l in lean_noblock.splitlines() if not l.strip().startswith('--')]
code = '\n'.join(lines)
for kw in ['axiom','theorem','lemma','sorry','admit']:
    print(kw, '=', len(re.findall(r'\b'+kw+r'\b', code)))
print(':= True =', len(re.findall(r':=\s*True\b', code)))
print('by trivial =', len(re.findall(r':=\s*by\s+trivial', code)))
```

**本次实测**：只排除 `--` 时误报 `sorry=2`（一行在块注释内 "Removed previous sorry"，一行是 `/-- ... (0 sorry)` docstring）；剥离块注释后正确得 `sorry=0`，论文 "0 sorry" 声明属实。**先跑此脚本再下结论，避免把"假阳性 sorry"当成发现报给用户。**

---

## 2. def-baked 重言式公理检测（[honest-axiom] 标签掩盖零内容）

当 `axiom X : name = value` 中的 `name` 已被 `noncomputable def name := value` 定义时，该公理是 **name=name 重言式**，零数学内容——即便标了 [honest-axiom] 并声称编码物理内容。

**检测法**：对每个 `axiom a_* : lhs = rhs`，grep 是否存在 `def lhs := ...` 且其 RHS 等于 `rhs`。

**CGICE V9 实例（全部零内容）**：
- `a4_kls_spectral_gap : lam1 = 35/3`，但 `lam1 := 35/3`（def）→ lam1=lam1
- `a_t3_harish_chandra_lower_bound : 35 = rho_sq_doubled`，但 `rho_sq_doubled := 35`（def）→ 35=35；真实 Harish-Chandra 内容 σ_ess⊂[|ρ|²,∞) 完全不在公理里
- `a_t5 : lam1 = 35/3` 与 a4 **逐字重复**
- `spec_gap_bound : Prop`（自由 Prop 常量）+ `a_t4 : spec_gap_bound`（断言未约束 Prop）
- `a1_geometric_manifold : ℕ := 35`（def，仅给 35 命名）

**更隐蔽的变体**：条件定理 `s1 : (3·λ_⊥=ρ 且 ρ=35) → λ_⊥=35/3`——前提已蕴含结论，35/3 通过假设走私进来，证明退化为算术重写。判断法：**看定理前提是否已逻辑等价于结论**。

**"证明"实质**：把物理量烘烤进 `def`，再用重言式公理"证"一遍，定理体沦为 norm_num/ring/rfl 机械重排。审计结论应为"未证明任何非平凡内容"，而非接受 "0 sorry = 已证明"。

---

## 3. 假修正检测：论文的 "fix" 本身可能是错的

当论文声称把某值从 A "修正"为 B（并说 A 是反向工程/错误），用**论文自己引用的精确参数**独立重算 A 和 B——反向工程标签可能贴反了。

**CGICE V9 实例**：§7.6 声称 H₀t₀ 正面积分 "修正" 0.9497→0.9484（称 0.9497 是反向工程乘积）。
- 正面积分 (2/(3√Ω_DE))·asinh(√(Ω_DE/Ω_M))，Ω_DE=0.682, Ω_M=0.317 → **0.9495 ≈ 0.9497**
- 0.9484 对应 Ω_M=0.318（=1−0.682 严格平坦），论文却同时引用 Ω_M=0.317（和=0.999）
- **结论**：正向积分本就给 ~0.9497，本无矛盾；"修正"凭空引入 ~0.0011 误差（≈0.08 km/s/Mpc）且反向误标。

**教训**：审查 "fix" 时，必须重算"旧值"和"新值"哪个才是真积分值，而非默认接受论文的"修正"叙事。尤其警惕"修正值恰好对应论文没引用的另一组参数"（本例 0.9484 对应 Ω_M=0.318 而非引用的 0.317）。

---

## 4. 公理计数膨胀分解

声称 "N axioms" 时按四类分解，识别计数注水：
- **占位状态变量声明**（`axiom V_eff : ℝ → ℝ` 等，零内容，只是声明函数存在）
- **重言式/自由 Prop**（见 §2）
- **数值断言公理**（`axiom H0_analytic_derivation : H0_km_s_Mpc = 67.42`，无推导直接断言）
- **物理内容公设**（真正有内容的公理）

**CGICE V9 实例**："73 axioms" → 占位 ~36 + 重言式 ~6 + 数值断言 ~5 + 真实公设 ~26。声称的"73"被占位声明和数值断言大幅稀释。**同理，"36 theorems" 约 2/3 是 rfl/norm_num/`exact 公理` 回引，唯一实质推导往往只有一两个教科书级计算。**

---

## 5. 跨文档"过称 vs 诚实"张力

当母框架（无形式化）与论文（有 0-sorry Lean 形式化）对同一物理量的地位表述矛盾时，**有形式化的一方通常更诚实**。

**CGICE V9 实例**：母框架称 H₀=67.42 / η_k=72/35 / DM:B=5.47 / λ_⊥=35/3 是"第一性原理严格导出"，论文已诚实降级为"现象学校准/参数化假设/观测输入/反向工程"。机制：母框架的"第一性原理推导"来自**无 Lean 形式化的手稿**，而 0-sorry Lean 反而诚实标注。结论：**以有形式化一方的口径为准**，母框架的"推导"标签统一下修为"几何动机 + 显式校准参数"。

---

## 独立重算数值速查（本次 CGICE V9 已核实，供同类审查参考）

|ρ|²_std = 17.5 / doubled = 35 / λ_⊥ = 35/3 = 11.667 / τ_CGICE = 6π/35 = 0.5386 / η_k = 72/35 = 2.057 / g* = √(24π²/35) = 2.6015 / e^{-280.7} = 1.24×10⁻¹²² / Λ_CC = (35/3)·e^{-280.7} = 1.447×10⁻¹²¹ / N_e = (35/6)·ln(1+10⁶) = 80.59 / 5.29³ = 148.036 / g_TC 单圈(Λ_ν) = 0.210 / H₀t₀ 正面积分 = 0.9495。
