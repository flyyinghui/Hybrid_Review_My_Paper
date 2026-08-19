# DOCX CN Translation Pipeline — DeepSeek v4-flash with Checkpoint

Reusable pattern for translating academic physics papers (EN→CN) via DeepSeek API
with batch checkpointing and python-docx reconstruction.

## When to Use

- Translating theoretical physics / academic papers from English to Chinese
- Paper size: 150-200 paragraphs, 30-80K characters
- Target: publication-quality Chinese prose with math/formula preservation

## Pipeline

### Phase 1: Extract + Structure

```python
from docx import Document
doc = Document(paper_path)
paras = []
for p in doc.paragraphs:
    if p.text.strip():
        style_name = p.style.name if p.style else 'Normal'
        paras.append({
            'text': p.text.strip(),
            'style': style_name,
            'heading': 'Heading' in style_name,
            'bold': any(run.bold for run in p.runs if run.bold)
        })
```

### Phase 2: Batch Translate with Checkpoint

**Critical**: Use `[N] text` output format, NOT `<SEP>` markers. DeepSeek v4-flash
naturally produces `[N] Chinese translation` with blank-line paragraph separation.
`<SEP>` markers are inconsistently honored by the model and cause 0/35 parse failures.

```python
BATCH_SIZE = 33  # ~8K chars per batch
batches = [paras[i:i+BATCH_SIZE] for i in range(0, len(paras), BATCH_SIZE)]

SYSTEM_PROMPT = """Translate each English paragraph into Chinese academic physics prose.
Rules:
- Output format: [N] Chinese translation (one per paragraph)
- Separate paragraphs with a blank line
- Preserve ALL numbers, formulas, refs [N], and equation labels EXACTLY
- Use standard Chinese physics terms
- Academic tone, no colloquialisms
- Output ONLY translations, no commentary"""

# Parse response: [N] text with blank-line separation
blocks = re.split(r'\n\n+', content)
for block in blocks:
    m = re.match(r'\[(\d+)\]\s*(.+)', block.strip(), re.DOTALL)
    if m:
        translated[m.group(1)] = m.group(2).strip()
```

### Phase 3: Rebuild DOCX

```python
doc_cn = Document()
doc_cn.styles['Normal'].font.name = 'SimSun'
doc_cn.styles['Normal'].font.size = Pt(11)
doc_cn.styles['Normal'].paragraph_format.line_spacing = 1.5

for pi, p in enumerate(batch):
    cn_text = translated.get(str(pi), f'[UNTRANSLATED] {p["text"][:80]}')
    if p['heading']:
        doc_cn.add_heading(cn_text, level=2)
    else:
        doc_cn.add_paragraph(cn_text)
```

## API Configuration

```python
from openai import OpenAI
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

resp = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[...],
    max_tokens=16384,
    temperature=0.1,
    extra_body={"thinking": {"type": "disabled"}}  # CRITICAL: disable thinking mode
)
```

**v4-flash thinking-mode trap**: Without `extra_body={"thinking": {"type": "disabled"}}`,
the model routes output to `reasoning_content` instead of `content`, returning empty
translation text. This is the #1 cause of 0-paragraph failures.

## Checkpoint Pattern

```python
CKPT = '/tmp/translation_ckpt.json'
completed = {}
if os.path.exists(CKPT):
    with open(CKPT) as f: completed = json.load(f)

for bi, batch in enumerate(batches):
    if str(bi) in completed:
        continue  # Skip cached
    # ... translate ...
    completed[str(bi)] = translated
    with open(CKPT, 'w') as f:
        json.dump(completed, f, ensure_ascii=False)
```

## Terminal Heredoc Trap

In WSL background terminals, `<< 'PYEOF'` heredocs for multi-line Python scripts
can fail silently — the bash process starts but never spawns Python. **Fix**: Write
the script to a `.py` file first, then execute:

```bash
# WRONG — heredoc in background terminal may hang:
terminal(background=True, command='python -u << EOF\n...\nEOF')

# RIGHT — write script file first, then execute:
write_file('/tmp/script.py', content)
terminal(background=True, command='python -u /tmp/script.py')
```

## Verified Run

2026-07-30: V17 6D spacetime paper (196 paragraphs, 48K chars) → 6 batches × 33 paras.
All 196/196 paragraphs translated. Key formulas preserved: SL(6,C), 35/3, Witten,
DESI, CGICE, 5,867, 1.71±0.15.

## Related Reference

- `references/docx-translation-image-embedding-fix.md` — Fix for images lost during
  DOCX rebuild after translation. Covers 5-step ZIP-level protocol: inject media,
  fix Content_Types, copy relationships, inject drawing XML, verify.
