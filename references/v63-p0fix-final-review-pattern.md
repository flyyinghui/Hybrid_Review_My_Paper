# V63 P0Fix Final Review Pattern (2026-08-04)

## Two-Stage Review Process

When a paper receives a detailed P0/P1 issue list and undergoes systematic fixes, use this two-stage review:

### Stage 1: Cross-Audit (before re-review)
1. Extract DOCX text + Lean ground truth counts
2. Run 26-check verification (see `proof-paper-cross-ref-revision/references/p0-fix-verification-checklist.md`)
3. Flag any residual P0 issues BEFORE launching review agents
4. Fix remaining issues immediately

### Stage 2: Final Hybrid Review (after audit passes)
1. Deploy 5-agent panel with P0 fix context injected
2. Each agent scores independently on their dimension
3. Journal recommendation with specific venue + rationale

## V63 Case Study

### P0 Issues from Initial Review
| # | Issue | Resolution |
|---|-------|-----------|
| P0-1 | m_D arithmetic error | FALSE POSITIVE — paper was correct |
| P0-2 | m_ν internal contradiction | FALSE POSITIVE — self-consistent by construction |
| P0-3 | κ=3505.8 doesn't satisfy β-function | FIXED: 3505.8→3266.67 (9800/3) |
| P0-4 | Stern-Brocot M_RS matrix error | FIXED: M_RS[2,1]=3→4 |
| P0-5 | "parameter-free" overclaims | FIXED: →"phenomenological predictions" |
| P0-6 | β-function scalar double identity | FIXED: honest note added to Appendix A |

### Key False Positives
The subagent reported:
- "Appendix M: 88→68 axioms" — FALSE. Subagent used grep that included block comments. Direct regex on code_only confirmed 88.
- "LEAN Code sorries=5 not 6" — Header fix removed one "sorry" occurrence from a block comment, dropping count from 6→5. The 5 remaining are all in documentation, 0 in actual proof code.

### Lessons
1. **Always verify subagent counts with direct regex**: Subagent grep-based counting is unreliable for Lean files with block comments.
2. **Header fixes can shift counts**: Track expected changes when editing headers that contain counted keywords.
3. **Unicode formatting mismatch**: DOCX uses both `×10¹³` (Unicode) and `x10^13` (ASCII) — search both.
