# Section Alignment via v4-pro + DOCX Insertion

When two papers have diverged on a shared topic (GW peaks, H₀ status, λ_KLS usage), use this workflow to realign the older/unreviewed paper to the ground-truth paper.

## Workflow

1. **Designate ground truth**: Pick the most-recently-reviewed paper (e.g., V16 after 3-round hybrid review)
2. **Extract ground truth section**: DOCX → full text for context injection
3. **Extract target section**: Identify paragraph indices (python-docx `enumerate(doc.paragraphs)`)
4. **Generate replacement**: deepseek-v4-pro, max_tokens=8192, temp=0.2
   ```
   Prompt: "Rewrite [target section] to be STRICTLY CONSISTENT with [ground truth].
   Use EXACTLY these values: [list]. Mark all unproven claims with [honest-axiom]."
   ```
5. **Parse output**: Split by `**PART 1**` / `**PART 2**` markers, then by `\n\n` for paragraphs
6. **Insert into DOCX**: 
   ```python
   for j in range(start, end):
       for run in doc.paragraphs[j].runs:
           run.text = ''
       doc.paragraphs[j].runs[0].text = new_paras[j - start]
   ```
7. **Fix cross-references**: grep for old terms ("two-peak"→"three-peak", "10⁻⁸ Hz"→"4.5×10¹¹ Hz") in other sections
8. **Verify**: Check old terms removed, new values present

## Pitfalls

### v4-pro timeout on 8192 tokens
v4-pro may hang on max_tokens=8192 (known trap). If >4 min with no output, kill and fall back to v4-flash (thinking=disabled). v4-flash is faster but may produce slightly lower-quality prose.

### DOCX paragraph boundary mismatch
Generated text often has different paragraph count than target DOCX. Solution: merge remaining new paragraphs into last target paragraph, or add new paragraphs via `doc.add_paragraph()`.

### Cross-reference contamination
When fixing "two-peak"→"three-peak", the replacement may also hit unrelated mentions (e.g., "two-peak" in figure caption vs text). Use targeted run-level replacement, not global XML replace.

### v4-pro output uses LaTeX
Generated content may use `\section{}` / `\subsection{}` / `\begin{equation}`. Strip section headers with `.replace()` for DOCX insertion.
