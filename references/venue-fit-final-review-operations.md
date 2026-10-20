# Venue-fit 5-agent final review — operational recipe

The final ("终审") review before submission uses a 5-agent **venue-fit** panel, distinct from
the ARS 5-person peer review and the AWA 12-specialist parallel review. It is optimized for
judging whether a formalization-heavy theory paper is submission-ready and *where* to send it.

## Agent set + dispositions

| agent | role | disposition (auditor stance) |
|---|---|---|
| consistency | 一致性审计 | **literalism** — verify every count/number/reference against machine-level grep/Python; never accept "should be fine" |
| technical | 技术/数学审计 | **skepticism** — independently re-derive every step; default assumption is "author flipped a factor 2 / direction / hid an assumption" |
| logic | 逻辑自洽审计 | **skepticism (most adversarial)** — construct counterexamples, hunt circular reasoning, flag "language borrowed vs equations followed" |
| lean_specialist | Lean 形式化专家 | **literalism (strictest)** — trust only compilation / `#print axioms` / grep counts, never header comments; flag `rw def + linarith` shallow proofs as tautology |
| publication_strategist | 投稿策略顾问 | **empathy** — read as a hostile referee/editor; judge overclaim risk per target venue's tolerance |

## Execution recipe (verified 2026-10-17)

- **Model**: `deepseek-flash` with `extra_body={"thinking":{"type":"disabled"}}`.
  `deepseek-v4-pro` (thinking) **hangs** on full-manuscript prompts — never use it for the reviewer agents.
- **`max_tokens=16384`**, not 8192. The technical agent is the longest (it re-derives a dozen
  formulas) and 8192 truncates it mid-P2, losing its score/verdict. If a single agent truncates,
  rerun *that agent* with 16384.
- **Feed the full manuscript** (170–190KB) in one prompt; deepseek-flash handles it.
- **Inject machine-level Lean ground truth** (grep counts: theorem/lemma/def/abbrev/structure/axiom/sorry/admit + namespace list + compile status) so consistency/lean_specialist audit against *it*, not against the paper's own self-report.
- **Inject previous review history** (prior memo's N items) and require a per-item `fixed / remain / partial` judgment with evidence.
- **Run all 5 in parallel** via a bash wrapper (`for a in ...; do python review.py --agent $a & done; wait`) under `background=true, notify_on_complete=true`. One wrapper → one notification.

## Known failure modes

- **technical first-pass "factor 2" flags are often the agent's OWN arithmetic error.** On rerun
  it re-derives and self-withdraws the flag. Treat first-pass technical flags as "needs independent
  verification", not as confirmed defects — before fixing the manuscript, re-derive the claim yourself.
- A reusable single-agent executor pattern (argparse `--agent`, one file per agent, shared
  ground-truth + previous-review constants) keeps the 5 prompts consistent and re-runnable.

## P0 fix checklist (what review findings map to)

After the 5-agent review, the submission-blocking fixes are usually: abstract rewrite (promote the
calibration-independent result to first contribution, demote "remains necessary" tail), §12/coverage-table
wording alignment with body disclaimers, explicit "conditional on independently specified X" labels on
exclusion chains, and "0-axiom is a compilation-hygiene indicator, not a proof of non-triviality" disclosure.
