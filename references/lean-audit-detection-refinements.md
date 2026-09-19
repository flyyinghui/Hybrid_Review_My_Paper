# Lean 证明审计 — 三项检测精化

来源：CGICE V9 FOP 论文 + Lean 终审（2026-08-23）。补充 SKILL.md Pitfall 4 与 `references/lean-false-axiom-patterns.md`。

## 1. 块注释/docstring 导致的 sorry 假阳性

**症状**：`grep -v '^--' | grep -c 'sorry'` 返回 2，但实际 active sorry = 0。
**根因**：`/- ... -/` 块注释跨多行；`/--` docstring 以 `/` 开头（非 `--`），naive 的 `grep -v '/-'` 只删掉含 `/-` 的那一行，块内部的 "Removed previous sorry"、"/-- ... (0 sorry) ..." 等字眼仍被计入。

**正确计数（排除所有注释形式）**：

```python
import re
lean = open(f, encoding='utf-8').read()
lean = re.sub(r'/-.*?-/', '', lean, flags=re.DOTALL)   # ① 先剥块注释 + /-- docstring
lines = [l for l in lean.splitlines() if not l.strip().startswith('--')]  # ② 再剥行注释
code = '\n'.join(lines)
for kw in ['axiom','theorem','lemma','sorry','admit']:
    print(kw, len(re.findall(r'\b'+kw+r'\b', code)))
```

**铁律**：任何非零 sorry/admit/`:= True`/`by trivial` 计数，必须先 `grep -n` 看行上下文，确认是 active 代码还是注释字眼，再报 P0。

## 2. def-baked 重言式公理（零内容公理的新机制）

**症状**：`noncomputable def lam1 : ℝ := 35/3` 之后紧跟 `axiom a4 : lam1 = 35/3`。
**根因**：值已烘烤进 def，公理退化为 `lam1 = lam1`（rfl 可证），零内容——与 `1×1=1` 命名成定理同一病类，但机制不同。

**实例（CGICE V9）**：
- `def lam1 := 35/3` + `axiom a4_kls_spectral_gap : lam1 = 35/3` → 重言式
- `def rho_sq_doubled := 2*(35/2)`(=35) + `axiom a_t3 : 35 = rho_sq_doubled` → 35=35
- `axiom spec_gap_bound : Prop`（自由 Prop 常量）+ `axiom a_t4 : spec_gap_bound` → 空断言
- `axiom a_t5 : lam1 = 35/3` 与 a4 逐字重复 → 重复重言式

**检测规则**：对每条 `axiom A : X = c`（或 `X = Y`），grep 检查 X 是否已 `def`/`noncomputable def` 且值恰为 c。若是 → 零内容公理。修复方向：删除，或改为真实前提语句（如 `Prop` 形式的 `σ_ess ⊂ [|ρ|², ∞)`、`Witten 束缚 ⇒ 离散谱`），即便以未证前提声明也比 "35=35" 诚实。

## 3. 公理计数膨胀（占位状态变量稀释）

**症状**：论文声称 "73 axioms"，但逐条分类后真正有物理内容的公设仅 ~26 条。
**根因**：占位状态变量声明（`axiom V_eff : ℝ → ℝ`、`axiom J_top : ℕ → ℝ → ℝ` —— 只声明函数存在性，非物理假设）与数值断言公理（`axiom H0_analytic_derivation : H0 = 67.42`）被计入公理总数。

**检测规则**：审计 "N axioms" 时逐条分四类并报告占比：
1. 占位函数/常量声明（零内容）
2. 重言式/自由 Prop（零内容）
3. 数值断言公理（可直接 `norm_num` 或应降级为 `def`）
4. 真实物理公设

若 (1)+(2)+(3) > 60%，"N 公理体系" 的表述严重注水——应要求论文报告「真实内容公理数」而非裸的 `axiom` 关键字计数。
