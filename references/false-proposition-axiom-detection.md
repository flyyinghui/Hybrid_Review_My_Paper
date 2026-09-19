# 假公理三型检测（CGICE V9.1 终审实录 2026-08-19）

当论文声称「zero sorry / fully verified」但 Lean 里存在**假公理**时，比 sorry 更糟——假公理通过爆炸原理可证任意命题。审计不能只看 sorry 计数，必须逐条检查每条 axiom 的**命题本身是否为真**。

## 三型假公理

### 型 1：假命题公理（∀ 量化写错，可证 False）

```lean
-- 原意：半经典势阱条件 |∇V|² − hΔV ≥ 0（对特定 V_eff 成立）
axiom spec_gap_bound : ∀ (grad_sq lapV : ℝ), 0 ≤ grad_sq - lapV
```

**问题**：全称量化写错——把「对 V_eff 的具体形式成立」误写成「对任意实数对成立」。取 grad_sq=0、lapV=1，得 `0 ≤ -1`（假）。Lean 可证 `¬(0 ≤ -1)`，于是该公理 + 反例 → False。

**检测**：对每条 `∀ x y, P(x,y)` 形式的公理，手工找反例（代入极端值 0/1/-1）。若 P 对某实例为假，则是假命题公理。

**修复**：量化范围改为绑定 V_eff 的算子（`∀ χ, 0 ≤ grad_sq_of χ - lapV_of χ`），或删除该公理。

### 型 2：假实数等式公理（exp/sqrt 精确值不等，norm_num 盲区）

```lean
axiom covariance_dissipation_value :
  covariance_dissipation 35 tau_c = (10 : ℝ) ^ (-(122 : ℤ))
-- 即 exp(-2×35×4.01) = 10⁻¹²²
```

**问题**：`exp(-280.7) = 1.2403×10⁻¹²²`，而 `10⁻¹²² = 1.0×10⁻¹²²`，两者**不相等**（差 1.24 倍）。Lean 的 `norm_num` 对 `Real.exp` 透明性不足，无法察觉 exp 等式为假。

**检测**：Python 精确重算每条含 `Real.exp`/`Real.sqrt`/`Real.pi` 的公理等式。**量级对 ≠ 精确值对**——exp(-280.7) 和 10⁻¹²² 量级都是 10⁻¹²²，但精确值差 1.24 倍。

**修复**：改为真区间断言（`0 < e^{-280.7} ∧ e^{-280.7} < 2×10⁻¹²²`），或让参数由等式**定义**（τ_c = 122·ln10/(2·35) ≈ 4.0131）而非独立硬编码。

### 型 3：零内容公理（平凡恒等式命名成深刻定理）

```lean
axiom a23_bochner_horizontal_laplacian : (1 : ℝ) * (1 : ℝ) = (1 : ℝ)  -- 1×1=1
axiom a24_stratonovich_sde_solver : (1 : ℝ) = (1 : ℝ)                  -- 1=1
```

**问题**：公理内容是与命名无关的平凡恒等式，却命名为「Bochner 水平拉普拉斯等价」「Stratonovich SDE 存在唯一性」——表演性声明。真正的定理内容（Eells-Elworthy-Malliavin 构造）未形式化，用 `1=1` 占位。

**检测**：grep 出所有 `axiom` 声明，检查命题体是否含 `(1:ℝ) = (1:ℝ)`、`1*1=1` 等平凡形式。

**修复**：删除，或改为诚实注释「Mathlib 流形框架未形式化，声明为研究级前提，无 Lean 内容」。

## 审计协议

1. **逐条公理真值检查**：不只看公理间是否矛盾（可证 False 的旧模式），还看每条公理**自身是否为真命题**。
2. **Python 精确重算**：对每条含 exp/sqrt/π 的数值等式公理，用 Python 精确计算两侧，判断是否相等。
3. **平凡体检测**：grep `= (1 : ℝ)` 或 `(1 : ℝ) * (1 : ℝ)` 找零内容占位。
4. **"zero sorry" 声明陷阱**：假公理不违反 zero sorry（公理不是 sorry），所以「zero sorry」声明技术上为真但误导——需额外检查假公理数。

## 关联

- `references/lean-axiom-consistency-audit.md`：公理间矛盾（可证 False）的旧模式
- `references/math-claim-independent-verification.md`：数值断言独立重算 + 假实数等式公理（101 量级案例）
