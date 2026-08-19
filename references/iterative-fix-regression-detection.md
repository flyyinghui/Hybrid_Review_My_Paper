# Regression Bug Detection in Iterative Paper+Lean Fix Cycles

**Sessions**: 2026-08-06 (V14→V15→V16)
**Pattern**: When fixing P0 issues across paper+Lean version iterations, verify that fixes did not introduce NEW bugs.

## Detected Regression Types

### Type 1: Header-Code Mismatch (Bourgain Trap)
- V15 header CHANGELOG claimed "Removed mathematically false Bourgain theorems"
- V15 code STILL contained `Bourgain_slicing_conservation` (false theorem: A*B≥1 from A>0,B>0)
- V15 code STILL contained `time_explosion` depending on the false theorem
- **Detection**: `grep -n "Bourgain_slicing_conservation\|time_explosion" file.lean` in active code (not comments)
- **Fix**: V16 ACTUALLY removed them. Replace with single `[honest-axiom: physical-analogy]` axiom

### Type 2: Stale Theorem with Old Values
- V15 correctly fixed `energy_sum_rule` (1.0e-10+1.4e-9+1.0e-9=2.5e-9)
- V15 NEW theorem `Omega_GW_total_eq_Omega_DM` still used V14 values (2.3e-12, 5.4e-9)
- Theorem used `rfl` on `Real.exp` — fails in `noncomputable section`
- **Detection**: Search for OLD numerical values in active code after value changes
- **Fix**: Delete the stale theorem, reference the correctly-proven `energy_sum_rule` instead

### Type 3: Observational Comparison Drift
- Section 8 theorems (`tensor_to_scalar_ratio_lt_Planck_limit`, `Omega_GW_at_mHz_above_LISA_sensitivity`) used V14 peak values
- `tensor_to_scalar_ratio` was self-admittedly "intentionally false"
- **Fix**: Replace entire section with `[phenomenological]` placeholder axioms, defer to future study

### Type 4: Scale Mismatch (T5)
- Paper claims ΣΩ_GW = Ω_DM but values differ by 10⁸× (2.5e-9 vs 0.264)
- Lean uses arbitrary calibrated units, not standard Ω
- **Fix**: Add honest note explaining normalization; don't claim direct equality

## Audit Checklist After Each Fix Iteration

```python
checks = [
    # Header-claims vs code reality
    ('Bourgain_slicing_conservation', False),
    ('time_explosion', False),
    ('intentionally false', False),
    # Old values in active code
    ('2.3e-12', False),
    ('5.4e-9', False),
    # New theorems reference correct values
    ('Omega_GW_DM_equivalence_V16', True),
    ('energy_sum_rule', True),
    # No orphaned fragments
    ('deriv_mul', False),
    ('h_product_deriv', False),
]
```

Run after every Lean patch. Use `re.sub(r'--.*', '', code)` to strip comments before checking.
