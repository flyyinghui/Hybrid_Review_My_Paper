# Bibliography 核对执行工作流（引用 ↔ 参考文献交叉核对 + 补充）

**触发场景**：核对论文参考文献、补充缺失引用、确保所有引用在正文标注。

**实战案例**：CGICE v10 论文（2026-09-11）核对发现 10 条参考文献仅 3 条在正文标注（7 条孤儿），且正文提到 Perelman / Coleman-Weinberg 人名但列表缺失。最终 12 条全部标注。

## 三类引用缺陷（比"幻影引用"更完整的分类）

| 缺陷类型 | 定义 | 检测 | 严重度 |
|---|---|---|---|
| **幻影引用** | 正文引用 [N] 但参考文献列表无 N | `正文引用编号 − 列表编号` | 高（审稿一票否决） |
| **孤儿引用** | 列表有 N 但正文从未标注 [N] | `列表编号 − 正文引用编号` | 中（最常见！CGICE 10 条里 7 条孤儿） |
| **缺失文献** | 正文提到人名/概念但列表完全没有该文献 | 搜正文人名，比对列表作者 | 高（Perelman / Coleman-Weinberg 案例） |

**经验**：孤儿引用远比幻影引用常见——论文写作时列了参考文献但忘记在正文标注。

## 三步工作流

### Step 1: Python 正则提取 + 交叉核对

```python
import re
lines = open(path, encoding="utf-8").read().splitlines()
# 找 ## References 起始
ref_start = next(i for i, ln in enumerate(lines) if re.match(r'^##\s*References', ln))
# 参考文献编号
refs = [int(m.group(1)) for ln in lines[ref_start+1:] if (m := re.match(r'^(\d+)\.\s', ln.strip()))]
# 正文引用编号（仅统计参考文献之前的部分）
body = "\n".join(lines[:ref_start])
cited = set(int(m.group(1)) for m in re.finditer(r'\[(\d+)\]', body))
# 交叉核对
ghost = cited - set(refs)   # 幻影：正文引用但列表缺失
orphan = set(refs) - cited  # 孤儿：列表有但正文未标注
```

**陷阱**：LaTeX 数学公式里的方括号（如 `\right]`、`[e_1,[e_1,e_2]]`）会被 `\[(\d+)\]` 误匹配。用 `re.finditer(r'\[(\d+)\]', body)` 后需人工核对上下文，或先 strip 数学块。

### Step 2: 补充孤儿引用标注（精确字符串替换）

对每条孤儿引用，在正文找到**概念首次出现处**插入 `[N]`：
- 用 Python 直接读文件 + `str.replace(old, new)`，不用 patch 的模糊匹配（LaTeX 转义 `\\(\beta\\)` 需精确匹配）
- 先 `repr(line)` 看精确文本（避免 `\\` 转义歧义），再替换

**CGICE 案例的标注位置映射**（Witten Laplacian 等概念首次出现处）：
- [2] Witten → §2.3 "Its 0-form Witten operator is" → "…operator [2] is"
- [3] Bakry-Gentil-Ledoux → §2.3 加权 Laplacian "For β>0, consider" → "…consider [3]"
- [5] Vassilevich → §7.3 热核展开 "For a Laplace-type operator" → "…operator [5]"
- [7][8][9] FRG 三文献 → §7.3 beta 函数/固定点/有效作用量处

### Step 3: 补充缺失文献（正文提到人名但列表没有）

搜正文关键人名（Perelman/Witten/Bakry/Coleman/Weinberg/Kantorovich/…），比对列表作者，找出缺失：
- 大脑 `brain.recall()` 概念桥接**确认文献方向**（recall "Perelman entropy Ricci flow"、"Coleman Weinberg effective potential" 等，命中概念即确认该文献必须补充）
- 补充经典文献书目（如 Coleman-Weinberg Phys. Rev. D 7, 1888 (1973)、Perelman arXiv:math/0211159 (2002)）

### Step 4: 验证

重跑 Step 1 的交叉核对，确认：幻影=空、孤儿=空、正文引用编号 == 列表编号。

## 大脑桥接的作用

`brain.recall()` 用于**确认文献方向的正确性**（不是提供完整书目——大脑存的是概念，不是书目）。CGICE 案例：6 组 recall（witten_laplacian / bakry_emery / heat_kernel / perelman_entropy / coleman_weinberg / nonlinear_sigma_frg）全部命中正确概念，确认了 7 条现有文献方向 + 2 条缺失文献方向。

**正确用法**：`NeuralMemoryBrain()` 构造即自动 `graph.load()`（无独立 `load()` 方法）；`brain.recall(query, top_k=5)` 返回 dict 列表，用 `r.get("content","")`。
