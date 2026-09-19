# 审稿误报甄别：Unicode 清单缺陷 + 点积符号错误（CGICE V10 终审实录）

2026-09-15 CGICE V10 5-agent Hybrid review 终审。5 个审稿代理报了 3 个
"P0/P1" 问题，独立核验后**全部是误报**。根源有两类，都值得在转达审查发现前先自查。

## 误报类型 1：审计脚本自身的正则缺陷传导给审稿代理

**症状**：consistency 代理报 "P0：论文声称 138 theorems + 3 lemmas = 141，但 Lean 清单显示 140"；
bibliography/consistency 代理报 "P1：论文写 `gaussianKL_instantaneous_grönwall`，但 Lean 清单是
`gaussianKL_instantaneous_gr`"。

**根因**：喂给审稿代理的"Lean 地面真相清单"是用临时提取脚本生成的，正则用了
`[A-Za-z0-9_]` 匹配标识符。Lean **允许 Unicode 标识符**（`ξ`、`ö`、`γ`、`⊥` 等），
`[A-Za-z0-9_]` 遇到这些字符就截断：
- `sum_ξ_indicator_s` / `sum_ξ_indicator_t` → 都截断成 `sum_`（去重后 141 → 140，产生假计数差）
- `gaussianKL_instantaneous_grönwall` → 截断成 `gaussianKL_instantaneous_gr`（产生假命名不一致）

**判据**：给审稿代理喂"地面真相清单"前，先验证清单本身的正确性。
Lean 标识符提取正则必须支持 Unicode（用 `\w` 在 Python3 re 默认只匹配 ASCII，需
`re.UNICODE` 或显式用宽字符类），或者直接 grep 原文件逐行核对每个"不一致"的标识符。

**修复动作**：grep 原文件 `grep -n "gaussianKL_instantaneous" proof.lean` 确认真实名称；
grep 重名 `grep -oE '^(theorem|lemma) \w+' | uniq -d` 确认是否有真重名。

## 误报类型 2：审稿代理的符号推导错误（点积对称性）

**症状**：technical 代理报 "P1：§6.2 连续 master identity 的符号 `dF/dt + Ψ_p(j) + Ψ_p*(-∇ξ) = 0`
与标准推导相反，应为减号"。

**审稿代理的错误**：推导中写了 `∫ ∇ξ·j = -∫ j·∇ξ`，进而推出符号相反的结论。
但点积是对称的：`∇ξ·j = j·∇ξ`，所以这一步错号。

**独立核验的正确推导**（`j = -p∇ξ` 时）：
- `dF/dt = ∫ ξ ∂_t p = -∫ ξ div j = ∫ ∇ξ·j = -∫ p|∇ξ|²`
- `Ψ_p(j) = ½∫|j|²/p = ½∫ p|∇ξ|²`，`Ψ_p*(-∇ξ) = ½∫ p|∇ξ|²`
- 故 `dF/dt + Ψ_p(j) + Ψ_p*(-∇ξ) = -∫p|∇ξ|² + ½∫p|∇ξ|² + ½∫p|∇ξ|² = 0` ✓

论文符号正确，Lean `flux_force_master` 符号也正确（`freeEnergyRate + fluxPower + forcePower = 0`）。

**判据**：审稿代理报告的"符号/代数错误"，先亲自重算一遍（尤其内积、分部积分、共轭的符号），
不要盲信代理的中间推导。这与规则组 E（Reviewer Arithmetic False-Positive Verification）同源：
审稿人自己会犯约定/对称性错误。

## 通用流程（转达审查发现前必做）

1. 对每个 P0/P1 的"数值/计数/命名/符号" finding，独立核验：
   - 计数：grep 原文件重新计数，别依赖提取脚本的去重结果。
   - 命名：grep 原文件确认真实标识符（Unicode 截断是高发）。
   - 符号/代数：Python/SymPy 或手算重推一遍。
2. 只有独立核验确认的 P0 才转达为阻断级；误报单独归类并标注"审稿误报，无需修复"。
3. 审计脚本的正则缺陷要修脚本本身，而不是让论文迁就错误的清单。
