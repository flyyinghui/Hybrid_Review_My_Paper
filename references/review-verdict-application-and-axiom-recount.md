# Review-Verdict Application + Axiom Count Drift (2026-08-19 multi-paper session)

Workflow for applying a cross-paper review report's P0/P1/P2 verdicts to the
SL(6,C) four-paper set (V17 / CGICE / V63 / V16), then reconciling the MD-vs-Lean
axiom/theorem counts. Reused across three papers in one session.

## Step 1 — Scope the review to THIS paper (grep, don't assume)

A cross-paper review lists verdicts that may only apply to ONE paper. Before
editing, grep the target paper (MD + Lean) for the review's named references:

| Review verdict | grep for | Live in |
|---|---|---|
| P0-1 Deng-Hani molecular-chain misuse | `Deng` `Hani` `molecular chain` | V17 §III.F only (CGICE clean, V63 has `Deng-Hani cluster expansion` in Lean comments) |
| P0-2 Atiyah-Singer demotion | `Atiyah` `Singer` `index theorem` | V17 (12×) + V16; CGICE uses `D1 bridge` (phenomenological, already fine) |
| P1-3 Bourgain slicing caveat | `Bourgain` | V17 only |

If grep returns 0, SKIP that verdict for this paper — do NOT manufacture a fix
for a reference the paper never made. Say so in the report ("not applicable").

## Step 2 — Apply only the verdicts that hit

- **Ghost-reference removal**: replace the misused citation with the standard
  result it was masking + an audit tag. E.g. V63 `A_DH_T2 : G_c = 8π²/(N_R Λ²)`
  is the STANDARD NJL gap-equation critical coupling — the "Deng-Hani kinetic
  exactness" label is the misuse. Fix = relabel to "NJL gap-equation standard
  result [P0-1: Deng-Hani removed]" and keep the axiom (the formula is correct,
  only the attribution was wrong). Do NOT delete a correct axiom over a wrong
  label.
- **Atiyah-Singer demotion**: the classical theorem is compact-manifold-only;
  on non-compact SL(6,C)/SU(3,3) the Dirac operator has continuous spectrum and
  the Fredholm index diverges. The honest restatement is "Moscovici L²-index,
  (g,K)-cohomology heat-kernel coefficients uncomputed — research-level premise".

## Step 3 — Insert the Derivation-vs-Assumption boundary matrix (P1-1)

Every paper's intro gains a Table 1 with exactly three rows:

| Category | what goes in it |
|---|---|
| Derived | η_k = 72/35 = C₂·h^∨/dim, g_TC² = 24π²/35, \|ρ\|² = 35, DM:baryon 75:15 = 5.00 |
| Calibrated | τ_c = 4.01, N_e = 80.6, H₀ = 67.42, GW peak freqs, DM:baryon 5.47 |
| Postulated | SL(6,C) group choice, λ_⊥ = λ_∥/3 equipartition, strong log-concavity, μ_c |

This is the "derived vs calibrated vs honest-axiom" triage the review demands —
it catches overclaims (a calibrated number dressed as a first-principles
prediction) at a glance.

## Step 4 — Axiom-count drift (MD claims vs Lean reality)

The recurring P0 across all four papers: the MD states N axioms, the Lean file
has a different count, and the MD contradicts ITSELF. CGICE showed FOUR numbers
for one quantity:

- Abstract: "twenty-five axioms" (25)
- Intro: "fourteen axioms" (14)
- Conclusion: "61 axiom declarations" (61)
- Lean reality: 69

Detection: regex the MD for every `(\d+) axioms?` / `(twenty-|fourteen-|sixty-)`
phrase and diff against `grep -c '^axiom ' file.lean` (active lines, comments
excluded). Fix = ONE number everywhere, matching the Lean reality, phrased as
"N core axioms (A1–A25) + state variables + phenomenological calibrations =
N_total Lean declarations".

## Step 5 — Renumber for continuity (MD ↔ Lean)

When axioms were abolished (explosion-principle cleanup) or added (EEM A23–A25),
the A-numbering gets holes (A6, A17 missing; A16 misplaced). Rebuild a contiguous
A1–AN in BOTH files with one mapping table:

```
A7→A6  A16→A7  A11→A10  A12→A11  A13→A12  A14→A13  A15→A14
A18→A15 ... A25→A22   (then a26/a27/a28 → a23/a24/a25 in Lean)
```

Apply with `re.sub` + a mapping dict (word-boundary, order-independent — the
mapping is a pure function so no sequential-collision bugs). Renumber the Lean
`aN_name` identifiers with regex `\ba(\d{1,2})(?=[_\s:(])` (the `_` suffix means
`\b` alone misses `a16_master_equation`). Recompile to confirm the rename didn't
break call sites.

## Pitfall — docx run-splitting defeats naive string replace

A docx paragraph's text is scattered across many runs (each LaTeX symbol, each
font change is its own run — a 5-line axiom list had 47 runs). A
`p.text.replace(...)` on the whole paragraph text does NOT write back, and a
`for run in p.runs: if "needle" in run.text` misses needles split across runs.
Fix: print each run's text first, find the SINGLE run that contains the full
needle (or the longest fragment), replace there. Verify by re-reading
`p.text` after save.
