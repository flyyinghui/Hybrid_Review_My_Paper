# Honesty-fix depth: a hedge reword is not a fix (round-7 → round-8, LightSpeed V2)

2026-10-20 re-review cycle on `LightSpeed_Phase_Boundary_V2`. Round 7 flagged the
abstract boxed Eq (1) "fixed by the effective metric" as language-borrowing (a
matched input dressed as a derivation). The round-7 fix changed "fixed by" →
"consistent with" and put an "[M]" tag in the *conclusion*. Round 8 (all 5
agents) judged it PARTIAL/REMAIN: the boxed `⟹` still read as a derivation.

## Core pattern: softening the verb does not remove a derivation implication

When a reviewer flags a claim as "matched input dressed as a derivation", the
overclaim lives in the LOGICAL STRUCTURE (`⟹`), not in the verb. Changing
"fixed by X" → "consistent with X" softens the verb but leaves the implication
intact: `[M] ⟹ conclusion` is still a tautology, because the premise IS the
matched input.

The structural fix that satisfies the reviewers:

1. Move the `[M]` tag onto the **premise** (the matched input), not the conclusion.
2. Change the conclusion to a **non-derivation verb**: "read off from the matched
   effective metric" (not "fixed by", not "consistent with", not "determined by").
3. Result: `regular common metric principal symbol [M] ⟹ cone + speed read off
   from that matched metric` — honest, because the `⟹` now says "given the matched
   input, the cone follows", a real (if conditional) statement.

```
Wrong:  "fixed by the effective metric"  →  "consistent with the effective metric"
Right:  "regular common metric principal symbol [M]  ⟹  … c_* read off from the matched effective metric"
```

## Corollary: the prose must match the box — fix both together

Even after fixing the box, the prose sentence right after it can still carry the
old overclaim. Round 7 fixed the box but left prose "not postulated as an
independent input" — which CONTRADICTS the `[M]` tag (if the principal symbol is
a matched input, c_* IS partly an independent input). Fix prose and box in the
same pass: "read off from the matched effective metric [M], rather than
postulated as an additional free parameter beyond it."

## Second pattern: a caveat does not fix a theorem NAME

`cpl_eos_parameter_elimination` (definitional identity w_a=-3w_0(1+w_0)) and
`pl_stokes_pairing_invariant` (a 2×2 linear change-of-basis) both got honest
caveats in round 7 ("under the specific single-component parameterization …
not a general statement"). Round 8 still flagged the NAMES: "elimination" implies
deriving w_a from data; "Stokes pairing" is a loaded term (Pham, Cecotti–Vafa).
**A prose caveat is not a rename.** If the name overclaims, rename it
(`cpl_eos_parameter_identity`, `pl_linear_pairing_invariant`) — don't just caveat it.
The rename must land in BOTH the .lean file (theorem name) and the .md (all cites).

## Third pattern: an inventory table added to fix "incomplete enumeration" can introduce a table/prose mismatch

Round 7 added §A.5a (complete 31-theorem / 15-def inventory) to close a
"8 chains sum to ~29 not 31" finding. Round 8 (3 agents) flagged a NEW defect:
the table listed 31 theorems but the prose chains (i)–(viii) only named ~20
(`observation_envelope_exclusion`, `boundary_energy_lower_bound`,
`poincare_normalization` + 7 auxiliary defs were table-only). Fix: at insert
time, add an explicit sentence declaring the table authoritative — "the table
below is the authoritative complete inventory; the prose names the load-bearing
declarations and does not exhaustively relist every auxiliary definition."

## Meta: why re-review scores DROP on "cosmetic" fixes

Round 7 avg 5.5 → round 8 avg 4.7. The round-7 fixes were ~70% relabeling. The
re-review agents (sharper eyes + round-7 findings injected as adversarial context)
caught: (a) the hedge reword didn't remove the `⟹` overclaim, (b) 2 new defects
introduced by the fixes, (c) the deeper "no dynamics work package / net predictive
≈ 0" issue that wording cannot fix. **When a review's fixes are all verb-level,
expect a score drop on re-review**; only structural fixes (move [M] to premise,
rename the theorem, or add a real derivation) move the score up. See also
references/re-review-score-drop-unverified-rigor.md.
