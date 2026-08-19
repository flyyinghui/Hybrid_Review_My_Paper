# Adversarial Context Injection for Sequential Hybrid Reviews

**Discovered**: V55→V56→V57 multi-round review (2026-07-23), neutrino condensation paper.

## Pattern

When running a hybrid review of a REVISED manuscript, inject the PRIOR review's findings as mandatory context. This forces reviewers to:
1. Check whether prior Critical/Important issues were fixed
2. Evaluate the revision against the prior baseline, not from scratch
3. Produce calibrated scores relative to the prior round
4. Detect "new packaging of old problems"

## Template

```python
PRIOR_CONTEXT = """【前次评审历史 — MUST audit against these findings】

V{N-1}综合评分: X.X/10。P0致命缺陷:
C1: description
C2: description
...

YOUR TASK: For each prior P0 defect, state whether V{N} FIXED, PARTIALLY FIXED, or DID NOT FIX it.
Then provide your independent assessment of V{N}.
"""
```

## Key Lesson

Without adversarial context, reviewers treat each version as a fresh submission — they re-discover old problems, produce inconsistent scores across rounds, and miss the incremental progress (or lack thereof). With it, scores become calibrated: a revision that fixes 8/10 P0 defects but leaves core epistemological issues gets a modest score bump (3.1→3.7), not a clean slate.

## Output Format Addition

When using adversarial context, add these fields to reviewer output:
```json
{
  "v55_issues_fixed": ["C2", "C10", ...],
  "v55_issues_remain": ["C4", "C5", ...],
  "new_issues": ["new problem 1", ...]
}
```
