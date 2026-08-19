# P0 Persistence Across Versions — Framework Insufficiency Signal

**Observed**: Triple GW V5→V6→V7→V8 (2026-07-25), 4 review rounds, same 4 P0 issues survived every version.

**Score trajectory**: 1.3 → 1.4 → 1.7 → (V8 pending)

**The anti-pattern**: When the same P0 defects appear in 3+ consecutive review rounds despite targeted fixes, the problem is NOT insufficient patching — it is **framework insufficiency**. The proof framework itself lacks the mathematical infrastructure to support the claimed results.

## The 4 Persistent P0 Issues (Triple GW case study)

| P0 | Issue | V5 status | V6 "fix" | V7 "fix" | Why unfixable in current framework |
|----|-------|-----------|----------|----------|-------------------------------------|
| P0-1 | No GW production mechanism | Missing | T_μν added as axiom | Same axiom, renamed | SL(6,C) → linearized GR coupling requires computing second-order perturbations on the moduli space — no known derivation exists |
| P0-2 | Frequencies from numerology | N_e = 60,100,160 chosen ad-hoc | "Geometric redshift" but same N_e | Same N_e, claimed from V(φ) | Deriving N_e from first principles requires solving the full moduli potential dynamics — the KLS framework only gives bounds, not exact values |
| P0-3 | No comparison to data | Missing | Mentioned LVK/NANOGrav names | Same mentions, no computation | Computing Ω_GW(f) requires a physical GW production model (see P0-1) — without it, numbers are arbitrary |
| P0-4 | Incoherent mathematics | Riccati-Hessian stated without derivation | Bakry-Émery bound attempted | Incorrect CD(K,∞) bound used | The KLS constant is defined for convex bodies; the SL(6,C)/SU(6) symmetric space Laplacian is a different mathematical object — the bridge between them is conjectural |

## Decision Rule

**IF** the same P0 issue appears in review rounds N, N+1, and N+2:
1. **STOP** iterative patching
2. **CLASSIFY** the P0: is it fixable within current framework, or does it require framework extension?
3. **If framework insufficiency**: the correct response is NOT another round of fixes. Options:
   - (a) Admit the limitation and downgrade the claim (e.g., "conjecture" not "theorem")
   - (b) Redesign the proof framework from scratch
   - (c) Split the paper — publish the parts that ARE derivable, leave the rest as open problems

**Contra-indicator**: When scores ARE rising (>+1.0 per version) and P0s are genuinely being resolved, iterative patching IS the right approach. The P0 persistence rule only triggers when scores plateau (<+0.5 per version) AND the same P0 IDs recur.

## Score Plateau Detection

```python
def detect_p0_persistence(review_history):
    """Returns True if P0 persistence detected across 3+ versions."""
    if len(review_history) < 3:
        return False
    
    # Extract P0 IDs from last 3 reviews
    p0_sets = []
    for review in review_history[-3:]:
        p0_ids = set(p['id'] for p in review.get('p0_blocking', []))
        p0_sets.append(p0_ids)
    
    # Check if any P0 ID appears in all 3
    persistent = p0_sets[0] & p0_sets[1] & p0_sets[2]
    
    # Check score trajectory
    scores = [r.get('avg_score', 0) for r in review_history[-3:]]
    delta = scores[-1] - scores[0]
    
    return len(persistent) > 0 and delta < 0.5
```

## Triple GW V5→V7 Score Data

| Version | R0_EIC | R1_MATH | R2_GW | R3_COSMO | R4_DEVIL | Avg |
|---------|--------|---------|-------|----------|----------|-----|
| V5 | 1.5 | 1.5 | 0 | 3.0 | 0.5 | 1.3 |
| V6 | 1.5 | 1.2 | 1.2 | 1.5 | 1.5 | 1.4 |
| V7 | 1.8 | 1.5 | 1.5 | 2.1 | 1.8 | 1.7 |

Delta V5→V7: +0.4 (below 0.5 threshold). P0-1 through P0-4 present in all three rounds → **P0 persistence confirmed**.

## Recommended Response (for Triple GW specifically)

The user should:
1. **Accept** that GW production from pure SL(6,C) geometry cannot be derived with current mathematical tools
2. **Reposition** the paper as a "geometric motivation for triple-peak GW search" rather than a "derivation"
3. **Drop** the Lean proof claims (they prove trivial identities, not physical theorems)
4. **Add** a dedicated section comparing with existing GW detector constraints as observational motivation
