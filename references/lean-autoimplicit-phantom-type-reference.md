# Lean 4 `autoImplicit` 幻影类型引用检测（axiom 签名级，2026-09-18 发现）

## 机制（核心新知识）

Lean 4 的 `autoImplicit` 选项（默认开启）会让 **`axiom`/`def`/`theorem` 签名中的未知标识符被静默当作「隐式绑定的变量（未知类型）」**，而不是报 "unknown identifier" 错误。

结果：一个 axiom 签名引用了**全文件零定义**的类型，`lake build` 依然成功。

```
axiom foo (X : UndefinedType) : UndefinedFunc X ≥ (1/8 : ℝ)
-- 编译通过！UndefinedType / UndefinedFunc 被 auto-bound 成隐式变量
```

## 症状（如何识别）

1. `lake build` 成功（如 8725 jobs），但某 axiom 签名里的类型标识符 `grep -c` 计数 = 1（只出现在声明行本身，无定义、无其他引用）。
2. 从**模块外** `#check` 该符号 → 报 "unknown identifier"；但 `lake build` 该模块本身 → 成功。二者矛盾即为 autoImplicit 幻影。

## 检测工作流（三步）

```bash
# 1. 提取所有 axiom 签名里的类型标识符，grep 全文计数
grep -c 'SymmetricSpaceSL6CSU33' file.lean   # → 1 = 只声明处出现 = 疑似幻影

# 2. 从模块外 #check（新文件 import 该模块）
cat > tmp_check.lean <<'EOF'
import <ModuleName>
#check SymmetricSpaceSL6CSU33
#check RicciCurvature
EOF
lake env lean tmp_check.lean   # → "Unknown identifier" 确认幻影

# 3. 最小复现确认 autoImplicit 机制（非 typo）
cat > /tmp/t.lean <<'EOF'
axiom foo (X : UndefinedType) : UndefinedFunc X ≥ (1/8 : ℝ)
EOF
lean /tmp/t.lean
# → 输出 "Function expected at UndefinedFunc ... autoImplicit option causes an
#    unknown identifier to be treated as an implicitly bound variable"
```

## 判定与修复

- **判定**：签名类型引用计数=1 + 模块外 #check 失败 + lake build 成功 → autoImplicit 幻影引用。
- **修复**：删除该悬空 axiom（它引用不存在的类型、从未被其他声明引用，是死代码）。删除后 axiom 计数相应减少，需重新核验附录 A 计数。
- V18 案例：`ricci_lower_bound (X : SymmetricSpaceSL6CSU33)` 删除后 axiom 106→104。

## 与已知「12 幻影引用」的区别

- 已知模式（旧）：**theorem 证明体**引用未定义名 → 直接编译失败（unknown identifier），易发现。
- 新模式（本次）：**axiom 签名**引用未定义**类型** → autoImplicit 静默绑定 → 编译成功，极难发现。
- 后者更隐蔽，因为 `grep -c 'sorry'` 和 `#print axioms` 都不会暴露它。

## 关联

- `references/relabeled-axiom-recurrence-and-isolated-audit.md` — 孤立公理（零引用）检测的姊妹模式；本模式是「孤立 + 引用幻影类型」的升级变体。
- SKILL.md 规则组 A5（孤立公理检测）应扩展：引用计数 = 1 的 axiom 还需检查其**签名类型**是否也是幻影。
