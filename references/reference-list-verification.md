# 参考文献核验脚本模式（phantom/orphan/范围引用/数学区间误报）

来源：三大时空相 V18 第四轮复审（2026-09-19）。机器核验 + 5 代理独立复核交叉确认。

## 核验目标

投稿前必须核验：① 正文引用的每个 `[N]` 都在参考文献列表里（幻影引用 = P0）；② 列表每条都被正文引用（孤儿引用 = P2）；③ 编号连续无缺口。

## Python 脚本模式（stdlib-only）

```python
import re, io
text = io.open(paper_path, encoding='utf-8').read()
ref_marker = text.find('\nREFERENCES')
body = text[:ref_marker]            # 正文（REFERENCES 之前）
refs_section = text[ref_marker:]    # 参考文献列表

# 1. 列表条目编号
ref_listed = set(int(m.group(1)) for m in re.finditer(r'^\[(\d+)\]\s', refs_section, flags=re.M))

# 2. 正文引用：匹配 [N]、[N--M]、[N-M]、[N,M]，排除数学区间
cite_re = re.compile(r'\[(\d+)(?:\s*[-–—]{1,2}\s*(\d+))?(?:\s*,\s*(\d+))?\]')
cited = set()
for m in cite_re.finditer(body):
    # 排除数学区间：前面紧跟 ∈/∉/= 或数字（如 κ ∈ [10,100]）
    before = body[m.start()-1] if m.start() > 0 else ''
    if before in '∈∉=' or before.isdigit():
        continue  # 数学区间误报
    a = int(m.group(1)); cited.add(a)
    if m.group(2):                      # 范围 [N--M] 展开
        for i in range(a, int(m.group(2))+1): cited.add(i)
    if m.group(3):                      # [N, M] 第二个
        cited.add(int(m.group(3)))

phantom = sorted(cited - ref_listed)   # 幻影引用（正文引但列表无）
orphan  = sorted(ref_listed - cited)   # 孤儿引用（列表有但正文未引）
```

## 三个关键坑

1. **`[1--5]` 双横线范围引用**：正则 `[-–—]{1,2}` 必须允许**双横线**（`--`），否则 `[1--5]` 匹配失败 → [1]-[5] 被误判为"孤儿引用"（本案例首轮核验误报 5 个孤儿，修正正则后归零）。

2. **数学区间误报**：`κ ∈ [10,100]` 被朴素正则误解析为文献 [10] 和 [100]，产生幻影引用 [100]。排除规则：引用 `[` 前一个字符是 `∈`/`∉`/`=` 或数字 → 跳过（本案例唯一的"幻影 [100]"就是此误报）。

3. **范围引用覆盖孤儿判定**：`[1--5]` 展开后 [1][2][3][4][5] 都算"被引用"，不能只看单数字 `[N]`。

## 验证清单

- 幻影引用 = 0（P0 阻断级，投稿前必查）
- 孤儿引用 = 0（P2，`[1--5]` 范围引用覆盖后应为 0）
- 列表编号连续（`list(range(1, max+1)) == sorted(ref_listed)`）

## 复审集成

把机器核验结果（列表条数、phantom、orphan、连续性）作为独立字段注入 5 代理复审 prompt，要求每个 reviewer 独立复核（本次 5 代理均返回 `phantom=[] orphan=[] continuous=True`，与机器核验一致）。

## 内容层核验：AI/大脑召回的引用本身可能是幻觉

格式核验（phantom/orphan）只查"编号一致性"，**不查"文献真实性"**。二者互补，投稿前都必查。新增教训（光速分界面第三轮，2026-10-04）：神经网络大脑 `brain.recall()` 返回的概念可能携带**错误的 arXiv ID / 作者 / 标题**，是幻觉引用。

案例：大脑召回建议 `twistor SL(6,C) 齐性空间 arXiv:2407.09876`，web_search 验证后该 ID 实为 *"Detection of hidden emissions in two rotating radio…"*（astro-ph，完全无关）。修复：替换为确凿的标准文献——Dynkin 分支规则 → Slansky 1981 (Phys. Rep. **79**, 1–128)；实形式/Cartan 分类 → Knapp *Lie Groups Beyond an Introduction* 2nd ed. (2002)。

规则：**任何 AI 生成或记忆召回的文献线索（arXiv ID、DOI、作者名、期刊卷期）在用作参考文献前，必须 `web_search` 逐条验证真实性**，尤其是大脑召回补充的线索。发现 ID 与标题不符 → 立即替换，不把幻觉引用带进论文。这是"增补正确有效的参考文献"这个用户要求的硬门控：验证过才算"正确"。

