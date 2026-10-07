# Re-review score drop: unverified prior rigor + honesty re-normalization

When a proof-paper goes through a SECOND 5-agent hybrid review (re-review) after a
revision, the weighted score often DROPS below the prior round (observed: 6.3 → 5.46
on the light-speed phase-boundary paper, 5/5 still Major Revision). This is NOT a
regression — it is the correct re-normalization of an inflated prior score. Three
mechanisms combine, and a reviewer who doesn't understand them will misread the
result and either over-fix or wrongly panic.

## Why the score drops (the three mechanisms)

1. **Unverified prior rigor.** The prior round awarded rigor 9/10 partly on a *claim*
   that was not actually verified in the delivered artifact: the `#print axioms`
   commands were commented out, and the header said "their presence is not a claim
   that they were executed in this delivery." A reviewer trusts this, scores rigor
   high, and lets that high rigor carry the weighted total. When the revision actually
   compiles (`EXIT=0`, `#print axioms` reports only `[propext, Classical.choice,
   Quot.sound]`), rigor stays high (8–8.5) but the *content* is now visible for what
   it is — conditional, with thin novelty — so novelty/significance drop and drag the
   weighted total down.

2. **Honest "toy model" content.** If the revision's main increment is a *conditional
   linear model* (a two-rate ODE decay semigroup, a slow-plane invariance, a variance
   closure), reviewers will call it what it is: a toy model, not a derived dynamical
   phase transition. This is the honesty-downgrade paradox applied across rounds —
   the honest labeling removes the "marketing layer" that propped up the prior score.

3. **The central claim is unchanged.** The paper still establishes a *conditional
   compatibility construction*, not the headline dynamical claim. On re-review, after
   the framing fixes, reviewers state this more bluntly than before ("No. It
   establishes only a conditional compatibility construction, not a dynamical phase
   boundary"), which reads as a downgrade even though it was true all along.

**Read the drop correctly:** "the revision removed the inflation" — not "the revision
made it worse." If the revision also *added* verified content (more theorems, actual
compile, honest coverage table), that is real progress on the rigor axis even though
the weighted number falls.

## Re-review prompt engineering (the convention that works)

A re-review is only useful if the reviewers can cleanly adjudicate what changed. Two
conventions make the FIXED/PARTIAL/REMAIN table reliable:

1. **The ground-truth block must explicitly enumerate residuals that were NOT
   changed.** Example (this surfaced a residual P0 correctly):

   > NOTE: the theorem `vev123_entry_counts` STILL uses `native_decide`
   > (compiler-backend dependent) rather than `decide`/`norm_num` — this is the one
   > residual reproducibility hazard flagged in the prior round and it has NOT been
   > changed.

   Without this explicit "NOT changed" list, reviewers either miss the residual or
   have to diff the Lean file themselves (they won't). State it; it becomes a clean
   REMAIN entry and forces the author to either fix it or disclose it.

2. **Prior findings carry stable IDs and require per-item adjudication.** Inject the
   prior round's P0/P1 as `[P0-R0-1]`, `[P1-R2-5]`, ... and require each to be marked
   FIXED / PARTIAL / REMAIN with a one-line reason, plus a summary line
   `Summary: N FIXED, M PARTIAL, K REMAIN`. This gives a diffable, cross-round audit
   trail and lets you see at a glance which class of finding is stuck (usually
   REMAIN = framing/title overclaim + literature gaps; FIXED = compile-status honesty
   + scope labels).

3. **Require an explicit yes/no to the central claim.** "Does this revision establish
   that X is a Y, or only a conditional construction?" The 5/5-identical "No — only a
   conditional compatibility construction" is the single most decision-relevant output.

## Execution notes (reusable)

- deepseek-flash (NOT v4-pro for large-prompt review; v4-pro hangs on >120K chars),
  `extra_body={"thinking":{"type":"disabled"}}`, `ThreadPoolExecutor(max_workers=3)`,
  `timeout=300`, `max_tokens=6000`. 5 reviewers over a ~110KB manuscript return in
  13–19 s each.
- Build the ground-truth block as verified facts only: compile EXIT code, theorem/def
  counts, `#print axioms` output, and the explicit NOT-changed residuals. Do NOT put
  interpretive claims in it — reviewers treat "objective ground-truth" as undisputable.
