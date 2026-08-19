# V55→V56 Follow-up Hybrid Review Pattern (2026-07-23)

## Trigger

User explicitly requires that a revised manuscript's review MUST build on the prior review:
"请重新在对V55版本审稿基础上，再启动Hybrid-review-my-paper技能...审稿意见必须基于V55版本意见后再审议，否则就推翻之前审稿意见了。"

## Protocol

### Step 0 — Load prior review
Read the prior review MD, extract ALL P0/P1 defects with their IDs (C1-C10, I1-I13).

### Step 1 — Build adversarial context block
Prepend the V{N} P0/P1 list to EVERY reviewer prompt. Include scores and verdicts.
The block must instruct: "【必须逐条对照V{N}的P0缺陷给出V{N+1}状态】"

### Step 2 — Add fix-status audit fields
Each reviewer's JSON output MUST include:
```json
{
  "v55_issues_fixed": ["C2", "C10", ...],
  "v55_issues_remain": ["C4", "C5", ...],
  "new_issues": ["BE-RG c coefficient unexplained", ...]
}
```

### Step 3 — Use `str.replace()` not `.format()`
Paper text contains LaTeX braces. Use `BASE_PROMPT.replace("__ROLE__", ...).replace("__TASK__", ...)` pattern.

### Step 4 — Compile fix-status table
Cross-reference which P0/P1 issues were judged fixed by which reviewers. Use "✅ fixed / ⚠️ partial / ❌ not fixed" status.

### Step 5 — Handle JSON parse failures
`detailed_comments` with embedded quotes breaks `json.loads()`. Fall back to regex field extraction:
```python
score_m = re.search(r'"score":\s*([\d.]+)', text)
verdict_m = re.search(r'"verdict":\s*"([^"]+)"', text)
```

## V55→V56 Case Study

**V56 changes**: γ calibration→derivation, predictive degree +2→+3, Lean 0 sorry, Appendix E renamed.

**Results**: 5/6 MAJOR_REVISION, 1/6 REJECT. Average 3.9/10 (V55: 3.1/10, +0.8).

**Fix status**:
- ✅ C2 (compile error), C10 (abstract length)
- ⚠️ C1 (version chain), C7 (predictive degree), C8/C9 (references)
- ❌ C4 (D1 definitional identity), C5 (dual-path loop), C6 (epistemic status)

**New issues found in V56**:
- BE-RG c≈0.00475 source unexplained
- γ "derivation" still needs m_τ as boundary condition
- 0.5% gap between derived 2.22 and claimed 2.23 unexplained
- Axiom burden increased (21→25 + 50 honest-axiom tags)
- Predictive degree +3 internally contradicted (λ_KLS still phenomenological input)
