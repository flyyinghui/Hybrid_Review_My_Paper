# Score Plateau Diagnostic Pattern (2026-07-25)

## The Pattern

When a paper undergoes multiple review rounds and the scores stay flat across versions despite substantial changes, the core framework — not the implementation — is the issue.

## Detection

```
Version: V5 → V6 → V7 → ... → VN
Scores:  1.3 → 1.4 → 1.7 → ... → 1.7
Δ:       —    +0.1  +0.3  ...    0.0
```

A plateau is defined as: **Δ ≤ 0.1 across 3+ consecutive versions**, OR **score unchanged after substantial Lean/tactic upgrades**.

## What It Means

| Scenario | Diagnosis |
|----------|-----------|
| Score stays low (1-2) after Lean upgrades | **Physics gap** — the derivation chain itself is broken, not the formalization |
| Score stays low (1-2) after prose improvements | **Framework gap** — the theory lacks testable predictions or observable consequences |
| Score stays low despite honest-axiom cleanup | **Fundamental limitation** — the axioms themselves cannot produce the claimed results |

## Triple GW Case Study

V11 added Bakry-Émery explicit tactics, Bourgain slicing, and Ricci flow derivations — substantial Lean proof upgrades:
- V7: ~23 theorems, basic Lean
- V11: 28 theorems, 0 sorries, 12 tactic types, 811 lines

Yet score: V7=1.7 → V11=1.7. **Zero improvement.**

Why: The three fatal P0 issues are PHYSICS gaps:
1. GW production from SL(6,C) has no known derivation
2. λ_KLS=35/3 requires ad hoc 3D equipartition
3. N_e=160 requires ln(35/33)=160 which is mathematically false

Lean cannot fix physics. A stronger formal proof of a broken derivation chain is still broken.

## Recommended Response to Plateau

1. **Stop adding Lean content** — it won't help
2. **Identify the physics-only P0 issues** that Lean cannot address
3. **Choose an honest path**:
   - Path A: Reclassify unprovable claims as phenomenological parameters
   - Path B: Find a different physical mechanism that CAN be derived
4. **Reset the paper's claims** to match what is actually derivable
5. **Re-target to an appropriate venue** (Foundations of Physics for honest-axiom work)

## Scoring Impact of Honest Reclassification

Historical data shows that honest reclassification (e.g., "geometric theorem" → "phenomenologically determined parameter") often LOWERS scores in the short term but is the prerequisite for eventual publication. See `proof-paper-cross-ref-revision/references/progressive-honesty-score-paradox.md`.
