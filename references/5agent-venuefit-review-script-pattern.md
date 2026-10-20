# 5-agent venue-fit 终审脚本模式（CGICE V10 第四轮实录）

> 来源：2026-10-13 CGICE V10 第四轮终审（review_cgice.py 更新 + 5-agent 并行运行）。
> 适用：对"论文手稿 + Lean 形式化证明"双文件做 venue-fit 终审（CQG / Nature Physics / FoP 判定）。

## 脚本结构（可复用）

单执行器脚本 `review_<project>.py`，两个核心块：

1. **`AGENTS` dict**：5 个 agent 的 `role` + `task`（consistency / technical / logic / lean_specialist / publication_strategist），每个 task 内嵌"重点检查"清单 + 严格输出格式（P0/P1/P2/P3 分级 + 评分 X.X/10 + 结论）。
2. **`LEAN_GROUND_TRUTH`**：机器级地面真相（剥离嵌套块注释 `/- -/` 与行注释 `--` 后行首锚定统计），供 agent 对照论文声明。

模型调用：`deepseek-flash` + `extra_body={"thinking": {"type": "disabled"}}`（确保 `content` 非空，不进 reasoning_content）。

## 每次论文/Lean 更新后必须同步三件事

1. **计数**：theorem / lemma / def / abbrev / structure / axiom / sorry / admit / namespace 全量重跑（用 execute_code 剥离注释后 `re.findall(r'(?m)^\s*' + kw + r'\b')`）。
2. **编译状态**：`EXIT=0` + `grep -c error` = 0 + 黄金门控（`#print axioms` 仅 propext/Classical.choice/Quot.sound）。
3. **本轮变更说明**：把"相对上一轮终审的变更"写进 LEAN_GROUND_TRUTH，让 agent 能聚焦新引入的风险（否则 agent 会重复审旧问题）。

**漏掉任何一项，agent 会拿到过时地面真相，产出假阳性 P0。**

## 关键陷阱：Python triple-quote 提取 bug

更新 LEAN_GROUND_TRUTH 时，这个写法是**错的**：

```python
old_gt = txt[txt.index('LEAN_GROUND_TRUTH = """'):txt.index('"""', txt.index('LEAN_GROUND_TRUTH = """')+3)+3]
```

`+3` 只跳过 3 个字符，`txt.index('"""', 位置+3)` 找到的是**开引号**（`= """` 里的 `"""`）而非结束引号 → 只替换了 `LEAN_GROUND_TRUTH = """` 一小段，旧内容残留，导致 `SyntaxError: invalid character`。

**正确做法**：用锚定结束标记整体替换：

```python
start = txt.index('LEAN_GROUND_TRUTH = """')
end = txt.index('\n\nAGENTS = {')   # 用下一个已知标记定位结束
txt = txt[:start] + new_block + txt[end:]
```

通用教训：提取/替换 triple-quoted 字符串，不要用 `"""` 本身定位边界（会命中开引号），用**下一个已知唯一标记**（如 `\n\nAGENTS`）定位结束。

## 反复出现的元问题（CGICE 系列三轮一致）

1. **摘要防火墙**：摘要用完成时/断言语气（"yields unit charge"、"strengthen the mathematical core"），正文带 [M]/[F]/[A] 边界标注 → 读者仅读摘要高估已证内容。consistency/logic/technical 三个 agent 会各自独立指出，是最一致的信号。
2. **"独立推导" vs "微积分证书"**：BPST 积分（HasDerivAt + Tendsto 组合）是实质微积分证书，但若被积密度是**先验定义**的，则不是"从第一性原理推导"——措辞"independent physical derivation"过度。
3. **定义重言式**：biconditional 若把结论写进定义（D1Matching := g_TC²=8π²/λ_⊥），是 V64 式定义重言式，非实质闭环。

## 汇总报告结构

评分表（agent × 本轮 × 上轮 × 变化）+ P0 分级清单 + 投稿判定（CQG/Nature Physics 各自的 READY/MAJOR REVISION/NOT READY + 最低验收项）+ 核心判断（哪些是新引入风险 vs 已知未解决）。
