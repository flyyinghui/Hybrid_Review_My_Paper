# Review Re-run Workflow & Wording-Level P0 Taxonomy

Session-derived patterns for re-running a 5-agent hybrid review after paper edits, and for the
recurring class of **wording-level (non-arithmetic) P0 fixes** in formalized theory papers.

## 1. Freshness check BEFORE reporting audit results

The subtle bug this surfaced: the user asked to "see the final audit result after modifications,"
but the latest review report (`Hybrid_Review_*_r4.md`, mtime 21:12) **predated** the paper's last
edit (`cgice_paper_v10_fop.md`, mtime 21:54). The report therefore did NOT reflect the current
paper state.

**Rule**: before declaring any review "final" or answering "show me the result", compare mtimes:

```bash
cd <paper_dir> && ls -lt --time-style=+%Y-%m-%d_%H:%M:%S *.md | head -20
```

If the newest review report is OLDER than the paper's newest edit, the report is stale → re-run
the review rather than quoting it. This is a one-command check that prevents confidently reporting
stale scores.

## 2. Single-agent executor + parallel runner (the re-run mechanism)

The clean pattern for re-running an N-agent review on an updated manuscript:

**Executor script** (`review_<paper>.py`): one `--agent <name>` arg, a dict of per-agent
role/task prompts, and — critically — an embedded `LEAN_GROUND_TRUTH` string carrying (a) the
machine-level declaration counts and (b) a **"本轮修订" (this-round revision) narrative** that
enumerates exactly what changed since the last review round. Reviewers read the diff narrative
instead of diffing two 140KB papers blind.

**Parallel runner** (bash, launched with `background=true` + `notify_on_complete=true`):

```bash
cd <paper_dir>
rm -rf /tmp/<paper>_review && mkdir -p /tmp/<paper>_review
for a in consistency technical logic lean_specialist publication_strategist; do
  /usr/local/lib/hermes-agent-v14/venv/bin/python review_<paper>.py --agent $a > /tmp/<paper>_review/$a.log 2>&1 &
done
wait; echo ALL_DONE
```

Do NOT use `&` inside a foreground `terminal()` call — it is rejected. Wrap it in a `.sh` file and
run with `terminal(background=true)`. Model = `deepseek-flash` with
`extra_body={"thinking":{"type":"disabled"}}` (deepseek-chat alias is deprecated).

## 3. Wording-level P0 taxonomy (6 recurring categories)

When a review flags P0s that are **wording, not arithmetic**, they cluster into these six fix types.
All are one-to-few sentence edits. Apply them all in a single pass:

1. **Abstract strong-verb conditioning** — replace completion-voice verbs with conditional voice:
   `strengthen`→`contribute concrete ... steps`, `yields`→`conditionally yields`,
   `connect`→`bridge`/`relate`. (logic P0-1)
2. **Lean identifier physical-vocab = labels** — add a sentence in the "Scope of the Lean layer"
   paragraph: theorem identifiers carrying physics words (`speed_of_light_ratio`,
   `lineage_components`, `equipartition`) are *labels*, not assertions about light cones /
   lineages / equipartition. (logic P0-2)
3. **"supplied by" → "presentation ... given by [internal consistency only]"** — when a second
   route to the same number exists, its intro sentence must not read as independent evidence.
   (technical P0-1)
4. **Semantic-slippage cut-off sentence** — when two quantities are numerically equal but derived
   independently, add an explicit "X and Y are not derived from each other; the former is a
   normalization-dependent spectral threshold, the latter a dimensionless matching convention."
   (technical P0-2)
5. **Table footnote for arithmetic-consequence theorems** — a theorem like `tauI_eq_6pi_over_35`
   proves the arithmetic consequence of a matching input, NOT the input itself; state this in the
   boundary column. (technical P0-3)
6. **Evidence-mapping completeness** — the §5.5 certificate table must list EVERY namespace's
   theorem group (e.g. `InstantonEndpoint`), not just the "count". Machine-level counts can match
   while the mapping table silently omits a whole namespace. (consistency P0-01)

## 4. LaTeX backslash-safe editing (patch tool hazard)

The `patch` tool double-writes `\` in `.md` files containing LaTeX. For any edit touching `\(...\)`
math, do it in Python with **raw strings**, then verify by codepoint:

```python
# raw string: r"\(\|\rho_{\mathrm{res}}\|^2=35\)"  produces single backslashes
for i, ch in enumerate(seg):
    print(i, ord(ch))          # backslash == 92, verify no two consecutive 92
```

Reject if any two adjacent chars are both 92 (double backslash). This catches the "double-written
backslash" corruption before it ships.
