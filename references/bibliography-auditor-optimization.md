# Bibliography Auditor — SkillOpt 四方案对比结果

> 实验日期: 2026-07-16 | 模型: deepseek-chat | 10 篇合成论文 + 1 篇真实论文

## 结果总览

| 方案 | 合成评分 | JSON失败 | 真实论文命中 | 结论 |
|:--|:--|:--|:--|:--|
| Baseline (当前) | 6.3 | 1/8 ❌ | 0 | 不稳定 |
| **Few-shot (3案例)** | 5.1 | **0/8** ✅ | **21条** | ✅ **胜出** |
| Manual refinement | 0.0 | 0/8 | 13条 | 过度约束 |
| Two-stage | 0.0 | 0/8 | 12条 | 稳妥但平庸 |

## 核心发现

1. **Few-shot 是唯一零 JSON 破损 + 真实论文有产出的方案**
2. Manual refinement 的详细步骤指令反而让 auditor 报告错误的错误类型
3. Two-stage 引入额外延迟但未提升质量
4. SkillOpt ReflACT（5 epoch）完全失败——原因不是 prompt 质量问题，是 JSON 输出稳定性压倒一切

## 获胜 Prompt（已部署）

```text
You are a bibliography auditor for academic papers. Audit the reference list and in-text citations.

ERROR TYPES (with real examples from past audits):
- GHOST_CITATION: [14] cited but doesn't exist in reference list
- UNCITED_REF: Reference [24] listed but never cited in body text
- DUPLICATE_NUMBER: Two different papers both labeled [28]
- ARXIV_ONLY: Ref [31] is arXiv:1903.xxxxx but published in Phys.Rev.D 2019
- AUTHOR_ERROR: "Weinburg" should be "Weinberg"
- YEAR_VENUE: Year 2020 should be 2021 / venue mismatch
- FABRICATED: "Eldan & Chen (2021)" but Chen is sole author

WORKFLOW:
Step 1: Extract ALL [N] citation numbers from body text. Sort, deduplicate.
Step 2: Extract ALL [N] entries from reference list. Sort, deduplicate.
Step 3: Cross-check body vs refs. Body number not in refs = GHOST.
Step 4: Reverse cross-check refs vs body. Ref not in body = UNCITED.
Step 5: For arXiv-only refs, note if published version likely exists.
Step 6: Compare author names in body prose vs reference list entries.

Output as JSON array. Each item: severity (CRITICAL/IMPORTANT/MINOR), type, detail, ref_number.

EXAMPLE:
[
  {"severity":"CRITICAL","type":"ghost_cite","detail":"[14] not in ref list","ref_number":14},
  {"severity":"IMPORTANT","type":"uncited_ref","detail":"[7] never cited","ref_number":7}
]

PAPER TEXT:
{text}
```

## 后续方向

- 不需要 SkillOpt 自动优化 bibliography-auditor——ReflACT 闭环在结构化输出场景下不可靠
- Few-shot 注入是最简单有效的提升手段
- 如果未来需要进一步提升，收集更多真实审计案例追加到 few-shot 示例中
