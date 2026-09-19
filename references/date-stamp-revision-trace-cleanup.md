# 投稿前清理：历史版本/时间信息残留的具体案例（CGICE V10）

**触发条件**：投稿前清理 md/tex 论文手稿，检查历史版本信息、修改时间戳、内部文档引用、修订痕迹。

**五类残留 + 清理方式**（CGICE V10 论文 2026-09-15 清理实录，全部命中）：

### 1. 日期戳前缀 `[Xxx, 2026-09-12]`
例：`[Normalization convention, 2026-09-12]: the anomalous dimension is evaluated in ...`
**清理**：删除整个日期戳前缀 `[Normalization convention, 2026-09-12]:`，保留其后的实质数学内容（归一化约定说明）。

### 2. 修订历史表述
- `The earlier value 72/35=12·6/35 used the mathematical (Killing-form) normalization ... which is inconsistent with b=12` — 「earlier value / inconsistent」是修订痕迹。
- `This replaces the earlier incorrect identification of g_TC²=24π²/35 with the FRG fixed point.` — 「This replaces the earlier incorrect」是修订痕迹，整句删除。
**清理**：把「earlier value + inconsistent」改写为**正向表述**（如「the factor 2 separating this from the Killing-form normalization ... is the restricted-root multiplicity m=2」），保留物理事实、删除修订语气；「This replaces ...」整句删。

### 3. 内部文档引用
例：`The review report and companion framework are supplied internal research documents, not substitutes for the missing physical derivations.`
**清理**：删除提及「review report / companion framework / internal research document」的句子，保留正常的学术声明（如「The cited general works support their stated mathematical methods; they do not establish this model's phenomenological identifications.」）。

### 4. 大写强调词（NOT / DISTINCT / WRONG / NO / ONLY / EXACT）
例：`is DISTINCT from`、`NOT 12`、`this is NOT the nonzero IR fixed-point orbit`。
**清理**：改为斜体 `*distinct*` / `*not*`，与全文语气一致。检测：`grep -noE "\b(NOT|DISTINCT|WRONG|NO|ONLY|EXACT)\b"`。

### 5. patch 工具插入 LaTeX 的 `\\tag{}` 双反斜杠陷阱
用 `patch`（skill_manage 的 patch 或 patch 工具）插入 LaTeX 公式编号 `\tag{4.5a}` 时，实际写入文件的是 `\\tag{4.5a}`（**双反斜杠**），LaTeX 渲染会把它当换行符 `\\` + `\tag`，导致渲染错误。
**检测**：`grep -c '\\\\tag{' paper.md`（Python repr 里 `\\\\` = 双反斜杠）。
**修复**：Python 脚本 `t.replace('\\\\\\\\tag{', '\\\\tag{')`（把双反斜杠 `\\tag` 还原成单反斜杠 `\tag`）。或用 Python 直接写文件而非 patch 工具插入含 `\` 的 LaTeX。

**统一清理检查命令**（投稿前跑一遍）：
```bash
grep -noE "20[0-9]{2}-[0-9]{2}-[0-9]{2}|\[V[0-9]|\[FIX|\[Normalization|\[2026|earlier value|earlier incorrect|This replaces|WITHDRAWN|review report|companion framework|internal research" paper.md
grep -noE "\b(NOT|DISTINCT|WRONG|NO|ONLY|EXACT)\b" paper.md
grep -c '\\\\tag{' paper.md
```

**关键原则**：清理历史版本/时间信息时，**保留实质数学内容、只删修订语气和时间戳**。改写「earlier value / inconsistent」为正向表述，而非直接删整段（否则丢失物理事实）。
