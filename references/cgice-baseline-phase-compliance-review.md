# CGICE-Baseline Phase-Compliance Review（跨论文动力学遵循度审查）

以母框架动力方程（CGICE 几何-信息动力方程 CGICE-1/2/3/4）审查子论文（三大时空相 V18 三阶段）的动力学机制是否「遵循」母框架方程。2026-09-19 验证。

## 核心区分：语言借用 vs 方程遵循

这是跨论文审查的关键维度，比「内部一致性」更严：

| 判定 | 含义 |
|---|---|
| **follows** | 子论文的因果箭头是母框架方程的直接推论（方程级推导）|
| **partial** | 部分直接应用（如正确引用 KL 耗散排除平衡时间晶体），但核心箭头未由方程推出 |
| **language_only** | 只借用符号/语言（Langevin/OT/KL），无方程级映射，因果链是 honest-axiom/postulate/[P] 校准 |

**关键区分**：`内部一致性评分`（公理/定理/参数自洽 + 0 sorry，V18 得 6.5）与 `跨论文动力学遵循度评分`（三阶段是否真正由 CGICE 方程驱动，V18 得 4.8）是两个正交维度。后者标准更严，通常更低。

## 判定矩阵（V18 案例，5 代理一致度）

| 阶段 | 判定 | 一致度 |
|---|---|---|
| Phase I（localization→inflation）| partial / language_only | 2:3 |
| **Phase II（OT→time→CDM）** | **language_only** | **5/5 一致** |
| Phase III（KL→DE）| partial | 4:1 |

Phase II 是 pure language borrowing：OT 输运射线→宏观时间的因果链与 CGICE-3 Casimir 守恒之间**无任何方程级映射**（Monge L¹ 成本 ≠ Brenier-McCann 平方成本；transport ray = time 是 postulate 非定理）。

## 「语言借用」的标志性措辞（红旗）

1. **「closed dynamical system replacing ΛCDM」** —— 子论文声称四方程闭合，但同一段自己承认 `CGICE_System` 只是 function/parameter 字段记录、无约束强制四方程成立。这与母框架 §4.5「方程不闭合宇宙学反馈回路」自相矛盾。
2. **「geometric origin of dark energy」** —— 把匹配输入（λ_⊥=35/3 是 3D 均分 honest-axiom A-DIM3）包装成谱几何推导。
3. **诚实标注与过强措辞并存** —— K/C/A/P/O 标注系统本身是对的，但个别「closed」「origin」措辞与诚实标注矛盾，正是审查要抓的。

## 执行配方

1. **前置加载母框架机制清单**（already-resolved mechanism list）：三谱对象区分（λ_∥=35 / λ₁≥29 / λ_⊥=35/3）、η_k=36/35（Hermitian 约定 C_A=h^∨=6）、g_TC 双值（D1 耦合 2.60 vs FRG 定点 1.8395）。否则会把框架内已解决的角色分工误判为 P0 矛盾。
2. **提取基准方程**：CGICE-1 (4.1) Langevin / CGICE-2 (4.3) Lyapunov / CGICE-3 (4.9) Casimir / CGICE-4 (4.10) KL 耗散 + §4.5 边界声明「不闭合宇宙学反馈回路」。
3. **提取子论文三阶段**（IV.A/B/C 各阶段的支配方程 + 因果箭头 + 诚实标注）。
4. **5 代理串行 deepseek-flash**（thinking=disabled, temperature=0），每个代理输出 `cgice_compliance: {phase1/phase2/phase3: follows|partial|language_only}`。
5. **聚合判定** + 区分「语言借用 vs 方程遵循」的 findings。

## 关键结论（可复用于 SL(6,C) 系列后续审查）

- 母框架（CGICE v10）是「0 公理 + 全实证明定理 + 显式边界声明」的范式——这是子论文该学的标准。
- 子论文（V18）大量借用了 CGICE 语言，但三阶段因果箭头（localization→inflation、OT→time、KL→DE）无一是 CGICE 方程的直接推论。
- 修复方向：①建立 CGICE 方程 ↔ 三阶段的显式映射表（把隐性「语言借用」转为可审计的「条件定理桥接」）；②删「closed dynamical system」措辞 → 改「conditional benchmark」；③Phase II 方程化 or 显式降级 honest-axiom；④修正 T_mix 谱隙（用 λ₁ 非 λ_∥）。
