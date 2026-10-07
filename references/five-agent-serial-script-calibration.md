# 5-agent serial review script — calibration + f-string gotchas (2026-10-07)

## Observed latency (deepseek-flash, thinking disabled)

For a ~185KB / ~2060-line manuscript, the 5-agent serial review completed in ~73s total (~10-15s per agent, `max_tokens=8192`, `temperature=0.0`, `extra_body={"thinking":{"type":"disabled"}}`). The SKILL.md "5 agents ~8 min" estimate is conservative — actual latency on deepseek-flash is often 10-20x lower. Launch with `terminal(background=true, notify_on_complete=true)` and poll; do not assume 8 minutes or you will over-allocate and stall the session.

## f-string gotchas in the review-script template

- The prompt template is an f-string interpolating `{PRIOR}` (adversarial context = prior-round P0/P1 list) and `{paper}` (full manuscript). A reference to an undefined variable (e.g. a stale `{current}` left over from an earlier draft) raises `NameError` at call time — name the variables deliberately and grep for stale placeholders before launching.
- Paper content containing `{` / `}` (LaTeX `\begin{}`, Markdown) is SAFE inside f-string *variable interpolation*: only `{expr}` patterns in the template source are parsed, never the substituted variable's value. No escaping of the paper text is needed.

## Confirmed working recipe

Standalone Python script + OpenAI SDK (`base_url=https://api.deepseek.com`, key read from the project `.env`), model `deepseek-flash`, `extra_body={"thinking":{"type":"disabled"}}`, `max_tokens=8192`, `temperature=0.0`, `timeout=600`. Serial loop; write each reviewer to `/tmp/review_<name>.part` immediately after its API call; compile the report at the end. Adversarial context = prior-round P0/P1 list; require a `known_p0_verdicts` field mapping each prior item to `fixed`/`remain`/`partial` (so the round is a *diff against last round*, not a fresh de-novo review). This is the reliable pattern when the main agent model is v4-pro — `delegate_task` children would inherit v4-pro and hang, so a direct-API script is the only safe path.
