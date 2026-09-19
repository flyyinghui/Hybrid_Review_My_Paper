# Lean 标识符提取的 Unicode 陷阱 → 审稿误报根因

**触发条件**：审稿代理报告「论文声称的计数/定理名 与 Lean 清单不一致」，或 Stage 3.5 审计做论文↔Lean 计数核对。

**根因**：从 Lean 提取 theorem/lemma/def 名称时，正则 `[A-Za-z_][A-Za-z0-9_]*` **不匹配 Lean 的 Unicode 标识符**（`ξ`、`ö`、`ρ`、`α`、`⊥`、`∥`），名称在第一个非 ASCII 字符处被**截断**。

**真实案例**（CGICE V10 终审，2026-09-15，两个审稿误报同源）：
1. `sum_ξ_indicator_s` 和 `sum_ξ_indicator_t` 都截断成 `sum_` → 去重后 141 声明变 140 → consistency 代理误报 P0「论文 138+3=141 vs Lean 清单 140 不一致」。
2. `gaussianKL_instantaneous_grönwall` 截断成 `gaussianKL_instantaneous_gr` → writing 代理误报 P1「论文引用 `grönwall` 与清单 `gr` 不匹配」。

**论文计数 141 和定理名 `grönwall` 都是正确的**——误报根因是喂给审稿代理的「Lean 清单」本身被提取脚本污染。

**甄别规则**（呼应 REVIEWER ARITHMETIC FALSE-POSITIVE VERIFICATION）：
- 审稿代理报告「计数/名称 vs 清单不一致」时，**先独立 grep 原始 Lean 文件**，不要信代理引用的清单数字。
- 行级计数 vs 去重计数对比：`grep -cE '^(theorem|lemma) '`（行级）≠ `set(re.findall(...))`（去重）→ 差异即重名/截断。
- 确认：`grep -n "sum_ξ\|grönwall" proof.lean` 看原始声明是否含 Unicode。

**修复正则**：`\w[\w']*`（Python re 的 `\w` 默认 Unicode）或 `[^\s:]+`，不要 `[A-Za-z0-9_]`。

**教训**：核对「论文声称 vs Lean 实测」必须用 `grep -c` 行级计数，而非正则提取 + 去重计数。任何经「提取脚本二次加工」的清单喂给审稿代理前，都要验证清单本身未被截断/去重污染。
