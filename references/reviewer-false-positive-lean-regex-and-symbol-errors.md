# 审稿代理误报的两个新根因：Lean 清单正则缺陷 + 审稿代理自身数学符号错误

CGICE V10 终审（2026-09-15）暴露两类**审稿代理误报**，均须在转达为 P0 前独立验证。

## 根因 1：喂给审稿代理的 Lean 定理清单被正则截断（Unicode 缺陷）

提取定理名清单的脚本若用 `[A-Za-z0-9_]` 正则，会截断 Unicode 标识符：

- `sum_ξ_indicator_s` / `sum_ξ_indicator_t` → 都截断成 `sum_`（`ξ` 非 ASCII）
- `gaussianKL_instantaneous_grönwall` → 截断成 `gaussianKL_instantaneous_gr`（`ö` 非 ASCII）

后果：审稿代理拿到缺陷清单后误报两个 P0/P1：
1. 「计数不一致 141 vs 140」—— 两个 `sum_ξ_indicator_*` 去重后少 1，代理判「论文 141 vs 实测 140」。
2. 「定理名 grönwall vs gr 不一致」—— 实际 Lean 里是 `gaussianKL_instantaneous_grönwall`，论文写对了，清单截断了。

**两条都真实正确，误报根因是清单缺陷，不是论文错误。**

修复：提取名用 `[^\s]+` 或 `\w`（Python re 默认 Unicode），**不要用 `[A-Za-z0-9_]`**。
Lean 标识符合法支持 Unicode（`ξ`/`ö`/`α`/`γ`）。

## 根因 2：审稿代理自身犯数学符号错误

5-agent 里 technical 代理会犯**点积对称性错误**：`∫∇ξ·j = ∫j·∇ξ` 被写成
`-∫j·∇ξ`，据此误报 `flux_force_master` 主命题 `dF/dt + Ψ_p(j) + Ψ_p*(-∇ξ) = 0`
「符号与标准推导相反」（实际符号正确）。

这是 `reviewer-arithmetic-false-positive-verification.md` 的姊妹案例——除了
「多个代理集体误读算术」外，还存在「单个 technical 代理自己算错」的情形。

## 通用门控规则（升级版）

任何「审稿代理声称的数值/符号/计数矛盾」，在转达为 P0 前：

1. **grep 源文件验证代理声称的值是否真实存在**（本次 141/grönwall 均真实正确，
   代理被缺陷清单误导；flux_force_master 符号经独立重算正确，代理点积算错）。
2. **检查喂给代理的中间产物（清单/提取文本）是否有缺陷**——代理可能被自己的
   输入误导，而非论文本身有错。
3. **独立重算**（点积对称性、约定依赖值、T_F 归一化），不盲信代理中间步骤。

三者都通过才定 P0；否则标注「审稿代理误报」并附独立重算证据。
