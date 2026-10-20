# 多论文体系审查：版本对齐 + 编译状态一致性审计

适用于「同一母框架下的多篇论文」体系（如 SL(6,ℂ) 的 5 篇：CGICE / 三大时空相 / 右手中微子 / 三峰引力波 / 光速分界面）的交叉审查。审查某单篇论文时，不能只看它内部自洽，还要核对它与上游框架、与自身形式化产物的对齐。

## 检查点 1：编译状态标注一致性（P0 级硬伤）

**问题模式**：论文内不同位置对「Lean 形式化是否编译通过」的表述自相矛盾，且与地面真相冲突。

**案例（光速分界面 V2）**：
- L43（scope tag 定义）写 "this integrated revision **has not been compiled**"
- L1547（Data availability）写 "This integrated revision **compiles cleanly**… 0 errors, 0 sorry, 0 admit"
- L1619（Appendix A.3）写 "The integrated revision **compiles cleanly**…"
- 实际编译结果：0 error，SHA `2805f6cf`，黄金门控仅 `[propext, Classical.choice, Quot.sound]`

**根因**：早期草稿的「未编译」声明在后续编译通过后未同步更新，残留成自贬错误。

**审计方法**：
1. 全文 grep `compil` / `sorry` / `axiom` / `admit`，收集所有关于编译状态的表述。
2. 交叉对比各处的结论是否一致。
3. 与地面真相核对：`grep -cE "^theorem " *.lean`（定理数）、`grep -cE "sorry|admit" *.lean`（**注意区分注释里的词 vs 真占位符**——grep 命中 "0 sorry / 0 admit" 注释、或 "admit" 作普通英文「承认」时是假阳性，需看上下文）、`lake build` 的 exit code、`#print axioms` 结果。
4. 任何一处「未编译」声明与「编译通过」声明并存 = 必须修正为准确表述。

**教训**：审稿人逐字核对编译状态。论文自贬编译状态 = 主动让出最硬的形式化优势。这是「诚实化过度到自贬」的一个具体形态。

## 检查点 2：多论文体系版本对齐断裂

**问题模式**：单篇论文引用上游母框架的某个版本，但上游已演进到更新的版本，导致该论文的核心对象悬浮于上游框架之外。

**案例（光速分界面 V2）**：
- 全文引用 "unified framework **V2** [1,2]"
- 但上游统一框架已到 **V3**（新增 `SL6CUnified.SpacetimePhases` 三扇区 54 定理 + 矩阵行列式深化 5 定理 + 热力学选择补充）
- 关键：V3 的 `positiveFiberParent = (5,1)` 就是光速 V2 的核心对象 SU(1,5)（Hermitian signature $(1,5)$），但两文未建立等价声明 → 光速 V2 的原创创新（SU(1,5) 作为「第一个负方向出现的临界点」）与上游框架脱节

**审计方法**：
1. 列出该论文体系所有论文 + 各自的版本号。
2. 审查单篇论文时，grep 它引用的上游框架版本号，与上游当前最新版本比对。
3. 若版本落后，检查：上游新版本是否新增了与该论文核心对象直接相关的定义/定理（grep 上游 lean 的 namespace + 关键符号）。
4. 建议作者显式建立「本论文对象 X ↔ 上游框架对象 Y」的等价声明。

## 检查点 3：跨论文记号统一（附带）

同一对象在多篇论文中用不同记号时（如 Signature 记 $(n_+,n_-)=(5,1)$ vs $(n_-,n_+)=(1,5)$），建议显式建立统一映射公式并形式化。

**案例**：光速 V2 的序参量 $\Phi=n_-/6$（SU(6)=0 / SU(1,5)=1/6 / SU(3,3)=1/2）与 V3 的 `Signature = ℕ×ℕ` 可统一为 $\Phi = q/(p+q)$，可编码三条 `phi_su6/su15/su33` 定理（norm_num 即可）。

## 通用教训

多论文体系审查的「独有贡献」判定：当某篇论文有上游框架没有的定理族（如光速 V2 的因果锥定理 `six_causal_projects_four` / `conditional_matter_phase_and_threshold`），应显式标记为「相对母框架的净增量」，并在引言明确分工（「V3 管 phase / 本文管 cone」），否则易被审稿人判为重复劳动。
