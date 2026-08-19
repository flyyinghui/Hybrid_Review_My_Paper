# Revision Landing Check Pattern

**Pattern established**: 2026-07-30, V17 6D Spacetime paper post-revision audit.

## When to Use

User says "已根据修改意见做了完善，再核对哪些没落地" — they've revised based on a prior review and want a structured gap analysis of what was fixed vs. what remains.

## Pipeline

### Phase 1: Re-extract Current Artifacts

Re-extract paper DOCX → plain text. Re-check Lean stats from .lean file. Do NOT reuse old extractions — the point is to detect what CHANGED.

### Phase 2: Automated Scan Against Prior P0-P3 Checklist

For each item in the prior review's checklist, run targeted regex/grep scans on the updated paper text:

- P0-1: Lean stats unified? → regex for all `\d+ (lines|theorems|axioms)` mentions
- P0-2: "0 sorries" claim fixed? → case-insensitive search
- P0-3: Abstract truncated? → check abstract section completeness
- P0-4: FIG.9 stale? → search FIG references for old version numbers
- P0-5: b₀ arithmetic → search for `b₀|b0.*12[78]`
- P0-6: c³/Gℏ dimension → literal search
- P0-7: Phantom V16 → version reference scan

### Phase 3: Classify Each Item

| Status | Meaning |
|:-------|:--------|
| ✅ FIXED | Prior defect no longer detectable |
| ⚠️ PARTIAL | Some occurrences fixed, some remain |
| ❌ NOT FIXED | Defect fully present |
| 🆕 NEW | Issue not in prior review |

### Phase 4: Lean Stat Conflict Detection (Specialized)

This is the most frequently residual issue. Users often fix the first occurrence and leave others:

```python
actual = {'lines': 5867, 'axioms': 395, 'theorems': 95, 'lemmas': 18, 'honest': 230}
pattern = r'(5[,.]?\d{3}|48|95|379|395|252|230)\s*(lines|theorems|axioms|lemmas|honest)'
for val, category in re.findall(pattern, paper):
    num = int(re.sub(r'[,.]','', val))
    if num != actual.get(category.lower()):
        print(f"Stale {category}: {num} (actual: {actual[category.lower()]})")
```

Common residual conflicts: `5619 lines` vs `5867 lines`, `48 theorems` vs `95 theorems`, `379 axioms` vs `395 axioms`, `252 honest-axiom` vs `230 honest-axiom` — all four usually coexist in partially-fixed papers.

### Phase 5: Additional Scans

- Version artifact scan: `\bV1[0-6]\b` — pre-V17 version references
- Duplicate paragraph scan: identical paragraphs with len > 50 chars
- Orphan reference scan: `\[3[2-5]\]` — refs never cited
- ALL-CAPS label scan: `\b[A-Z]{3,}(?:\s+[A-Z]{3,})+\b`
- AI tool name scan: `DeepSeek|neural memory brain`
- CGICE-3 ghost: `CGICE[- ]?3`

## Output Format

Concise MD with:
1. Summary table (✅/⚠️/❌/🆕 counts)
2. Completed items
3. Partially completed with exact residual locations
4. Not fixed with exact locations
5. New issues (if any)
6. Prioritized next-action items (cost-benefit)

## Pitfalls

1. **"Fixed" is often partial.** Global find-replace misses instances. Always scan for ALL occurrences.
2. **Lean stat conflicts are the #1 residual.** Users fix the first occurrence but leave others. Expect coexistence.
3. **b₀ arithmetic errors survive global replace.** Downstream numerical consequences need separate verification.
4. **New duplicate paragraphs appear during revision.** Copy-paste during editing creates new artifacts.
