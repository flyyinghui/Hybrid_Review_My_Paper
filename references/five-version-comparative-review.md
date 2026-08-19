# Five-Version Comparative Review Pattern

## When to Use
When the user has 3+ versions of the same paper and wants a comprehensive comparison across logical completeness, mathematical rigor, and testability dimensions.

## Pipeline (5 Steps)

### Step 1: Extract All Versions
```python
# Use python-docx batch extraction with unique output names
for f in version_files:
    tag = extract_version_tag(f)  # e.g. V11, V13, V15, V17, Final
    out = f'/tmp/6D_{tag}.txt'
    # Extract: Document(f).paragraphs → text → write out
```

### Step 2: Deploy Dimension-Specialized Reviewers
Two parallel agents (not 5 generic ones):
- **Agent 1**: Logic Completeness + Mathematical Rigor (combined)
- **Agent 2**: Testability + Publication Readiness (combined)

Each reads ALL versions and produces a scored comparison table.

### Step 3: Watch for Regression
Common pattern: a version labeled "Final" may actually be a pre-correction snapshot. 
- **Detection signal**: If "Final" uses SL(6,C)/SU(6) when V13+ uses SL(6,C)/SU(3,3) → it's a V4/V5 era artifact, not a genuine final
- **Check**: Compare key mathematical facts (moduli space dimension, w₀ value, GW sum rule presence) across versions

### Step 4: Track Prediction Evolution
Build a trajectory table for each major prediction:
- DM/baryon ratio: raw→corrected→tension acknowledgment
- GW frequencies: qualitative→quantitative with error bars
- w₀: static phantom (falsified)→hierarchical time crystals (matched post-hoc)
- g_TC: gap acknowledgment→RG flow→non-perturbative enhancement

### Step 5: Synthesize Roadmap
Not just "which is best" but:
- Which elements from each version should be combined?
- What was lost across versions that should be recovered? (e.g., V11's baryon depletion integral derivation)
- Phase 1→4 roadmap with specific actions and time estimates

## Key Pitfalls

1. **"Final" ≠ Final**: Always verify the final version against the evolution chain. A file named "Final" may be a pre-correction snapshot.
2. **Cosmetic fixes ≠ real fixes**: b₀ symbol changed to 39 but all downstream numbers still computed with 127 → detect by recomputing one downstream value
3. **Version count matters**: For 5+ versions, use 2 specialized agents not 5 generic ones (cost-efficient)
4. **Unique output names**: Never write all extractions to `/tmp/paper.txt` — use `/tmp/6D_{TAG}.txt`

## Verified Run
2026-07-30: V11/V13/V15/V17/Final comparison. V17 ranked first all 4 dimensions. "Final" identified as V4/V5 snapshot with wrong moduli space.
