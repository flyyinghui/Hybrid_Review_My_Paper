# Re-review Preparation: Refresh Ground Truth + Feed Full Paper

## When this fires
Re-running a 5-agent hybrid review (`review_cgice.py`-style) on a paper that has been **extended since the last review round** (e.g. a new section/namespace added, declaration counts changed).

## Two stale-state traps in the review script
1. **Hardcoded LEAN_GROUND_TRUTH counts go stale.** The script's ground-truth block (e.g. "303 thm / 9 lemma / 119 def / 13 namespace") is baked in at authoring time. After the paper grows (303→382 thm), the agents audit against the *wrong* ground truth and will flag phantom count mismatches. **Before every re-review, recompute the ground truth** from comment-stripped Lean and patch the script:
   ```python
   lean = open(lean_path).read()
   # strip /- -/ block comments and -- line comments before counting
   theorem = len(re.findall(r'^\s*theorem\s+', lean, re.M))
   # ... lemma, def, structure, namespace, axiom, sorry, admit
   ```
   Also list the namespace names explicitly (20 of them) — agents must not "miss" newly added namespaces.

2. **Fixed-char truncation misses the new content.** The prior script truncated the paper to the first 60K chars (≈ line 555). If the extension lives *beyond* that cut (e.g. the D1 instanton block at §7.3.1, lines ~719–956), the agents review a paper that silently omits **exactly the new material being re-reviewed**. When the paper is ~190K chars (~47–63K tokens), feed the **full paper** — deepseek-flash's 128K context holds it. Only truncate when total tokens genuinely exceed the window; never use a stale char constant.

## Also inject prior-review history (mandatory, per V56 lesson)
The review prompt must carry a `PRIOR_REVIEW_HISTORY` block: the previous round's P0/P1 defect IDs + the remaining single-sentence items, and instruct each agent to return a `vN_issues_fixed / vN_issues_remain / partial` status table per item. This prevents the reviewer from re-litigating already-fixed defects or silently reverting earlier decisions.

## Execution shape
- Model: `deepseek-flash` with `extra_body={"thinking": {"type": "disabled"}}` (v4-pro hangs on >120K-char prompts). `temperature=0.0`, `max_tokens=8192` output, `timeout=900`.
- Run the 5 agents **in parallel** as separate background terminal processes, each writing `/tmp/<dir>/<agent>.md`; `notify_on_complete=true`. Wall time ≈ max(single agent) ≈ 50–430s, not 5×.
- API key from `~/.env` (`DEEPSEEK_API_KEY`), OpenAI SDK + `base_url="https://api.deepseek.com"`.
- The 5 axes: consistency / technical (math) / logic / lean_specialist / publication_strategist.
