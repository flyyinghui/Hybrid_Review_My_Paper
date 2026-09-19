# 论文手稿 ↔ Response-to-Reviewers 一致性同步

**触发场景**：手稿迭代后，需要把 `Response_to_Reviewers*.docx` 里过时的声明（标题、模型名、参数、章节号、结论数字、术语统一方向）同步到最新手稿状态。用户原话示例："根据最新论文手稿的篇章结构与主要结论、推导参数阈值内容，修改审查意见的回应文件"。

## 流程（5 步）

1. **定位两文件**：手稿 final docx + Response docx（同一目录，按日期后缀识别最新版）。
2. **提取手稿实际状态**（以手稿为准，不是 Response 为准）：
   - 标题：`grep -o` 或 head
   - 章节结构：`grep -nE '^#{1,4} '`
   - 术语用词统计：`grep -oiE 'term1|term2' | sort | uniq -c`（判定实际统一用哪个词）
   - 模型名/参数/阈值：pandoc 提取正文，定位核心章节
3. **提取 Response 全部段落**：`python-docx` 遍历 `doc.paragraphs` 打印 `[i] text`。
4. **逐条 diff 找矛盾**，重点核对五类：
   - 标题用词（Safety vs Security —— 以手稿为准，**即使审稿人曾建议相反方向**）
   - 模型名（ST-GAT vs ResGAT）
   - 参数（βgdp/βinn/βinf 三指数 vs 单一 β≈0.86）
   - 章节号（结论 §4 vs §5）
   - 术语统一方向（手稿实际统一用了哪个词，**可能反转审稿人建议**）
5. **run 级替换**（保留格式）：
   - 目标词完整在单 run 内 → `r.text.replace`
   - 跨 run 或需整段重写 → 第一个 run 存全文、其余 run 清空
6. **验证**：grep 旧词残留=0 + 新词生效 + `zipfile.testzip()`=None + `Document()` 可打开。备份原文件。

## 关键陷阱

1. **审稿人原话（Reviewer's Comment）不能改**——只改 Author's Response 部分。grep 到旧词残留在 Comment 段是正确保留，不是遗漏。
2. **术语统一方向可能反转**：审稿人建议"统一用 Security"，手稿最终可能统一用 Safety。以手稿为准，Response 需如实说明"最终采用 Safety，仅保留 biodiversity/food/public health security 固定搭配"。
3. **补充核心结论数字**：摘要/结论响应里补入手稿最新定量结论（效率 +19%、脆弱性 −46%、+1.23% 等），使 Response 更具体、更有说服力。
4. **单 run 完整匹配检测**：`any(t in r.text for r in p.runs)` 先探测目标词是否跨 run，再决定替换方式。
5. **章节结构变化**：手稿从"三章逻辑链"升级为"五章结构（3技术章+Discussion+Conclusions）"时，Response 的章节描述需同步，且结论章节号（§4→§5）必须改。

## 案例

城市空间增长论文 20260916final 手稿，Response 8 处过时一次性修复：
- 标题 Development and Security → Development and Safety
- ST-GAT → ResGAT（×2）
- βgdp=1.15/βinn=1.20/βinf=0.85 三指数 → 单一 β≈0.86
- 三章逻辑链 → 五章结构 + Zoning-Structure-Mode → Pattern + 补全第三章标题
- 结论 §4 → §5（×2）
- 术语统一 Security → 反转为 Safety（审稿人原建议是 Security）
- 补充结论数字（+19.0% / −46.4% / +1.23% / 6,300 km²）
