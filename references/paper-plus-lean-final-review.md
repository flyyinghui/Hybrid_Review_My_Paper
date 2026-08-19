# Paper + Lean Proof 6-Agent Final Review Pattern

**Pattern established**: 2026-07-30, V17 6D Spacetime paper review.

## When to Use

When a theoretical physics/math paper has BOTH a manuscript DOCX and an associated Lean 4 formal proof file, deploy this 6-agent parallel review pattern instead of the standard 5-agent AWA review.

## Deployment: 3 Batches

### Batch 1: Structure + Logic + Technical (3 agents)

```
delegate_task(tasks=[
  {goal: "Consistency & Structure Reviewer: Audit internal consistency, 
          cross-reference integrity, terminology stability, paper-vs-Lean alignment.
          CHECK: all Lean stat claims in paper match actual .lean file stats.
          CHECK: abstract completeness, figure citations, version artifacts, 
          orphan references, duplicate paragraphs.",
   toolsets: ["terminal","file"]},
  {goal: "Logic & Argument Reviewer: Evaluate argument chain integrity, 
          claim support, gap honesty, circularity detection, Deng-Hani alignment.",
   toolsets: ["terminal","file"]},
  {goal: "Technical & Mathematical Reviewer: Check equation correctness, 
          dimensional analysis, boundary conditions, approximation validity,
          AND Lean proof quality (axiom/theorem ratio, tactic diversity, 
          :=True stubs, sorry count, tautological axioms).",
   toolsets: ["terminal","file"]},
])
```

### Batch 2: Writing + Bibliography + Lean Specialist (2-3 agents)

```
delegate_task(tasks=[
  {goal: "Writing Quality & Bibliography: Audit prose clarity, academic tone,
          paragraph structure, section transitions, citation format, bib completeness.",
   toolsets: ["terminal","file"]},
  {goal: "Deng-Hani Framework Compliance (if applicable): Score all 5 core 
          DH innovations, identify missing derivation steps, generate gap priority list.",
   toolsets: ["terminal","file"]},
])
```

## Pre-Flight: Extract File Stats

Before deploying reviewers, extract both paper text and Lean stats. **NEW (2026-08-04): Must also run numerical consistency pre-flight check** — Triple GW V13 review found paper and Lean describing DIFFERENT models (H₀=67.59 vs 67.42, z_eff=e^640 vs 4.29). See `proof-paper-cross-ref-revision/references/preflight-paper-lean-consistency-check.md`.

```python
# Paper
from docx import Document
doc = Document(paper_path)
text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])

# Lean stats
lean_text = open(lean_path).read()
stats = {
    'lines': len(lean_text.split('\n')),
    'axioms': count_startswith('axiom '),
    'theorems': count_startswith('theorem '),
    'lemmas': count_startswith('lemma '),
    'sorries': count_non_comment('sorry'),
    'honest_axiom': count('[honest-axiom]'),
    'true_stubs': count(':= True' or ':=True'),
    'tactics': count_tactic_calls(lean_text),
}

# ⚠️ MANDATORY: Numerical consistency check (2026-08-04)
# Compare ALL key numerical constants (H₀, z_eff, λ_KLS, Θ, DM:B ratio, N_e)
# between paper and Lean. If ANY conflict found, DO NOT deploy reviewers —
# fix the inconsistency first.
from preflight_consistency import check_paper_lean_consistency
conflicts = check_paper_lean_consistency(text, lean_text)
if conflicts:
    raise RuntimeError(f"Paper-Lean numerical conflicts: {conflicts}")
```

## Key Review Dimensions

| Dimension | Paper Check | Lean Check |
|:----------|:-----------|:-----------|
| Consistency | Cross-refs, terminology, numerical values | Paper claims vs actual stats |
| Logic | Argument chain, gap honesty, circularity | Axiom/theorem ratio, tautologies |
| Technical | Equation correctness, dimensions, BC | Tactic diversity, sorry/stub count |
| Writing | Prose, tone, citations, abstract | – |
| Framework | Deng-Hani compliance (if applicable) | Formalization completeness |

## Output Format

Final MD report with:
- 6-dimension scored table
- Critical findings (C1..Cn) with exact paper locations
- Lean verification sub-report with actual-vs-claimed comparison
- Prioritized P0/P1/P2 fix checklist
- Post-fix score estimate
- Venue recommendation

## Pitfalls

1. **Lean stat paper-vs-actual mismatch is near-universal.** Always extract actual stats before deploying reviewers. Feed actual stats to the consistency reviewer.
2. **:=True stubs ≠ sorries.** Both are gaps, but reviewers must distinguish. Sorries are explicit admissions; :=True stubs are hidden gaps.
3. **Tautological axioms**: `axiom geodesic_complete : exp_map x v = exp_map x v` — check for these.
4. **Axiom/theorem ratio > 3.0**: The formalization is predominantly assumptions, not derivations.
