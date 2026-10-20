# Review Script Ground-Truth Refresh (re-running a 5-agent review on a new paper version)

## When to use
Re-running a multi-agent review (5-agent venue-fit 终审, consistency/technical/logic/lean_specialist/publication_strategist) on a **newer version** of a paper where the existing review script holds **stale ground truth** (old theorem/def/namespace counts) and the paper has grown (e.g. a D1 extension added +79 theorems).

## Steps
1. **Recompute machine-level ground truth** from the current Lean source: theorem / lemma / def / structure / namespace / axiom / sorry / admit counts, compile status (olean newer than source = compiled), golden-gate `#print axioms`.
2. **Update the review script's `LEAN_GROUND_TRUTH` block** (stale `303 thm / 119 def / 13 namespace` → `382 thm / 165 def / 20 namespace`).
3. **Inject `PRIOR_REVIEW_HISTORY`**: list the previous round's remaining P0/P1 items so agents judge `fixed` / `remain` per-item instead of re-discovering them. This is mandatory — the user explicitly rejects a re-review that does not carry prior-round defect context (V56 lesson).
4. **Feed the FULL paper, not a truncated prefix.** New content (the D1 extension) lives mid-paper (~line 719 of 1737), beyond an old 60K-char truncation — a prefix cut misses the entire new material. 188K chars ≈ 47–63K tokens fits deepseek-flash 128K context.
5. **Update agent prompts' hardcoded numbers** (theorem counts, namespace names) to match the new ground truth — otherwise the agents audit against stale numbers.

## DeepSeek execution facts
- Model `deepseek-flash` + `extra_body={"thinking":{"type":"disabled"}}` (content non-empty; v4-pro hangs on >120K char prompts).
- OpenAI SDK + `base_url="https://api.deepseek.com"`, `temperature=0.0`, `max_tokens=8192` (output), `timeout=900`.
- Launch each agent as a **separate background terminal process** (parallel, `notify_on_complete=true`). Expect ~50–430s per agent.
- Verify liveness after launch via `ps aux | grep <script>` — the `process list` tool may return empty while processes are actually running.

## Review-output disposition
- Archive the 5 per-agent `.md` files into the paper directory with a timestamped name (`Hybrid_Review_<PAPER>_5agent_<DATE>_<agent>.md`) so the next round can load them as prior history.
- Consolidate P0 findings across agents **with dedup** — the same compilation-status residual is often reported by consistency + logic + publication_strategist independently; list it once.
- Distinguish "表述层" (presentation: wording, table-cell omission, disclosure position) from "实质层" (arithmetic, overclaim, hidden tautology). Only the former is fixed by single-sentence edits; the latter moves the venue verdict.

## Review-scope honesty
A "honesty extension" (converting hidden assumptions into explicit open conditions) raises honesty scores but contributes **zero net predictive power** — the venue verdict (CQG MAJOR REVISION / Nature Physics NOT READY) does NOT change from a D1-style extension. Report this explicitly rather than implying the extension improved the physics.
