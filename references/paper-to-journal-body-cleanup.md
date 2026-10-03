# Paper-to-Journal-Body Cleanup (Review Fix Checklist)

从 5-agent 终审发现的「重构/审计白皮书 → 期刊投稿稿」修复清单。适用于把内部重构文档（跨引用内部手稿代号、无作者块、审计式章节）改写成可投稿论文的场景。评分参考：内容层（数学+诚实+形式化）可达 7-8 分，体例层（作者块/引用/摘要/章节结构）常只有 3-4 分。

## 高频 P0/P1 修复项（按性价比排序）

1. **重建引用体系**：正文内部代号 `[C10][S20][N64][G19]` 与 References `[n]` 打通，消除孤儿引用（投稿硬门槛，孤儿引用会导致 desk-reject）
2. **补作者块**：姓名/单位/通讯邮箱/ORCID（投稿系统第一步必需）
3. **摘要 ≤250 词**（PRD/JHEP），去掉内部代号（V64/GW V19/CGICE 等），展开缩写
4. **公式编号引用**：每个 `\tag` 需被正文引用（期刊要求，本次 69 个公式仅 15 个被引用）
5. **章节结构**：审计式 15 节 → Introduction/Method/Results/Conclusion 骨架

## 孤儿引用消除 + 重新编号技术

- 90% 孤儿引用是「重构文档」通病：正文用内部代号，References 用 `[n]`，两套体系互不打通
- **引用映射**：grep 正文概念词（`symmetric space` / `Bakry` / `Witten` / `seesaw` / `gravitational` / `renormalis` ...）定位落点，逐条在相应章节插入 `[n]`
- **删除堆料文献**：正文零讨论的（如 Ricci flow 的 Hamilton/Perelman，全文 "Ricci" 只出现在参考文献自身）→ 删除后**必须重新编号**并同步正文引用（`[16]→[15]` 等）
- **双轨编号打通**：`[E1]=[12]` 用 "Dufaux et al. 2007 (Ref. [12])" 形式，消歧义
- 引错对象检测：正文概念与文献错配（如 "Witten gap" 应指 Witten 变形 Laplacian [Witten 1982]，而非 Witten 1981 超对称破缺）

## 验证脚本（stdlib，可直接跑）

```bash
MD="path/to/paper.md"
# 摘要词数（Abstract 到下一节之间）
awk '/^## Abstract/{flag=1;next} /^## 1\./{flag=0} flag' $MD | wc -w
# 孤儿引用：正文（References 之前）引用的编号 vs 参考文献编号
body=$(awk '/^## References/{exit} {print}' $MD | grep -oE '\[[0-9]+(, *[0-9]+)*\]' | grep -oE '[0-9]+' | sort -un)
for i in $(seq 1 N); do echo "$body" | grep -qE "(^| )$i($| )" || echo "缺失 [$i]"; done
# 残留双轨代号
grep -c '\[E1\]\|\[E2\]\|external reference' $MD
```

## 编译声明一致性（P0，3 审稿人独立发现）

论文声称 "compiled exit 0"，但 Lean 文件头部写 "NOT compiled" → 判 P0 矛盾。根因是编译后未同步头部注释。详见 physics-proof-engine 的 `references/lean-compile-fix-session-2026-10-01.md` 第 5 节。
