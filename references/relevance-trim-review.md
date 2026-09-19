# 逻辑自洽性 + 物理关联性复审（relevance-trim review）+ 删除/精简执行

2026-09-19 三大时空相 V18 第六轮复审验证的模式。当用户要求「检查前后论述逻辑自洽性与物理现象关联性，删除或精简不相关内容」时，用本 pattern。

## 5 代理角色设计（聚焦三维度，区别于常规 5 维终审）

| 代理 | 职责 | JSON 输出字段 |
|---|---|---|
| `consistency` | 前后论述逻辑自洽（摘要 vs 正文 vs 附录 vs Lean 计数）| `inconsistencies` |
| `relevance` | 物理现象关联性（识别与主线不相关的内容）| `irrelevant_content`（recommendation: delete/simplify/keep + reason）|
| `logic` | 三阶段/论证链因果连贯性（因果箭头是否明确标注 honest-axiom/条件定理/开放问题）| `inconsistencies` + `irrelevant_content` |
| `redundancy` | 冗余/重复检测（同一推导多章重复、历史版本残留、修订表）| `redundancy` |
| `cross_check` | 跨章节参数阈值一致性（η_k/g_TC/三谱对象/N_e/DM比/分支比/w₀ 全文统一 + superseded/withdrawn 标记完整性）| `inconsistencies` |

JSON 契约：`{"score", "inconsistencies":[{location,severity,description,fix}], "irrelevant_content":[{location,content,recommendation,reason}], "redundancy":[...], "summary"}`。

## 典型「不相关内容」信号（多代理会一致命中）

系列论文复审时，子论文混入其它层的旁支是最常见的不相关内容：
- **场论层(V63)/现象学层(GW) 内容混入几何层**：VEV 真空唯一性、Fisher 引力、时间荷↔ν_R 对偶、Cartan 紧化桥、三重峰 GW 谱数值——这些属 companion 论文范畴，与「三阶段动力学」主线无推导链。
- **内部修订日志**：REVISION 20260918/20260919/20260919_1 这类修订表是 process log 非科学内容，投稿前应删。
- **已 superseded/withdrawn 但正文仍完整保留**：如 Klartag needle（已标 SUPERSEDED 但正文 15 行还在）。

## 删除/精简执行（trim script 陷阱）

1. **从后往前删**（`del lines[start:end)`），end 索引多算一行会**误删下一个标题**。本次误删了 `# *IV. Three-Phase Emergence*`（删除范围 [661,679) 把 679 行的 §IV 标题也删了），需 patch 补回。**精确删除要确认 end 边界是「下一标题的上一行」而非「下一标题行」**。
2. **删附录后必须重编号 + 修悬空引用**：删了附录 C，原附录 D 要重编号为 C；正文里指向已删附录的引用（如 `Appendix C table`）要么改指向存活章节（→`§IV.C`），要么删，否则 P0 级悬空引用。
3. **删前备份**：`cp x.md x.md.bak_pre_trim`，删除是破坏性的。

## 与其它 review 模式的关系

- 常规 5 维终审（consistency/logic/technical/writing/bibliography）判「内部一致性」；本 pattern 判「物理关联性 + 精简」。
- 跨论文终审（CGICE 基准）判「方程遵循度」——三者是不同维度，评分不可直接比较（内部一致性 6.5 vs 跨论文遵循度 4.8 vs 关联性精简 5.0）。
