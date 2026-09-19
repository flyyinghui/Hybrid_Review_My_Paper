# 参数化伪装成动力学闭合 (Parameterization Disguised as Dynamical Closure)

## Trigger

论文引入**分支比 / 耦合常数 / 占比 / 质量分数**等参数来「闭合」一个数值矛盾（如 0.46% vs 8.59% 的 18.7× 矛盾），并把结果叙述为「协变质量转移动力学」「dynamical mechanism」「covariant mass-transfer dynamic」等动力学语言。

## 反向工程签名（命中任一即判 [P] 唯象参数，非推导）

1. **参数定义式把观测值写进分子**：`f_DE = Ω_DE_obs / ((47/547)·148.036)` — 待解释的观测值本身出现在参数定义里，反解出参数后再声称参数「预测」了该观测值。
2. **Lean 定理只证存在性**：`∃ f_DE, Ω_DE(f_DE) = 0.682` 平凡成立——任何目标值都能靠调节一个自由参数达到；定理不证**唯一性**、不证**动力学来源**。
3. **叙述层把「存在吸收观测值的参数」升级为「动力学机制」**：`This shifts the mechanism from a numerical coincidence to a covariant mass-transfer dynamic`。

判别核心：**代数真证 ≠ 物理闭合**。`norm_num/field_simp` 能干净地证「∃ 参数使等式成立」（0 sorry），但这不构成物理闭合——真正的闭合需要从上游动力学（分支物理/粒子谱/Γ_b/Γ_trans）**导出**参数，而非反解。

## 诚实化修复（三步，全在叙述层，不改 Lean 证明）

1. 参数标 `[P]` 并在 K/C/A/P/O 分级表登记；明确「fixed BY 观测值，reverse-engineered」。
2. 措辞降级：`RESOLVED` → `PARAMETERIZED (not dynamically resolved)`；`simultaneously closes` → `EXISTENCE-level phenomenological branching ratio`。
3. 区分「代数存在性」与「动力学闭合」：动力学导出标 `[O]`；补一句 `removes the 18.7× arithmetic tension but does not by itself constitute a dynamical mass-transfer mechanism`。

## 案例：三大时空相 V18 第四→第五轮（2026-09-19）

| 轮次 | 评分 | 关键动作 | 结果 |
|------|:--:|------|------|
| 第四轮 | 6.5 | 用「INDEPENDENT 单红移基准不得混同」**诚实降级** P0-3 | 5 代理一致 6.5 |
| 第五轮 | 6.20 | 引入分支比 f_DE 主动「闭合」矛盾 | phase3 给 5.0，均值 6.20 |

- 四代理（phase2/phase3/phenom/math）**一致**判 f_DE 反向工程。
- 代数真证无争议：`resolved_transmutation_fraction_existence` 的 norm_num/field_simp 证明干净（0 sorry），审稿人认可代数正确性。
- 问题**全在叙述层**：把「存在一个能吸收观测值的自由参数」说成「动力学机制」。
- **诚实降级悖论再印证**：诚实标注（标 [P]、标 [O]）比「假装闭合」（叙述成动力学）得分更高。第四轮的诚实降级拿 6.5，第五轮的虚假闭合掉到 6.20。

## 关键教训

- 动力学/现象学审稿人（phase3 类）对「引入新自由参数 + 叙述成动力学」最敏感——这类改动**预期被降分**，除非同时给出参数的动力学导出，或明确标 [O]。
- 任何「为闭合数值矛盾而引入的参数」，默认先按反向工程审查：检查参数定义式里是否含观测值本身。
- 诚实化修复是**纯文本**操作（改叙述 + 登记分级表 + 标 [P]/[O]），不触碰 Lean 证明——因为代数真证本身是对的，错的只是叙述。
