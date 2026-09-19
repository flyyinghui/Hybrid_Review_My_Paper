# Lean 4 autoImplicit 幻影公理签名检测

**触发场景**：审计 Lean 证明的公理/定理签名时，发现某符号（类型名/函数名）在文件中仅出现一次（声明处），但编译却成功。

## 机制（根因）

Lean 4 默认开启 `autoImplicit` 选项。当 `axiom`/`theorem` 签名中出现**未定义的标识符**时，Lean 不会报 "unknown identifier"，而是把它当作**隐式自动绑定的变量**（未知类型）：

```lean
axiom foo (X : UndefinedType) : UndefinedFunc X ≥ (1/8 : ℝ)
-- 编译通过！等价于
-- axiom foo {UndefinedType : Type} {UndefinedFunc : UndefinedType → ℝ} ...
```

## 后果

该公理是**悬空声明（phantom/dangling）**——引用的类型/函数从未定义，公理本身也从未被任何定理引用，是死代码。它伪装成"已形式化"，实际无数学内容。比"幻影引用"（theorem 体内 `exact phantom_lemma`）更隐蔽：签名看起来合法，编译不报错。

## 检测方法（三步，缺一不可）

1. `grep -c '符号名' file.lean` == 1（仅声明处出现）= 悬空候选
2. 从模块外 `#check 符号名` → `unknown identifier`（确认符号从未定义）
3. 最小复现：新建 .lean 写 `axiom foo (X : Bar) : Baz X`，`lean` 编译通过即确认 autoImplicit（对比：真未定义类型在普通 `def`/`theorem` 语境会报 unknown identifier）

## 修复

删除该悬空公理（连同其 docstring + `@[honest_axiom]`），或补上缺失的类型/函数定义。删除后重新精确计数 axiom，同步更新论文附录的声明计数与文件头注释。

## 与既有坑的区别

- **幻影引用（phantom reference）**：theorem 体内 `exact phantom_lemma`，引用未定义的引理 → 编译报错。
- **本坑（autoImplicit phantom axiom）**：axiom **签名本身**含未定义类型 → 编译**通过**，更隐蔽。
- **孤立公理（isolated axiom）**：声明了但零引用，但类型/函数是真实定义的；本坑是类型/函数本身也未定义。

## 案例

V18 三大时空相 `ricci_lower_bound (X : SymmetricSpaceSL6CSU33) : RicciCurvature X ≥ (1/8 : ℝ)`：
- `SymmetricSpaceSL6CSU33` 与 `RicciCurvature` 全文件各出现 1 次（仅此声明处），零定义
- `lake build` 成功（8725 jobs），`#check` 报 unknown identifier
- 从未被任何 theorem 引用 → 删除后 axiom 106→104

同批还发现 `kls_ricci_relation` 与 `geometric_mass_gap_relation` 签名完全相同（`lambda_KLS ≥ c_universal * (M_geo : ℝ)^2`），是真重复，二者都零引用，删一留一。
