# 投稿适配性终审（venue-fit review）：publication-strategist 代理 + 期刊格式合规清单

触发：用户问「适不适合投 X 期刊」（如「评估是否适合投稿 Foundations of Physics」）。此时 5 代理配置从默认的 consistency/logic/technical/writing/bibliography 换为 **consistency + technical + logic + lean_specialist + publication-strategist**——最后一个是专门的投稿适配性维度，不是普通写作审稿。

## publication-strategist 代理的两层判断

### A. 期刊格式合规（机械性，投稿前必须）

针对 Springer Foundations of Physics（及同类 Springer 期刊）作者指南：

| 检查项 | 要求 | 常见违规 |
|---|---|---|
| 摘要词数 | 150-250 词 | 摘要后紧跟 Keywords/约定表被排版系统误并入摘要 → 用 `\begin{abstract}` 显式界定 |
| 关键词数 | 4-6 个 | 9 个超限 |
| 章节层级 | 最多三级十进制 | `III.D′`/`III.F′` 带撇号变体是非标准层级，触发编译警告 |
| 源文件 | 必须 .tex + 编译 PDF | 只交 Markdown 直接退回（含 Pandoc 标记 `[§III.B]{.mark}` 非 LaTeX） |
| AI 辅助披露 | Springer 2023 起强制 | 无 Acknowledgments/独立声明段 |
| noncomputable def | 说明物理意义 | 36 个 noncomputable 定义未说明是否可数值计算 |

### B. 科学门槛（决定 READY/NOT READY）

- **至少一个真实动力学工作包**（从方程到物理观测量的完整链条），非 `opaque Prop` 命题包装。
- **诚实公理容忍度**：Foundations of Physics 对 honest-axiom 方法容忍度最高（比 PRD/PRL 更适合「条件模型 + 诚实标注」定位），但**仍要求明确的物理内容**——净预测度≈0 + 三峰撤回 + w₀ 撤回后，核心价值只剩「把观测量组织到单一几何原理下」，这在 FoP 可发表的前提是补齐真实动力学链条。
- 判定输出三级：READY / MAJOR REVISION / NOT READY，MAJOR REVISION 要给**最低验收项清单**（分机械修复 / P0 修复 / 物理内容提升三组）。

## 评分分裂：诚实性 vs 技术严谨性

本次 V18 终审的关键元观察——**诚实化只落在正文文字层，没传导到 Lean 代码层**：

- 诚实性 7.5/10（预测度≈0、三峰撤回、λ_⊥=35/3 标注独立输入、PhaseCgiceBridge「语言借用」诚实披露——都做到了）
- 技术严谨性 3.5-4.5/10（正文已写 `e^{−2ℓt}` 但 Lean 仍 `exp(-ℓt)`；正文已承认 5.47 是观测输入但 Lean 公理仍当谱定理）

诊断信号：**正文诚实标注与 Lean 代码语义脱节** = 「诚实化未双向落地」。不是过度声称问题（那已解决），而是诚实标注没同步到形式化代码。修复方向是让每个诚实标注对应的 Lean 声明同步降级（axiom→def、删伪谱定理公理、注释补反例）。

## 三个「编译通过但数学错误」的硬错误类型（V18 实例）

1. **因子 2 算术错**：`ouCov` 指数 `-ell*t` 应为 `-2*ell*t`，正文已写正确但 Lean 定义未同步。残差 ℓ(C−D/ℓ)≠0，反例 ℓ=D=1,C₀=2,t=0 导数 −1 vs 要求 −2。
2. **比例写反**：metzler 稳态向量 [v,u]（B=v,D=u），DM/重子比 = D/B = u/v，注释写 v/u。
3. **观测输入伪装谱定理**：`perron_frobenius_dominant_eigen` 公理断言保守 Metzler 生成元（列和为零）主特征值=5.47，但谱界为 0。修复=删公理 + `def targetRatio := 547/100`（诚实观测常量）。

共性：三者都编译通过、0 sorry，但数学/语义错误。印证「0 sorry 是源码卫生条件，不能替代命题语义审查」。修复后声明计数同步（116→114 axiom、174→173 thm、73→71 opaque、125→126 def）必须回写论文附录 A 统计段。

## 执行方式（复用既有协议）

5 代理串行直调 `deepseek-flash`（thinking=disabled，`max_tokens=8192, temperature=0.0, timeout=600`），**不用 delegate_task**（子代理继承主 model 会 v4-pro 挂死）。对抗性上下文注入完整 P0/P1 清单（来自前轮审稿报告），要求逐条判 fixed/remain/partial。每个代理输出立即写 `/tmp/<name>.part`。机器级 Lean 统计（剥离嵌套块注释后行首锚定计数）作为地面真相先于 LLM 审稿。完整执行配方见 `references/rereview-adversarial-defect-list-execution.md`。
