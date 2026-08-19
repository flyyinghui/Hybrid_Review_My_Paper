# CGICE V9 R2 Hybrid Review — Header-Only Fix Pattern

**Established**: 2026-08-11, 2nd-round CGICE review.

## The Pattern

After a paper claims "P0 fixes applied," a second-round review found that the "fixes" were header notes appended to the paper without actually changing the body text. The paper simultaneously made contradictory claims (e.g., "within an order of magnitude" AND "~122 orders off").

## Detection Protocol

For R2+ reviews, verify each claimed fix by:
1. Find the original error text in the R1 report
2. Search for it in the current paper
3. If the error text STILL EXISTS alongside a correction note → NOT FIXED

## Score Divergence Pattern

v4-pro single-audit gave CGICE V9 9/10. 5-agent hybrid review found 8 P0 defects → 2/10 consistency + 3/10 logic + 1/10 math.

Rule: single-model audits inflate scores for papers with honest-sounding language. Multi-agent adversarial review is essential.

## Fix Protocol (from V9→V10)

1. Comprehensive DeepSeek rewrite with ALL fix instructions in single prompt
2. Verify each fix with automated grep-style checks
3. No "header notes" — change the actual body text
4. Post-fix: grep for old error phrases to confirm zero residue
