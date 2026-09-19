# Nested Block-Comment Sorry False Positive — 审计脚本嵌套块注释假阳性

**来源**：四论文联合审查（2026-08-29）跑 Stage 3.5 审计（proof_consistency_audit.py）时，
中微子 V63 的 `Neutrino_Condensation_proof_63.lean`（1723 行）被判 4 处 active sorry → BLOCK，
但 `grep -n sorry` 逐行核查发现 4 处全是注释文字（"0 sorry 声明"、CHANGELOG 表格、"The file
compiles with zero sorry keywords"），实际 **0 active sorry**。

## 根因：非贪婪正则无法处理嵌套块注释

审计脚本的块注释剥离用的是：
```python
lean = re.sub(r'/-.*?-/', '', lean, flags=re.S)   # 非贪婪，遇到第一个 -/ 就停
```
Lean 4 块注释 `/- ... -/` **可以嵌套**（`/- 外层 /- 内层 -/ 仍在外层 -/`）。非贪婪 `.*?`
在**第一个** `-/` 处提前终止，导致后续嵌套结构错位——块注释内部的行（含 "sorry"/"admit"
字样）漏到 active 列表，被 `count_active(r'\bsorry\b')` 误计。

## 症状识别

- 审计报 `sorry=N>0`，但 `grep -n 'sorry' file.lean` 逐行看，命中行全是
  `--` 注释、`/- ... -/` 块内说明文字、CHANGELOG、表格里的 "0 sorry" 字样。
- 特征：命中行内容含 "zero sorry" / "0 sorry" / "0 active sorry" 等**反向声明**，
  而非真正的 `theorem ... := by ... sorry` 证明体。

## 修复方向（务必先确认再判定）

1. **任何非零 sorry/admit/`:= True`/`by trivial` 计数，判定 P0 前必须
   `grep -n 'sorry' file.lean` 逐行看上下文**（这是 ars-awa-hybrid-review Pitfall 4 的强化版）。
2. 更健壮的块注释剥离：用**行级状态机**跟踪嵌套深度，而非单条非贪婪正则：
   ```python
   depth = 0; out = []
   for line in lean.splitlines():
       depth += line.count('/-')
       if depth == 0: out.append(line)
       depth -= line.count('-/')   # 注意同行的 /- 和 -/ 顺序
   ```
3. 判定标准：真正的 active sorry 应形如 `theorem X : ... := by ... sorry`（证明体末尾），
   而非注释/字符串里的 "sorry" 字样。

## 关联

- ars-awa-hybrid-review SKILL.md Pitfall 4（Lean Stats Regex Trap）已记录 `grep -c` 计注释的
  问题；本 reference 是其**嵌套块注释**这一具体失败模式的补充。
- 该 bug 目前存在于 `scientific-discovery-proof` 的 `stage3_ppe/proof_consistency_audit.py`
  （含刚加的 "检测 0: active sorry BLOCK"）——检测逻辑正确，但块注释剥离非贪婪，遇到嵌套
  注释会假阳性。修复应落在剥离函数，而非下调 sorry 检测。
