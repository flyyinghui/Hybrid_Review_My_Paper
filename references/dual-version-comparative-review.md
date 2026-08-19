# Dual-Version Comparative Paper Review

## Pattern
When two versions of the same paper exist (e.g., expanded V11 vs condensed PRD), deploy a 5-agent hybrid review panel to compare them on three axes: logical completeness, mathematical rigor, and verifiability. Each agent scores both versions independently and identifies a winner on their assigned dimension.

## Agent Assignment

| Agent | Dimension | Key Questions |
|-------|-----------|---------------|
| EIC | Overall | Journal fit, originality, which version to submit |
| R1 | Logical Completeness | Narrative flow, transition smoothness, gap count |
| R2 | Mathematical Rigor | Derivation correctness, honesty about assumptions |
| R3 | Verifiability | Falsifiable predictions, parameter counting, testability |
| R4 | Devil's Advocate | Fatal flaws in each version, which is "less wrong" |

## Prompt Structure
- Include BOTH full papers in the prompt (V11 ~100K chars truncated to 25K+15K, PRD ~30K full)
- Each agent receives its dimension-specific system prompt
- JSON output: `{score_a, score_b, winner, justification, key_quotes_a, key_quotes_b}`

## Scoring Divergence Patterns
- **EIC prefers condensed version**: Higher scores on logical flow and falsifiability
- **Math reviewer prefers expanded version**: Higher scores on honesty and rigor
- **Verifiability splits**: EIC values sharp predictions (prefers condensed); Cosmo reviewer values honest limitations (prefers expanded)
- **Devil's Advocate aligns with EIC**: "More bounded claims are more testable"

## Session Reference
2026-07-26: 6D spacetime phase evolution paper. V11 (6.2MB, 100K chars, 507 paras) vs PRD (338KB, 30K chars, 138 paras). Scores: V11=5.8, PRD=6.4. EIC recommended PRD submission with honesty declarations fused from V11.
