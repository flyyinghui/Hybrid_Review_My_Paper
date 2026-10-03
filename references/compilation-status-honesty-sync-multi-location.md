# 编译状态诚实性表述的多处同步（P0 陷阱）

## 触发
论文编译通过后，把"未编译 / 待编译"的诚实性表述更新为"已编译通过"。

## 陷阱：表述分布在多处，不是只有摘要或附录一处
论文手稿里的编译状态诚实性表述**散布在 3+ 个位置**：
- §1 声明标签表（S 标签定义："compilation status must be checked locally"）
- 具体定理节的正文（如 §9.2 "final compilation status is part of the pending local build, not claimed here"）
- 附录 A 结尾的核查段落（"no `lake build` result is claimed"）

只改最显眼的 1–2 处会遗漏其余位置，造成**正文内部自相矛盾**（一处说"待编译"、另一处说"0 errors"），被 5 代理终审的 consistency-checker 抓出 P0。

## 必须 grep 的全部变体（一次性搜全）
```
pending | not claimed | not asserted | not been compiled | compilation pending |
compilation is not asserted | final compilation status | no successful lake build |
stopped after elaboration | pending local elaboration | not compiled for this delivery
```
不要只 grep 一个词（如 "pending"），要覆盖上面的全部同义变体。

## 案例（V19, 2026-09-21）
论文手稿 3 处编译状态表述：第 27 行（§1 S 标签）、第 867 行（§9.2 GWTT 定理）、第 936 行（附录 A）。
更新了第 27、936 行，遗漏第 867 行。consistency-checker 抓出 P0：
"§9.2 'pending local build' 与附录 A 'build completes 0 errors' 直接矛盾"。

## 修复协议
1. grep 全部变体 → 得到完整清单（不止一处）。
2. 逐处替换为统一表述（如 "verified locally by the pinned Lean 4 / Mathlib build (0 errors)"）。
3. 替换后再 grep 一次，确认零残留。
4. 交给 5 代理终审前，把这作为 consistency-checker 的显式检查项（"编译状态表述是否全文一致"）。
