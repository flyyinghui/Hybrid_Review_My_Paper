#!/usr/bin/env python3
"""Multi-paper cross-review template using DeepSeek v4-flash thinking mode.
Usage: modify PAPER_PATHS and AXIOM_DOC, then run."""
import os, re, json
from docx import Document
from openai import OpenAI

# ════════════════════ CONFIGURE ════════════════════
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    # Try common .env locations
    for env_path in [
        "/mnt/d/123321/CityHDGanalysis/Spatial_Reasoning_Agent/.env",
        os.path.expanduser("~/.hermes/.env"),
    ]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("DEEPSEEK_API_KEY="):
                        API_KEY = line.split("=",1)[1].strip().strip('"').strip("'")

PAPER_PATHS = {
    "Paper1": {"docx": "/path/to/paper1.docx", "lean": "/path/to/proof1.lean", "label": "Paper 1 Title"},
    "Paper2": {"docx": "/path/to/paper2.docx", "lean": "/path/to/proof2.lean", "label": "Paper 2 Title"},
    "Paper3": {"docx": "/path/to/paper3.docx", "lean": "/path/to/proof3.lean", "label": "Paper 3 Title"},
}
AXIOM_DOC = "/path/to/shared_axiom_doc.md"  # shared framework reference
OUTPUT_PATH = "/tmp/multi_paper_review.md"

# ════════════════════ EXTRACTION ════════════════════
def extract_paper(docx_path, lean_path, label):
    data = {"label": label}
    if docx_path and os.path.exists(docx_path):
        doc = Document(docx_path)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        data["paper_text"] = "\n".join(paras)[:15000]
        data["total_paras"] = len(paras)
        # Extract key numbers
        num_pattern = r'(?:H[₀0]|λ_KLS|lambda_KLS|g_TC|CDM|DM:B|N_e|Omega_GW|z_eff|M_R|kappa|m_[\wν]|b[₀0]|C[₂2])\s*[=≈~]\s*[\d.eE+\-×x]+[^,\n]{0,60}'
        data["key_numbers"] = list(set(re.findall(num_pattern, "\n".join(paras))))[:30]
    if lean_path and os.path.exists(lean_path):
        with open(lean_path, 'r', encoding='utf-8', errors='replace') as f:
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
        data["lean_defs"] = re.findall(r'def\s+(\w+(?:_\w+)*)\s*:?\s*\w*\s*:=\s*([\d.eE+\-]+)', lean_text)[:40]
    return data

# ════════════════════ BUILD PROMPT ════════════════════
axiom_text = ""
if os.path.exists(AXIOM_DOC):
    with open(AXIOM_DOC, 'r', encoding='utf-8') as f:
        axiom_text = f.read()[:15000]

all_data = {}
for code, cfg in PAPER_PATHS.items():
    all_data[code] = extract_paper(cfg["docx"], cfg["lean"], cfg["label"])

prompt = f"""You are an expert mathematical physicist reviewing interconnected papers.

## REVIEW TASK
Review for: 1) Mathematical derivation accuracy 2) Numerical self-consistency (paper vs Lean) 3) Cross-paper consistency 4) Publication readiness

## SHARED FRAMEWORK
{axiom_text}

## PAPERS
"""
for code, d in all_data.items():
    prompt += f"""
### {d['label']}
Lean: {d.get('lean_lines',0)} lines | {d.get('lean_stats',{})}
Paper: {d.get('paper_text','')[:15000]}
Key numbers: {chr(10).join(d.get('key_numbers',[])[:20])}
Lean defs: {chr(10).join(f'{name} := {val}' for name,val in d.get('lean_defs',[])[:25])}
---

## OUTPUT FORMAT
1. Individual Paper Reviews (P0/P1/P2 per paper)
2. Cross-Paper Consistency Matrix (table)
3. Numerical Audit (verified calculations)
4. Publication Recommendations
5. Priority Fix Roadmap

Focus on mathematical and numerical correctness. Be specific.
"""

# ════════════════════ API CALL ════════════════════
print(f"Prompt: {len(prompt)} chars. Sending to v4-flash thinking...")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
resp = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=24576,
    temperature=0.0,
    timeout=600,
)
choice = resp.choices[0]
reasoning = getattr(choice.message, 'reasoning_content', '') or ''
content = choice.message.content or ''

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(f"# Multi-Paper Review — V4-Flash Thinking\n")
    f.write(f"Reasoning: {len(reasoning)} chars | Content: {len(content)} chars\n---\n")
    f.write(content)

print(f"Saved to {OUTPUT_PATH} ({len(content)} chars review, {len(reasoning)} chars reasoning)")
