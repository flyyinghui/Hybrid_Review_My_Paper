# Verify Agent Findings Against File State Before Reporting

Two failure modes observed in a 5-agent venue-fit review (CGICE V10, 2026-10-13) that
produced false P0s and wasted a repair round. Both are review-script/harness bugs, not
reviewer-judgment bugs — but the agent synthesizing the report must compensate.

## 1. Hardcoded ground-truth false positive

The review script's `LEAN_GROUND_TRUTH` had a stale hardcoded "structure: 2" (actual: 1).
The consistency agent then flagged "paper says 1 structure, machine says 2" as a P0 —
a pure false positive that consumed a full "fix" round (and, worse, was reported to the
user as a real finding before I re-verified with grep).

**Rule:** regenerate the machine-level ground truth from the actual file
(`grep -c '^structure '`, `grep -c '^theorem '`, etc.) immediately before launching
reviewers. Never copy a count from a prior run or an LLM-authored summary.

## 2. Truncated-view hallucination

The script fed each agent only `paper[:60000]` + 4000 chars after "Appendix A". Agents
then hallucinated "CartanWeyl namespace missing from the list" (it WAS present, at
line ~1033, beyond the 4000-char window) and "gTC bridge not registered" (it WAS in
Appendix D.2). When synthesizing agent reports, treat every "X is missing / absent /
not registered" claim as a HYPOTHESIS to verify with `grep` against the actual file —
agents infer "absent" from an incomplete view.

## Rule

An agent's "X is missing or inconsistent" claim is a hypothesis to verify, not a fact.
`grep` the file to confirm before it enters the summary as a P0/P1. Symmetrically, when
an agent reports a numeric/structural finding (e.g. "(2.7) exponent-moment mismatch"),
re-derive or grep it yourself before escalating — the previous CGICE review's "(2.7)"
flag turned out to be a wavefunction-vs-density wording ambiguity, not an arithmetic
error (the moments were correct for |ψ|² = e^(−ax²/h)).
