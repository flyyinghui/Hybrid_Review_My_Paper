# 框架文件统计同步：四论文 Lean 口径统一 + 装饰声明计数陷阱

**触发场景**：把多篇共享母框架的论文最新 Lean 统计同步进统一框架文件（如 `SL6C_Unified_Geometric_Dynamics_Framework.md`）时，必须先统一计数口径，否则会把"论文自报数"和"实测活跃数"混在一起。

## 核心教训 1：装饰声明被朴素正则漏掉

Lean 声明可带 `@[...]` 装饰器，且装饰器**与声明关键字同行**：

```lean
@[honest_axiom] axiom Metric : ...   -- 行首是 @，不是 axiom
@[honest_axiom] axiom TensorType : ...
```

朴素正则 `^\s*axiom\s+` **匹配不到**这种声明。GW-V19 案例：裸正则数出 47 axiom，论文声称 48——差 1 就是 2 个带装饰器的 axiom 被漏掉；lemma 22 vs 25 同理。

**正确正则**（允许装饰器前缀）：

```python
decl = r'^\s*(?:@\[[^\]]*\]\s*)?'
ax = len(re.findall(decl + r'axiom\s+' + ident, code, re.M))
th = len(re.findall(decl + r'theorem\s+' + ident, code, re.M))
le = len(re.findall(decl + r'lemma\s+' + ident, code, re.M))
```

## 核心教训 2：必须先剥嵌套块注释，再计数

`/- ... -/` 支持嵌套。朴素 `re.sub(r'/-.*?-/','',flags=re.S)` 非贪婪匹配会在第一个 `-/` 提前终止，嵌套注释内部内容漏到活跃列表，注释里的 "0 sorry" 字样被误计为 active sorry。

**正确剥离**（行级状态机跟踪嵌套深度）：

```python
def strip_lean_comments(text):
    out=[]; i=0; n=len(text); depth=0
    while i<n:
        if depth>0:
            if text[i:i+2]=='/-': depth+=1; i+=2; continue
            elif text[i:i+2]=='-/': depth-=1; i+=2; continue
            else: i+=1; continue
        else:
            if text[i:i+2]=='/-': depth=1; i+=2; continue
            elif text[i:i+2]=='--':
                j=text.find('\n',i)
                if j==-1: break
                i=j+1; continue
            else: out.append(text[i]); i+=1
    return ''.join(out)
```

## 核心教训 3：论文自报数 ≠ 实测活跃数

论文正文常报告 **grep 原始计数**（含注释内弃用声明），而框架文件应统一用**活跃声明数**（strip 注释后）。差异来源：

- V17 论文自报 "65 axiom + 42 theorem"（另一处又写 36 theorem，自相矛盾），实测活跃 **62 axiom + 48 theorem**
- CGICE 论文自报 "99 theorems"（2026-09-07 checkpoint），实测文件 **109 theorem**（后续已更新）

**判定规则**：以实际文件 + 统一口径（剥嵌套注释 + 装饰声明感知正则）的实测为权威。论文自报数仅作参考，若与实测不一致，用实测。

## 四论文权威统计（2026-09-11 实测，活跃声明口径）

| 论文 | Lean 文件 | 行数 | axiom | theorem | lemma | sorry |
|---|---|---|---|---|---|---|
| V17 时空 | 6D_Spacetime_Formal_Proof_V17.lean | 7,940 | 62 | 48 | 18 | 0 |
| CGICE v10 | cgice_proof_v10.lean | 1,163 | 0 | 109 | 0 | 0 |
| V63 中微子 | Neutrino_Condensation_proof_63.lean | 3,751 | 35 | 59 | 23 | 0 |
| GW-V19 | triple_gw_dm_proof_v19.lean | 2,603 | 48 | 88 | 25 | 0 |

（GW-V19 论文自报 48 axiom / 25 lemma 与实测一致；V17 的 62/48 与框架既有值一致——只有 V63 的 59 theorem 和三峰 GW 的 V17→V19 版本演进是需要更新的。）

## 框架文件更新工作流

1. 逐篇实测 Lean 文件（统一口径：剥嵌套注释 + 装饰声明感知正则）
2. 与框架现有表格数字 diff，找出需更新的行
3. 与论文自报数 cross-check，标注口径差异
4. 批量精确替换（按行号/上下文锚定，**禁全局裸数字替换**——`48`/`42`/`53`/`24` 等会误伤不相关行）
5. 全局安全替换先做（版本号 `GW-V17→GW-V19`、文件名），再做行级数字替换
6. 密度值（axiom/100行、theorem/100行）随行数变化重算

**批量替换用 Python 脚本 + 每条替换记录命中次数**（`src.count(old)` 验证唯一命中），比逐个 patch 更安全，且能立即暴露"未命中"的锚点错误。
