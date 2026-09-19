# Multi-Paper Cross-Review with DeepSeek V4-Flash Thinking

## When to Use

When you need to review **3+ papers simultaneously** with cross-paper consistency checking against a shared theoretical framework, use this single-API-call pattern instead of the standard 5-agent delegate_task approach.

**Advantages over delegate_task**:
- Single API call → no batch coordination, no synthesis overhead
- Thinking mode provides 30-50K chars of reasoning trace (useful for diagnosis)
- Cross-paper numerical consistency is checked in one context window
- ~3-5 minutes total (vs 5-10 minutes for multi-agent)

**When NOT to use**:
- Single paper reviews (use standard 5-agent pattern)
- Papers too large for context (>30K chars each → use delegate_task)
- When you need per-dimension scores (the single call gives holistic assessment)

## Pipeline

### Step 1: Extract Paper Content

```python
from docx import Document
import re

def extract_paper(docx_path, lean_path, label):
    data = {"label": label}
    
    # Paper abstract + first 15K chars
    doc = Document(docx_path)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    data["paper_text"] = "\n".join(paras)[:15000]
    
    # Lean stats
    with open(lean_path) as f:
        lean_text = f.read()
    data["lean_lines"] = len(lean_text.split('\n'))
    data["lean_stats"] = {
        "axioms": len(re.findall(r'(?<![/-])\baxiom\b', lean_text)),
        "theorems": len(re.findall(r'(?<![/-])\btheorem\b', lean_text)),
        "lemmas": len(re.findall(r'(?<![/-])\blemma\b', lean_text)),
        "sorries": len(re.findall(r'\bsorry\b', lean_text)),
        "honest_axiom": len(re.findall(r'\[honest.axiom\]', lean_text)),
        "phenomenological": len(re.findall(r'\[phenomenological\]', lean_text)),
    }
    
    # Numerical definitions
    data["lean_defs"] = re.findall(
        r'def\s+(\w+)\s*:?\s*\w*\s*:=\s*([\d.eE+\-]+)', lean_text
    )[:40]
    
    return data
```

### Step 2: Build Comprehensive Prompt

Structure:
```
## REVIEW TASK
[Clear instructions: math accuracy, numerical consistency, cross-paper, venues]

## SHARED FRAMEWORK
[SL(6,C) axiom doc or equivalent reference document ~15K chars]

## PAPER SUMMARIES
For each paper:
  - Paper text (first 15K chars)
  - Lean stats (lines, axioms, theorems, lemmas, sorries)
  - Key numerical values from paper
  - Lean definitions (def ... := ...)

## OUTPUT FORMAT
[Structured: Individual Reviews → Cross-Paper Matrix → Numerical Audit → Venues → Roadmap]
```

### Step 3: Call API

```python
from openai import OpenAI
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

resp = client.chat.completions.create(
    model="deepseek-v4-flash",  # thinking mode is DEFAULT
    messages=[{"role": "user", "content": prompt}],
    max_tokens=24576,
    temperature=0.0,
    timeout=600,
)

# Thinking trace in reasoning_content, final answer in content
reasoning = getattr(resp.choices[0].message, 'reasoning_content', '')
content = resp.choices[0].message.content

# Save both
with open(output_path, 'w') as f:
    f.write(f"# Review — V4-Flash Thinking\n")
    f.write(f"Reasoning: {len(reasoning)} chars | Content: {len(content)} chars\n")
    f.write("---\n")
    f.write(content)
```

### Step 4: Deliver

Copy to desktop:
```bash
cp /tmp/triple_paper_hybrid_review_*.md "~/Desktop/三论文混合审阅_*.md"
```

## Verified Run: V63+V17+V16 (2026-08-06)

- 3 papers, 6 files (3 DOCX + 3 Lean)
- Total extracted: ~45K chars paper text + ~20K chars axiom doc + stats
- Prompt: ~25K chars
- Reasoning: 48,693 chars
- Review: 15,796 chars structured output
- Time: ~4 minutes

Results: 10 P0 issues across 3 papers, 15-parameter cross-paper matrix, 11 numerical audit failures, all 3 papers NOT READY for publication.

## Pitfalls

1. **Prompt too large**: If the combined prompt exceeds ~120K chars, v4-flash may truncate. Target <80K chars. Use `paper_text[:15000]` per paper.

2. **Missing content**: v4-flash thinking mode may produce `content=""` if reasoning exhausts the token budget. Use `max_tokens=24576` minimum. If content is empty, check reasoning_content for partial results.

3. **Format instability**: The output format depends on prompt instructions. Be explicit: "Provide a structured review in Markdown with these sections: 1. Individual Paper Reviews 2. Cross-Paper Matrix 3. Numerical Audit 4. Publication Recommendations 5. Priority Fix Roadmap"

4. **Python .format() trap**: Never use `str.format()` with paper text containing LaTeX braces. Use `str.replace("__TOKEN__", value)` instead.
