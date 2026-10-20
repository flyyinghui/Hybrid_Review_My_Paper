# 5-agent venue-fit 终审执行配方（deepseek-flash）

对 SL6C/CGICE 系列论文手稿 + 伴生 Lean 证明做投稿前终审的固定配方。比通用 hybrid review 更针对"条件模型 + 形式化 + 诚实标注"类理论物理论文。

## 5 个 agent 与 disposition（性格特质驱动审查强度，必须逐字注入）

| agent | disposition | 职责核心 |
|---|---|---|
| consistency | 字面主义(literalism) | 逐字核对声明计数/编号/数值，只信机器级 grep/Python 计数 |
| technical | 怀疑主义(skepticism) | 独立重算因子链，默认"作者写错因子2/比例方向/谱定理伪装" |
| logic | 高度怀疑(对抗最强) | 构造反例、找循环论证、追问"语言借用 vs 方程遵循" |
| lean_specialist | 字面主义(最严) | 只信编译/`#print axioms`/grep，不信头注释；抓"定义重述"陷阱 |
| publication_strategist | 共情(empathy) | 代入陌生严苛审稿人视角，评估期刊适配 |

## 执行参数（硬约束）

- 模型 `deepseek-flash` + `extra_body={"thinking":{"type":"disabled"}}`（v4-pro 大 prompt 挂死）
- **`max_tokens=16384`** —— 8192 会截断 technical reviewer（输出停在 P2 中途，缺评分/结论）
- `timeout=900`；`temperature=0.0`；全文 173–188K chars 可整篇喂入
- 5 个 agent 并行（各自 background 进程 + notify_on_complete），写 `/tmp/<review>/<agent>.md`
- 单 agent 执行器脚本模式：`--agent <name>` 参数化 + `LEAN_GROUND_TRUTH`（机器级统计）+ `PREVIOUS_REVIEW`（前次历史）注入到 prompt

## 前次评审历史注入（必须）

prompt 末尾注入「前次评审历史」，要求 agent **逐条判 fixed / remain / 部分落实**。第二轮起注入两轮历史：
- 第一轮 = 上游优化建议文档的意见
- 第二轮 = 上一轮 5-agent 的 P0 清单（让 agent 验证 P0 是否真修复，而非重新发现）

## 陷阱

1. **technical reviewer 会误报数值"硬错误"**（如 UETC 前因子"差因子2"），但重跑（加大 max_tokens）后它会自己撤回。技术 agent 声称的"硬错误"必须先独立重算确认，不要直接采信进 P0。
2. technical reviewer 首轮输出易被截断 → 发现缺评分/结论时，单独重跑该 agent（max_tokens=16384）。
3. 核心定理会被 lean_specialist 判为"定义重述"（V64 教训复现）——结构性发现，需 §12 表格 gap 披露 + §12 开头 compilation-hygiene 免责声明正面处理，而非硬否认。
4. 评分口径：consistency/technical 通常 8+，logic/lean_specialist 通常 6.5–7，publication 给 MAJOR REVISION。
5. 前次 6 条意见里"黑洞/暗能量机制、信息 Hessian 成核"被诚实撤回时，5 个 agent 一致判为"部分落实（撤回项合理，加分而非减分）"。

## 输出汇总格式

5 份报告 → 评分表（5 列）+ P0 清单（按维度）+ 前次意见 fixed/remain 判定表 + 投稿建议（首选/备选/暂缓 + P0 修复路线图 + 投稿前必做项）。

## 通用 P0 修复清单（评审发现 P0 后的标准修法）

| P0 类型 | 标准修法 |
|---|---|
| 摘要/正文/§11 承诺强度不一致 | 摘要重写：mechanism→witness，第一贡献改为"校准无关"的正面陈述，义务提前 |
| 排除链算子选择循环 | 显式标注"conditional on an independently specified operator; none constructed here" |
| 某章论证目标悬空 | 把工具明确定位为"a posteriori verification tools, not predictions" |
| 核心定理定义重述 | 表格逐条披露"实际证明内容 vs 物理声称"gap |
| 0 axiom 被当作实质证明证据 | §12 开头加"compilation-hygiene indicators"免责声明 |
| 表格措辞比正文强 | 降级为"algebraic monotonicity fact about constants, not a manifold spectral theorem" |
| "lexical audit vs kernel verification"冲突 | 标注"declaration-counting scan only, not kernel verification" + "machine-level kernel run (exit code 0)" |
