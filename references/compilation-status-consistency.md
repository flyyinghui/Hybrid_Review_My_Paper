# 编译状态声明一致性排查（compil 变体全 grep）

来源：2026-09-22 V19 UnifiedDynamics 版五代理终审。手稿被外部进程（sibling subagent）扩展后，编译状态声明在正文多处残留"未编译"，与已完成的编译成功事实矛盾，被 consistency-checker / writing-reviewer / logic-reviewer **三个代理同时报为 P0**。

## 触发条件

- 手稿或 Lean 源在会话间隙被外部进程/子代理扩展（新增命名空间、新增定理、新增章节）。
- 你（或前一环节）刚完成编译 + 公理审计，需要把手稿里的"未编译"声明统一更新为"编译成功"。

## 核心陷阱：只 grep 常见变体会漏

"未编译"在论文里以多种措辞出现，单一 grep 会漏掉一半以上：

| 措辞变体 | 位置示例 |
|---|---|
| `has not been compiled` / `not been compiled` | 标题下、§1 |
| `was not compiled` / `not compiled` | §9.2、附录 A |
| `uncompiled` | 摘要、§10 结论 |
| `No Lean compilation was run` | 附录 E.3 |
| `No compilation performed` | 附录 E.2 表格 |
| `not executed here` / `was not executed` | 附录 E.3 步骤 |
| `compilation status must be checked locally` | S 标签定义 |
| `elaboration succeeded`（否定式） | 附录 A 声明说明 |

**统一检测命令**（一次抓全）：
```bash
grep -niE "compil|uncompiled|not executed" <paper.md>
```

**不要**只 grep `not compiled` / `uncompiled`（会漏 `No Lean compilation`、`not executed here`、`compilation status must be checked`）。

## 五代理审查的信号

若残留矛盾，**至少 3 个代理会同时报 P0**，且措辞一致："正文声称编译通过，但附录 E 声称未编译"。这是**事实性矛盾**（非逻辑缺陷），但会直接把决策从 ACCEPT 拉到 MAJOR_REVISION。

- consistency-checker：报 P0（编译状态前后不一致）
- writing-reviewer：报 P0（版本残留痕迹，最严重）
- logic-reviewer：报 P1/R1（对抗性上下文与正文矛盾，二者必有一误）

## 修复清单（一次改全）

1. 标题下声明、摘要、§1、§9.2、§10 结论 —— 每处"未编译"改为"编译成功（0 errors, N s）"。
2. S 标签定义 —— `compilation status must be checked locally` → `compilation verified locally (see Appendix A)`。
3. 附录 A 声明说明 —— 删除否定式 `not a claim that its Lean elaboration succeeded`。
4. 附录 E.3 —— 整个"验证任务/未执行"段落改为"verification performed"，把步骤 1-4 的"未执行"指令改为"已执行并完成"。
5. 版本号同步 —— 若附录 E.3 写了错误的 Lean 版本（如 v4.19.0 实际是 v4.34.0-rc1），一并修正。
6. 声明计数分解明确化 —— 如 `73 + 261` 改为 `73 + (220 baseline + 41 new)`，消除"261 是否已含新增 41"的歧义（consistency 代理会报这个为 P0-1）。

## 关联模式：外部扩展后的重新验证

会话间隙文件被 sibling subagent 扩展后，动手前**必须先重新验证四项**，否则会基于过期状态决策：

1. 声明计数（`grep -cE '^[[:space:]]*(theorem|lemma|def|structure)...'`）—— 可能从 256→297 之类大幅变化。
2. 命名空间列表（`grep -nE '^namespace '`）—— 可能新增整个命名空间。
3. 编译状态（`lake build` 重新跑）—— 新增内容可能有 elaboration 错误。
4. 两文件一致性（`diff -q Spacetime_*.lean 6D_*.lean`）—— 外部进程可能只改了其中一个。

时间戳（`ls -la --time-style=+%H:%M:%S`）可快速判断文件是否在会话间隙被改过。
