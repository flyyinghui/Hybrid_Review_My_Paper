# 5-agent 终审脚本生成的两个陷阱 + 可靠模式

## 触发场景
为 SL(6,C) 系列论文写 5-agent venue-fit 终审脚本（review_*.py，类似 review_cgice.py / review_v21.py）时，
脚本本身由另一个工具（write_file / execute_code）生成，容易踩引号/占位符转义陷阱。

## 陷阱 1：write_file 的 content 参数里 `\"` 被处理成裸 `"`
- 现象：在 write_file 的 content 里写 Python 字符串 `"...凡 \"rw 展开定义 + linarith\" 的..."`，
  写入文件后变成 `"...凡 "rw 展开定义 + linarith" 的..."`（未转义双引号），
  导致 Python 字符串提前结束 → `SyntaxError: invalid syntax. Perhaps you forgot a comma?`
- 根因：write_file 的 content 经 JSON 层处理，`\"` 被 JSON 解析为字面 `"`，再写入文件就是裸双引号。
- 规避：生成脚本时，所有任务描述/提示词内部的英文双引号 `"..."` 一律改用中文引号 `「...」`，
  或改用单引号；不要依赖 `\"` 转义。

## 陷阱 2：execute_code 里 `%` 格式化与脚本模板占位符冲突 → KeyError
- 现象：用 `'''...''' % {"paper_path":..., "agents":...}` 生成脚本时，
  脚本模板里给"生成的脚本"用的 `%(role)s` / `%(task)s` 占位符，被**外层** `%` 格式化误当占位符，
  报 `KeyError: 'role'`。
- 根因：`%` 格式化不区分"我要替换的占位符"和"生成脚本里留给运行时用的占位符"。

## 可靠模式（本次验证可用）
1. 用 `json.dumps(obj, ensure_ascii=False)` 序列化 AGENTS 字典和 LEAN_GROUND_TRUTH 字符串
2. 脚本模板 body 用**大写 PLACEHOLDER 标记**（如 `PAPER_PLACEHOLDER` / `LEAN_PLACEHOLDER` / `AGENTS_PLACEHOLDER`）
3. 用 `body.replace("PAPER_PLACEHOLDER", json.dumps(paper_path))` 逐个替换，**不用 `%` 也不用 f-string**
4. 生成后 `ast.parse(script)` 做语法检查，确认 `SYNTAX OK` 再落盘
5. 脚本内部 main() 里 prompt 拼接用 `+` 字符串加法（不用 `%` 格式化），避免二次冲突

```python
body = r'''import sys, re, argparse, os
from pathlib import Path
PAPER_PATH = PAPER_PLACEHOLDER
LEAN_GROUND_TRUTH = LEAN_PLACEHOLDER
AGENTS = AGENTS_PLACEHOLDER
...
prompt = ("你是 5-agent 终审的 " + agent["role"] + "。\n\n"
          + agent["disposition"] + "\n\n" + agent["task"] + "\n\n"
          + paper + "\n" + LEAN_GROUND_TRUTH)
'''
body = body.replace("PAPER_PLACEHOLDER", json.dumps(paper_path))
body = body.replace("LEAN_PLACEHOLDER", json.dumps(lean_gt, ensure_ascii=False))
body = body.replace("AGENTS_PLACEHOLDER", json.dumps(agents, ensure_ascii=False))
```

## 关键要素（每次终审脚本必备）
- LEAN_GROUND_TRUTH 块：机器级 grep 实测计数（theorem/lemma/def/axiom/sorry/admit/namespace）
  + 编译状态（LEAN_EXIT=0）+ golden gate `#print axioms` 结果
- 注入前次评审历史（论文附录 E/F 的修订账本），要求逐条判 fixed/remain
- 5 agent 角色：consistency / technical / logic / lean_specialist / publication_strategist
- 各 agent 的 disposition（字面主义/怀疑主义/高度怀疑/字面主义最严/共情）是区分审稿角度对抗性的关键
- 模型：deepseek-flash + `extra_body={"thinking": {"type": "disabled"}}` + max_tokens=16384 + timeout=900
  （8192 会截断 technical/lean_specialist 致缺评分结论）
- 并行：5 个 background terminal + notify_on_complete，各自写 /tmp/<paper>_review/<agent>.md
