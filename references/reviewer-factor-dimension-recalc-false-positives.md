# Reviewer Agent Factor/Dimension Recalculation False-Positives

Observed 2026-10-17 on Triple-GW V20 round-2 5-agent review. When the `technical`
reviewer agent (deepseek-flash, thinking disabled) performs independent
recalculation of a physics paper's algebra, it produces **confident, detailed
"hard arithmetic error" claims that are mostly convention-confusion false
positives**. It claimed 4 P0/P1 "hard errors"; 3 of 4 were false positives, which
wrongly dropped the technical score 8.4 → 6.5.

## The three false-positive modes observed

1. **Conformal-time vs physical-time source term (spurious factor a²).**
   Claimed `S_0 = F0G0d²/(M²a*²)` had an extra `1/a*²`. False: the agent substituted
   the conformal-time source `(2a²/M²)Π` into a *physical-time* equation. Physical-time
   source is `(2/M²)Π` (after dividing by a²), giving `FGd²/(M²a²)` — the paper was
   correct.

2. **Itô vs Stratonovich mixing (phantom "-12DC" term).**
   Claimed `κ̇₄ = -24qC³` was missing `-12DC`. False: the agent computed `Ṁ₄` in one
   stochastic interpretation and `Ċ` in the other. In a *consistent* interpretation
   (either Itô, where the `12DC` diffusion term cancels the `-6C·2D`, or Stratonovich),
   the result is `κ̇₄ = -24qC³`. Paper was correct.

3. **Oscillation-average ½ factor (phantom factor 2).**
   Claimed equation (7.13) was missing a factor 2. False: the agent dropped the paper's
   explicit `\overline{cos·cos} = ½ cos` oscillation-average factor that cancels it.
   Note the same agent had verified this *same* equation as "consistent" in round 1 —
   its factor recalc is unstable between rounds.

## The durable rule

Any agent-claimed "factor 2 / factor a² / dimension mismatch / missing term / wrong
sign" must be **independently re-derived by hand along the full source-term chain**
before being accepted or acted on. Specifically check:

- (a) conformal time vs physical time — source terms differ by a² (a'/a vs ȧ/a);
- (b) stochastic-interpretation consistency — Itô correction terms cancel or not;
- (c) oscillation/time-average ½ factors, and Fourier-space vs coordinate-space dimensions.

A bare dimension claim like `[C]=5` is usually a convention mismatch (φ normalization,
Fourier-space Π dimension, delta-function stripping), not a hard error — flag for
author confirmation, not P0. Only a claim where the agent shows the *entire* derivation
chain (and the chain survives your own re-derivation) deserves P0 severity.

## Related

- `proof-paper-cross-ref-revision/references/reviewer-numerical-false-positive-detection.md`
  (numerical value false-positives — the companion failure mode where the reviewer
  hallucinates a value that never appeared in the manuscript).
