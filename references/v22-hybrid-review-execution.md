# V22 Hybrid Review Execution Record (2026-07-06)

Full Stage 2a hybrid review of the neutrino condensation paper after F2 bridging postulate upgrade (V21→V22).

## Deployment

| Batch | Agents | Time | Issues Found |
|:--|:--|:--|:--|
| 1 | consistency-checker + logic-reviewer + technical-reviewer | ~190s | 42 |
| 2 | writing-reviewer + bibliography-auditor | ~183s | 29 |
| **Total** | **5 agents** | **~6 min parallel** | **71** |

## Key Findings by Agent

### Consistency Checker (16 issues)
- Ghost cross-ref "Section 4.4.4" → should point to §2.4.1 or §C.8
- Double "Table 1" — two unrelated tables
- Section numbering typos: "2.2. 2", "4 .3", "4 .3.1", "4 .3.2"
- Abstract "bridging identity" vs body "bridging postulate" — terminology mismatch
- "APPENDIX C.C8" and "Appendix C.0.1" formatting errors
- "Lemma Box 2.1" does not exist
- Figure 4/5 referenced out of order

### Logic Reviewer (13 issues, score 4/10)
- **Zero transition §2.2.3→§2.3** — most important pivot has no bridging sentence
- Abstract claims "postulate"; Introduction claims "first-principles resolution" — epistemic mismatch
- D1 content appears BEFORE its own subsection heading (§2.2.3)
- Forward references to undefined concepts (phantom DE, SPB, CGICE, time crystals)
- "Falsifiable prediction" for D1 not cleanly separable from seesaw chain
- Missing transitions at 5 section boundaries

### Technical Reviewer (13 issues, score 5/10)
- **λ_KLS ≈ 11.7 is NOT from Klartag & Lehec (2022)** — their paper proves dimension-dependent bound, not universal constant
- g_TC serves incompatible dual roles (gauge coupling + NJL four-fermion)
- Weinberg angle analogy misleading — θ_W is independently measured; g_TC is defined only through D1
- √2 convention inconsistently visible across formulas
- Multiple inconsistent DESI bound citations
- Stern-Brocot vs phenomenological mass values confused under same Σm_ν

### Writing Reviewer (score 5/10)
- **Overclaiming**: "maximally falsifiable" for unmeasurable M_R ≈ 10¹⁴ GeV
- **Contradiction**: "no free parameters" vs internal admission of 3 calibrated parameters
- **AI-tell markers**: "profound" (4×), "deep correspondence", "crucially", "remarkably", "We emphasize" (5×)
- **B4 negation-contrast trap**: 7 instances of "not X but Y"
- §2.2.3 reads like grant-proposal prose in a technical paper
- Sentence length: 32.1% exceed 30 words; 7.6% exceed 50 words

### Bibliography Auditor (16 issues)
- **11 references never cited in body**
- Duplicate [28] (Berges + Cheeger-Simons share same number)
- Ghost duplicate [16] in reference [1]
- [14] is not a real reference — sentence fragment
- Citation number mismatches: Brenier [31]→[30], Wetterich [18]→[27], Isham [40]→[39]
- Klartag & Lehec [2] does NOT give numerical value 11.7

## Revision Follow-up (P0-P10)

See `proof-paper-cross-ref-revision/references/v22-v24-multi-pass-revision.md` for the full revision chain.

## Pattern

AWA agents found 40+ content/prose/narrative issues that a structural-only audit (counting axioms, checking table numbers) would never detect. Confirms the hybrid review thesis: **ARS catches structural errors; AWA catches content errors. Neither alone is sufficient.**
