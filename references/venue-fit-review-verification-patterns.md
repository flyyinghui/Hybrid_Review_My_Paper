# Venue-fit round-7 findings — three durable review patterns (2026-10-20)

Extracted from a 5-agent venue-fit final review of `LightSpeed_Phase_Boundary_V2.md`
(468 thm / 0 sorry / 0 axiom / EXIT=0 / golden-gate clean). The Lean artifact was
submission-grade; every P0 was in the *paper's description of* the artifact, not the code.

## Pattern 1 — def/abbrev/structure must be THREE separate columns in LEAN_GT

The paper's Data-and-code + Appendix A.3 both said **"127 definitions"**. Machine truth:
`def: 125` + `abbrev: 3` (+ `structure: 0`). **127 matches neither 125 nor 128.**

Root cause: authors write "N definitions" while silently folding `abbrev` into `def` and
miscounting. This is a self-inflicted wound — it sits in the *same sentence* that boasts
"0 sorry, 0 axiom", so a referee who greps loses trust in every other count in the paper.

Action: your LEAN_GT block must report `theorem / lemma / def / abbrev / structure / axiom /
sorry / admit / noncomputable` as **separate lines**. The consistency + lean_specialist
agents audit against the breakdown; a flat "N definitions" claim is exactly what they exist
to catch. When the paper says "N definitions", independently recompute `def` vs `abbrev`
and flag any number that matches neither.

## Pattern 2 — a prior "ACCEPT" is not ground truth; verify prior "fixed" items against CURRENT body

Round 6 of this paper was **5/5 ACCEPT**, including the finding that the SU(1,5) slice has
a *"unique timelike line"* (O-2 closure, 4 theorems). Round 7's body (§V.M) **retracts** it:
"does not have a unique timelike line", with explicit witness `(1,1/2,0,…)` and the new
`timelike_line_not_unique` declaration.

Consequence: the round-6 "fixed" status was itself an overclaim. Three of five round-7 agents
independently flagged the prior item as **PARTIAL (walked back)**, not fixed.

Action: in the PRIOR block, instruct agents to judge every prior "fixed" item against the
*current manuscript text*, never against the prior report's verdict. A prior panel can ACCEPT
a claim that a later honest revision correctly weakens — that's good science, but it means the
prior "fixed" label was premature and must be reclassified.

## Pattern 3 — verify each reviewer P0 before fixing; sort into true-error / overclaim / naming

The round-7 cross-confirmed P0s split three ways on independent re-check (grep/Python):

| Finding | Recheck result | Correct disposition |
|---|---|---|
| "127 definitions" vs machine | **TRUE ERROR** — confirmed 125 def + 3 abbrev | P0, fix the number |
| A.5 "closes the remaining gaps" vs §V.N "Remaining physical construction" | **OVERCLAIM, partially hedged** — A.5 *does* add "does not claim to close all six bridges" | downgrade P0 → P1 (wording) |
| `sextic_root_multiplicities_unique` "false as stated" | **CONTENT CORRECT, NAME OVERPROMISES** — re-derived: the Diophantine system has unique (3,2,1) over ℤ≥0; only the name claims root-uniqueness | P1, rename to `sextic_multiplicity_system_unique` |

Action: never fix the manuscript off a first-pass P0 flag. Run your own grep/re-derivation on
each one and bucket it into **true error / wording-overclaim / naming-misleading** before
writing the fix list. First-pass "factor 2 / false as stated / contradicts" flags are often
the agent's own error or a naming problem, not a math error. The `technical` agent's own
re-derivation is usually in the report — read it, don't just relay it.

## Net read

"0 sorry / 0 axiom" is a **compilation-hygiene indicator, not a proof of non-triviality**.
A module of 31 `native_decide`/finite-algebra theorems framed as "full formal parity" /
"closes the remaining gaps" is the exact overclaim the lean_specialist disposition exists to
catch. The fix is framing: "closes the finite-algebra fragments of the chains", not "closes
the gaps".
