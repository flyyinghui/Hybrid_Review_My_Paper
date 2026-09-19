# Lean 4 声明计数的权威方法（Appendix 自报 vs 实测对齐）

## 何时触发
- 审稿/复审发现「公理计数不一致」（P0-6 类）：论文附录声称的 axiom/theorem 数与实测不符。
- 需要把附录里的自报计数对齐到 Lean 源文件的 ground truth。
- 修完一个版本后，附录计数漂移（例如「108 axiom + 155 theorem」实际是 110/158）。

## 核心教训：同一个 .lean 文件，不同计数方法给出不同数字

三大时空相 V18 复审实测（同一文件 6D_Spacetime_Formal_Proof_V18.lean，232KB）时，四种方法得到四种结果：

| 方法 | axiom 数 | 问题 |
|------|:--:|------|
| `grep -c "^axiom "` | 109 | **漏掉**带前导空白的缩进声明 |
| `grep -cE "^\s*axiom\s"` | **110** | ✅ **权威值** |
| Python 正则含 `@[...]` 装饰器 | 112 / 137 | **多计**（把正文/文档里「axiom 名」引用也算进去） |
| Python 剥嵌套块注释后行级正则 | 88 | **少计**（正则 `\b` 边界/装饰器行匹配口径问题） |

**权威方法 = 行首锚定 + 允许前导空白**：
```bash
grep -cE '^\s*axiom\s'     file.lean   # 110
grep -cE '^\s*theorem\s'   file.lean   # 158
grep -cE '^\s*lemma\s'     file.lean   # 43
```
为什么对：`@[honest_axiom]` 装饰器单独占一行，真正的 `axiom name : type` 声明在下一行且行首（可能缩进）是 `axiom`，所以 `^\s*axiom\s` 恰好匹配每条声明、不匹配装饰器行和正文引用。

## def 拆分为普通 def + noncomputable def

`def` 计数会把 `noncomputable def` 也算进去，附录常分开列两项，必须拆：
```bash
grep -cE '^\s*(noncomputable\s+)?def\s' file.lean   # 126（总计）
grep -cE '^\s*noncomputable\s+def\s'      file.lean   # 40
# 普通 def = 126 - 40 = 86
```
附录应写「86 definitions + 40 noncomputable definitions」（合计 126），而不是只写一个 def 总数。

## 其它声明类型同样行首锚定
```bash
grep -cE '^\s*opaque\s'    file.lean   # 30
grep -cE '^\s*structure\s' file.lean   # 20
grep -cE '^\s*class\s'     file.lean   # 4
grep -cE '^\s*abbrev\s'    file.lean   # 1
grep -cE '^\s*instance\s'  file.lean   # 3
```
⚠️ 附录自报的 structure/class 也常漂移（V18 附录写 19 structures / 3 classes，实测 20 / 4）——对齐时**每种声明类型都要重数**，不能只改 axiom/theorem。

## 代码级 sorry/admit/trivial/:=True 核验
计数前必须剥嵌套块注释（否则注释里的「0 sorry」字样被误计）：
```bash
grep -n "sorry" file.lean | head   # 逐行看上下文，确认全在注释内
```
V18 复审 `grep -c "sorry"`=15 / "admit"=4 / "by trivial"=1，但**全部在注释/文档字符串里**，代码级 0 sorry。判定「0 sorry」必须 `grep -n` 看行上下文，不能只信裸计数。

## 修 P0-6（附录计数对齐）的收尾流程
1. 用上面的权威 grep 命令对**每种**声明类型重数一遍。
2. 在附录里把自报计数整行替换为实测值（如 `108 axiom + 155 theorem … 3 classes + 19 structures` → `110 axiom + 158 theorem … 4 classes + 20 structures`）。
3. 替换后 grep 残留检查：`grep -nE "108 axiom|155 theorem|19 structures"` 应为空。

## 陷阱：grep 跨行片段返回「not found」假阴性
残留检查用**跨行**的 phrase 会误报「没改到」（因为文本中间有换行）。例如 `grep "does NOT by itself force physical comoving volume"` 匹配不到——实际文本是「does NOT by itself force\nphysical comoving volume」。修好后验证用**不跨行**的片段（如 `grep "does NOT by itself force"`）。

## 关联
- `references/lean-stats-traps-and-multivalue-coupling-diagnosis.md` — 计数口径 + 多值耦合诊断（同一类的旧版）。
- `references/framework-stats-sync-counting-methodology.md` — 四论文框架统计同步口径。
- `references/lean-nested-block-comment-sorry-pitfall.md` — 嵌套块注释 sorry 假阳性机制。
