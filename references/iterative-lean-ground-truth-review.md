# Iterative 5-agent Review: Machine Ground Truth + "本轮修订" in the Reviewer Prompt

When running multiple rounds of 5-agent hybrid review on a paper + Lean proof pair, the single highest-leverage prompt improvement is to embed (a) machine-level Lean ground truth and (b) a "this round's changes" section directly into every reviewer's prompt.

## Why

- **Without ground truth**, reviewers hallucinate axiom/theorem counts and re-flag already-fixed items. Each round regresses because reviewers don't know what changed.
- **With ground truth + change log**, reviewers (1) verify counts against a trusted source, (2) judge whether the previous round's P0s actually landed, (3) avoid re-flagging fixed items, (4) focus on genuinely new residuals.

## Script pattern (review_cgice.py, reusable)

A single-agent executor keyed by `--agent <name>`, with a shared `LEAN_GROUND_TRUTH` block injected into every prompt:

```python
LEAN_GROUND_TRUTH = """机器级 Lean 统计（剥离嵌套块注释 /- -/ 与行注释 -- 后，行首锚定）:
  theorem: 303 / lemma: 9 / def: 119 / axiom: 0 / sorry: 0 / admit: 0
  namespace: 13 (...)
  编译: Lean 4.34.0-rc1 + Mathlib, 0 errors 0 axioms 0 sorry
  (黄金门控 #print axioms 仅 propext/Classical.choice/Quot.sound)

本轮修订 (round N) 相对上一轮终审的变更:
  16. 摘要中段强动词条件化 ...
  17. §5 Scope 段尾加句 ...

前几轮修订:
  1. 新增 InstantonEndpoint 命名空间 ...
"""
```

Key design points:
- **机器级统计** is derived by stripping nested block comments (`/- -/`) and line comments (`--`) BEFORE line-anchored regex counting (`^\s*theorem\b` etc.). Nested block comments are the classic source of over-counting.
- **本轮修订** lists ONLY this round's changes (concise), **前几轮修订** lists prior rounds' changes so reviewers have full lineage.
- Run all 5 agents in parallel via a bash loop `for a in ...; do python review.py --agent $a & done; wait`, each writing `<agent>.md` to a shared dir.

## Reviewer roster that works

`consistency` (counts/constants/self-contradiction), `technical` (hard arithmetic errors, factor-2/direction/reversed-spectrum — the series' recurring error type), `logic` (conditional-model coherence, abstract firewall, circularity), `lean_specialist` (definitional-tautology / `:= by trivial` / shallow proofs), `publication_strategist` (CQG vs Nature Physics fit, net predictive degree).

## Scoring sanity

- `lean_specialist` is the honest floor: it scores the *formalization substance*, not the prose. A paper can have 0 axiom / 0 sorry and still score 6.5 because "303 theorem 中实质物理定理 = 0" (all finite algebraic identities / certificates / interfaces).
- "实质物理定理 = 0" is an inherent property of a *conditional model*, NOT fixable by prose edits — it is the true submission bottleneck (needs a real dynamics work-package), distinct from the text-layer P0s that ARE fixable.
- Expect text-layer P0s to clear after 1–2 rounds, then scoring plateaus at the substance ceiling. Further prose iteration yields diminishing returns.
