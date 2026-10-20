# Venue-fit review round-7 findings + P0/P1 fix pipeline (LightSpeed_Phase_Boundary_V2, 2026-10-20)

Real-round record: 5-agent venue-fit panel → 5/5 MAJOR REVISION (avg ~5.5) → P0/P1 fixes → re-compile EXIT=0. Three new pitfalls + one fix-pipeline pattern worth reusing.

## 1. def/abbrev conflation — a recurring self-report defect

The single most cross-confirmed finding (all 5 agents + machine grep): the paper's
Data-and-code + Appendix A.3 both said **"127 definitions"**, but machine truth was
**125 `def` + 3 `abbrev` = 128** (or 125 if abbrevs excluded). **127 matched neither.**

Root cause: authors conflate `abbrev` into `def` (or miscount by hand) and the number
lands in the very sentence that claims machine-verified honesty. This is the same
credibility-kill class as the round-6 "0 sorry" keyword claim that hid 3 `sorryAx`.

Rule for the reviewer: **never trust a paper's self-reported `def` count. Grep the
Lean file for `def` vs `abbrev` separately and compare.** The fix is always to state
the full breakdown (`N definitions and K abbreviations`), never a single merged number.

## 2. Batch string replacement: a broader substring silently covers a specific target

When editing the paper I ran a list of `(old, new)` pairs and required `count(old)==1`
per pair, writing the file only if every pair matched. One pair
(`"Picard–Lefschetz downward flow and Stokes pairing"` → new) was a **substring of**
a later, more specific pair (`"**(vi) Picard–Lefschetz downward flow and Stokes pairing.**"`).
The broad pair matched x2 (table row + body heading), so the specific pair matched x0,
reported "MISS", and — because my guard treated ANY miss as fatal — **the file was not
written at all**, silently discarding every edit already applied in memory.

Lesson: when a broad substring replacement subsumes a specific target, the specific
target's x0 is NOT a failure — the broad replacement already did that job. Two safe fixes:
(a) order replacements specific→broad and assert `count==1` only for genuinely independent
targets; or (b) treat a "MISS" as a warning, not a fatal, and still write — then re-grep
the *final* text for stale strings to confirm the net effect. The second is more robust:
**verify the final file with a stale-string grep, not per-pair match counts.**

## 3. Reviewer findings must be checked against the paper's own hedging

The logic agent flagged P0: "Appendix A.5 says `closes the remaining gaps` but Sec. V.N
lists all six bridges as `Remaining physical construction` — direct contradiction." On
grep, A.5 actually contained a hedging sentence immediately after the overclaim
("It does not claim that these conditional constructions already close all six microscopic
bridges"). So the contradiction was PARTIALLY neutralized → downgraded P0 → P1.

Lesson: a first-pass "X contradicts Y" finding is often softened by a nearby hedging
clause. Before fixing, grep the *full* sentence context around the flagged phrase, not
just the flagged substring. Downgrade the finding if the paper already hedged; only the
**headline phrase** ("closes the remaining gaps") still needs rewording.

## 4. Theorem-rename + recompile verification pattern

When a reviewer flags a theorem *name* as overpromising (e.g. `sextic_root_multiplicities_unique`
implies "root multiplicities are unique" but the theorem is a Diophantine-system uniqueness
proved by `omega`), the fix is surgical:

1. Rename in the .lean file (`sextic_root_multiplicities_unique` → `sextic_multiplicity_system_unique`),
   update the docstring to state what the theorem actually proves.
2. Sync the md: every citation of the old name (table rows + prose) → new name.
3. Re-compile the .lean file (EXIT=0) to prove the rename broke nothing.
4. Re-run the declaration-count grep to confirm theorem count unchanged (468 → 468).

The rename is name-level only when the *content* is already correct (the technical agent
re-derived the Diophantine system and confirmed (3,2,1) is the unique nonnegative solution).
Do NOT rewrite the proof body — only the name + docstring — when content is sound.

## 5. Full per-chain declaration inventory closes "sums to N" objections

The logic agent claimed "A.5's 8 chains enumerate only ~20 declarations, which sum to 29,
not 31." Fix: extract the module's full declaration list from the Lean file (regex
`^theorem\s+(\S+)` / `^def\s+(\S+)` inside the namespace block, bounded by the matching
`end`), then add a per-chain table that sums *exactly* to the claimed counts
(2+3+2+5+3+3+6+7 = 31 theorems; 1+1+2+4+1+2+4+0 = 15 defs). This kills the objection at
its root by making the count auditable rather than asserted.
