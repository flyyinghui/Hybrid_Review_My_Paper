# Second-Round Focused Rewrite Review + Ground-Truth Injection (2026-10-07 verified)

When a manuscript's FIRST review round already produced a confirmed P0/P1 defect list, a SECOND round that simply re-runs the same 5-agent prompts produces near-identical results (the paper hasn't changed). The high-value second round is a **focused rewrite + venue-strategy review**, not a repeat fact-check. This is the execution recipe that ran cleanly on SL6C V3 round 2 (scores converged 7.17–7.42, mean 7.29, vs round-1 6.5–7.5).

## When to use this variant

- Round 1 confirmed the defect list AND the known_p0_verdicts (fixed/remain/partial per item).
- The paper was NOT edited between rounds (so re-reviewing "did they fix it" would be a no-op).
- The user asks for "修改建议" / "concrete next edits" rather than another score.

## Three deltas vs the standard re-review (rereview-adversarial-defect-list-execution.md)

1. **Inject measured GROUND TRUTH into the prompt** to suppress reviewer false-positives that round 1 already produced. Concretely inject: abstract word count (LaTeX-stripped), compile EXIT_CODE, and the comment-stripped Lean declaration counts. Round 1 reviewers hallucinated "abstract 290/330 words" against a real 205; round 2 must not repeat it.
2. **Require PASTE-READY rewrite text**, not "shorten the abstract". For each P0/P1 item, the reviewer must return an exact English replacement sentence/paragraph (`rewrite_text` field), ready to paste.
3. **Classify each item BLOCKING vs ACCEPTABLE-AS-IS** (per target venue), so the user gets an actionable to-do list, not a re-litigation.

## Abstract word-count false-positive (the durable pitfall)

Symptom: multiple reviewers report "abstract exceeds the 250-word limit" with wildly divergent counts (247/290/330). Reality: the abstract is 205 words.

Root cause: reviewers count LaTeX formula tokens (`$SL(6,\mathbb C)$`, `$(3,1)+(0,2)$`) and math symbols as words.

Authoritative measurement (Python):

```python
import re
m = re.search(r'## Abstract\s*\n(.*?)(?=\n## )', paper, re.DOTALL)
abstract = m.group(1) if m else ""
nomath = re.sub(r'\$\$.*?\$\$', ' ', abstract, flags=re.DOTALL)
nomath = re.sub(r'\$[^$]*\$', ' ', nomath)
words = re.findall(r"[A-Za-z0-9][A-Za-z0-9\-']*", nomath)
print(len(words))  # authoritative English word count, LaTeX-stripped
```

Always compute this yourself BEFORE trusting any "abstract too long" finding, and state the measured count in the review prompt so reviewers calibrate on it.

## Six-dimension scoring (make the score interpretable)

The single `score` field is ambiguous (reviewers default to 0–1 or 0–10 unpredictably). Require six sub-scores AND the mean:

```
originality / correctness / significance / clarity / formalization_rigor / honesty
```

On SL6C V3 round 2 this surfaced the real signal: formalization_rigor 8.0–8.5 and honesty 8.5 (the paper's actual strengths) vs significance 5.5 (the honest weakness). A single number would have hidden this.

## Venue-ranking output

For a paper whose own honesty disclaims unique predictions (the SL6C framework case), ask each reviewer to rank PRD / SciPost Physics / Foundations of Physics / JMP / CQG and name a `first_choice`. The round-2 consensus (4/5 SciPost Physics, 1/5 Foundations of Physics, PRD last) is far more actionable than "not suitable for PRD".

## Scripting notes

- Reuse the round-1 script; change only (a) the PRIOR context block (paste round-1 known_p0_verdicts + the new round's changes-to-verify), (b) the task paragraph, (c) the output filename.
- Use `%`-formatting (not f-strings) for prompts that embed LaTeX (f-string expressions cannot contain backslashes).
- `deepseek-flash` + `extra_body={"thinking":{"type":"disabled"}}`, `max_tokens=8192, temperature=0.0, timeout=600`, serial loop, write each `.part` immediately. ~80s total for 5 agents.
- The `bash: /.local/bin/env: No such file or directory` warning at process start is the WSL empty-HOME artifact — harmless when the script invokes python by absolute path; `export HOME=/root` in the wrapper suppresses it.
