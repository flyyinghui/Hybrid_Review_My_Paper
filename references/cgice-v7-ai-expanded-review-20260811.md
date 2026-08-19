# CGICE V7 — 5-Agent Hybrid Review of AI-Expanded Paper (2026-08-11)

## Context

V6 CGICE paper (190 lines, 11K chars, 14 axioms, 3 theorems) was expanded to V7 (780 lines, 46K chars) via DeepSeek v4-flash. Expansion added CGICE-1~4 dynamical equations, two appendices, §2.5-2.7 (phase space), T4 theorem, and expanded references.

## Review Configuration

5 agents in 2 batches. Focus: logical self-consistency + mathematical rigor.

**Batch 1** (3 agents): consistency-checker, logic-reviewer, math-rigor-reviewer
**Batch 2** (2 agents): writing-reviewer, bibliography-auditor

Token cost: ~1.6M input / ~43K output across 5 agents (~347s total).

## Key Findings

### Structural Pattern: AI-Expanded Papers Inherently Produce Duplicate Sections

When an LLM is asked to "add an extended discussion section" (§9) after already having a "duality discussion" (§6), the model produces **near-verbatim duplication** (52-73% word overlap). Three subsection titles were identical between §6 and §9.

**Detection method**: word-overlap ratio between section pairs. Flag at >40%.

### Structural Pattern: Reverse Ordering — Equations Before Axioms

The expansion placed CGICE-1~4 dynamical equations (§3) BEFORE the axiom system (§4). This is structurally indefensible — the reader cannot evaluate equations whose axiomatic basis hasn't been introduced. The LLM followed the instruction to "insert after §2.4" without recognizing the logical dependency.

**Prevention**: Explicitly instruct the expansion prompt to maintain axiom→equation ordering. Better: insert equations as a *consequence* section after axioms.

### Mathematical Pattern: Manifold Inconsistency Across Sections

The V6 paper used SL(6,C)/SU(6) throughout. The V17 reference introduced SL(6,C)/SU(3,3) as the "correct" manifold for CGICE dynamics. The V7 expansion mixed BOTH without reconciliation — §2.1-2.4, §2.7, Axiom A1 use SU(6); §2.5-2.6, §3, Appendix A use SU(3,3). Worse: dim(SL(6,C)/SU(3,3)) = 70−17 = **53**, not 35.

**Detection**: grep section-by-section for manifold identifiers; flag any section that disagrees with the axiomatic definition.

### Mathematical Pattern: Bakry-Émery Derivation on Wrong Manifold

§2.7 attempted to derive λ₁=35/3 via Bakry-Émery theory on SL(6,C)/SU(6), but:
- Non-compact symmetric spaces have NEGATIVE Ricci curvature (Ric=−½g), not positive
- The CD(ρ,∞) inequality (3/2)g ≥ (35/3)g is manifestly false (1.5 ≥ 11.67)
- 35·(1/√35)² = 1, not 35/3 — arithmetic error
- KLS inequality applies to convex bodies in ℝⁿ, not to non-compact symmetric spaces

**Pattern**: When an LLM is asked to "derive" a value that is actually a group-theoretic input (|ρ|²=35, /3 = isotropy assumption), it fabricates a mathematical path. Review must independently verify every derivation chain.

### Verification Pattern: Paper-Ahead-of-Lean Sync Gap

V7 paper claims T4 (topological charge conservation) exists and is "formally verified." The Lean proof file (cgice_proof_v6_fixed.lean) has only 3 theorems — T1, T2, T3. No T4 exists. Appendix A.4 itself admits "in progress."

**Detection**: Cross-reference every theorem claim in paper against `grep -c 'theorem' proof.lean`.

### Prose Pattern: T1 Proof Admits Tautology

§5.1 explicitly states "This is a tautology" then jumps to the result with no logical bridge. This is an LLM faithfully "deriving" the equation by acknowledging it reached a dead end, then asserting the desired answer anyway.

## Scores

| Agent | Score | Key Issue |
|-------|-------|-----------|
| Consistency | 3/10 | Two manifolds, 2 RG equations, T4 fake-verified, axiom count drift |
| Logic | 2/10 | Reverse order, T1 tautology, T2 decay≠periodic, §6/§9 duplicate |
| Math Rigor | 1.2/10 | 5+ errors in §2.7 alone, CGICE-1~3 ill-defined on manifold |
| Writing | 4.5/10 | §6/§9 52-73% overlap, 43 sentences >30w, American spelling |
| Bibliography | 6/10 | 25% references uncited, 3 arXiv-only not flagged |

**Overall: 3.3/10 — NOT READY FOR SUBMISSION**

## Lessons for Future AI-Expanded Papers

1. **Always cross-ref expanded paper against original Lean proof** — expansion may add theorems not in Lean
2. **Check for manifold/symmetry-group drift** — LLMs mix up closely related mathematical objects
3. **Verify every "derived" value** — 35/3 has a group-theoretic origin (|ρ|²=35, /3 isotropy), not a KLS/Bakry-Émery derivation
4. **Scan for section duplication** — word-overlap >40% between non-consecutive sections = AI artifact
5. **Check equation ordering** — axioms must precede equations that depend on them
6. **RG flow calculations are high-risk** — LLMs cannot reliably compute numeric values from formulas; always spot-check
