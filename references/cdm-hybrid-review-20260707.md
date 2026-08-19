# CDM Topological Kink Paper — Hybrid Review Findings (2026-07-07)

## Context

Paper: "Cold Dark Matter as Emergent Topological Kinks from SL(6,C) Geometric Crystallization: Neural-Augmented Formal Proof of the 5:1 Mass Ratio"
- 76 paragraphs, ~3,100 words, 16 references
- Claims to prove CDM:visible = 5:1 ratio via SL(6,C) geometric crystallization
- Lean proof: 599 lines, 16 axiom lines, 8 `exact trivial`, 5 `admit`, 1 `sorry`

## 5-Agent Panel Scores

| Dimension | Score | Reviewer |
|-----------|:-----:|----------|
| Consistency | 3/10 | Consistency checker |
| Logic | 2/10 | Logic reviewer |
| Technical | 2/10 | Technical reviewer |
| Writing | 6/10 | Writing reviewer |
| Bibliography | 3/10 | Bibliography auditor |
| **Overall** | **3.2/10** | — |

## 6 P0 Showstoppers

| # | Finding | Source |
|---|---------|--------|
| C1 | **Rank 90 > matrix dim 70**: Lean asserts `rank A_final = 90` for a 70×70 matrix | Logic+Tech |
| C2 | **5:1 ratio hardcoded as A5**: `darkDegrees=75 ∧ visibleDegrees=15` encoded in axiom, not derived | Logic+Tech |
| C3 | **Lean proof is empty shell**: 8 axioms `exact trivial`, 5 lemmas `admit`, 4 theorems prove `True`, 31 undefined identifiers, 0% substantive | Consistency+Tech |
| C4 | **OllamaLens TEXTUAL_COOCCURRENCE = category error**: LLM co-occurrence ≠ mathematical validation | Logic |
| C5 | **Reference [9] fabricated co-authorship**: Listed as "Eldan & Chen (2021)" but Yuansi Chen is sole author | Bibliography |
| C6 | **KLS inequality misapplied**: KLS applies to ℝⁿ convex bodies, not infinite-dimensional moduli spaces | Tech |

## Editorial Decision

**NOT READY for submission (3.2/10)**

Recommended path: Downgrade from "formal proof" to "formalized conjecture" → target *Physics Letters B* (short format, single-idea focus).

## New Reusable Audit Pattern

P57: **Empty Shell Proof Detection** (hollow-proof-detection.md):
- Count `exact trivial` + `admit` + `:True` theorems + undefined identifiers
- If >50% of proof items are hollow → classify as "skeleton, not proof"
- 0% substantive ratio → 0/10 technical score
