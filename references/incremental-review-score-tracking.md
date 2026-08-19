# Multi-Version Incremental Review — Score Tracking Pattern

## When to use
When the same paper goes through multiple hybrid review rounds (V5→V6→V7→...),
track scores across versions to detect whether fixes are substantive or cosmetic.

## Key pattern (from Triple GW V5→V6→V7)
| Version | Score | Key P0 fixes | Δ |
|---------|:-----:|------|:--:|
| V5 | 1.3/10 | baseline — arithmetic errors, N_eff=161.2, no GW mechanism | — |
| V6 | 1.4/10 | N_eff→3.046, removed ad-hoc normalization, added methodology note | +0.1 |
| V7 | 1.7/10 | KLS gap attempt, Lean restructure | +0.3 |

## Critical lesson
**Cosmetic fixes don't change scores.** The V5→V6→V7 trajectory shows that:
- Fixing arithmetic errors and N_eff only moved scores +0.1
- Adding a methodology note had zero impact
- The core P0 issues (GW production mechanism, e-fold dynamics, Omega_GW computation) were never actually solved — reviewers correctly identified that the fixes were "cosmetic"

## Detection signal
When Δ < 0.5 between versions, the fixes are cosmetic, not substantive. 
The paper needs fundamental rethinking, not incremental patching.

## Injecting prior review context
Each subsequent review MUST inject the prior version's P0 list as mandatory adversarial context. Without it, reviewers re-discover the same issues and scores drift unpredictably. The V5→V6 review without V5 context produced scores that didn't reflect actual improvements.
