# Cosmetic Numerical Fix Detection — Symbol Changed, Arithmetic NOT Propagated

## Pattern

When a review identifies a numerical error (e.g., b₀=127 should be 39), the author may
change the **symbol** (replace "127" with "39" in the formula declaration) without
recomputing any **downstream numbers** that depend on it.

The paper then contains an internal contradiction: the formula says b₀=39 but all
computed values still use b₀=127 arithmetic.

## Verified Case (2026-07-30, V17 6D Spacetime Paper)

| Quantity | Paper (after "fix") | True value with b₀=39 |
|:---------|:-------------------|:---------------------|
| b₀ (declared) | 39 at line 167 | 39 ✓ |
| b₀ (used in calculation) | 127 at line 50 | 39 |
| g_TC² | 0.0096 | **0.0288** |
| g_TC | 0.098 | **0.170** |
| Shortfall | 26.5× | **15.3×** |
| Landau pole ratio | ~12.1 | **~3288** |

**Smoking gun**: Line 167 writes `b₀=39` but the same line computes
`exp(8π²/(127·0.25))` — the 127 is baked into the arithmetic.

## Detection Protocol

For any corrected parameter P in a paper revision:

1. **List all downstream quantities** that depend on P
2. **Recompute at least 3 of them independently** (Python/calculator)
3. **Compare against the paper's values** — any mismatch means the fix was cosmetic
4. **Flag as P0** if > 1 downstream number is stale

## Example Verification Script

```python
# Independent recomputation to verify b₀ correction
b0 = 39  # corrected value
g0 = 0.5
# One-loop running
g_TC_sq = g0**2 / (1 + (b0 * g0**2 / (8 * 3.14159**2)) * 62.2)
g_TC = g_TC_sq ** 0.5
print(f"g_TC = {g_TC:.3f}")  # Should be ~0.170, not 0.098
```

## Prevention

In review response letters, when claiming a numerical correction:
- Show the corrected derivation end-to-end
- List all propagated values
- Include at least one independent verification (code snippet, spreadsheet)
