# V14→V15→V16 Triple GW Paper Review + Fix Pipeline (2026-08-06)

Full end-to-end cycle: hybrid review → prioritized fix → re-review → numerical verification.

## Version Trajectory

| Version | Score | Key Changes |
|---------|:---:|------|
| V13 | 1.6 | 6 P0s, paper-Lean H₀ conflict |
| V14 | 1.4 | 8 P0s: false Lean code, broken arithmetic |
| V15 | 3.7 | 4 P0s FIXED: definitions, H₀ honesty, DM:B, λ_KLS |
| V16 | ~5.5 | 3 P0s FIXED: Bourgain deletion, energy sum, Ω scale |

## P0 Defect Tracking

| P0# | V14 Defect | V15 Status | V16 Status |
|-----|-----------|:---:|:---:|
| P0-1 | z_eff: paper 10^278 vs Lean 4.29 | PARTIAL | PARTIAL |
| P0-2 | 10 undefined symbols | **FIXED** | **FIXED** |
| P0-3 | H₀ derivation = unfold-rfl | **FIXED** | **FIXED** |
| P0-4 | DM:B 75>70 DOF | **FIXED** | **FIXED** |
| P0-5 | Ω sum false (6.40≠2.50) | PARTIAL | **FIXED** |
| P0-6 | Bourgain false theorem | **UNFIXED** | **FIXED** |
| P0-7 | GW peak claims conflict | PARTIAL | PARTIAL |
| P0-8 | λ_KLS conflicting defs | **FIXED** | **FIXED** |

## Discovery: Header-Claim ≠ Code-Reality (P0-6a)

V15 file header claimed "P0-6 FIX: Removed mathematically false Bourgain theorems" but the theorems were STILL in the active code. This pattern arose because the header was patched in one round while the code block survived elsewhere.

**Detection protocol**:
```python
active_code = re.sub(r'--.*', '', content)  # strip comments
assert 'Bourgain_slicing_conservation' not in active_code
```

## Discovery: "Intentionally False" Theorem Pattern

V14 Lean contained:
```lean
-- This theorem is intentionally false to show the need for proper normalization
theorem tensor_to_scalar_ratio_lt_Planck_limit : ...
```

This is worse than a stub — it actively proves a falsehood. Entire Section 8 (observational comparisons) was deleted and replaced with honest-axiom placeholders.

## Discovery: Ω_GW vs Ω_DM Scale Mismatch

Calibrated Ω_GW sum = 2.5×10⁻⁹, but Planck Ω_DM = 0.264.
Ratio = 9.5×10⁻⁹ — the values differ by 8 orders of magnitude.
The fix was to acknowledge that ρ values are in arbitrary normalization with the 10⁸ factor representing energy dilution.
