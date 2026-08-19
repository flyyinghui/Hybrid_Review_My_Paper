# P0 Fix Verification Loop

## When to Use
After a hybrid review identifies P0 issues and fixes are applied, run a structured verification loop before declaring the paper ready.

## Protocol

### Phase 1: Apply Fixes (Batch)
Use lxml string replacement on DOCX XML for bulk fixes:
- κ values, M_R values, matrix entries → simple find/replace
- "parameter-free"→"phenomenological" → terminology fix
- Add honest-scope notes to appendices

For Lean files: same approach — direct string replacement.

### Phase 2: Verify (Systematic)
Run a numeric audit comparing DOCX+Lean against the review's P0 checklist:

```python
# Count old values must be 0
assert doc.count("3505.8") == 0
assert doc.count("parameter-free predictions") == 0
assert doc.count("8.0×10¹³") == 0  # OLD M_R

# Count new values must be present
assert doc.count("3266.67") >= 10
assert doc.count("phenomenological predictions") >= 1
assert doc.count("4.58×10¹³") >= 3  # NEW M_R
```

### Phase 3: Discover Residuals
Verification ALWAYS finds residual issues:
1. **String format variants**: Paper uses "8.0x10^13" not "8.0×10¹³" → fix ALL variants
2. **Header contradictions**: Lean header "0 sorry" but code has 6 → fix header
3. **Stale terms**: "SORRY-FREE" in changelog comments → clear them
4. **Appendix M count drift**: Subagent counts may differ from verified methodology → verify with same regex

### Phase 4: Re-verify
Run the full check again until 0 failures.

## Common Residual Issues

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Old value still present | Different Unicode/ASCII variant | Search all variants |
| Count mismatch | Subagent used different regex | Use verified regex from earlier audit |
| Header says "0 sorry" | Header never updated | Fix Lean header directly |
| "SORRY-FREE" in comments | Changelog/audit sections stale | Replace with neutral language |

## V63 Case Study
- Phase 1: 20+ lxml replacements across DOCX + Lean
- Phase 2: 20 checks, 3 failures found
- Phase 3: Fixed M_R variant (x vs ×), Lean header, SORRY-FREE comments
- Phase 4: 26 checks, all passed ✅
