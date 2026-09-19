# 嵌套块注释导致 sorry 假阳性（Lean 审计陷阱）

**触发**：用正则去块注释后统计 `sorry`/`admit`/`:= True` 数量时，得到一个非零计数，但文件"声称 0 sorry"。

**根因（2026-08-29 验证）**：块注释去除用了非贪婪正则 `re.sub(r'/-.*?-/', '', lean, flags=re.S)`。当 Lean 文件含**嵌套块注释**（`/- ... /- ... -/ ... -/`，常见于含 changelog/status 说明的证明文件末尾）时，非贪婪匹配在第一个 `-/` 处提前终止，后续的 `/-` 与更远的 `-/` 配对错乱，导致内层注释体（常含 "The file compiles with zero `sorry` keywords" 之类的状态说明文字）漏进 active 行列表，被误计为 active `sorry`。

**真实案例**：`Neutrino_Condensation_proof_63.lean`（1723 行）——审计脚本报 `sorry=4` + `GATE: BLOCK`，但 grep 逐行核查发现 4 处全是嵌套块注释里的 changelog/status 文字（"0 active sorry keywords"、"V55: 21 axioms... 0 sorry" 表格），实际 **0 active sorry**。

**检测协议（任何非零 sorry/admit 计数前必做）**：
```bash
grep -n 'sorry' proof.lean   # 逐行看上下文
```
判断每个命中是 (a) 状态说明句子（"zero sorry" 出现在注释）还是 (b) 真实的 `sorry` tactic。status/changelog 句 → 假阳性；真实 `sorry` tactic → 真 BLOCK。

**健壮修复**（替换非贪婪正则）：
- 括号匹配 / 栈式去除：从左到右扫描，维护 `/-` 嵌套深度，深度 ≥1 的行全部剔除。
- 或先 `lean.count('/-')` 与 `lean.count('-/')` 核对是否配对，不配对说明有嵌套或未闭合注释。

**关联**：这是 ars-awa-hybrid-review SKILL.md Pitfall 4（"Lean Stats Regex Trap"：grep 把 header 注释里的 "0 sorry" 当 active sorry）的**具体机制升级**——Pitfall 4 说的是"注释里的 sorry 字样"，本 reference 说的是"嵌套块注释导致注释体漏进 active 列表"的具体原因和修复。
