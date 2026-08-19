# DOCX Translation — Image Embedding Fix

**Problem**: When translating a DOCX via python-docx (extract → translate → rebuild), images are NOT preserved in the output. The rebuilt DOCX has translated text but zero media files and zero image references.

**Symptom**: Output DOCX file size drops dramatically (e.g., 1.14MB → 61KB). Opening in Word shows no images.

## Fix Protocol

### Step 1: Inject media files from source ZIP

```python
import zipfile

with zipfile.ZipFile(SRC_DOCX, 'r') as zf_src, zipfile.ZipFile(CN_DOCX, 'r') as zf_dst:
    media_files = [(n, zf_src.read(n)) for n in zf_src.namelist() if 'media/' in n.lower()]
    all_parts = {n: zf_dst.read(n) for n in zf_dst.namelist()}

with zipfile.ZipFile(CN_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf_out:
    for name, data in all_parts.items():
        zf_out.writestr(name, data)
    for name, data in media_files:
        zf_out.writestr(name, data)
```

### Step 2: Fix [Content_Types].xml — add PNG default

```python
import xml.etree.ElementTree as ET
CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
ET.register_namespace('', CT_NS)

ct = ET.fromstring(all_parts['[Content_Types].xml'])
has_png = any(e.get('Extension') == 'png' for e in ct if e.tag == f'{{{CT_NS}}}Default')
if not has_png:
    png_default = ET.SubElement(ct, f'{{{CT_NS}}}Default')
    png_default.set('Extension', 'png')
    png_default.set('ContentType', 'image/png')
    all_parts['[Content_Types].xml'] = ET.tostring(ct, encoding='UTF-8', xml_declaration=True)
```

### Step 3: Copy relationships from source

```python
# The CN DOCX has no image relationships. Copy from source:
all_parts['word/_rels/document.xml.rels'] = src_files['word/_rels/document.xml.rels']
```

### Step 4: Inject drawing XML elements

Translation preserves paragraph order, so images can be placed at proportional positions:

```python
import copy

src_paras = list(src_body.findall(f'{{{W}}}p'))
dst_paras = list(dst_body.findall(f'{{{W}}}p'))
ratio = len(dst_paras) / len(src_paras)

# Find image paragraphs in source (containing w:drawing)
for i, p in enumerate(src_paras):
    drawings = p.findall(f'.//{{{WP}}}drawing') + p.findall(f'.//{{{WP}}}inline')
    if drawings:
        dst_idx = int(i * ratio)
        new_p = copy.deepcopy(p)
        # Insert before sectPr (last child of body)
        dst_body.insert(list(dst_body).index(sect_pr), new_p)
```

### Step 5: Write back

```python
all_parts['word/document.xml'] = ET.tostring(dst_doc, encoding='UTF-8', xml_declaration=True)
with zipfile.ZipFile(CN_DOCX, 'w', zipfile.ZIP_DEFLATED) as zf_out:
    for name, data in all_parts.items():
        zf_out.writestr(name, data)
```

## Verification

```python
with zipfile.ZipFile(CN_DOCX, 'r') as zf:
    media = [n for n in zf.namelist() if 'media/' in n]
    print(f"Media files: {len(media)}")  # Must match source count
    doc_xml = zf.read('word/document.xml').decode('utf-8', 'replace')
    print(f"Has blip refs: {'blip' in doc_xml}")  # Must be True
```

## Pitfalls

1. **Don't forget Content_Types**: Without PNG default, Word may refuse to open the file even though images are in the ZIP.
2. **Don't forget relationships**: Images in ZIP but no relationship entries → images won't render.
3. **Copy drawing elements wholesale**: Trying to rebuild image XML from scratch fails — the `w:drawing` elements contain deeply nested OOXML structures (a:blip, wp:extent, wp:docPr, etc.). Deep-copy the entire paragraph element.
4. **NTFS write corruption**: Write the fixed DOCX to `/tmp/` first, then `cp` to the NTFS destination.

## Verified Run

2026-08-03: V63 neutrino paper (347 paragraphs, 6 images) → CN translation. After fix: 355 paragraphs, 6 images, 1013KB. All 6 images preserved with correct rId references.
