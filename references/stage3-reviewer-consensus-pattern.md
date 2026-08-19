# Stage 3: 5-Person Reviewer Consensus Pattern (Validated 2026-07-05)

## Context

First full execution of the ARS+AWA Hybrid Review Pipeline Stage 3 on a theoretical physics paper with formal Lean 4 verification claims. 5 reviewers (EIC + R1 Methodology + R2 Domain + R3 Cross-Disciplinary + Devil's Advocate) produced a unanimous REJECT with 6 cross-reviewer consensus fatal flaws.

## Reviewer Score Distribution

| Reviewer | Score | Decision |
|:--|:--|:--|
| EIC | 30/100 | Desk Reject |
| R1 (Methodology) | 55/100 | Major Revision |
| R2 (Domain) | 27/100 | Reject |
| R3 (Cross-Disciplinary) | 42/100 | Major Revision |
| DA | — | Reject |

## Consensus Fatal Flaws (All 5 Agreed)

1. **Lean proof is structurally vacuous** — 37 axioms encode all physics, theorems are ℝ-algebraic tautologies
2. **D1 circular definition** — g_TC² ≡ 8π²/λ_KLS is defined, not derived
3. **"Zero free parameters" false** — y_ν, κ, γ all fitted
4. **Leptogenesis missing** — most important consequence of heavy ν_R at 10¹⁴ GeV
5. **ko_theory_gy_parity type error** — `Bool ≠ ¬ Bool` won't compile
6. **√2 convention split** — Lean and paper use different seesaw formulas

## Key Finding: AWA Complementarity

| Issue Class | Found by ARS alone | Found by AWA | Both |
|:--|:--|:--|:--|
| Axiom/lemma counting | ✅ | — | ✅ |
| Reference list errors | ❌ | ✅ (15 missing, 6 wrong) | — |
| Narrative structure | ❌ | ✅ (§2→§3→§4 transitions) | — |
| √2 convention | ❌ | ✅ | — |
| AI-tell markers | ❌ | ✅ (91 em-dashes) | — |
| Version fossils | ✅ | ✅ (C.5 dependency graph) | — |

**Conclusion**: ARS-only audits find structural defects; AWA catches content and prose defects. Both are required for comprehensive review.

## Fix Protocol

After Stage 3 consensus, the fix protocol is:
1. Fix Lean type errors first (they block compilation)
2. Add Honest Scope v2 declaration (§3) covering all consensus defects
3. Add missing sections (e.g., leptogenesis)
4. Downgrade Abstract claims
5. Cross-audit DOCX ↔ Lean for convention consistency

## Verification Checklist

- [ ] All 6 fatal flaws addressed in both files
- [ ] Honest Scope v2 present in §3
- [ ] Type errors fixed in Lean (verify with `grep`)
- [ ] √2 convention notes in both Lean and DOCX
- [ ] Cross-audit: 0 missing, 0 broken cross-refs
