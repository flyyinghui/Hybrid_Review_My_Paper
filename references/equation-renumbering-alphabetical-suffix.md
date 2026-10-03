# Equation Renumbering: Alphabetical-Suffix → Continuous (V64, 2026-09-26)

## When this fires

审稿意见整合在 §X 主体**之后**插入新子节（§3.1 / §4.1 / §5.1），新子节的公式用了
「父公式后缀」编号（`9a/9b/9c`、`12a/12b/12c`、`15a`、`19a/19b`、`21a/21b/21c`），
导致编号与文档出现位置乱序：

- `9a/9b/9c`（§3.1）出现在 `10/11`（§3 主体）**之后**；
- `12a/12b/12c`（§4.1）出现在 `13` **之后**。

读者按编号交叉引用时会撞到不连续。审稿人（consistency 代理）会把这类乱序报为 P1/P2。

## 审计

```bash
grep -n '\\tag' paper.md   # 按行序提取所有公式编号
```
检查：序列是否连续？有无字母后缀夹在连续编号之间？正文引用是否指向正确编号？

## 修复：按出现顺序完全连续重编号（去掉所有字母后缀）

1. 建立 `旧编号 → 新编号` 映射（按 `\tag` 出现顺序）。
2. 用 `re.sub` 回调替换所有 `\tag{X}`：

```python
tag_map = {'9a':'12','9b':'13','9c':'14','12':'15','13':'16','12a':'17',
           '12b':'18','12c':'19','14':'20','15':'21','15a':'22','16':'23',
           '17':'24','18':'25','19':'26','19a':'27','19b':'28', ...}
content = re.sub(r'\\tag\{([^}]+)\}',
                 lambda m: '\\tag{' + tag_map.get(m.group(1), m.group(1)) + '}', content)
```

3. 正文引用用**精确字符串替换（带上下文）**逐处替换，不要全局正则。

## 关键陷阱：正文引用禁用全局正则 `\((\d+[a-c]?)\)`

它会误伤四类非公式圆括号数字：

| 类别 | 例子 | 后果 |
|---|---|---|
| 群符号 | SL(6), SU(6), U(1), SU(3), SU(2) | 数字被当成公式编号改掉 |
| 参考文献年份 | (1973), (2010), (2019), (2023) | 四位数年份被误改 |
| 函数值 | P(0)<0, Q(0) | (0) 被误匹配 |
| 数值中间量 | 单独出现的 (2), (6) | 与公式引用混淆 |

**正确流程**：
1. `grep -noE '\([0-9]+[a-c]?\)' paper.md | grep -v tag` 列出所有圆括号数字；
2. 人工逐条分类（公式引用 vs 群符号 vs 年份 vs 函数值）；
3. 只对**公式引用**做带上下文的精确替换，例如
   `"Differentiating (20) by the product and chain rules gives (21)"`
   → `"Differentiating (29) by the product and chain rules gives (30)"`。

## 验证（三项）

```python
tags = re.findall(r'\\tag\{([^}]+)\}', content)
# ① 连续编号 1..N 完整
nums = [int(t) for t in tags if t.isdigit()]
assert nums == list(range(1, len(nums)+1))
# ② 无残留字母后缀
assert not re.search(r'\([0-9]+[a-c]\)', content)  # 注意别匹配 (35/2) 这类
# ③ 群符号未误伤
# grep -c 'SL(6' / 'SU(6)' / 'U(1)' 数量与重编号前一致
```

## 附带教训（本次复审）

- **def 计数**：`grep -cE '^\s*def '` 会漏掉 `noncomputable def`。V64 的 28 def = 20 纯 def + 8 noncomputable def；先误判为 20（md 声称 28 被疑为错），复核才对齐。权威口径见 `references/lean-declaration-count-authoritative-method.md`。
- **审稿人算术误判**：technical 代理曾把 A₅ 正根数算成 5（实际 `5×6/2 = 15`），据此判「restricted-root multiplicity=2 维度不闭合」为错——实际 `dim = rank + 正根数×mult = 5 + 15×2 = 35` 完全闭合。独立重算正根数即可证伪，勿采纳。见 `references/reviewer-arithmetic-false-positive-verification.md`。
