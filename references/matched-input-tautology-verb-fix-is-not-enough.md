# "consistent with X" does NOT fix a matched-input tautology — move [M] to the premise

Round-7→Round-8 venue-fit re-review lesson (LightSpeed_Phase_Boundary_V2, 2026-10-20).

## The pattern

Round 7 flagged the abstract's boxed implication as language-borrowing:
`fixed by the effective metric` → author reworded to `consistent with the effective metric
(common metric principal symbol: matched input [M])`.

Round 8 re-review found this was **still** a P0, scored by 5/5 agents. Root cause: the verb
was softened but the `⟹` STRUCTURE was untouched. The box read

```
controlled 6D Lorentzian reduction + regular common metric principal symbol [M]
⟹ 4D causal cone + sharp local speed c_* consistent with the effective metric
```

but the "regular common metric principal symbol" **is** the matched input `S = c_*² T` (Eq 21).
So the box is `[M] ⟹ cone`, i.e. the conclusion is the premise restated — a tautology dressed
as a theorem. "Consistent with" merely swaps the derivation verb for a consistency verb; the
implication still *reads* as a derivation because `⟹` is still there.

## The correct fix (what actually landed in round 8.5)

1. **Move the `[M]` tag onto the PREMISE**, not the conclusion:
   `+ regular common metric principal symbol [M]`
2. **Change the conclusion to "read off from"** (passive extraction, not derivation):
   `⟹ ... sharp local speed c_* read off from the matched effective metric`
3. **Fix the prose sentence too** — "not postulated as an independent input" is ALSO an
   overclaim (if the symbol is matched, c_* IS partly an independent input). Use:
   `read off from the matched effective metric [M], rather than postulated as an additional
   free parameter beyond it`.
4. **Eq (21) prose**: "supplied by the minimally coupled action" implies derivation → change to
   `a matched input [M] chosen to be consistent with (11); it is not derived from (11)`.

## General rule for reviewer-driven honesty fixes

When a reviewer flags a verb (`fixed by`, `derived from`, `implies`) as overclaiming a matched
input, do NOT just swap to a softer verb (`consistent with`, `motivated by`, `suggests`). Check
the LOGICAL STRUCTURE first:

- If the conclusion follows by `⟹` from a premise that IS the matched input, it is a tautology
  regardless of verb. The fix is structural: tag the premise `[M]`, demote the conclusion to
  `read off from / consistent with / conditional on`, and remove the `⟹` if the "result" is
  just restating the input.
- The abstract box is the paper's single most-quoted sentence; a verb-only fix there is a
  desk-reject risk at FoP (the reviewer reads the box, reads Eq (21), and rejects on
  "restatement of premise").
- Symmetric-fix principle: the prose sentence AFTER the box must match the box's `[M]` tag. A
  box that says `[M]` but prose that says "not an independent input" is a *new* internal
  contradiction the literalist auditor will catch (this happened — consistency agent scored 3.5).

## Cross-venue note

This is the round-8 "score dropped despite fixes" mechanism: cosmetic relabeling + a new
prose/box contradiction + the deeper tautology still present. The fix is not another
relabeling pass; it is one structural edit (move `[M]` to premise, `read off from` conclusion)
plus one prose alignment.
