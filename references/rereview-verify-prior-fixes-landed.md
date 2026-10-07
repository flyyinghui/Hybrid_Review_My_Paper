# 复审前验证「前轮修复是否真的落地」+ 定理编号对齐 Lean 声明顺序

2026-10-03 LightSpeed_Phase_Boundary 复审实录。两个可复用模式。

---

## 模式一：前轮报告声称「已修复」≠ 论文文件已改（P0 级元问题）

**症状**：前轮终审报告 `5Agent终审报告_*.md` 明确写「P0 修复 6/6 完成、已收敛到诚实自洽」，但复审时 5 个审稿人一致判 REMAIN，grep 验证发现论文文件**一字未动**——只有头部注释（`<!-- 交付说明...含 5-agent 终审修订...现已诚实自洽 -->`）加了「已修复」声明，正文仍是旧版本。

**这是比「仅加头注释=P0未修复」更严重的脱节**：不是某个 P0 只改了注释，而是**整份终审报告声称修复、论文文件完全没改**。报告层的「已修复」是虚构的。

**检测方法（复审前必做，不能信任前轮报告的修复声明）**：
1. 提取前轮缺陷清单里每个 P0/P1 的**可 grep 残留标记**（计数词、人名、标题、措辞）：
   - 计数：`grep -c "22 theorems"`（应为 0，若 >0 则计数未修）
   - 人名：`grep "G. Coleman"`（应为 S. Coleman）
   - 标题：`grep "^# "` 对比旧标题
   - 措辞：`grep "deepening open bridge"` / `grep "Partially advanced"`
2. 若残留 >0，说明前轮修复没落地，直接在复审报告里标 REMAIN，不必等审稿人。
3. 独立读论文文件核对，**不信任前轮报告的任何「已修复/已收敛」声明**。

**修复要点**：真正执行修复 = 改论文文件正文，不是改报告、不是改头部注释。

---

## 模式二：定理编号对齐 Lean 声明顺序（正文叙述顺序 vs 代码声明顺序）

**症状**：论文正文按「章节叙述顺序」给定理编号，Lean 文件按「代码声明顺序」排列，两者不一致时编号系统性错乱。

**LightSpeed 案例**：
- 论文正文叙述顺序：Sec III.B degenerate_iff_phi_sq（标 15）→ Sec IV.A dimension account（标 16-19）
- Lean 声明顺序：Part 3 dimension account（dynkin=15, four_dim=16...）→ Part 4 degenerate（=21）

结果：论文里 15/21、16/15 交叉错位，Sec V.B 表 #15 排在 #21 之后，正文「Theorem 21 provides a local criterion」指向错误定理，审稿人必报 P0/P2。

**修复方法（对齐 Lean = ground truth，因为 Lean 是编译验证的）**：
1. 用注释剥离 + 行锚定 grep 得到 Lean 的**权威声明顺序**（`grep -cE '^\s*theorem\s'` 依次列名）。
2. 建立「论文旧编号 → Lean 正确编号」映射表。
3. 正文**定义处**逐个改编号（用带唯一 Lean 名的上下文做精确替换，避免裸数字误伤）：
   ```
   "**Theorem 16 (`dynkin_dimension_account`)).**" → "**Theorem 15 ...**"
   ```
4. 交叉引用逐个核对（"Theorems 18 and 19" → "Theorems 19 and 20" 等）。
5. Sec V.B 表整块重排（不是只改编号，是把行顺序也对齐 Lean）。
6. 修完 grep 验证：Sec V.B 表 15-22 顺序 == Lean 声明顺序。

**关键**：编号对齐必须「定义处 + 交叉引用 + 清单表」三处同步，只改一处会留下新的编号矛盾。

---

## 复审脚本编写三个坑（本次踩过）

1. **ROLE_PROMPTS 引号冲突**：审稿人角色 prompt 里若用英文双引号引述（如 `"22 theorems"`），与 Python 字符串边界的英文双引号冲突 → SyntaxError。修复：内部引述改用中文引号 `『』` 或全角引号。
2. **HOME 为空**：WSL background terminal 下 `bash: /.local/bin/env: No such file or directory`，修复：命令前 `export HOME=/root`（脚本本身不受影响，但 stderr 会刷这个）。
3. **公式替换的 `\n` 陷阱**：LaTeX 多行公式的换行是**真实换行符**（`$$` 块内两行），不是 Python 字符串里的 `\n` 转义。用 `r"...\n..."` 匹配会 miss；应直接用 patch 匹配真实的两个物理行。
