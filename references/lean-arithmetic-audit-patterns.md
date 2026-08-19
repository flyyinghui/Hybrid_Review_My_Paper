# V15→V16 Lean Arithmetic Audit Patterns (2026-08-06)

## Pattern 1: Header Claims ≠ Code Reality (P0-6a)

**Signal**: File header claims "Removed mathematically false Bourgain 'theorems'" but `grep` finds the code still present.

**Root cause**: Multiple rounds of patching — header was updated in one round, but the old code block survived because a second copy existed elsewhere in the file.

**Detection**: After any "removed X" claim in a changelog, grep the active code (excluding comments) for the supposedly removed identifier.

```python
# Strip comments before checking
active_code = re.sub(r'--.*', '', content)
active_code = re.sub(r'/-.*?-/', '', active_code, flags=re.DOTALL)
```

**Fixed in**: V16 (actual deletion), not V15 (header-only fix).

---

## Pattern 2: "Intentionally False" Theorems (V14→V16)

**Signal**: Lean theorem body or comments says "This theorem is intentionally false to show the need for proper normalization."

**Severity**: CRITICAL. A theorem that proves the NEGATION of its statement is worse than a stub — it actively misleads.

**Example**:
```lean
theorem tensor_to_scalar_ratio_lt_Planck_limit : Omega_peak_inflation/Omega_peak_PT < r_Planck_limit := by
  -- This theorem is intentionally false...
  have h_actual_ratio : Omega_peak_inflation/Omega_peak_PT > r_Planck_limit := by nlinarith
```

**Fix**: Delete entire theorem + any dependent theorems. Replace with `[phenomenological]` axiom placeholders.

---

## Pattern 3: Norm_Num False Positives from Calibrated Constants

**Signal**: `norm_num` proves an equality between constants that are numerically unequal (e.g., `6.4e-9 = 2.5e-9`).

**Root cause**: The constants are `def`-ed (not `axiom`-ed) so `norm_num` unfolds them to their definitions. If the definitions are wrong, `norm_num` silently proves the wrong equality.

**Detection**: Manually verify the arithmetic BEFORE trusting norm_num.

```python
# Verify: sum of three calibrated Ω_GW values equals claimed total
assert abs(Ω1 + Ω2 + Ω3 - Ω_total) < 1e-20
```

---

## Pattern 4: rfl Failure on Noncomputable Sections

**Signal**: Theorem uses `rfl` tactics on `Real.exp` or other transcendental functions inside a `noncomputable section`.

**Why it fails**: `Real.exp`, `Real.log`, `Real.sqrt` are noncomputable in Lean — `rfl` cannot reduce them. The theorem silently fails to compile.

**Fix**: Either (a) use `norm_num` when values are numeric constants, or (b) accept as axiom, or (c) restructure to avoid noncomputable function evaluation.

---

## Pattern 5: Ω_GW vs Ω_DM Scale Mismatch (10⁸ factor)

**Signal**: Calibrated Ω_GW values (~10⁻⁹) are claimed equal to Planck Ω_DM (=0.264) with no scaling explanation.

**Actual ratio**: 2.5×10⁻⁹ / 0.264 ≈ 9.5×10⁻⁹

**Honest fix**: Add explicit note that ρ values are in arbitrary normalization, with the 10⁸ factor representing energy dilution from production to present epoch.

---

## Pattern 6: Three-Agent Review Efficiency

**Signal**: Full 5+1 agent review finds same issues as streamlined 3-agent review but costs 2×.

**Efficient pattern**: Deploy 3 agents (consistency + logic + technical) with adversarial context from prior review. Each reads full paper + Lean. Found all 11 P0-P2 issues in V15 in ~6 min vs ~13 min for 5+1.

**Agent prompt template**: Include mandatory 【对抗性审阅历史】 block with prior P0 list + "逐条验证: FIXED/PARTIAL/UNFIXED" directive.

---

## Pattern 7: DOF Counting Overflow (75 > 70)

**Signal**: Claimed dark sector DOF count exceeds total representation dimension.

**Example**: SL(6,C) adjoint = 70 real dim. Claimed CDM = 35+20+20 = 75 > 70.

**Detection**: For any DOF counting claim, verify: `sum(claimed sub-counts) ≤ dim(representation)`.

---

## Pattern 8: Orphaned Code Fragments After Deletion

**Signal**: After using `patch` to delete a theorem block, orphaned lines from the old proof body remain (e.g., `deriv_mul`, `h_product_deriv`, orphaned `calc` blocks).

**Detection**: After any deletion patch, search for unique identifiers from the deleted block that should no longer appear.
