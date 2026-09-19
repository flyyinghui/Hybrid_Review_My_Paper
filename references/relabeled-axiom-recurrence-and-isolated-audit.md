# 换名复发检测 + 孤立假公理引用计数审计

来源：CGICE V9.1 第三轮终审（2026-08-20）。前一轮已"修复"的零内容公理在新一轮以更
响亮的名字复发，且一条可证 False 的假公理仅做头注释标记未改代码。补充
`false-proposition-axiom-detection.md` 与 `lean-false-axiom-patterns.md` 未覆盖的三条检测模式。

## 1. 换名复发（relabeled recurrence）

**症状**：上一轮终审发现并"删除"了零内容公理（如 a23 = 1×1=1、a24 = 1=1），
但新一轮文件里出现了**新的**零内容公理，只是换了个深刻的名字。

**CGICE 实例**：
- 上轮删除：`a23_bochner_horizontal_laplacian : (1:ℝ)*(1:ℝ) = (1:ℝ)`、`a24 : (1:ℝ)=(1:ℝ)`
- 本轮复发：`a_t3_harish_chandra_lower_bound : (35:ℝ) ≤ 35`、`a_t4_semiclassical_discrete_spectrum : (0:ℝ) ≤ 1`、`a_t5_eyring_kramers_first_excitation : (1:ℝ) = 1`

三条的**实际内容**是平凡算术恒等式（35≤35、0≤1、1=1），但名字声称承载
"Harish-Chandra 谱下界 / Witten 半经典离散谱 / Eyring-Kramers 首激发"的物理内容。
Lean 形式化层没有承载论文声称的任何物理内容——这是"表演性诚实"的变体。

**检测规则**：当上一轮报告说"已删除零内容公理 aX/aY"时，本轮复审**必须**对新的
axiom 清单逐条检查：是否存在 `(x:ℝ) ≤ x`、`(0:ℝ) ≤ 1`、`(1:ℝ) = 1`、`x = x` 这类
平凡恒等式，却套着深刻的物理/数学名称。用 grep 提取全部 axiom 声明并目检右侧内容。

## 2. 孤立假公理引用计数审计

**问题**：一条可证 False 的假公理（如 `spec_gap_bound : ∀ grad_sq lapV, 0 ≤ grad_sq - lapV`，
取 0,1 得 0≤−1=False）若**不被任何定理/引理引用**，则它不会在 Lean 里实际"爆炸"——
但躺在"0 sorry、全验证"的文件里仍是致命瑕疵（审稿人 grep 到即可否定整个形式化工作）。

**审计脚本（stdlib-only）**：
```python
import re
lean = open('proof.lean', encoding='utf-8', errors='replace').read()
for name in ['spec_gap_bound', 'a_t3_harish_chandra_lower_bound', ...]:
    decl = len(re.findall(rf'^axiom\s+{name}\b', lean, re.M))
    refs = len(re.findall(rf'\b{name}\b', lean))
    print(f"{name}: 声明{decl} 总出现{refs} 引用{refs-decl}")
```
引用计数 = 0 的 axiom 是**孤立公理**：要么是假公理（无害但不诚实），要么是零内容公理
（凑数）。两者都应从 axiom 清单中剔除，或降级为注释"研究级前提，Mathlib 未形式化"。

## 3. "≈ 偷换成 =" 的 paper↔Lean 分裂

**症状**：论文正文正确写 "≈"（如 N_e ≈ 80.6、Ω_DE ≈ 0.682），但 Lean 里把 "≈" 硬写成
"=" 且带截断小数：
```lean
axiom N_e_liouville_value : N_e_liouville = 80.59        -- 实际 80.590484
axiom bh_transmutation_produces_Omega_DE : ... = 0.680965  -- 实际 0.6809650894
```
**检测**：对每一条数值断言 axiom，用 Python 精确重算右侧表达式（math.exp/math.log/
sympy 展开），与声称值做严格相等比较。量级对但精确值错 = 假实数等式公理，必须删除
（引用 0 次时）或改区间断言 `|x - 80.59| < 0.001`。

## 4. 头注释 "FIX" + 代码未动（表演性修复的极端形态）

上一轮标记 P0 的公理，本轮文件仅在其上方加了一行 `-- [P1-2 FIX] ...` 注释，
axiom 内容**一字未改**。这是 `cgice-v9-r2-header-only-fix-pattern.md` 的极端形态：
连"部分修复"都没有，纯粹是注释声称。**复审必须 diff 上一轮的 P0 清单逐条对照当前
axiom 实际内容**，不能因为出现了 "[FIX]" 字样就默认已修复。

## 5. 一句话可复用结论

"zero sorry" 的证明若其 axiom 清单里混入（a）可证 False 的假命题公理、（b）平凡恒等式
套深刻名字的零内容公理、（c）"≈ 写成 ="的假实数等式公理，则比可见的 sorry 更危险——
假公理伪装成已验证。终审必须对 axiom 清单做三类审计 + 引用计数，而非只看 sorry 计数。
