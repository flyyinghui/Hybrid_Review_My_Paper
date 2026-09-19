# Re-Review Execution with Adversarial Defect-List Injection (2026-09-19 verified)

Follow-up Hybrid Review of a REVISED paper whose prior review already produced a P0–P3 defect list. The user expects reviewers to BUILD ON prior findings, not re-litigate them (see Pitfall 11). This is the concrete execution recipe that ran cleanly on the V18 三大时空相 re-review.

## Model (current, verified 2026-09-13 & 2026-09-19)

- **`deepseek-flash`** — the only valid flash model name. NOT `deepseek-v4-flash`, NOT `deepseek-v4.1-flash`, NOT `deepseek-chat` (all deprecated aliases → empty `content`).
- `deepseek-v4-pro` = the other valid name (reasoner; unreliable for long review prompts, see Pitfall 14).
- OpenAI SDK, `base_url='https://api.deepseek.com'`.
- Mandatory: `extra_body={"thinking": {"type": "disabled"}}` — otherwise `content` is empty (output goes to `reasoning_content`).
- `max_tokens=8192, temperature=0.0, timeout=600`.

## Timing (serial, 5 agents)

~16–20s per agent on ~100KB prompts (full 94KB paper + 110 axiom decls + prior defect list), ~87s total. The older "~8 min" estimate was for delegate_task/parallel under rate limits; direct serial scripted calls are far faster. Serial is still required — DeepSeek rate-limits concurrent calls.

## Prompt structure (per reviewer)

1. `COMMON_PREAMBLE` — reviewer role, honesty-labeling system (K/C/A/P/O), JSON output contract, "double-quotes escaped as `\"`".
2. `PRIOR_DEFECTS` — the FULL prior P0/P1/P2/P3 list as adversarial context, each item with the fix requirement. Instruct "逐条判定 fixed/remain/partial，不得凭空重新评审".
3. Reviewer-specific role + focus + which defect IDs to prioritize.
4. `LEAN_STATS` — comment-stripped ACTIVE counts (axiom/theorem/lemma/def/opaque/structure/class + sorry/admit/trivial) with a note of the PRIOR-round counts so reviewers see the delta.
5. Axiom declaration list (with signatures) — needed by the rigor reviewer to catch autoImplicit phantom types and provably-false axioms.
6. Full paper markdown.

## JSON output contract (each reviewer)

```json
{
  "score": 0.0,
  "known_p0_verdicts": {"P0-1": "fixed|remain|partial", "...": "..."},
  "known_p1_verdicts": {"...": "..."},
  "known_p2_verdicts": {"...": "..."},
  "known_p3_verdicts": {"...": "..."},
  "findings": [{"severity": "P0|P1|P2|P3", "location": "§/行号", "description": "...", "evidence": "...", "fix": "..."}],
  "summary": "..."
}
```

`findings` = only NEW discoveries or remain/partial evidence, never re-state fixed items.

## Aggregation (synthesis step)

- Parse each `.part` via regex, NOT `json.loads`: strip ```json fences → find first `{` to last `}` → `json.loads`.
- Tally verdict votes per defect across the 5 agents.
- Classify: **fixed** = ≥4/5 fixed; **remain** = ≥4/5 remain (or 5/5); else **partial**.
- Report shape: 已修复 / 未修复(阻断) / 部分修复 tables + a "本轮新发现" list (independent discoveries, e.g. a Landau-pole arithmetic error, a status-escalation residue).

## Critical execution details

- Serial loop; each reviewer output written to `/tmp/<tag>.part` IMMEDIATELY (recoverable if killed mid-compile).
- `str.replace('__TOKEN__', value)` NOT `.format()` — paper text has LaTeX braces.
- API smoke-test first (single tiny call) to confirm model name + thinking-disabled returns content.
- `terminal(background=true, notify_on_complete=true)`; stdout is buffered under background mode — poll the `.part` files / output dir, not the process stdout, for progress.

## Lean stats counting (must be comment-stripped, authoritative)

- Strip nested block comments with a depth-tracking state machine; non-greedy `re.sub(r'/-.*?-/','',flags=re.S)` FAILS on nested `/-` (see `references/lean-nested-block-comment-sorry-pitfall.md`).
- Authoritative line-level counts: `grep -cE "^\s*axiom\s"` / `"^\s*theorem\s"` / `"^\s*lemma\s"`.
- `@[honest_axiom]` decorators sit on their OWN line above the `axiom` — count separately.
- Any non-zero `sorry`/`admit`/`by trivial`/`:=True` must be confirmed by `grep -n` line context; in a clean proof ALL matches are in header/docstring comments (the file header even says "sorry=0, admit=0").

## Known trap (reconfirmed this session)

All 5 reviewers may return an IDENTICAL score (here 5.5/10) — treat that as "objective residual defects, not reviewer disagreement", and focus the report on the verdict tallies + new findings rather than the spread.
