# 假实数等式公理 → def 常量 修复模式（三峰引力波 V17 实录，2026-09-02）

## 触发场景

审查发现 Lean 文件里存在「假实数等式公理」——把十进制近似声明为精确等式：

```lean
@[phenomenological]
axiom h_log_f1_axiom : Real.log (450e9) = 26.8325   -- 26.8325 ≠ 精确 ln(4.5×10¹¹)
```

这是 `references/lean-false-axiom-patterns.md` 里的「量级对但精确值错的假实数等式」类型：因声明为 `axiom`，Lean **不检查真假**，编译通过，但等式本身是假的（`26.8325` 是 6 位近似，`Real.log (450e9)` 精确值是 `26.832513…`）。

## 识别：两步快速判断

1. **孤立公理**（零引用）：`grep -c "<axiom名>" file.lean` 返回 `1`（只有声明处，无任何 theorem/def 引用它）→ 可安全改动，不破坏编译。
2. **假等式**：声明形式是 `axiom X : <含 Real.log/exp/sqrt 的函数> = <十进制近似>`。超越函数的精确值几乎不可能是有限小数，所以 `=` 必假。

两条同时满足 → 适用本修复（改为 `def` 而非「删除」或「补诚实声明」）。区别于 `references/fake-axiom-removal-honest-declaration.md` 的「删除」路径：**当数值本身是正确的（只是声明方式假），改 def 比删除更好**——保留数值供论文引用。

## 修复：axiom → def（保留数值，消除假等式）

```lean
-- 修复前（假等式 axiom）
@[phenomenological]
axiom h_log_f1_axiom : Real.log (450e9) = 26.8325

-- 修复后（def 常量，诚实标注为数值近似）
@[phenomenological]
def h_log_f1 : ℝ := 26.8325   -- 数值近似 ln(4.5×10¹¹)=26.832513...，6位有效数字
```

要点：
- **保留数值**（`26.8325`），供论文/下游引用，只是不再声称「等于精确 ln 值」。
- **去掉 `axiom` 关键字和等式右边**，改成 `def 名 : ℝ := 数值`。
- **名字去掉 `_axiom` 后缀**（`h_log_f1_axiom` → `h_log_f1`），避免名不副实。若名字零引用（孤立公理），改名不破坏任何东西。
- **注释里写清**「数值近似，非精确等式」+ 精确值前几位（`= 26.832513...`），保留审计痕迹。

效果：axiom 计数减少（本次 4 个 log 假等式 axiom → def，65→61 axioms），假等式清零，编译不变（因零引用）。

## 相邻处理：幻影占位声明（诚实标注而非删除）

主文件头部常有幻影占位 axiom（`axiom Metric : Type`、`axiom TensorType`、`axiom RicciTensor : Metric → ℝ`），它们**被 Ric/ricci_nonpositive 等声明引用**，删除风险高（连锁删除破坏编译）。正确做法：**保留但诚实标注**，明确「占位类型声明，非物理公理，不计入物理公理计数」：

```lean
-- [P0-7 FIX] 以下 5 个占位声明（Metric/.../RicciTensor）是占位类型声明，非物理公理，
--   真实 Mathlib 类型类对接在 P09_manifold.lean 独立完成（0 自定义 axiom）。
--   计数声明：这 5 个占位不计入 61 个物理公理——只提供类型骨架，不携带物理假设。
axiom Metric : Type
```

## 修复后的完整验证链（三峰引力波 V17 顺序）

1. **论文 md 数值修复**（先做，不依赖编译）：Python 精准 `str.replace`（先 `shutil.copy2` 备份）按 P0/P1/P2 优先级替换数值。
2. **grep 校核残留**：修复后 `grep -c "<旧值>"` 应为 0；但诚实标注里引用的旧值（如「原 3.44K」）会残留，需人工确认是标注而非错误。
3. **Lean 修复**：假等式 axiom → def（本模式）+ 幻影占位诚实标注。
4. **编译验证**：`lean -o HonestAttr.olean HonestAttr.lean` 先生成本地模块 olean，再 `LEAN_PATH=<mathlib build>:<8 deps>:. lean file.lean`。见 `mathlib-offline-build/references/standalone-lean-compilation-via-lean-path.md`。`import Mathlib` 首次编译需数分钟（非挂死）。
5. **计数一致性核对**：机械审计（剥离注释后统计 axiom/theorem/lemma/sorry）vs 论文摘要/正文/Table vs Lean 头注释，三处数字必须一致。本次统一为 `61 axioms / 56 theorems / 26 lemmas / 2041 行 / 0 sorry`。

## 关键陷阱

- **`lean file.lean` 默认不生成 olean**（只 typecheck），`import` 本地模块会报 `unknown module prefix`。必须 `lean -o <out.olean> <file>` 显式生成。
- **假等式 axiom 用 `@[honest_axiom]`/`@[phenomenological]` 标注 ≠ 已修复**——属性标注是「诚实声明」，但等式仍是假的。真正的修复是改 `def` 或补精确值。
- **计数一致性要查三处**：论文摘要、论文正文 §3、论文 Table/附录 B，任何一处残留旧计数（如 57 theorems vs 实际 56）都是 P1 内部不一致。
- **论文数值替换注意 Unicode 精确匹配**：`×`/`⁴`/`⁻⁹`/薄空格 `\u2009`/LaTeX 转义引号 `\"` 都会让 `str.replace` 静默失败。失败时用 `repr()` 看真实字符，或用 `re.sub` + 定位索引替换。
