# Fix-Introduces-New-Defect & Reviewer Combinatorial-Count False-Positive

Session: V64 neutrino-condensation paper, three-round review loop (6.2 → 7.1 → 7.3, P0→P3 fully cleared), 2026-09-26.

Two durable patterns + one reminder. Both of the first two are NEW subclasses of the
existing "reviewer arithmetic false-positive" family (rule group E) but worth their own
entry because they each cost a full extra review cycle to surface.

## Pattern 1 — A conversion-table FIX is itself a new arithmetic surface

When a reviewer flags a "two normalizations mixed" P0 and the fix is to add an **explicit
conversion table** (e.g. $B_6$ charge → $T_\chi=B_6/2$ → $3(B{-}L)$), that table is a NEW
place to make arithmetic errors. The table's derived column must be cell-verified against
the declared identity, not eyeballed.

Real case: the table declared `3(B−L) = 3·q_{B₆}`, but the N_R row listed `3(B−L) = −3/2`.
Correct value: `3 × (−1) = −3`. Three reviewers independently caught the −3/2 in the NEXT
round — one full extra review cycle wasted.

**Rule**: after inserting any conversion/normalization/matching table as a fix, run a
programmatic check that every cell satisfies `derived_column = factor × source_column`
for all rows before declaring the fix done. A single off-by-factor cell (here ×2: the
author confused $q_{T_\chi}=q_{B_6}/2$ with $3(B{-}L)=3q_{B_6}$) is exactly the kind of
subtle error that survives one review and is caught by the next.

## Pattern 2 — Reviewer combinatorial-count false positive (number of roots)

Before relaying a reviewer's "dimension doesn't close" / "multiplicity is wrong" claim as
a finding, verify the **combinatorial count** yourself.

Real case: reviewer claimed `dim SL(6,C)/SU(6) = 35` fails under "restricted-root
multiplicity 2" because "A₅ has 5 positive roots → 5 + 5·2 = 15 ≠ 35". The error: the A₅
root system has **n(n+1)/2 = 15** positive roots, not 5. Correct closure:
`dim = rank + #positive_roots × mult = 5 + 15×2 = 35` ✓. The paper was right; the fix was
NOT adopted.

This is the combinatorial-count variant of reviewer false positive: the reviewer miscounted
a discrete structure (number of roots / multiplicities), not an arithmetic expression. Key
checklist when a reviewer reports a "dimension / rank / multiplicity" mismatch:
- positive roots of Aₙ = n(n+1)/2 (A₅ = 15, NOT 5)
- positive roots of Bₙ/Cₙ = n², Dₙ = n(n−1)
- dim = rank + Σ(positive_roots × multiplicity)
- for the complex symmetric space SL(n,C)/SU(n), every restricted root has multiplicity 2

## Pattern 3 — "Remove/rename X" fixes leave residuals (grep all phrasings)

Deleting CI metadata from the abstract (P0) left a residual status sentence the next round
flagged ("The accompanying Lean source separates scalar and finite-dimensional proof
bodies..."). When a fix is "remove X", grep ALL phrasings of X afterward — a sentence can
express the same idea in different words than the one you matched. Same family as
`references/compilation-status-consistency.md` (grep `compil|uncompiled|not executed`).

## Execution note (re-review loop)

The serial `deepseek-flash` re-review ran at ~5–20s/agent on ~65K-char prompts (full paper
+ prior defect list), well under the older "16–20s on 100KB" estimate. Keep using
`extra_body={"thinking":{"type":"disabled"}}`, `max_tokens=8192`, `temperature=0.0`,
`timeout=600`, and write each reviewer's JSON to a `.part` file immediately.
