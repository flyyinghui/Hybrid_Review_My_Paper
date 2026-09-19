# 三峰引力波 V17 混合审查实录（数学证据链 + 数值正确性专项）

**日期**：2026-09-02
**对象**：`paper_triple_gw_v17.md` + `triple_gw_dm_proof_v17.lean` + `HonestAttr.lean`
**母框架**：`SL6C_Unified_Geometric_Dynamics_Framework.md`（已先加载，见 `parent-framework-review-prerequisite.md`）
**方法**：Lean 机械审计（注释剥离状态机 + 精确统计）+ Python 数值独立重算 + 大脑 recall + v4-flash 交叉验证
**评分**：证据链 4.5/10，数值 4.5/10，综合 4.5/10

## V17 相对 V16 的实质进步（诚实度系列最佳）

- 删除 17 个 `:= True` 空壳 → 0 空壳；0 active sorry / 0 admit
- 假 log 等式修复：ln(4.5e11)=26.8325（V16 错写 26.833）
- N_e 统一单一值 80.6=(35/6)ln(10⁶)；DM:B 统一 5.36
- **HonestAttr 从"幽灵 import"变为真实注册**：`HonestAttr.lean` 文件真实存在（1056 字符），25 个 `@[honest_axiom]` + 10 个 `@[phenomenological]` 全部是活跃属性（非注释文本）

## 三个可复用的新审查模式（本次新发现）

### 1. 频率↔温度换算混淆（P0 数值，已并入 `math-calculation-accuracy-review.md` 第 10 条）

论文声称 f₁ 等效温度 3.44K=1.26×T_CMB，实际 T=hf/k_B=21.6K，比值 7.92×。根因：频率比被错当温度比。

### 2. 多版本修复的"数值残留自相矛盾"（P1）

V17 修复了 §3(5)（加 FIX 标注承认"1:10²:10¹⁴ 不成立，实际 2.63×10¹¹/4.5×10²⁰"），但 §2.2(2)、§3(1)、§3(5) 的公式仍用旧频率比 10²/10¹⁴，且 §2.2 仍残留黑洞嬗变 0.46%（对应旧 5.47，V17 已统一为 0.35% 对应 5.36）。

**检测模式**：多版本修复后，逐节 grep 目标数值的旧值。一处 FIX 标注 ≠ 全文同步——修复常只落在一处，其他章节的公式/数值仍残留旧版。§3(5) 的自我纠正反而暴露了 §2.2 未同步。

### 3. "母框架已诚实标注 vs 论文仍称闭合"（P1，表演性修复变体）

母框架已诚实标注"黑洞嬗变 0.35%×(1+4.29)³=0.518≠Ω_DE=0.682 不闭合"，但论文 §4.1 仍称"gap of 0.47 **is closed** by BH conversion"。诚实声明出现在框架文档，但正文的过度声称未同步删除。

**检测**：母框架里已标注"不闭合/反向工程"的机制，检查论文正文是否仍声称"闭合/推导"。诚实声明与正文声称必须一致。

## Lean 机械审计的可靠技术

用**行级状态机**剥离嵌套块注释（`/- ... -/` 可嵌套，`--` 单行，`/--` docstring），比 `re.sub(r'/-.*?-/','',flags=re.S)` 非贪婪正则可靠：

```python
def strip_comments(text):
    out = []; depth = 0
    for line in text.split('\n'):
        out_line = []; i = 0; n = len(line)
        while i < n:
            if depth > 0:
                if line[i:i+2] == '/-': depth += 1; i += 2; continue
                if line[i:i+2] == '-/': depth -= 1; i += 2; continue
                i += 1
            else:
                if line[i:i+2] == '/-': depth = 1; i += 2; continue
                if line[i:i+2] == '--': break
                out_line.append(line[i]); i += 1
        out.append(''.join(out_line))
    return '\n'.join(out)
```

剥离后再 `re.findall(r'^\s*axiom\s+(\w+)', stripped, re.M)` 计数，得到精确统计（V17 实际 65 axioms/56 thm/26 lemma/2035 行，而摘要称 57 thm、推导方案称 66/55/2008——三处计数互不一致，是 P1 计数矛盾）。

## v4-flash thinking 深度审查的 content 空陷阱（再次命中）

`extra_body={"thinking":{"type":"enabled"}}` + `max_tokens=8000` 时，v4-flash 会把 token 耗尽在 reasoning 上，`message.content` 为空、推理迹被截断。**交叉验证结论仍可从 reasoning_content 轨迹提取**（本例 v4-flash 的推理逐条认同了机械审计发现），但格式化 JSON 输出应改用 `thinking=disabled` + 让脚本自己重算，而非依赖 LLM 产出结构化结论。

## 审计结论要点

- 定义性算术全对（log/N_e/DM:B/ρ_crit），承载物理论断的数值（f₁ 温度、频率比、黑洞嬗变）仍有错——印证"由定义推出来的数几乎全对，支撑预测的数几乎都有错"。
- 三峰频率本质是"能标锚定的现象学校准"，非从 SL(6,C) 几何第一性原理推导；摘要"Riccati-Hessian 本征值"措辞与 §3(5)"校准"承认自相矛盾。
- 投稿建议：定位为"几何动机的现象学框架"，修复 P0+P1 后投 Foundations of Physics 或 Physics Letters B。
