# Performative-Honesty Detection Patterns (Triple-GW V16, 2026-08-16)

Discovered during the revised final review of triple-GW V16 (score 2.2 → 3.1). All five
patterns are variants of one failure mode: **the revision made it LOOK fixed, but the
substance is unchanged.** These generalize to any paper that claims formal-verification
rigor (Lean/Coq/Isabelle) or a "honest-axiom disclosure" mechanism.

## 1. Performative honesty — commented-out attribute tags

Paper claims "axioms are declared as `@[honest_axiom]` / `@[phenomenological]`" but the
Lean file has **0 real attributes** — every tag is commented-out text (`-- @[honest_axiom]`).
Comments have zero compile semantics and cannot be machine-audited. The disclosure system
looks rigorous but is decorative.

Detection (always run both):
```bash
grep -c '^[[:space:]]*@\[honest_axiom\]'      file.lean   # real attribute (claimed, should be >0)
grep -c -- '-- *@\[honest_axiom\]'             file.lean   # commented-out text (the fake)
```
If the paper claims "declared as `@[...]`" but the first grep returns 0, it is performative
honesty. Verdict framing: "documentation-level honest, mechanism-level fake."

## 2. Axiom-count collapse when Lean expands but paper stats frozen

When a Lean file is expanded during revision (e.g. 1071 → 1979 lines) but the paper's
abstract/§appendix/header stats are never updated, the axiom-count contradiction
**multiplies** — one contradiction becomes four (here: header "14 axioms", abstract "41",
appendix "11+8=19", actual 66). The file's own header comment is also stale ("~1101 lines"
vs actual 1979).

Detection: always recount against the actual file (`grep -c '^\s*axiom'`, `wc -l`), and
check whether the file's own header comment matches its own body. A disclosure system that
can't count its own assumptions destroys its credibility — this is worse than having no
disclosure system.

## 3. Problem outsourced to finer axioms (conditional theorem with hardcoded conclusion)

A "repair" converts one big axiom into a "conditional theorem" whose premises are themselves
axioms, and whose conclusion STILL hardcodes the target number. Example: 
`eldan_chen_localization : Feasible → Lyapunov → Iwasawa → StrongLogConcave 35` — the real
Eldan–Chen theorem says nothing about "35"; the number is baked into the axiom. The "proof
chain" then reduces to `add_le_add` + `norm_num`; all content lives in the axioms.

Detection: for each "conditional theorem", run `#print axioms <name>`. If it depends on >0
custom axioms whose conclusions contain the target number, it's outsourcing, not solving.
Contrast-clean case: a conditional theorem whose premises are ALL moved to explicit
hypotheses and whose `#print axioms` is (near-)empty of custom axioms.

## 4. Circularity migrated from axiom to def

The "SORRY FIX" for N_e=161 moved the circularity from `axiom N_e_formula_axiom` to
`def t_freeze := t0 / Real.exp (161 / lam_KLS)`. The target value 161 is still embedded;
`N_e = lam_KLS * ln(t0/t_freeze)` is now trivially true by definition. Renaming the vessel
(axiom → def) does not break the circle.

Detection: grep def bodies for the target number. A "derived" value that appears literally
inside its own definition is still circular. Also watch for the value drifting across the
paper (161 / 160 / 161.18 all present) — a number that can't be pinned to one value was
never really derived.

## 5. Grep-term-too-narrow false negative in audits

An audit greps "parameter-free", gets 0 hits, and concludes the overclaim is gone — but the
paper paraphrased it as "independent of any free parameters" / "without recourse to free
parameters" in the intro and conclusion. The overclaim survives under a synonym, in the two
most visible locations.

Detection: grep semantic variants, not just the literal phrase. Always check intro and
conclusion FIRST — they are the highest-visibility locations and the ones a desk editor
reads before anything else.

## Cross-cutting rule

For a "revision landing" audit, the question is never "did the author add an honest label
or a new theorem?" — it is "did the OLD text survive, and does the NEW mechanism have
compile-level force?" Grep for the old text; grep for the real (uncommented) mechanism.
Anything that only exists in comments or paraphrases is not fixed.
