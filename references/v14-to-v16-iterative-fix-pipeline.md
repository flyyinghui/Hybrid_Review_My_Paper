# V14→V15→V16 Iterative Fix Pipeline Learns

*Captured from Triple GW paper 3-version fix cycle (2026-08-06)*

## Score Trajectory

| Version | Score | Key Fix |
|---------|:-----:|---------|
| V14 | 1.4/10 | Baseline: 8 P0 defects |
| V15 | 3.7/10 | 4 FIXED, 3 PARTIAL, 1 UNFIXED |
| V16 | ~5.5/10 | All 3 remaining P0s fixed |

## Multi-Round Fix Patterns

### Pattern 1: Regression Introduction
V15 correctly fixed `energy_sum_rule` but **introduced** a new bug — `Omega_GW_total_eq_Omega_DM` was a parallel theorem that still used V14 values (2.3e-12, 5.4e-9). When fixing one theorem, check ALL other theorems that reference the same values.

### Pattern 2: Header-Code Drift
V15 header claimed Bourgain false theorems were removed, but the code still contained them. Root cause: the header was edited but the delete-patch never applied. See `references/bourgain-header-claim-trap.md`.

### Pattern 3: Scale Mismatch Detection
Ω_GW(total) = 2.5×10⁻⁹ vs Ω_DM(Planck) = 0.264 — a 10⁸ discrepancy. The paper claimed equality but had never computed the ratio. Fix: add honest normalization note acknowledging the calibration is in arbitrary units.

### Pattern 4: "Intentionally False" Theorems
V15 Section 8 contained a theorem (`tensor_to_scalar_ratio_lt_Planck_limit`) whose proof body said "This theorem is intentionally false to show the need for proper normalization." This is **never acceptable** in a Lean formalization. Fix: delete the entire section and replace with honest-axiom placeholders.

## Dual-Track (Lean + DOCX) Sync Protocol

1. Fix Lean first (define all symbols, correct arithmetic, remove false theorems)
2. Generate a DOCX modification checklist mapping each Lean change to paper sections
3. Apply DOCX fixes: XML-level `str.replace` for simple text, python-docx paragraph-level for cross-`<w:r>` text
4. Cross-audit: verify all numerical values match between Lean and paper
5. Run numerical verification (Python or v4-pro) on all claimed equalities

## Key Pitfalls When Fixing Multi-Round

1. **The "second system" effect**: Each fix round can introduce new bugs in parallel code paths
2. **Lingering old values**: Changing a definition doesn't automatically update all theorems that used it
3. **Comment vs code divergence**: Header changelogs are not verified by the type checker
4. **Scale errors**: Equal-sign claims must be dimensionally and numerically verified
