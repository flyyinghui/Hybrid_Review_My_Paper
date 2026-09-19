# 逻辑自洽性 + 物理关联性复审 + 精简不相关内容（含删除/附录重编号陷阱）

来源：三大时空相 V18 第六轮复审（2026-09-19），聚焦「前后论述逻辑自洽性 + 物理现象关联性 +
删除或精简不相关内容」。5 代理一致 5.0/10，删除 375 行（−24%）。

## 一、5 代理角色设计（区别于内部一致性/CGICE 遵循度复审）

当用户要「检查前后逻辑自洽性 + 物理关联性 + 删除不相关」时，用这 5 个角色（不是常规的
consistency/logic/technical/writing/bibliography）：

1. **consistency** — 前后论述矛盾（摘要 vs 正文 vs 附录 vs Lean 计数）
2. **relevance** — 物理现象关联性（识别与主线不相关的旁支，给 delete/simplify/keep 建议）
3. **logic** — 三阶段论证链连贯性（因果箭头是否清晰、是否有逻辑跳跃）
4. **redundancy** — 冗余/重复检测（同一推导多处重复、历史版本残留、修订表）
5. **cross_check** — 跨章节参数阈值/标记一致性（superseded/withdrawn 是否完整）

JSON 契约：`inconsistencies`（severity+fix）+ `irrelevant_content`（recommendation: delete/simplify/keep
+ reason）+ `redundancy` + `summary`。

## 二、旁支识别判据（物理关联性）

系列论文中，每篇有自己的「层」——三大时空相=几何层、CGICE=动力层、V63=场论层、GW=现象学层。
复审时把**其他层的内容混入当前层**判为不相关旁支：

- §III.G VEV(1+2+3) 真空唯一性 → 无推导链（后经 VEV 探索重新关联，见下）
- §III.H Fisher 引力 + 时间荷↔ν_R 对偶 → 场论层/现象学层旁支
- 附录 C Cartan compactification bridge → 现象学层/伴随 RHN 论文内容
- Revision tables（3 张修订表）→ 内部日志非科学内容
- §V 三重峰 GW 具体频率 → 已撤回，保留数值会误导

判据：①内容是否真与主线（三阶段动力学）有方程级/推导链联系？②是否属于另一篇论文的范畴？
③是否已 superseded/withdrawn 但残留正文？

## 三、删除范围陷阱（实测）

**从后往前删除用 0-indexed 范围 [start, end) 时，end 必须精确对到「下一个标题所在行」而非
「上一个内容结束行」**。否则会多删下一节的标题：

- 误删案例：§III.H 是 662-678（1-indexed），§IV 标题在 679。删除范围写成 [661, 679) 把 §IV
  标题一起删了。正确应为 [661, 678)（end 指向 679 标题行本身，即 0-indexed 678）。

**防御**：
1. 删除前 `grep -nE "^#{1,3} "` 打印完整章节结构，逐节核对 end 行号。
2. 删除后立即再 grep 章节结构，确认所有 `#` 标题都在。
3. 发现误删标题，用 patch 在下一节标题前补回（不要用 `old==new` 的空 patch）。

## 四、附录重编号 + 悬空引用修复

删除中间附录后（如删附录 C），后续附录要**重编号**，否则编号断裂：

1. 附录 D → 附录 C（标题 + 正文交叉引用 `given in Appendix D` → `given in Appendix C`）。
2. 已删附录的正文引用改指向新位置（如 `Appendix C table` → `§IV.C`）。
3. 用 `grep -nE "Appendix [A-Z]"` 列出**所有**引用（含标题、正文、交叉引用），逐一改，
   不要只改标题。

## 五、精简的边界（避免过度删除）

- 已 superseded 的节：保留一行 `[SUPERSEDED …]` 说明 + 标题，删正文（不是整节删，保留可追溯）。
- 已撤回的预测：删具体数值，保留「withdrawn」声明（数值会误导，声明是诚实边界）。
- 与主线弱关联但 Lean 里已形式化的（如 §V 的 GWTT TT 投影证明）：谨慎，先判断是否真与主线无关。
- 删除前必备份：`cp file.md file.md.bak_pre_trim`。
