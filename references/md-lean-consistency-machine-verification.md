# MD-Lean 一致性机器验证 + 审稿人清单截断假阳性（2026-09-20）

## 1. 审稿人清单截断假阳性（重要教训，P0 级）

**症状**：终审时把 Lean 定理名清单**截断成"部分"**（如 `theorems[:40]`、`defs[:30]`、
`axioms[:20]`）传给审稿人，审稿人把 MD 引用的、但不在截断清单里的定理名**全部误判为
"幻影引用"**，产生几十条假阳性 P1（如 "PhaseI.cartan_hadamard_hess_r2 未在列表中"）。

**根因**：审稿人只能验证"清单里有"的，无法验证"清单外"的。清单截断 = 审稿人信息盲区
= 系统性假阳性。实际这些定理都存在（grep 逐一验证过），只是不在截断的前 N 个里。

**修复**：
1. 传给审稿人的定理名清单**必须完整**，或明确标注"清单不完整，引用缺失需 grep 核实"。
2. **机器级验证（grep）优先于 LLM 审稿**：先 grep 确认每个 MD 引用的定理名是否真存在，
   只把真缺失的喂给 LLM 判定严重度。不要把"清单外"的喂给 LLM 当幻影引用。
3. 三个常见"缺失"假阳性类型（grep 时先排除）：
   - `Namespace.name` vs `namespace_name`（MD 用点号写命名空间，Lean 用下划线前缀，
     如 `PhaseII.geodesic_time_ray` = 实际 `phaseII_geodesic_time_ray`）
   - 短名被正则过滤（如 `Rates.A` 的 `A` 太短被过滤，实际 `def Rates.A` 存在）
   - MD 已声明 "not an active declaration"（正确说明已删除，非幻影引用）

## 2. MD-Lean 一致性机器验证脚本模式

先机器验证，再 LLM 终审。核心四步：

```python
import re
md = open('paper.md').read()
lean = open('proof.lean').read()

# ① 剥离 Lean 块注释（处理嵌套）得到活跃代码
def strip_comments(text):
    lines = text.split('\n'); out = []; depth = 0
    for ln in lines:
        s = ln; i = 0; new = []
        while i < len(s):
            if depth > 0:
                if s[i:i+2] == '-/': depth -= 1; i += 2
                elif s[i:i+2] == '/-': depth += 1; i += 2
                else: i += 1
            else:
                if s[i:i+2] == '--': break
                elif s[i:i+2] == '/-': depth += 1; i += 2
                else: new.append(s[i]); i += 1
        if depth == 0 and new: out.append(''.join(new))
    return '\n'.join(out)
lean_active = strip_comments(lean)

# ② 提取 MD 反引号标识符，去掉命名空间前缀后 grep Lean 活跃代码
md_backticks = re.findall(r'`([A-Za-z_][A-Za-z0-9_.]*)`', md)
for full in md_backticks:
    name = full.split('.')[-1]
    pat = re.compile(r'\b(?:def|theorem|lemma|axiom|opaque|structure|class|abbrev)\s+' + re.escape(name) + r'\b')
    if not pat.search(lean_active):
        # 可能缺失，grep 行上下文核实（排除上面三种假阳性）

# ③ 对比 MD 附录 A 计数 vs Lean 权威统计（行首锚定，非 grep -c 全文件）
def count(p): return len(re.findall(p, lean_active, re.MULTILINE))
lean_stats = {'axiom': count(r'^\s*axiom\s'), 'theorem': count(r'^\s*theorem\s'), ...}

# ④ 数值声明交叉核对：MD 关键数值 vs Lean 地面真相（grep 常量）
```

**计数权威方法**：用 `grep -cE '^\s*axiom\s'`（行首锚定）或剥离注释后
`re.findall(r'^\s*theorem\s', active)`，**不要**用裸 `grep -c 'axiom'`（会统计注释
里的 "axiom" 字样）。同一文件插入新定理后，附录 A 的计数会**漂移**（如 171→174），
每次改完 Lean 必须重新统计并同步附录 A 计数。

## 3. 计数漂移检测

**症状**：插入 N 个新定理后，MD 附录 A 的 theorem 计数还是旧的（如 171，实际 174）。

**根因**：Lean 改了，附录 A 的声明计数没同步。

**修复**：每次修改 Lean 后，重新跑权威统计（剥离注释 + 行首锚定），
对比 MD 附录 A 的计数声明，不一致就更新 MD。

**终审报告应显式区分**：机器级一致性（计数、定理名、数值的 grep 交叉核对，精确）
vs LLM 审稿（表述、语义、结构，可能假阳性）。机器级通过 + LLM 8/10 =
mostly_consistent，无需大改。
