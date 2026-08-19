# Cross-Paper Consistency Review Protocol

*Captured from V63 Neutrino vs V16 Triple GW review (2026-08-06)*

## When to Use

When two or more papers share a theoretical framework (e.g., both claim to derive from SL(6,C) with λ_KLS=35) and need to be cross-checked for mutual consistency.

## Protocol Steps

### Step 1: Extract the shared framework claims
From each paper, extract ALL claims about:
- Shared parameters (λ_KLS, H₀, DM:B, N_e, Θ thresholds)
- Observatory predictions (GW frequencies, amplitudes, peak count)
- Derivation mechanisms (GW production method)
- Epistemic status (derived vs calibrated vs honest-axiom)

### Step 2: Build a comparison matrix
Compare every claim across papers:

| Dimension | Paper A (e.g., V63 Neutrino) | Paper B (e.g., V16 Triple GW) | Verdict |
|-----------|------|------|---------|
| λ_KLS usage | 35/3 directly | 35 (fundamental) + 35/3 (effective) | CONFLICT |
| GW peak count | 2 peaks | 3 peaks | DIVERGENT |
| f₁ frequency | ~10⁷ Hz → redshifted | 4.5×10¹¹ Hz | CONFLICT |
| GW mechanism | Bubble nucleation S₃/T | Riccati-Hessian fixed points | DIVERGENT |
| H₀ status | "geometric overdetermination" | [honest-axiom] calibrated | CONFLICT |

### Step 3: Categorize each mismatch
- **CONFLICT (🔴)**: Same parameter, different value or status — MUST be resolved before any paper is submitted
- **DIVERGENT (🟡)**: Different scope/perspective on same framework — may be acceptable if explicitly justified
- **CONSISTENT (🟢)**: Same value and status in both papers

### Step 4: Identify the ground-truth version
The paper that has undergone more rigorous review (more review rounds, transparent honest-axiom declarations) should be treated as the ground truth. In the V63 vs V16 case, V16 was the ground truth because it had gone through V13→V14→V15→V16 with systematic honest labeling.

### Step 5: Generate the alignment document
Produce a detailed changelist showing exactly what must change in the non-ground-truth paper to align.

### Step 6: Execute the replacement
Use `write_file` for new content generation (v4-pro for max 8192 tokens, v4-flash for reliability), then python-docx paragraph-level replacement.

## Key Pitfalls

### Pitfall CS1: Stale "derived" claims
If the ground-truth paper has downgraded a claim from "derived" to [honest-axiom], the secondary paper must inherit that downgrade. Missing this creates an embarrassing inconsistency where one paper says "X is derived" and the other says "X is calibrated."

### Pitfall CS2: Different math → same numbers
If two papers use completely different mathematical mechanisms (bubble nucleation vs Riccati-Hessian flow) but claim to produce the "same" GW predictions, at least one mechanism is wrong. Do not paper over the inconsistency — flag it explicitly.

### Pitfall CS3: Internal mathematical errors
Before alignment, verify each paper's internal mathematics. V63's S₃/T formula gave ≈929 but the paper claimed ≈35. Aligning content without fixing internal errors just propagates mistakes.

### Pitfall CS4: Number-of-peaks mismatch
If one paper predicts 2 GW peaks and another predicts 3 from the same framework, both cannot be correct. The ground-truth paper's peak count must be adopted by all.

## Verified Run: V63 → V17 Alignment

Source: V63 neutrino paper Section V claimed 2 GW peaks at PTA (10⁻⁸ Hz) + LISA (10⁻² Hz)
Truth: V16 triple GW correctly has 3 peaks at 4.5×10¹¹ Hz, 1.71 Hz, 10⁻⁹ Hz
Action: Rewrote V63 Section V + Appendix E.5-E.6 to match V16
Tool: deepseek-v4-pro generated replacement text → python-docx paragraph replacement
Outcome: V63_V17.docx with all GW content aligned to V16
