# V14→V15 Fix Regression Patterns

Two-session, three-agent review cycle that discovered new categories of fix-regression bugs.

## Timeline

1. **V14 Review** (2026-08-06): 8 P0 defects, score 1.4/10
2. **V14→V15 Fix Session**: 10-step systematic Lean patching + DOCX synchronization
3. **V15 Review** (2026-08-06): 3 new blocking defects discovered, score 3.7/10

## New Regression Patterns

### Pattern A: Head-Comment vs Code Dissonance

P0-6 Bourgain was "fixed" in the file header comment block but the actual false theorem code was NOT removed. The V15 lean file claims in its changelog:

```
- P0-6 FIX: Removed mathematically false Bourgain "theorems" (A*B ≥ 1 from A>0,B>0).
  Bourgain slicing retained as [honest-axiom: physical-analogy].
```

But `Bourgain_slicing_conservation` theorem (the exact false theorem claiming `A_time * A_space ≥ 1` from `h: A_time > 0, h': A_space > 0`) is still present in the code body. The `time_explosion` theorem that depends on it is also still present.

**Root cause**: During multi-step patching, the file header was updated to document intended fixes, but the corresponding `patch(old_string=...)` call for the theorem body either didn't match (whitespace/comment differences) or was never issued. The header comment became a "wish list" rather than a "changelog."

**Prevention**: After any fix round claiming code deletion, verify with `grep`:
```bash
grep -c "theorem_name" file.lean  # should be 0 if "removed"
```

### Pattern B: Partial Value Fix → Adjacent Theorem Staleness

`energy_sum_rule` was correctly fixed with new ρ_GW values (1.0e-10, 1.4e-9, 1.0e-9), but `Omega_GW_total_eq_Omega_DM` (~30 lines later) still used the V14 values (2.3e-12, 5.4e-9). The old theorem was never updated.

**Root cause**: Fixing one theorem required changing multiple downstream references. The fix was applied surgically (single `old_string` → `new_string` patch) but the adjacent theorem's hardcoded values were not in the patch scope.

**Prevention**: After any value fix, `grep` for old numerical values globally:
```bash
grep -n "2.3e-12\|5.4e-9" file.lean  # should return 0 matches
```

### Pattern C: Ω_GW Scale Mismatch (Units Gap)

The sum of three peak Ω_GW values is 2.5×10⁻⁹, but Ω_DM (from Planck 2018) is 0.264 — a factor of ~10⁸. The paper's "calibration" language papers over this without explaining the conversion factor.

**Root cause**: Ω_GW values are likely defined in non-standard units (not Ω = ρ/ρ_crit), or a hidden scaling factor converts between "peak Ω_GW" and "total Ω_GW." The paper never specifies the unit convention.

**Prevention**: Always independently compute Ω_DM from Planck parameters:
```
Ω_DM = Ω_c h² / h² = 0.120 / 0.674² ≈ 0.264
```
Compare against paper's claimed total. Flag any discrepancy > 10%.

## Successful Fix Patterns (Preserve These)

### Lean Definition Completion (P0-2)

Adding 10 missing definitions in a single insertion block (new Section 1b) before they're referenced. Pattern:
```lean
/- SECTION 1b: GRAVITATIONAL WAVE OBSERVABLES [V15 FIX] -/
def f_peak_PT : ℝ := 1.71
def f_peak_inflation : ℝ := 4.5e11
def Omega_peak_PT : ℝ := 1.4e-9
... (all 10 definitions)
```

### Honesty Downgrade Chain (P0-3, P0-4)

Removing false derivation claims and replacing with honest declarations:
- `theorem h0_frw_derivation ... := by unfold H0_pred; rfl` → DELETE, replace with `axiom H0_pred = 67.42`
- `def cdm_to_baryon_ratio := 5.0 [honest-axiom]` → `def ... := 5.0 [phenomenological]`

### Duplicate Code Cleanup (P1)

Removing the entire duplicate Bourgain section (Section 3 and Section 5 had identical blocks). Pattern: find the second occurrence, replace with honest-axiom wrapper.

### DOCX Synchronization

Two-tier approach:
1. **XML-level**: `str.replace()` on `word/document.xml` for text that fits in a single `<w:t>` element (~70% of fixes)
2. **python-docx paragraph-level**: For text split across multiple `<w:r>` elements, iterate `doc.paragraphs`, search `para.text`, modify individual `run.text`

## Session-Specific Files

- V14 review: `Hybrid_Review_TripleGW_V14_20260806.md`
- V15 fix checklist: `V14_to_V15_Paper_Fix_Checklist.md`
- V15 review: `Hybrid_Review_TripleGW_V15_20260806.md`
- All in: `C:\Users\<user>\Desktop\papers\三峰引力波证明\三峰引力波证明_20260806\`
