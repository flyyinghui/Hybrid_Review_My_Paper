# Multi-Paper Translation Pipeline (V4-Pro + Anthropic SDK)

**Date**: 2026-08-06 | **Verified**: 3 papers (832 paragraphs total, ~23 min)

## Pipeline

```python
from anthropic import Anthropic
from docx import Document
import json, os, time

client = Anthropic(
    api_key=API_KEY,
    base_url="https://api.deepseek.com/anthropic",
    timeout=900,
)

CHUNK_SIZE = 1800  # words per chunk

def translate_chunk(text, chunk_i, total):
    prompt = f"""Translate this academic physics paper text from English to Simplified Chinese.
RULES:
- Preserve ALL LaTeX math EXACTLY as-is
- Preserve ALL numbers, units, Greek letters in math mode
- Use formal Chinese academic style (物理学术期刊水准)
- Do NOT translate proper names of theorems, institutions, or author names

Chunk {chunk_i+1}/{total}

TEXT:
{text}

CHINESE TRANSLATION:"""

    for attempt in range(3):
        try:
            resp = client.messages.create(
                model="deepseek-v4-pro",
                max_tokens=32768,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}],
            )
            content = ""
            for block in resp.content:
                if hasattr(block, 'text'):
                    content += block.text
            if content.strip():
                return content.strip()
        except Exception as e:
            time.sleep(30)
    return None
```

## Performance

| Paper | Paragraphs | Chunks | Time |
|-------|:--:|:--:|------|
| V16 (708KB) | 213 | 5 | ~6 min |
| V63 (736KB) | 428 | 9 | ~12 min |
| V17 (855KB) | 191 | 4 | ~5 min |

**Average**: ~43s per chunk, ~1.5 chunks per minute.

## Checkpoint/Resume Pattern

Store per-paragraph translations in JSON:
```json
{"done": {"0": "中文译文...", "5": "中文译文...", ...}, "total_paras": 275}
```

After each chunk:
1. Split translated chunk back into paragraphs (by `\n\n---\n\n` delimiter)
2. Map to original paragraph indices
3. Store in checkpoint JSON
4. Atomic write via `.tmp` + `os.replace()`

On resume: load checkpoint, skip already-translated indices.

## Pitfalls

1. **Paragraph count mismatch**: API may merge or split paragraphs. Match by count; fall back to storing whole chunk against first index.
2. **LaTeX corruption**: Always include "Preserve ALL LaTeX math EXACTLY as-is" in prompt. Still check output for broken `$$` or `\\(`.
3. **NTFS write issues**: Write checkpoint to `/tmp/`, not NTFS-mounted paths. Use `os.replace()` for atomic writes.
4. **Empty paragraphs**: Don't translate paragraphs < 15 chars (section breaks, figure captions). Keep as-is.
