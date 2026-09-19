# Status Escalation — 把参数化假设重新标签为"第一性原理推导"的过度声称检测

## 缺陷类定义

**Status escalation（地位升级）**：作者/修改意见把同一个量从诚实的
"[PARAMETERIZATION hypothesis]" / "Ansatz" 重新标签为 "first-principles
derivation" / "rigorous theorem"，而底层推导链并未真正建立。这是"表演性诚实"
（performative honesty）的**镜像方向**——不是把标签藏在注释里，而是把假设升格为推导。
比可见的 `sorry` 更危险，因为授予虚假的验证信心。

**触发信号**：某量在 Table 1 标 "Derived (first-principles)"，但正文某处仍承认它是
"honest-axiom" / "premise" / "stated as an Ansatz"；或一轮"修改意见"要求把假设
"升级为推导"，升级理由只是"群论解码""热核展开"等听起来严格的词汇。

## CGICE V9.1 FRG 案例（2026-08-27，5 代理一致裁定）

修改意见要求把异常维度 η_k = 72/35 从 "[PARAMETERIZATION hypothesis]" 升级为
"First-Principles FRG Heat-Kernel Derivation"（Seeley-DeWitt 热核展开）。
5 代理中 technical + logic + consistency + bibliography 四个独立裁定为过度声称。

技术理由：
1. **a₁→η_k 投影是未证明的 Ansatz**。Seeley-DeWitt 系数 a₁ = E + (1/6)R_M 是标准
   热核结果（Vassilevich 2003 确有），但"a₁ 投影异常维度 η_k = −∂_k ln Z_k 到李代数
   不变量"这一步没有推导、没有方程、没有文献支持。
2. **公式在 FRG 文献中不存在**。η_k = C₂(adj)·h^∨/dim(M) 不在任何 FRG 文献中
   （含新引用的 Codello-Percacci 1207.4499、Dupuis 2006.04853、Codello 1505.03119）。
3. **异常维度是动态量**。标准 FRG 中 η_k 依赖耦合 + 调节子，不是纯群论常数。
4. **标量曲率公式错误**。R_M = C₂(adj)·h^∨/Tr(1) 量纲不一致（R 有长度⁻² 量纲，
   C₂·h^∨/dim 无量纲），非对称空间标准标量曲率公式。
5. **符号翻转未论证**。热核公式导出 |η_k| = 72/35（正），β_NP 却用 η_k = −72/35（负）。
   若 η_k > 0 则 β_NP 对 g > 0 恒正、无非平凡定点。负号是定点存在所必需，须显式论证。

诚实处理：保留热核展开作为**动机**（motivation），诚实标注 η_k = 72/35 为
**群论 Ansatz**（"MOTIVATED by, not derived from"），删除错误标量曲率公式，补负号论证。

## 检测清单（审查"推导升级"声明时逐条验证）

1. **文献存在性**：声称的公式是否真的在被引参考文献中？grep 被引论文，若公式不在
   其中 → 过度声称。
2. **推导链方程支撑**：每一步是否有方程，而非文字断言"X 投影到 Y"？
3. **量纲一致性**：等式两边量纲是否一致？
4. **符号约定**：|η_k| vs η_k 的绝对值/符号翻转是否有物理论证？

## 通用教训

**修改意见本身可能要求一个数学上不成立的"升级"。** Agent 不能机械执行修改意见——
必须先独立验证"推导"是否真实存在（尤其当升级理由只是"群论解码""热核展开"等听起来
严格的词汇时）。当审查裁定修改意见是过度声称，按用户一贯的"宁可诚实降级，不过度
声称"原则执行降级（保留动机、诚实标注 Ansatz），而非坚持升级标签。

关联：progressive-honesty-score-paradox（诚实化可能降分，但不是退步）；
`relabeled-axiom-recurrence-and-isolated-audit.md`（换名复发是降级/改名隐藏，本模式是
升格为推导，方向相反）。
