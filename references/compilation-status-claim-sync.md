# 编译状态/声明计数表述的分散残留（2026-09-21 P0 教训）

## 症状

修改论文的"编译状态"表述（如 "not compiled" → "compiled 0 errors"）时，只改了 2 处（§1 标签说明、附录 A 结尾），漏了 §9.2 的第 3 处。5 代理终审时 consistency-checker 报 P0："§9.2 声称 'pending local build, not claimed here' 与附录 A 'build completes 0 errors' 直接矛盾"。

## 教训

"编译状态 / 编译通过 / 声明计数 / 0 sorry" 这类**元声明**在论文里会分散在多个位置，修改时容易遗漏：

- 摘要（abstract）
- §1 标签说明（S/A/M/C/O 表格的定义行）
- 各章节的 "Lean 验证" 段落（如 §9.2 GWTT 证明的收尾句）
- 附录 A 声明计数表 + 结尾段
- Materials and verification 段

## 修复协议

修改这类元声明时，**必须 grep 全文所有残留关键词一次性改干净**，而非只改已知的那几处：

```bash
grep -nE "pending|not claimed|not asserted|compilation status|final compilation|not been compiled|compilation pending|no successful.*build|no .*lake build.*claimed|not compiled for this delivery" paper.md
```

完整关键词清单（编译状态类）：`pending`, `not claimed`, `not asserted`, `compilation status`, `final compilation`, `not been compiled`, `compilation pending`, `no successful lake build`, `no lake build claimed`, `not compiled for this delivery`, `compilation is not asserted`。

## 验证

修改后再次 grep 确认归零；并在终审时把"编译状态已统一为 X"写入对抗性上下文，避免审稿代理重复报同一问题（或反过来，让审稿代理专门核查是否还有残留）。
