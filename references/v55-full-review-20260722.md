# V55 Hybrid Review: Full Session Record (2026-07-22)

## Timeline

```
Day 1:
├── Initial 5-agent review → 3.1/10 REJECT (10 Critical)
├── C3 fix: g_TC² 6.748→24π²/35≈6.768 (Lean + DOCX)
├── C4+C6 fix: D1 from "proven theorem" → three-layer (definitional postulate → conditional theorem → phenomenological hypothesis)
├── C5 fix: dual-path "independent verification" → "consistency check / redundancy check"
├── Appendix C sync with Lean ground truth (lines 1266→1315, definitions 4→5, seesaw_scale_kls→chern_simons_mass_suppression)
├── CN translation (708 paragraphs, 13 batches)
└── Re-review → 4.3/10 CONDITIONAL

Day 2:
├── C1 fix: predictive degree −1→+2 (user corrected: outputs exceed inputs)
├── C2 fix: "GEOMETRICALLY DETERMINED" → "PHENOMENOLOGICALLY FIXED with geometric motivation from A₅ |ρ|²=35"
├── §2.5 "net −1" contradiction fixed
├── Final review → 5.5/10 ✅
└── Contribution Comparison Review (3 experts: neutrino theory + cosmology + publication strategy)
```

## Key Patterns

### Predictive Degree Audit Protocol

When a paper's predictive degree appears in multiple locations with contradicting values:
1. Extract ALL occurrences across DOCX (grep XML for "predictive degree")
2. Verify parameter accounting: count inputs (calibrated κ, postulated D1, phenomenological λ_KLS) vs outputs (masses, scales)
3. User makes the final decision on the counting scheme
4. Bulk XML replace ALL occurrences to unified value
5. Re-verify with grep for both old and new values

### Honest-Language Upgrade Pattern

When a paper claims "geometric derivation" of a quantity that was actually fixed phenomenologically:
- BEFORE: "GEOMETRICALLY DETERMINED" → implies first-principles derivation
- AFTER: "PHENOMENOLOGICALLY FIXED by requiring [observable] in [range], with qualitative geometric motivation from [root system]" → honest about the circularity
- Apply to ALL occurrences: body text, tables, Lean comments
- Verify: grep for old phrasing → must return 0

### Three-Layer D1 Status Pattern

For a definitional identity that bridges geometry and physics:
1. **Definitional postulate** (physical level): g_TC² ≡ 8π²/λ_KLS defines the correspondence
2. **Conditional theorem** (formal level): follows from declared axioms in Lean
3. **Phenomenological hypothesis** (testable level): λ_KLS=35/3 is fixed by requiring M_R in seesaw window

### Contribution Comparison Review Mode

When user asks "比较学术贡献度":
- Deploy 3 domain experts (not 5 generic reviewers)
- Output: 1-10 comparison table vs competing models + publication strategy
- Key dimensions: M_R anchoring, flavor structure, testability, theoretical motivation, formal verification

## Publication Recommendation

- **EPJC** (primary): best fit for theoretical construction papers
- **PRD** (backup): needs |m_ββ| + leptogenesis supplement
- Pre-submission must-dos: |m_ββ| calculation, leptogenesis η_B, N_eff constraint, parameter sensitivity
