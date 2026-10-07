# Overclaim 修复措辞的连锁副作用（2026-10-07 SL6C V3 三轮评审验证）

当评审要求「降级 overclaim 措辞」（加 conditional / motivated / supplied / obstructed 限定词）时，修复操作本身会引入三个连锁陷阱。这套模式在 SL6C V3 三轮闭环（发现缺陷 → 给具体改写文本 → 修复 → 验证 fixed）中反复出现。

## 1. 摘要字数假阳性（reviewer 把 LaTeX 公式符号计入词数）

reviewer 报「摘要超 250 词（290/330）」时，**先实测**，不要直接采信。用去公式后的英文词计数：

```python
import re
abstract = "..."  # 提取 ## Abstract 段到下一个 ## 标题
nomath = re.sub(r'\$\$.*?\$\$', ' ', abstract, flags=re.DOTALL)  # 去 $$...$$
nomath = re.sub(r'\$[^$]*\$', ' ', nomath)                        # 去 $...$
words = re.findall(r"[A-Za-z0-9][A-Za-z0-9\-']*", nomath)         # 英文单词
print(len(words))
```

案例：5 个 reviewer 报摘要 290/330 词，实测 **205 词**（PRD 限内）——纯假阳性，`$4+2$`、`$\Theta$`、`$(3,1)+(0,2)$` 等公式符号被 reviewer 计成了词。**判定规则：任何「摘要超限」类发现，先跑上面这段实测再定性 P 级别。**

## 2. overclaim 修复措辞导致摘要膨胀

「加 conditional/motivated/supplied/obstructed 限定词」的修改**会加词**。案例：摘要 205 词 → 应用 6 项 blocking 修改后 → **270 词（超限）**。修复 overclaim 反而制造了新的超限问题。

压缩技巧（目标 ≤240 留余量，不同期刊计数口径略有差异）：
- **删冗余句**：如 "A conditional coarse-graining identity connects this distinction to the statistical free-energy functional."（信息量低的桥接句，整句删，省 ~15 词）
- **名词短语压缩**：`on supplied sector free energies and cells` → `on supplied data`
- **删技术细节**：`with positive counts first`（正文有，摘要可省）
- **每次修改后必须重新实测词数**，不能假设「改了措辞不影响字数」。

## 3. Lean 定理改名后 SHA-256 失效

定理改名（如 `spectral_mediation_excludes_neutral_spinodal` → `spectral_mediation_bound_excludes_neutral_spinodal_given_mediator_identification`）**改变源文件 hash**，论文 B.1 里的 SHA-256 必须重算。审稿人（R4）会专门检查「改名后 SHA 是否仍匹配」。

改名流程（四步，缺一不可）：
1. `grep -c 旧名` 确认 MD + Lean 双文件的出现次数（声明 + 所有引用）
2. 全局 `str.replace`（MD 正文引用 + Lean 声明和引用一起改，旧名 grep 归零验证）
3. 重编译验证 `EXIT_CODE=0`（改名可能破坏引用链）
4. **重算 SHA-256 更新到 B.1**（改名前的 SHA 立即失效）

## 4. 三轮评审闭环模式（比「评审→发现缺陷→再评审」更高效）

- **第一轮**：发现 overclaim 缺陷，产出 P0/P1 清单
- **第二轮**：**让 reviewer 给「可直接粘贴的改写文本」**（JSON 里 `rewrite_text` 字段，英文原文），而非「应缩短摘要」这类泛泛建议；同时给投稿策略（venue ranking + first_choice）
- **第三轮**：修复后验证 fixed/remain/partial + 收尾判断

关键：第二轮 prompt 必须**显式要求**「give the exact replacement sentence(s) in English, ready to paste, not 'shorten the abstract'」，否则 reviewer 只给泛泛建议，修复仍靠猜。

评分轨迹参考：三轮 6.5–7.5 → 7.17–7.42 → 6.83–7.0，honesty 维度从 8.5 升到 9.0（诚实化彻底后，弱点从「overclaim」转移为「significance 不足」——这是收敛信号，不是继续修表述层的理由）。
