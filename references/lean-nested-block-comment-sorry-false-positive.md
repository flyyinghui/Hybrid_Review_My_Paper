# Lean 嵌套块注释 → sorry 假阳性（审计脚本自身 bug）

## 问题

`proof_consistency_audit.py`（scientific-discovery-proof 的 Stage 3.5 L1 审计脚本）用正则剥离块注释：

```python
lean = re.sub(r'/-.*?-/', '', lean, flags=re.S)  # ← 非贪婪匹配，有 bug
```

Lean 4 的块注释 `/- ... -/` 是**可嵌套的**。当文件里出现嵌套结构
（如 `/- ... /- 内层 -/ ... -/` 的 CHANGELOG / 验证说明 / 表格），非贪婪 `.*?`
会在**第一个 `-/` 处提前终止**，导致后续块注释内部的行（含 "sorry" 字样，
如 "0 active sorry" 声明、"The file compiles with zero `sorry` keywords"）
漏到 active 列表，被 `count_active(r'\bsorry\b')` 误判为 active sorry。

## 后果

0 sorry 的干净证明文件被审计门误判为 **BLOCK**（"N 处 active sorry"），
产生假阳性——正好削弱了 v2.3.0 刚加的 active-sorry BLOCK 检测的可靠性。

## 真实案例（2026-08-29）

中微子 V63 `Neutrino_Condensation_proof_63.lean`（1723 行）被审计脚本判 BLOCK，
报告 4 处 active sorry。逐行 grep 确认：4 处全部在块注释/说明文字里——
行 17「33 theorems + 27 lemmas, 0 active `sorry`」、行 2662「The file compiles
with zero `sorry` keywords」、行 2738/2748 的 CHANGELOG 表格「0 sorry」。
实际 active sorry = 0。

## 修复方法

不用正则剥离嵌套块注释，改用**深度计数扫描器**（Lean 4 块注释可嵌套）：

```python
def strip_block_comments(text: str) -> str:
    out = []
    depth = 0
    i = 0
    while i < len(text):
        if depth == 0 and text[i:i+2] == '/-':
            depth = 1
            i += 2
            continue
        if depth > 0 and text[i:i+2] == '/-':
            depth += 1
            i += 2
            continue
        if depth > 0 and text[i:i+2] == '-/':
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(text[i])
        i += 1
    return ''.join(out)
```

（另需处理字符串字面量内的 `/-`/`-/`，但 Lean 证明文件里少见，先做深度计数即可。）

## 检测铁律（Pitfall 4 的延伸）

任何非零 sorry/admit/`:=True`/`by trivial` 计数，**必须先用 `grep -n 'sorry'` 看行上下文**
才能报告 P0/BLOCK。这条规则不只针对手工 grep——连审计脚本自己的正则都可能产生假阳性。
若审计脚本的 sorry 计数 > 0，先确认脚本的块注释剥离是否正确（有无嵌套 `/-`）。
