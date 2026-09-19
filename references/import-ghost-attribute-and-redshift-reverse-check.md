# Import 幽灵属性文件 + 指数红移公式反推验证（V16 三峰引力波审查 2026-08-30）

两个在"论文+Lean 联合审查"中出现的可复用检测模式。前者是"表演性诚实"从
"注释文本"升级后的**新变体**；后者是"数值计算准确性"审查时对指数型红移公式的
**反推验证法**。

## 模式 1：Import 幽灵属性文件（表演性诚实 v2）

### 症状链（逐轮演化的"假修复"）
1. **第一轮**（表演性诚实 v1）：`@[honest_axiom]` / `@[phenomenological]` 全是
   `-- @[...]` 注释文本，真实属性行数 = 0。审稿指出后——
2. **第二轮**（本次发现）：作者把注释标签升级为**活跃**的 `@[honest_axiom]` 属性
   （不再有 `--` 前缀），并在文件头加 `import HonestAttr`——表面看修复了。
3. **陷阱**：`HonestAttr.lean`（注册文件）**根本不存在**于论文目录。`import HonestAttr`
   编译直接失败，`@[honest_axiom]` 属性从未通过 `initialize` + `registerBuiltinAttribute`
   注册，仍是无语义的语法糖。

### 判定：这不是"修复"，是把"注释文本"换成"无法编译的 import 声明"

### 检测三步（务必全做，缺一即误判为"已修复"）
1. **grep import 行**：`grep -n '^import' file.lean`，找出所有自定义模块
   （如 `import HonestAttr`）——非 Mathlib 的自定义 import 都要怀疑。
2. **find 注册文件**：`find <论文目录> -name "HonestAttr*"`（必要时全局）。
   确认注册文件存在，且内含 `initialize` / `registerBuiltinAttribute` /
   `Attribute.register` 代码。**只有注释里出现属性名 ≠ 注册**。
3. **编译验证**：`lake env lean file.lean`（复制到 mathlib 项目根目录，具体子模块
   import 而非 `import Mathlib` 全库）。`import <缺失文件>` 会直接报错，编译不过。

### 真实案例（V16，2026-08-30）
- `triple_gw_dm_proof_v16.lean` L44 `import HonestAttr`，但论文目录及全局
  `find` 均无 `HonestAttr.lean`。
- 头注释声称 "14 axioms · 22 theorems · 13 lemmas · ~1101 行"，实测
  "66 axioms · 55 theorems · 26 lemmas · 2008 行"——四处计数（头注释/摘要/§3/附录）
  互不兼容。
- 结论：5 代理一致判 P0-1（表演性诚实）**remain**——前一轮修的是"注释→活跃"，
  但底层"属性注册"从未落地。

---

## 模式 2：指数红移公式反推验证（f = f₀·e^(-N_e) 类）

### 触发条件
论文出现"频率/能量从产生值经 e-fold 红移衰减"的公式，典型形式：
- `f_obs = f₀ · e^(-N_e)` 或 `f_obs = f₀ / exp(N_e)`
- `z_eff = e^(N_e)`，能量密度 `ρ ∝ z_eff^(-4)`

### 独立验证三步
1. **独立重算指数**：`e^60 ≈ 1.14×10²⁶`，`e^100 ≈ 2.69×10⁴³`，`e^160 ≈ 8.7×10⁶⁹`。
   直接把 `f₀ / e^(N_e)` 算出来，与论文声称的 `f_obs` 对比。
2. **反推 N_e**：若论文声称的目标值 `f_obs` 是已知校准值，反解
   `N_e_required = ln(f₀ / f_obs)`，与论文声称的 N_e 对比。
3. **判读差异**：
   - 差几个数量级 → 算术错误（P0，最致命）；
   - `N_e_required ≠ N_e_claimed` 但 `f_obs` 恰好是目标值 → N_e 是**目标值反推的
     校准**，不是从第一性原理推导。

### 真实案例（V16 §3）
| 论文声称 | 实际计算 | 差异 |
|---|---|---|
| f₁ = 9.61×10⁴⁴/e⁶⁰ ≈ 4.5×10¹¹ Hz | 8.42×10¹⁸ Hz | **7 个数量级** |
| f₂ = 9.61×10⁴²/e¹⁰⁰ ≈ 1.71 Hz | 0.358 Hz | ~5 倍 |
| f₃ = 9.61×10³⁰/e¹⁶⁰ ≈ 10⁻⁹ Hz | 3.13×10⁻³⁹ Hz | **30 个数量级** |

反推：要得到 f₁=4.5×10¹¹ 需 `N_e = ln(9.61e44/4.5e11) ≈ 76.6`（论文写 60）；
f₃=10⁻⁹ 需 `N_e ≈ 92.0`（论文写 160）。→ **三峰频率是目标值反推的校准，且算术本身算错**。

### 教训
"声称从 f₀ 红移推导出观测频率"的论文，最容易在指数衰减这一步算错数量级。
审查时务必：①独立重算 `e^(N_e)` ②反推 N_e 对比 ③若两处都不自洽，判定为
"校准伪装成推导"而非单纯的算术笔误。

---

## 附带：假实数等式 axiom 的超越函数案例

- `axiom h_log_f1_axiom : Real.log (450e9) = 26.833` —— 精确值 `ln(4.5×10¹¹) ≈ 26.8325`
  （差 0.0005）。
- `axiom h_log_kls_axiom : Real.log 35 = 3.55535` —— `ln 35 ≈ 3.555348`（勉强对，但应
  是 theorem 非 axiom）。
- 教训：`Real.log` / `Real.sqrt` / `Real.exp` 等**超越函数的值即使"看起来对"，也可能
  有小数位误差**。逐条用 Python `math.log/sqrt/exp` 重算，任何 `axiom <transcendental> = <decimal>`
  的精确等式断言都要查——这是"假实数等式 axiom"（`false-proposition-axiom-detection.md`）
  的超越函数子类。

## 附带：写审查脚本时的引号陷阱

用 `write_file` 写 Python 审查脚本时，JSON content 里的 `\"预测\"` 经 JSON 解析后变成
裸 `"预测"`，导致 Python 字符串字面量未闭合 → SyntaxError。**修复**：字符串内嵌引号一律
用中文全角引号 `「」` 或 `""`，不要用 `\"` 转义英文引号。
