# 投稿前修改痕迹清理：三类分类 + 保留诚实声明 + 改写重复陷阱

关联 `date-stamp-revision-trace-cleanup.md`（五类残留）与 `version-commentary-strip-prd-reconstruction.md`（版本论述剥离）。
本文件记录 2026-09-16 两篇论文（CGICE v10 + 三大时空相 V18）痕迹清理实战的增量：**三类痕迹的精确分类、
"删工作日志/留诚实声明"的判断原则、以及 str.replace 改写句子产生重复的具体陷阱。**

## 三类修改痕迹的精确分类

1. **历史版本信息**（版本演进记录）
   - 版本号：`V14.1` / `V15` / `V17` / `V63`（指代本论文旧版或"旧口径"）
   - 对比措辞：`old version's misuse` / `the earlier statements` / `previously stated/quoted` /
     `superseding the earlier X` / `was originally mapped` / `now withdrawn`
   - 结构标签：`annotated historical remark` / `retired historical remark` / `historical audit notes`

2. **修改时间标注**（日期戳）
   - `2026-08-29` / `09-12` / `09-13` / `09-14` / `09-15` / `09-16`
   - 内嵌标题日期：`[Formal proof — 2026-09-13]` → `[Formal proof]`；`B.6 ... — 2026-09-13` → `B.6 ...`

3. **修改错误标注**（fix/repair/错误对比）
   - `R09 fix` / `J08 fix` / `J04/J05 fix` / `R23 fix` / `P0-2 repair` / `P0 repair` / `P0-2 correction`
   - `wrong sign convention` / `deprecated erroneous value` / `rounding error` /
     `normalization-mixing error` / `misuse of` / `is wrong` / `the earlier incorrect claim`

## 删除 vs 保留的判断原则（关键）

- **删除**：工作日志痕迹 —— "哪一轮审稿改了什么"、"什么日期改的"、"之前错了现在改成 X"。
  这些是过程记录，终稿/投稿稿不应出现。
- **保留**：诚实边界声明 —— `withdrawn`（预测撤回）、`not an active declaration`、
  `commented out in Lean`、`[O]`/`[M]`/`[A]`/`[F]`/`[C]` 状态标注、`honest-axiom`。
  这些描述论文/Lean 的**当前实际状态**，是学术诚实性的必要部分，不是工作日志。

判定一句话是不是"工作日志"：它是否在回答"**当前结论是什么**"（保留）还是"**我们这一版改了/修了什么**"（删除）。
例：`f₂ = t_P⁻¹|I|(T_cryst/T₀)/λ is withdrawn`（保留，当前状态）；`...has the temperature ratio in the wrong direction and is withdrawn`（删"wrong direction"，留"is withdrawn"）。

⚠️ 不要连带删除：`§EVIDENCE_CHAIN_20260830` 这类** Lean 代码里的实际 section/namespace 标识符**
（删了会导致论文与 Lean 代码脱节）；`was resolved by Klartag and Lehec` 这类正常学术叙述；`erroneous extra density` 这类数学论证内容。

## 关键陷阱：str.replace 改写句子产生重复

**症状**：改写后相邻两行出现相同子句（同一句子的后半段重复出现）。

**根因**：替换目标短语太短（如 `is wrong: the`），改写时把"原文**后续本该保留**的完整子句"也写进了
new_string，导致 new_string 结尾与原文后半句拼接重复。

**案例**（Cosmic Noon 句，2026-09-16）：
- 原文：`..."Cosmic Noon = z_eff 4.29" is wrong: the Madau–Dickinson star-formation-rate peak is at z ≈ 1.9; ...computed from the specified convolution`
- 错误替换：`"is wrong: the"` → `"is not the Madau–Dickinson...peak, which is at z≈1.9; ...computed from the"`
- 结果：new_string 的 `computed from the` 与原文后面已有的 `Madau–Dickinson...computed from the specified convolution` 重复。

**修复模式**：
1. 改写只替换"错误标注短语"本身，new_string **止于错误标注短语结束**，原文后续内容原样保留；
2. 替换后必须 grep 改写句，检查是否出现"相邻两行重复子句"；
3. 发现重复后，把重复片段合并（保留一段），用 patch 精确删除多余部分。

## 工程化执行（Python 脚本）

```python
def apply_repls(path, repls):
    text = open(path, encoding='utf-8').read()
    for old, new in repls:
        c = text.count(old)
        if c == 1: text = text.replace(old, new)
        else: print(f"WARN {c}x {old[:60]!r}")   # 0=未匹配(MISS)，>1=歧义(MULTI)
    return text
```

- 每个替换用 **count==1 门控**：count==0 报 MISS（文本可能已变），count>1 报 MULTI（字符串不够唯一）。
- **超长单行**（如 5000+ 字符的"Lean declaration count"流水账段）：按行定位后 `ln.find(marker)` 截断到关键标记，不手写整行。
- **跨行整块删除**：`re.sub(r"起始句.*?结束句\.\n", '', text, flags=re.DOTALL)`。
- 备份 `.bak` 后再执行；改写完成后做一次全面 grep 残留核验（日期/fix/版本号三类）。

## 本次实战统计（可作复杂度预估）

三大时空相 V18：53 处替换 + 1 处超长行截断（5029→240 字符）+ 1 块编译记录删除 → 1443→1406 行；
CGICE v10：2 处句内改写（Conclusion 段 + A.4 构建产物段）。全程 0 sorry 相关的 Lean 状态不受影响。
