# P0+P1 Rapid Fix Pipeline (V38→V39 Pattern)

When an AWA hybrid review produces P0 (showstopper) and P1 (major) findings, apply them programmatically in a single pass across DOCX + Lean files.

## Proven Pattern

### DOCX Fix Script Template

```python
import docx, os
doc = docx.Document(SOURCE)
fixes = [
    ('old_text', 'new_text'),  # simple text replacement
]
for p in doc.paragraphs:
    for run in p.runs:
        for old, new in fixes:
            if old in run.text:
                run.text = run.text.replace(old, new)
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    for old, new in fixes:
                        if old in run.text:
                            run.text = run.text.replace(old, new)
doc.save(OUTPUT)
```

### Lean Fix Script Template

```python
with open(LEAN_FILE) as f: text = f.read()
# Axiom body upgrades, changelog insertion, convention comments
text = text.replace(old_pattern, new_pattern)
with open(LEAN_FILE.replace('_N', '_N+1')) as f: f.write(text)
```

## Common P0 Fixes

| Issue | DOCX Fix | Lean Fix |
|:--|:--|:--|
| Dimension error (26→35) | `run.text.replace('real dimension 26', 'real dimension 35')` | N/A |
| Ratio self-identity (both sides identical) | Restore geometric side to pre-correction value in comparison context | N/A |
| Axiom count mismatch (A1-A24→A1-A28) | Global replace | Global replace |
| Citation misdirection (~30%) | Targeted `run.text.replace('[OLD]', '[NEW]')` | N/A |
| `:=True` stubs | N/A | Replace with constrained ℝ-algebraic bodies |
| √2 convention opacity | N/A | Insert explicit mapping comment |

## Ratio Replacement Trap

Replacing a ratio globally (e.g., 2.32→2.56) breaks "10-15% deviation between geometric X and phenomenological Y" comparison text — both sides become identical numbers. **Must restore pre-correction value** in the geometric side only.

Detection: after global replace, search for identical ratios in adjacent phrases describing "deviation" or "difference."

## Parallel Execution

DOCX fix and Lean fix run in parallel:
```
terminal(background=true, notify_on_complete=true) → DOCX fix
terminal(background=true, notify_on_complete=true) → Lean fix
```
Then sync PRD + Appendix versions in a third script applying the same fixes to the PRD-formatted source.

## P1 Fixes

| Issue | Approach |
|:--|:--|
| Abstract too long | Rewrite in single pass: clear all runs, set `p.runs[0].text = new_abstract` |
| Conclusion ≈ Discussion copy | Compress AI tool mentions; remove verbatim repeats |
| "prediction"→"parameterization" | Global replace in runs |
| Σm_ν multiple values | Standardize to single value; preserve IH bound (correct experimental value) |
| Appendix F honesty | Add `run.add_run('[HONEST SCOPE: ...]')` after assertion paragraph |
| "DERIVED"→"GEOMETRICALLY MOTIVATED" | Global replace |

## IH Bound Note

The inverted hierarchy bound (Σm_ν < 0.064 eV) is a CORRECT experimental value from DESI. Do NOT change it when standardizing the paper's own NH prediction to 0.062 eV. Distinguish: paper's prediction = 0.062 (NH), DESI's IH bound = 0.064 (experimental).
