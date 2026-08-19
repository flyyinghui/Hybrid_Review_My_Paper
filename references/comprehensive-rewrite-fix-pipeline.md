# Comprehensive DeepSeek Rewrite for Bulk P0 Fixes (V7→V8 Pattern)

**Established**: 2026-08-11, CGICE V7→V8 fix pipeline.

## When to Use

When a hybrid review finds 10+ P0/P1 fixes and they need to be applied in a single pass. Traditional patch-by-patch would take 30+ minutes of manual editing. A single comprehensive DeepSeek v4-flash call applies all fixes in ~60 seconds.

## Protocol (6 Steps)

### Step 1: Classify All Fixes
Categorize every review finding:
- **Mechanical**: global search-replace (manifold names, dimension values)
- **Section-rewrite**: replace entire subsections (§2.7 Bakry-Émery → honest statement)
- **Structural**: reorder sections, merge duplicates
- **Addition**: insert new subsections/paragraphs

### Step 2: Build Fix Instructions
Write explicit replacement text for each fix. For section rewrites, provide the EXACT replacement text (not "change X to be more honest about Y" — give the actual new paragraph).

### Step 3: Single v4-flash Call
- Model: `deepseek-v4-flash`
- Thinking: DISABLED (`extra_body={"thinking": {"type": "disabled"}}`)
- Temperature: 0.1
- Max tokens: 24576-28672
- Timeout: 600s
- Prompt = fix_instructions + "=== ORIGINAL PAPER ===" + paper_text

### Step 4: Verify Fixes
Run automated checks for each fix category:
- SU(3,3) count = 0
- Section ordering correct
- Key phrases present/absent
- Dimension values consistent

### Step 5: v4-pro Directional Audit
Single v4-pro audit to check fix direction — NOT a quality gate (see Pitfall 18).

### Step 6: Multi-Agent Final Gate
≥3-agent adversarial panel for final quality decision.

## Key Pitfalls

1. **F-string brace conflicts**: Fix instructions containing LaTeX with curly braces (`f^{k}_{munu}`) MUST use `.replace()` or `.format()` with careful escaping, NOT f-strings.

2. **Prompt size**: V7→V8 prompt was 53K chars — near but within the safe zone for v4-flash. Larger papers may need section-by-section fixing.

3. **Over-fixing**: The DeepSeek rewrite may apply fixes that weren't requested (e.g., adding new sections). Always diff the output against the original.

## Performance

| Method | Time | Consistency |
|--------|------|-------------|
| Manual patch-by-patch | ~30 min | Variable (human error) |
| Single comprehensive rewrite | ~60s | High (all fixes from single prompt) |

## CGICE V7→V8 Case Study

- 12 P0 + 8 P1 issues found by 5-agent review
- 53K char prompt with explicit fix instructions
- 64.3s generation time
- 10/12 P0 FIXED, 2 PARTIAL
- v4-pro audit: 7/10 (directional)
- Multi-agent verification confirmed all fixes landed correctly
