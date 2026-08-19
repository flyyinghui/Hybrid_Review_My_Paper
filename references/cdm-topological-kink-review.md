# CDM 暗物质拓扑缺陷论文 Hybrid Review 实录 (2026-07-07)

## 执行摘要

- 论文：Cold Dark Matter as Emergent Topological Kinks from SL(6,C) Geometric Crystallization
- 文件：DOCX (76段/3100词) + Lean proof (599行/16axiom行/8 `exact trivial`)
- 5 代理部署：consistency + logic + technical + writing + bibliography
- 总发现：**14 CRITICAL** + **18 IMPORTANT** + **10 MINOR**

## 五维评分

| 维度 | 评分 | 关键致命发现 |
|:--|:--:|------|
| Consistency | 3/10 | 公理命名分裂为两套体系 / 字符数虚报 +4474 / `{total_concepts}` 模板未填充 |
| Logic | 2/10 | Rank=90 矩阵维度 70（不可能）/ 5:1 公理化非导出 / 5 引理全 admit |
| Technical | 2/10 | KLS 误用于模空间 / Riccati 方程符号错误 / SL(6,C)/SU(3,3) 维数 35 非 70 |
| Writing | 6/10 | 自夸泛滥（"complete"×5/"first-principles"×2）/ 摘要 300+词需压缩 |
| Bibliography | 3/10 | [9] Eldan-Chen 论文作者错误 / 13+ 幻影引用缺失 / 理论基础完全依赖未审自引 |
| **综合** | **3.2/10** | — |

## 6 大 CRITICAL 发现

1. **Rank 90 > 矩阵维度 70**：`rank A_final = 90` 但矩阵是 70×70，17 处引用此矛盾
2. **5:1 比率被公理化**：A5 硬编码 `darkDegrees=75 ∧ visibleDegrees=15`，T3 仅提取此值
3. **Lean 证明是空壳**：8 公理全 `exact trivial`，5 引理全 `admit`，31 未定义标识符
4. **OllamaLens TEXTUAL_COOCCURRENCE 是范畴错误**：LLM 共现≠数学验证
5. **参考文献 [9] 事实错误**：标注为 Eldan & Chen (2021)，实际是 Yuansi Chen 独作
6. **KLS 不等式误用于无穷维模空间**

## 投稿建议

论文提出了有趣的猜想但**不是证明**——是 Lean 语法包裹的猜想草图。
推荐路径 A：移除全部 "proof" 声称 → 定位为 "formalized conjecture" → 投 *Physics Letters B*。

## 代理部署模式

```python
delegate_task(tasks=[
    {"goal": "consistency-checker: ...", "toolsets": ["terminal","file"]},
    {"goal": "logic-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "technical-reviewer: ...", "toolsets": ["terminal","file"]},
])  # Batch 1: 3 agents (结构 + 逻辑 + 数学)
delegate_task(tasks=[
    {"goal": "writing-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "bibliography-auditor: ...", "toolsets": ["terminal","file"]},
])  # Batch 2: 2 agents (写作 + 文献)
```

## 与之前审阅的比较

CDM 论文比中微子凝聚 V38（评分 3.8/10）更差——CDM 不仅有空壳证明问题，
还有**数学不可能性**（rank 90 > 70）和**引用错误**（[9] 作者张冠李戴）。

两项共同模式：
- 论文声称 "完整的正式证明" 但 Lean 文件中全用 `:= True` 存根
- 神经网络组件（大脑搜索/OllamaLens/文本共现）被误归为数学验证
- 核心数字（75/15 或 Σm 值）被编码为公理而非导出
- 参考文献列表被系统性损坏（幽灵引用 + 幻影引用 + 错误引用编号）
