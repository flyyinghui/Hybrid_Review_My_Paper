# AWA-ARS Divergence Tracking Pattern

First observed during the V20a Neutrino Condensation paper hybrid review (2026-07-05). When both ARS pipeline audits and AWA parallel agent reviews are applied to the same paper, systematic divergence emerges in what each system catches.

## Divergence Pattern

| Issue Category | ARS Cross-Audit (C.5/C.0-C.4/§3) | AWA Parallel Review | Gap |
|:--|:--|:--|:--|
| Axiom/lemma/theorem counts | ✅ Catches all structural mismatches | ⚠️ Not designed for | AWA assumes structural consistency |
| Table content (axiom names, line counts) | ✅ Deep table audit | ⚠️ Not designed for | AWA reviews prose, not tables |
| Bibliography completeness | ❌ Not covered | ✅ Catches missing refs, wrong citations, duplicates | **Largest gap** |
| Narrative structure (§ transitions, GPS) | ❌ Not covered | ✅ Catches absent transitions, undefined terms | **Critical gap** |
| Mathematical convention consistency (√2) | ❌ Not covered | ✅ Catches convention splits across sections | **Critical gap** |
| AI-tell markers (em-dashes, negation-contrast) | ❌ Not covered | ✅ Quantitative detection | Stylistic |
| Text corruption detection | ⚠️ Partial | ✅ Catches orphaned math fragments | ARS only catches known patterns |

## Recommended Hybrid Coverage Matrix

For a complete paper review, both systems should run:

```
Stage 2a (AWA):
  ├─ bibliography-auditor    → Catches what ARS never checks
  ├─ consistency-checker     → Terminology, cross-refs
  ├─ logic-reviewer          → Narrative structure, GPS
  ├─ technical-reviewer      → Math conventions, formula splits
  └─ writing-reviewer        → Prose quality, AI-tell

Stage 2.5 (ARS Integrity):
  └─ Covers: citation verification, data accuracy, failure mode checklist

Stage 3 (ARS Formal Review):
  └─ Covers: 5-person panel, editorial decision, revision roadmap
```

## Key Finding

> **ARS catches structural errors (counts, table content, version drift). AWA catches content errors (bibliography, narrative, conventions, prose). Neither alone is sufficient.**
