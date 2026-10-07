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

## Python scripting pitfalls (2026-10-03 re-confirmed)

Two syntax traps bite when authoring the re-review script (both hit this session):

- **f-string expression cannot contain a backslash** (Python 3.11, `execute_code`): `f"...{count(r'^\s*theorem\s')}..."` → `SyntaxError: f-string expression part cannot include a backslash`. Fix: hoist the regex to a variable first (`pat = r'^\s*theorem\s'` then `f"...{count(pat)}"`), or use `%`-formatting. This re-surfaces on any comment-stripping / Lean-stats-counting script inside `execute_code`.
- **ASCII double-quotes inside Chinese prompt strings collide with the string delimiter**: a ROLE_PROMPTS value written as `"...如 "22 theorems" vs "29 theorems"..."` terminates the outer `"..."` string early → SyntaxError. Fix: quote inner English terms with Chinese corner quotes 『』/「」, or triple-quote the whole value. Same trap applies to any prompt-embedding dict mixing Chinese narration with quoted English terms (theorem names, string literals like `"isthe"`, `"S. Coleman"`).

## Lean stats counting (must be comment-stripped, authoritative)

- Strip nested block comments with a depth-tracking state machine; non-greedy `re.sub(r'/-.*?-/','',flags=re.S)` FAILS on nested `/-` (see `references/lean-nested-block-comment-sorry-pitfall.md`).
- Authoritative line-level counts: `grep -cE "^\s*axiom\s"` / `"^\s*theorem\s"` / `"^\s*lemma\s"`.
- `@[honest_axiom]` decorators sit on their OWN line above the `axiom` — count separately.
- Any non-zero `sorry`/`admit`/`by trivial`/`:=True` must be confirmed by `grep -n` line context; in a clean proof ALL matches are in header/docstring comments (the file header even says "sorry=0, admit=0").

## Known trap (reconfirmed this session)

All 5 reviewers may return an IDENTICAL score (here 5.5/10) — treat that as "objective residual defects, not reviewer disagreement", and focus the report on the verdict tallies + new findings rather than the spread.

**Score-scale confusion (2026-10-03)**: the JSON contract's `"score": 0.0` is ambiguous — reviewers default to a 0–1 scale and return meaningless 0.62/0.55/0.0 values unless the prompt EXPLICITLY states "score is 0–10, 10 is highest (NOT 0–1)". Symptom: three consecutive re-review rounds returned scores clustered at 0.0–0.62 (unusable); only after adding the explicit scale sentence did reviewers return 4.5. **Fix**: for any scoring terminal review, (a) state the 0–10 scale in the preamble, and (b) request a six-dimension breakdown (originality/correctness/significance/clarity/formalization_rigor/honesty) so the total is interpretable. For a pure fix-verification re-review, drop `score` from the contract entirely — verdict tallies (fixed/remain/partial) are the only signal you need.
