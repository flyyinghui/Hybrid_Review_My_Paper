# Theorem-Label vs Lean-Coverage Gap (覆盖度夸大检测)

**触发**：审稿时发现论文正文把某命题标为 "Theorem T1/T2/T3/T4"，但 Lean 只形式化了其中的**代数简化部分**（或完全未形式化）。

**核心判据**：区分「值漂移」（body-vs-lean value drift，正文说一个值、Lean 是另一个值）与「覆盖度夸大」（coverage overclaim，正文称 "Theorem" 但 Lean 只证了简化版代数恒等式）。后者不会触发 value-drift grep，因为数值/定义都一致，但「Theorem」标签暗示的形式化覆盖远超实际。

**V64 案例（5 代理交叉一致发现）**：

| 正文 "Theorem" | Lean 实际覆盖 | 缺口 |
|---|---|---|
| T1 Noether 流 J_χ^μ 协变守恒 | 仅 `conserved_of_zero_derivative`（ODE 版）| 协变 Noether 流、Lorentz 流形、Stokes 定理未形式化 |
| T2 正则共轭 {χ,P_χ}=1 | 仅 `phase_velocity_of_charge`（K⁰=0 分支）| 含 K⁰ 的完整 P_χ=a³(φ²χ̇+K⁰) 未形式化 |
| T3 局部时钟 | **完全无** | 无 Lorentz 几何/因果结构/timelike 梯度 |
| T4 唯一正径向极小 | 仅 `finite_energy_excludes_zero`（φ≠0 障碍）| 唯一正根 + W_q''>0 + 健康域未形式化 |

**检测方法**（lean_specialist + math_rigor 代理）：
1. 对正文每个 "Theorem T_N"，grep Lean 中对应定理名。
2. 判断 Lean 定理的**命题类型**是否与正文声称的物理内容同等级：`phase_velocity_of_charge : w = q/(bF)` 是代数反解，不含辛结构 {χ,P_χ}=1；`seesaw_rank_le_two_twoRHN : rank ≤ 2` 未推到 det=0 → 零特征值 → 至少一个零质量。
3. 若 Lean 定理的语义弱于正文声称，判 **P1 覆盖度夸大**。

**修复方向**（二选一，推荐 b 为主）：
- (a) 补 Lean 定理（T4 唯一正根、T2 含 K⁰ 完整版较易补；T1/T3 需 Lorentz 几何/因果结构，重）。
- (b) 正文明确标注 "Lean 仅覆盖 XX 代数部分，其余为纸面推导（C 级）" —— 这是诚实性修复，比硬补形式化更务实。

**与既有检测的关系**：不同于 `honestification-asymmetry-body-vs-lean.md`（值漂移）和 `paper-vs-lean-semantic-drift.md`（语义漂移）——本检测针对「Theorem 标签 vs 形式化覆盖范围」的等级落差，数值/定义完全一致时也会触发。
