# Comparative Two-Paper Review Pattern (2026-08-01)

Deploy 5 specialized agents in 2 batches to compare two papers sharing a common mathematical framework.

## Agent Architecture

**Batch 1 — Quantitative (3 parallel agents)**:
- Framework consistency: shared foundations, contradictions, internal coherence
- Mathematical rigor: theorem:axiom ratio, Lean stats, derivation chain closure
- Predictive testability: predictive degree, falsification thresholds, experimental channels

**Batch 2 — Strategic (2 parallel agents, after batch 1)**:
- Publication strategist: venue recommendations, companion strategy, revision requirements, priority
- Cross-referencing synthesizer: mutual borrowing, cross-citations, unified narrative, incompatibility warnings

## Execution

1. Extract both DOCX to SEPARATE `/tmp/` files
2. Compute Lean stats (lines, axioms, theorems, lemmas, sorries, stubs)
3. Deploy batch 1 — 3 parallel agents, each reads both papers
4. Feed batch 1 findings into batch 2 context
5. Synthesize → `Hybrid_Review_[A]_vs_[B]_Comparative_[Date].md`

## Verified Run

2026-08-01: V17 (6D Spacetime, SL(6,C)/SU(3,3)) vs V61 (Neutrino Condensation, SL(6,C)/SU(6)). 
Found fatal SU(3,3)/SU(6) moduli space contradiction. V61 (6.0/10) > V17 (4.0/10) across all dimensions.

## Pitfalls

1. **v4-pro timeout >150K chars**: use v4-flash for full-paper review prompts
2. **Cross-batch context**: feed raw batch 1 summaries into batch 2, not just task descriptions
3. **Separate extraction files**: never loop two papers to same output path (last-write overwrites first)
