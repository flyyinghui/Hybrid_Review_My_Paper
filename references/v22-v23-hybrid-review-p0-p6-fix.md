# P0-P6 Prioritized Fix Pipeline: V22→V23 Hybrid Review Execution

**Session**: 2026-07-06  
**Source**: Hybrid Review Stage 2a — 5 AWA agents, 71 findings (26 Critical / 22 Important / 23 Minor)  

## Synthesis Methodology

After receiving 5 parallel agent reports, synthesize findings across ALL agents before implementing. Group by cross-agent consensus:

| Pattern | Flagged by | Priority |
|:--|:--|:--|
| Overclaiming ("maximally falsifiable", "no free parameters", "first-principles resolution") | 4/5 agents | P0-P2 |
| Terminology inconsistency (postulate/conjecture/hypothesis/resolution) | 3/5 agents | P0, P4 |
| λ_KLS ≈ 11.7 provenance misattributed to Klartag & Lehec | 2/5 agents | P0 |
| Citation system broken | 2/5 agents | P6 |
| AI-tell markers (profound, deep, crucial, remarkable) | 1/5 agent | P7 |
| No section transitions (5 boundary gaps) | 1/5 agent | P3, P8 |

## P0-P6 Implementation

| # | Fix | Effort | DOCX | Lean |
|:--|:--|:--|:--|:--|
| P0 | λ_KLS provenance: Klartag & Lehec proves POSITIVITY, not numerical value | Medium | ✅ 4 replacements | ✅ A2 comment |
| P1 | "No free parameters" → "three calibrated parameters (γ, κ, m_τ)" | Small | ✅ 3 replacements | — |
| P2 | "Maximally falsifiable" → "indirectly testable through low-energy observables" | Small | ✅ 5 replacements | — |
| P3 | Add §2.2.3→§2.3 transition paragraph | Small | ✅ ElementTree insertion | — |
| P4 | Introduction: "first-principles resolution" → "postulate-driven framework" | Small | ✅ | — |
| P5 | Stern-Brocot Σm_ν: 0.062→0.064 eV (raw sum 0.0636) | Small | ✅ 3 targeted replacements | — |
| P6 | Citation system rebuild: duplicates, ghosts, uncited | Large | ⚠️ Deferred to V24 | — |

## DOCX Modification Pattern

```python
# Pattern: Raw XML string replacements preserve OMML equations
xml = xml.replace(old_text, new_text)

# Pattern: ElementTree body insertions for new paragraphs
from xml.etree import ElementTree as ET
root = ET.fromstring(xml)
body = root.find("{ns}body")
new_elem = ET.fromstring(xml_string)
body.insert(index, new_elem)

# Pattern: Always cleanup + verify
xml = re.sub(r'<[^>]*(begChr|endChr|sepChr|grow)[^>]*/>', '', xml)
zipfile.ZipFile(dst).testzip()  # must be None
```

## Cross-Audit Verification

```python
checks = [
    ("definitional identity", 0),      # DOCX: 0 residual
    ("bridging postulate", "> 10"),    # Both files
    ("first-principles resolution", 0), # Removed
    ("three calibrated", 3),           # DOCX: 3 occurrences
    ("indirectly testable", 5),        # DOCX: 5 occurrences
    ("0.062 eV", "phenomenological only") # Stern-Brocot fixed
]
```

## Deferred to V24

- P6: Citation system — 11 uncited refs need individual verification
- P7-P10: Prose quality — AI-tell markers, B4 negation-contrast, section transitions
- Stern-Brocot vs phenomenological mass clear demarcation
- g_TC dual role (gauge + NJL) clarification
