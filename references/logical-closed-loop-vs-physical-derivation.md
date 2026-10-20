# 逻辑闭环 ≠ 物理闭环：biconditional 定义重言式陷阱

> 来源：2026-10-13 CGICE V10 第三轮 5-agent 终审，lean_specialist P0-1（5.5/10，一轮内 6.5→5.5 的分数倒退根因）。
> 场景：作者把一个 [M] 匹配假设包装成「闭环 biconditional」形式，伪装成「闭环证明」。
> 这是 `open-bridge-deepening-honesty-traps.md` 的**陷阱 4**（第四种开放桥深化诚实性陷阱）。

---

## 反例（CGICE V10 `D1BridgeClosure` 命名空间，2026-10-13）

```lean
def instantonAction (g : ℝ) : ℝ := 8 * Real.pi ^ 2 / g ^ 2   -- 定义
def d1Matching (g : ℝ) : Prop := instantonAction g = matchingRate   -- 假设 [M]

-- 声称的「闭环」biconditional：
theorem d1_matching_iff_coupling_sq (g : ℝ) (hg : g ≠ 0) :
    d1Matching g ↔ g ^ 2 = 8 * Real.pi ^ 2 / matchingRate := by
  unfold d1Matching instantonAction matchingRate
  have hg2 : g ^ 2 ≠ 0 := pow_ne_zero 2 hg
  constructor <;> intro h <;> field_simp [hg2, Real.pi_ne_zero] at h ⊢ <;> nlinarith [h]
```

逻辑上等价于 `(8π²/g² = λ_⊥) ↔ (g² = 8π²/λ_⊥)`，即「除法可逆」`a/b = c ↔ b = a/c`。
配套还有 `instanton_action_at_gtc_eq_matching_rate`、`d1_matching_holds_at_gtc`、`gtc_sq_iff_d1_matching` 三个同类恒等式。

---

## 核心诊断：两种「闭环」的本质区别

| | 逻辑闭环（假设 ⇔ 结论） | 物理闭环（推导 ⇒ 结论） |
|---|---|---|
| 结构 | 从假设 `S_inst = λ_⊥` 出发，证明它与 `g² = 8π²/λ_⊥` 等价 | 从第一性原理（几何/拓扑/谱）独立推出 `S_inst = λ_⊥` |
| 数学本质 | 算术移项 `a/b = c ↔ b = a/c` | 需要跨结构的实质推理 |
| 证明体 | unfold 定义 + field_simp + nlinarith/ring | calc 链 / 谱定理 / 拓扑分类 |
| 实质内容在哪 | 全部在 def 和 [M] 假设里 | 在证明体里 |

**判定标准（一行）**：把「假设」那一侧删掉后，若定理还能证明同样的结论 → 物理推导；
若删掉假设后定理立即退化 → 逻辑重言（定义重述）。

---

## 检测信号（审稿侧 + 作者侧）

1. biconditional 的一侧是 [M] 假设，另一侧是「代入定义后的代数结果」。
2. 证明体 = unfold 定义 + field_simp + nlinarith/ring，**无 calc 链、无跨结构推理**。
3. 「闭环 / closed loop」一词被用来描述「假设 ⇔ 结论」，而非「推导 ⇒ 结论」。
4. 定理的实质内容**全部**在 def 和 [M] 假设里，证明体零贡献。
5. 命名暗示「匹配在 g_TC 处成立」（`d1_matching_holds_at_gtc`），实际是「在 g_TC 定义处，匹配假设的代数重述成立」。

---

## 与既有陷阱的关系

- 是 `open-bridge-deepening-honesty-traps.md` 的**陷阱 4**（新增）。
- 与 `parameterization-disguised-as-dynamical-closure.md`（参数化伪装成动力学闭合）是姊妹陷阱。
- 与 V64 教训（`definitional-tautology-trap`）同源但机制不同：
  - V64：`S ≡ 谱底·‖φ‖²+V_top` 后 bound 变重言式（**单向**）。
  - 本案：biconditional 的「**双向**」外观掩盖了它只是除法可逆（**双向伪装**更隐蔽）。

---

## 修复

1. docstring 明确写「this is a definitional unfolding / matching condition restated as a
   coupling-value identity, not a derivation」。
2. 把「closed loop」措辞**降级**为「matching condition restated as a coupling-value identity」。
3. 定理名 `d1_matching_holds_at_gtc` 改为 `d1_matching_restated_at_gtc`。
4. 若要真正的物理闭环，需要**独立推导** S_inst = λ_⊥（拓扑荷 → 瞬子作用量 → 谱隙），
   而非假设匹配——见配套建议 `cgice-d1-physical-closure-roadmap`。

---

## 关键洞察（元层）

作者带着「我想把开放桥推进一步」的动机时，最容易把**定义重述**误判为**闭环**——因为
biconditional 的「双向箭头 ⟺」在排版/逻辑符号层面恰好满足了「闭环」的**视觉意象**（首尾相接）。
这是「语义超载」的一种新变体：不是定理名超载（如 `radial_gap_lower_29`），而是**逻辑连接词
⟺ 的超载**——⟺ 本身暗示「充分必要、双向可证」，但这里双向都只是除法可逆。
