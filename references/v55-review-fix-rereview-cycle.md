# V55 Review → Fix → Re-Review Cycle (2026-07-22)

Complete pipeline: initial 5-agent review → fix roadmaps → targeted re-review → final score.

## Pattern: Round 1 Review → Fix → Round 2 Re-Review

When the first review finds systemic issues, the cycle is:

```
Round 1 (5 agents): find all issues
  ↓
Fix pipeline (C3-C6 + Appendix C + C1-C2): apply fixes
  ↓
Round 2 (3 agents): verify fixes, find residuals
  ↓
Final report: score delta, remaining issues, publication recommendation
```

### Round 1 → Round 2 Score Delta

| Dimension | R1 (pre-fix) | R2 (post-fix) | Δ |
|:--|:--:|:--:|:--:|
| Consistency | 3/10 | 4/10 | +1 |
| Logic | 3/10 | 4/10 | +1 |
| Writing | 3/10 | 5/10 | **+2** |

Writing improved most because the 7-way D1 terminology split was the dominant noise source.

## Critical Fix: DOCX Extraction Overwrite

When extracting multiple DOCX files to the same path in a loop, the LAST file overwrites earlier ones. V55 review had this bug: `Section_22_Restructured_V55.docx` (13K chars) overwrote `Neutrino_Condensation_Reviewed_Optimized_EN_V55.docx` (199K chars) → subagents got only §2.2 fragment.

**Fix**: Always use unique output paths per file:
```python
for f in os.listdir(d):
    if target_pattern in f:
        out = f'/tmp/{f.replace(".docx", ".txt")}'
```

## Round 2: 3-Agent Light Review

After fixes applied, a full 5-agent review is overkill. 3 agents (consistency + logic + writing) suffice:
- Consistency: verifies fixes applied, checks residuals
- Logic: re-evaluates core claims after fixes
- Writing: checks terminology unification, marker cleanup

Skip bibliography and technical in Round 2 unless the fix pipeline touched those areas.

## Fix Pipeline Execution Order

The fix order matters: C3 (numerical) → C4+C6 (D1 status) → C5 (dual-path) → C7 (predictive degree) → Appendix C sync.

Later fixes depend on earlier ones: Appendix C tables reference the D1 status and predictive degree fixed earlier.
