# 5-agent venue-fit 终审：disposition 设计 + 脚本生成陷阱

2026-10-19 三大时空相 V21 / CGICE V10 两轮 5-agent 终审实战沉淀。

## 1. 五代理维度 + disposition（对抗性人格设计）

每个 agent 给一个明确的"性格特质"，防止大模型审稿时滑向中庸/客套：

| agent | 角色 | disposition 特质 | 核心怀疑点 |
|---|---|---|---|
| consistency | 一致性审计 | **字面主义**（literalism）：只信机器级验证，不接受"应该没问题" | 声明计数、编号、数值逐字核对 |
| technical | 技术/数学审计 | **怀疑主义**（skepticism）：默认作者写错了因子 2/比例方向 | 硬算术错误、重言式、校准伪装 |
| logic | 逻辑自洽审计 | **高度怀疑**（对抗性最强）：主动构造反例、找循环论证 | 结论是否暗中依赖待证命题 |
| lean_specialist | Lean 形式化专家 | **字面主义（最严）**：凡 "rw+linarith" 浅层证明一律可疑重言式 | 0 axiom/sorry 是否等于实质证明 |
| publication_strategist | 投稿策略顾问 | **共情**（empathy）：代入审稿人/编辑立场 | 各期刊最低验收项 |

关键：disposition 描述要**具体到行为**（"逐字核对""独立重算""构造反例"），不是空泛的"严格""客观"。

## 2. 脚本生成两个陷阱（生成"生成脚本的脚本"必踩）

### 陷阱 A：write_file content 里 `\"` 被 JSON 转义吞掉

write_file 的 content 参数是 JSON 字符串。写 `\"rw 展开定义 + linarith\"` 时，JSON 解析把 `\"` 变成 `"`，写进文件的 Python 脚本里就是**未转义**的 `"rw ... linarith"`，导致字典字符串提前结束 → `SyntaxError: invalid syntax`。

**解决**：生成的脚本里所有内部双引号改用中文引号「」，或干脆不写内部英文双引号。

### 陷阱 B：execute_code 里 `%` 格式化 vs 生成脚本里的 `%(role)s` 占位符冲突

用 `'''...''' % {"paper_path":..., "agents":...}` 生成脚本时，脚本模板里的 `%(role)s` / `%(disp)s` 也被当作 `%` 占位符 → `KeyError: 'role'`。

**解决（可靠方案）**：不用 `%` 格式化。三步：
1. `agents` 和 `lean_gt` 用 `json.dumps(..., ensure_ascii=False)` 序列化
2. 脚本模板里用唯一占位符（`AGENTS_PLACEHOLDER` 等）
3. `body.replace("AGENTS_PLACEHOLDER", agents_json)` 注入，最后 `ast.parse(script)` 验语法

## 3. 执行参数（已验证）

- 模型：`deepseek-flash`，`extra_body={"thinking": {"type": "disabled"}}`（否则 content 空）
- `max_tokens=16384`（8192 会截断 technical reviewer 致缺评分/结论）
- `temperature=0.0`，`timeout=900`
- 全文 258KB 论文可整篇喂入（不截取）
- LEAN_GROUND_TRUTH 注入**机器级实测计数**（行首锚定）+ 前次评审历史（逐条 fixed/remain 判断）
- 5 个 agent 用 background=true + notify_on_complete 并行跑，完成后统一汇总

## 4. 评分汇总模式

5 份评审统一读回，汇总成：评分表 + 核心 P0（各 agent 交叉一致的部分）+ 投稿建议表（首选/备选/暂缓/不建议）。**多个 agent 独立报出同一个 P0 = 高置信真问题**（如 5 代理一致发现"声明计数 624 vs 554"）。单一 agent 独有发现（如 consistency 的"标签互斥"）也要保留，但标注来源。
