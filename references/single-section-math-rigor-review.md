# Single-Section Mathematical Rigor Review

When the user requests a focused review of a specific section's mathematical derivation (not the full paper), use a compact 3-specialist panel instead of the full 5-7 agent review.

## Deployment

```python
delegate_task(tasks=[
    {"goal": "technical-reviewer: Audit every mathematical step...", 
     "context": "Read /tmp/section.txt and /tmp/paper_context.txt...",
     "toolsets": ["terminal","file"]},
    {"goal": "logic-reviewer: Evaluate derivation coherence...", 
     "context": "Check logical chain validity, hidden assumptions...",
     "toolsets": ["terminal","file"]},
    {"goal": "consistency-checker: Audit internal consistency...", 
     "context": "Verify status labels, references, honest-scope...",
     "toolsets": ["terminal","file"]},
])
```

## Review Dimensions (Math Rigor Focus)

| Reviewer | Focus | Example Questions |
|:--|:--|:--|
| Technical | Math correctness | Are theorems correctly stated? Are proofs valid? Category errors? |
| Logic | Derivation coherence | Do stages logically chain? Hidden assumptions? Status labels honest? |
| Consistency | Internal alignment | Status table vs text consistent? References real? Contradictions? |

## Scoring

Three independent scores /10, weighted equally. Overall < 5/10 = NOT READY for integration.

## Verified Run: λ_KLS v6 Review (2026-07-24)

- Target: Section_lambda_KLS_Rigorous_Derivation_V57_Replacement_v6.docx
- Context: V57 paper §2.3-2.4
- Scores: Technical 3/10 | Logic 4/10 | Consistency 4/10 → **3.7/10 REJECT**
- 7 Critical findings: arithmetic error, ρ definition inconsistency, Eldan-Chen category error, Birman-Schwinger unjustified, 4 hidden assumptions, "proof sketch" labeled RIGOROUS, Deng-Hani placeholder reference
