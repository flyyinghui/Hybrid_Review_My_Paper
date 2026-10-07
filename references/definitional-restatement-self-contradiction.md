# Definitional restatement contradicting the paper's own negative result

A recurring overclaim pattern surfaced by the third-round review of the "light-speed
interface" manuscript. It is a sharper cousin of the definitional-tautology trap: the
paper does NOT define the conclusion as an alias of a premise — instead it claims a
specific value is "derived from the structure" while the SAME paper proves elsewhere
that the value is ARBITRARY.

## The pattern

1. The paper proves a **negative / freedom theorem**: some quantity X is not fixed by
   the data — e.g. `equipartition_ratio_any_divisor` (r∥/r⊥ = d for ANY nonzero divisor
   d), `spectral_ratio_does_not_fix_cone`, `same_healthy_form_two_speeds`.
2. Elsewhere the paper claims a **specific value of X is "derived"**, tagged [T]:
   e.g. "c² = λ∥/λ⊥ = 3 follows from the SU(1,5) structure."
3. The two are logically incompatible. If X is arbitrary (step 1), then no group
   structure can force X = 3 (step 2).

## Concrete case (c² = 3)

The chain presented as a "derivation" was:

1. λ∥ = |ρ|² = 35  (a genuine theorem — Weyl-vector norm)
2. λ⊥ = λ∥ / rank(A₃) = 35/3  (**a definition**, disguised as a theorem)
3. c² = λ∥/λ⊥ = 3  (arithmetic)

Reviewers unanimously flagged step 2: **"The new module adds the *label* 'rank(A3)'
to the divisor, but the divisor is still chosen."** The paper's own Prop.1 proved
r∥/r⊥ = d for *any* d — so relabeling d → rank(A₃) does not turn a choice into a
derivation. The value c² = 3 is a unit convention / equipartition choice dressed as a
spectral prediction.

The fix (honest downgrade): re-tag the claim [T] → [M]/[O], replace "derived" with
"follows as an arithmetic identity from the equipartition choice λ⊥ = λ∥/3", and state
explicitly that "the structure does NOT select the divisor, as Proposition 1 shows."

## Detection checklist (for the reviewer)

When auditing a paper for overclaim, run BOTH greps and cross-check:

- Negative/freedom theorems: `any_divisor`, `does_not_fix`, `arbitrary`, `counterexample`,
  `not established`, `choice`, `convention`.
- Positive/derivation claims: `derived`, `follows from`, `emerges`, `theorem`, `[T]`,
  `predicts`, `determines`.

If the SAME quantity appears in both lists (e.g. the ratio "3" is both "arbitrary" per
Prop.1 and "derived" per Sec. V.I), it is a blocking self-contradiction — a P0, not a
stylistic nit. The reviewer should name the specific negative theorem that contradicts
the positive claim, so the author cannot hand-wave it away.

## Corollary: "label the divisor" is never a derivation

Giving a free parameter a group-theoretic NAME (rank(A₃), dim, dual Coxeter number, …)
does not make it forced. A free divisor remains free unless the paper supplies an
additional symmetry (e.g. SO(3) spatial isotropy) that BREAKS the freedom — and that
symmetry is itself a new [M] input. The honest statement is "X = 3 by convention /
equipartition", never "X = 3 is derived from the structure".

## Related pitfalls

- `definitional-tautology-trap.md` (in proof-paper-cross-ref-revision): defining the
  target predicate as an alias of the premise. This is the STRONGER cousin — here the
  contradiction is with the paper's own negative result, not with a definition.
- `honesty-downgrade-paradox.md`: fixing the overclaim drops the score (honest framing
  removes the "marketing layer"); expected, not a regression.
