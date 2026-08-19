# v4-pro Multi-Paper Cross-Review Protocol

## When to Use

Use **deepseek-v4-pro** (NOT v4-flash) for multi-paper cross-review when:
- Reviewing 3+ papers simultaneously with cross-paper consistency checking
- Papers share a common theoretical framework (e.g., SL(6,C))
- Each paper has an associated Lean formal proof file
- Prompt is **< 50K characters** (v4-pro safe zone)
- User explicitly requests v4-pro or "maximum tokens" reasoning

**Contrast with v4-flash approach** (`references/multi-paper-v4flash-thinking-review.md`):
- v4-pro: deeper mathematical reasoning, fewer hallucinations, slower (~160s)
- v4-flash: handles larger prompts (>120K), thinking trace visible, faster (~240s total)

## Pipeline (6 Steps)

### Step 1: Locate All Files

```
paper DOCX + Lean proof file for each paper
Optionally: shared axiom/framework document (e.g., 6Dconcept.md)
```

### Step 2: Extract Lean Statistics

```python
import re

def extract_lean_stats(lean_path):
    with open(lean_path, 'r', encoding='utf-8', errors='replace') as f:
        lean_text = f.read()
    
    return {
        "lines": len(lean_text.split('\n')),
        "chars": len(lean_text),
        "axioms": len(re.findall(r'(?<![/-])\baxiom\b', lean_text)),
        "theorems": len(re.findall(r'(?<![/-])\btheorem\b', lean_text)),
        "lemmas": len(re.findall(r'(?<![/-])\blemma\b', lean_text)),
        "sorries": len(re.findall(r'\bsorry\b', lean_text)),
        "honest_axiom": len(re.findall(r'\[honest.axiom\]', lean_text, re.IGNORECASE)),
        "true_stubs": len(re.findall(r':=\s*True\b', lean_text)),
        # Extract numerical constants
        "defs": re.findall(r'def\s+(\w+)\s*:?\s*\w*\s*:=\s*([\d.eE+×/\-]+)', lean_text)[:30],
    }
```

### Step 3: Extract Paper Key Content

Extract from each DOCX:
- **First 25%**: Abstract + Introduction (~4000 chars) — establishes claims
- **Middle 30%**: Core derivations (~4000 chars) — where math happens  
- **Last 20%**: Conclusions (~3000 chars) — what's claimed as results
- **All numerical claims**: Regex patterns for key constants

```python
num_patterns = [
    r'(?:λ_KLS|lambda_KLS)\s*[=≈~]\s*[\d./eE+×\-]+[^,\n]{0,80}',
    r'(?:g_TC|g\\{TC\\})\s*[=≈~]\s*[\d./eE+×\-]+[^,\n]{0,80}',
    r'(?:H[₀0])\s*[=≈~]\s*[\d./eE+×\-]+[^,\n]{0,80}',
    r'(?:Ω_\{?GW\}?|Omega_GW)\s*[=≈~]\s*[\d.eE+×\-]+[^,\n]{0,80}',
    r'(?:M_R)\s*[=≈~]\s*[\d.eE+×\-]+[^,\n]{0,80}',
    # ... add per-domain patterns
]
```

### Step 4: Build Review Prompt

Structure (target <50K chars):

```markdown
## REVIEW TASK (explicit instructions)
## PAPER SUMMARIES (for each: stats + abstract + derivations + conclusions + Lean stats + numerical claims)
## CROSS-PAPER CONSISTENCY AUDIT (per-axis questions)
## REQUIRED OUTPUT (5-section format)
```

**5-section output format** (proven effective):
1. 单篇论文审查 — P0/P1/P2 per paper
2. 跨论文一致性矩阵 — 8-axis table with verdicts
3. 数值验证 — re-derive 5 critical claims
4. 发表就绪评估 — score + venue + conditions
5. 优先修复路线图 — ordered fix list

**8-axis cross-paper matrix** (SL(6,C) framework template):
| Axis | Description |
|------|-------------|
| λ_KLS value | What value? Derived or postulated? |
| g_TC value | Consistent across papers? |
| GW mechanism | Same physical origin? |
| GW frequencies | Compatible predictions? |
| DM mechanism | Condensate vs GW energy vs geometric? |
| H₀ status | Derived/calibrated/axiom? |
| ρ_DM/ρ_b ratio | Same derivation? |
| Neutrino masses | Consistent m₁,m₂,m₃,M_R? |

Verdicts: CONSISTENT / MINOR DIFF / MAJOR CONFLICT / INCOMMENSURABLE

### Step 5: Call v4-pro API

```python
from openai import OpenAI
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

resp = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=32768,
    temperature=0.0,
    timeout=900,
)
content = resp.choices[0].message.content
```

**Key constraints**:
- Prompt MUST be <50K chars (safe zone; >120K hangs)
- Use `terminal(background=true, notify_on_complete=true)` not `execute_code` 
- timeout=900 (v4-pro ~160s typical for 47K prompt)

### Step 6: Deliver

Save to `/tmp/triple_paper_hybrid_review_v4pro.md` AND copy to Desktop:
```bash
cp /tmp/triple_paper_hybrid_review_v4pro.md "/mnt/c/Users/Think/Desktop/三论文混合审阅_v4pro_YYYYMMDD.md"
```

## Verified Run: V63+V17+V16 (2026-08-07)

- 3 papers, 6 files (3 DOCX + 3 Lean proofs)
- Prompt: 47,104 chars
- v4-pro response: 7,841 chars in 159.5 seconds
- Results: V63=2/10, V17=3/10, V16=4/10 — all NOT READY
- Key findings: internal g_TC contradiction (2.60 vs 0.5) in V63, H₀ circularity in V17, 10⁸× dilution factor in V16
- Cross-paper: DM mechanism conflict (neutrino condensate vs GW energy), GW frequency conflict

## Pitfalls

### v4-pro Size Limit
While v4-pro worked for 47K chars, it silently hangs at >120K chars. 
- **Safe**: <50K chars → always use v4-pro for deep math review
- **Risky**: 50-100K chars → test carefully
- **Unsafe**: >120K chars → use v4-flash instead

### Prompt Truncation
For papers >100K chars each, extract ONLY the key sections (abstract, core derivations, conclusions). Do NOT include the full paper text. Use regex-extracted numerical claims as a lightweight summary.

### Missing Lean Content
If reviewing papers without Lean proofs, skip the Lean stats section but maintain the same prompt structure. The review will be less thorough on formal verification aspects.

### Single vs Multi-paper
This protocol is specifically for CROSS-PAPER consistency reviews. For single-paper deep reviews, use the standard 5-agent delegate_task pattern or the `references/paper-plus-lean-final-review.md` protocol.
