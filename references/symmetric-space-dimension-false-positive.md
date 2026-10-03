# 对称空间维度账的审稿人误判（restricted-root multiplicity）

**Session**: 2026-09-26, V64 中微子论文终审。

## 误判案例

technical 审稿人声称"§2 restricted-root multiplicity=2 维度不闭合"——把 A₅ **正根数**误记为 **rank（5）**，得出 `5 + 5×2 = 15 ≠ 35`，要求重算 multiplicity。

## 独立验证（正确账目）

对称空间 SL(6,C)/SU(6) 的实维数：
- `dim = rank + Σ(正 restricted root × multiplicity)`
- A₅ 正根数 = **n(n+1)/2 = 5×6/2 = 15**（不是 rank=5）
- rank = 5，multiplicity = 2（complex symmetric space 统一为 2）
- `dim = 5 + 15×2 = 35` ✓ 闭合

审稿人把「正根数」与「rank」混淆，维度账差 20。

## 通用公式速查

| 对称空间 | rank | 正根数 | multiplicity | dim |
|---|---|---|---|---|
| SL(6,C)/SU(6) | 5 | 15 | 2 | 35 |
| 一般 SL(n,C)/SU(n) | n−1 | n(n−1)/2 | 2 | n²−1 |

## 教训

1. 对称空间维度账 = **rank + 正根数×multiplicity**，正根数 ≠ rank（A_n 正根数 = n(n+1)/2）。
2. 任何「维度不闭合」的审稿声称，先独立重算正根数，不盲信。
3. 属「审查员算术假阳性」家族（同见 `reviewer-arithmetic-false-positive-verification.md`、`agent-false-positive-independent-verification.md`）。
