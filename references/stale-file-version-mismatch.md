# Stale-File / Wrong-Version Review (agents silently read the OLD file)

## Symptom (2026-08-23, CGICE re-review)

Deployed 3 review agents pointing at `/tmp/cgice_paper_rev.txt` and `/tmp/cgice_lean_rev.txt`
(names that did NOT exist). The agents silently fell back to `/tmp/cgice_paper.txt` /
`/tmp/cgice_lean.txt` — STALE copies made hours earlier during a translation/extraction task
(906/823 lines), while the user had since MODIFIED the real files (902/816 lines). All 3 agents
"reviewed" the OLD version; their findings (A5 still present, I_cycle_dual missing, a3 unchanged)
directly CONTRADICTED the parent's own grep of the current files. A full review cycle was wasted
and had to be re-run.

## Detection

1. **Agent reports line counts / stats that don't match the current file.** CGICE case:
   - agent said "paper 906 lines, lean 823 lines, axiom=73, lemma=13"
   - actual current: "paper 902, lean 816, axiom=72, lemma=12"
   - a 4–7 line offset + count drift = stale copy.
2. **Agent says "the file X does not exist, I used Y instead"** — visible in `tool_trace` as a
   failed `read_file` followed by `search_files`/`read_file` on a different path.

## Fix (mandatory BEFORE deploying any re-review of a modified file)

1. **Re-copy the CURRENT files** to /tmp with the EXACT names the prompts reference:
   `cp /mnt/.../paper.md /tmp/paper_rev.txt` (same for the .lean / companion files).
2. **Verify line counts** with `wc -l` — they must match what you read directly from the source
   right before deploying.
3. **Tell each agent the expected line count** in the prompt ("已确认存在，read_file 读，行数已标出：
   902 行"), so the agent can self-detect a stale/wrong file and report it rather than silently
   proceeding on the wrong version.
4. **Cross-check your own grep against agent claims before synthesizing.** If your direct grep of
   the current file says "A5 deleted" but the agent says "A5 present", the agent read a stale copy.
   Do NOT average the two verdicts — trust the direct read of the current file, re-copy, re-deploy.

## Root cause

`/tmp` is scratch space where earlier tasks (translation, extraction) leave stale copies under
generic names (`cgice_paper.txt`). A re-review hours later pointing at a NEW name that was never
created (`_rev.txt`) silently resolves to the stale generic copy. Never assume `/tmp` contents are
current — always re-copy + verify line counts.
