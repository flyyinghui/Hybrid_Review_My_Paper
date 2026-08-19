# Stage 2.5 Integrity Check Methodology

Proven methodology from the neutrino condensation paper hybrid review (2026-07-05).

## Reference Integrity Script

The core check extracts all reference entries and cross-references them against body citations:

```python
from docx import Document
import re

doc = Document(paper_path)

# Extract reference entries
ref_entries = {}
in_refs = False
for p in doc.paragraphs:
    t = p.text.strip()
    if t.startswith('[1]') and not in_refs:
        in_refs = True
    if in_refs:
        m = re.match(r'\[(\d+)\]\s*(.+)', t)
        if m:
            ref_entries[int(m.group(1))] = m.group(2)
        if 'APPENDIX' in t or 'Appendix' in t:
            break

# Extract all in-text citations
body_text = ' '.join([p.text for i, p in enumerate(doc.paragraphs) if i < ref_start_idx])
cited = set()
for m in re.finditer(r'\[(\d+(?:,\s*\d+)*)\]', body_text):
    for num in m.group(1).split(','):
        cited.add(int(num.strip()))

# Checks
gaps = [n for n in range(1, max(ref_entries.keys())+1) if n not in ref_entries]
uncited = set(ref_entries.keys()) - cited
missing = cited - set(ref_entries.keys())
```

## AI Failure Mode Checklist

Seven-mode checklist (adapted from ARS v3.2):

| Mode | Check | Indicator |
|------|-------|-----------|
| M1: Citation hallucination | All cited refs exist in list | `len(missing) == 0` |
| M2: Hallucinated results | Claims match verifiable sources | Cross-ref against known ground truth |
| M3: Shortcut reliance | Honest scope declarations present | Search for "limitation" / "honest scope" |
| M4: Bug-as-insight | No reversed causal claims | Manual review of proof chain |
| M5: Methodology fabrication | Tools described actually exist | Check for "Physics Proof Engine" etc. |
| M6: Frame-lock | Alternatives considered | Search for competing frameworks cited |
| M7: Data fabrication | Numerical values internally consistent | Compare Abstract vs body values |

## Key Findings from Application

The hybrid review discovered that ARS-only audit methods miss entire categories of issues that AWA agents catch:
- Bibliography collapse (6 wrong citations, 15+ missing, 3 duplicates)
- √2 convention split across sections
- Narrative structure breaks (missing transitions, undefined core concepts)
- Text corruption fragments
- AI-tell markers (91 em-dashes, 14 negation-contrasts)
