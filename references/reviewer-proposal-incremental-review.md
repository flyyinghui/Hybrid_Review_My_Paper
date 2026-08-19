# Reviewer-Proposal Incremental-Value Review Protocol (2026-07-17, ninth verified run)

When the USER receives a reviewer MD proposing mathematical upgrades to specific manuscript
sections, do NOT run the full 5-agent paper review. Run this targeted protocol instead.

## When to use
- Input = reviewer MD file proposing to "rigorize" / replace specific sections (e.g. §2.3.1–2.3.3)
- Question = "does this proposal improve rigor?" and/or "can conjecture X now be proven as theorem?"

## Protocol (validated on 论文审稿意见_右手中微子凝聚20260717_1.md vs V52)

1. **Extract the CURRENT manuscript section first** (python-docx, locate by heading prefixes,
   dump to /tmp/*.txt). Do not skip this — in the verified run, V52 §2.3.1–2.3.3 ALREADY
   contained ~80% of the reviewer's "new" derivation. Without extraction the review would
   have wildly overestimated incremental value.
2. **Assemble ADVERSARIAL CONTEXT** and inject it into every reviewer prompt:
   - All prior review verdicts on the same topic (e.g. "Bakry-Émery formula judged fabricated
     2.35/10 on 2026-07-15"), with dates and scores
   - Known unresolved P0 issues from earlier panels (e.g. V46's 6 P0 items on the D1 chain)
   - The ACTUAL current stats of companion artifacts (Lean axiom/theorem counts) — reviewer
     MDs frequently quote stale numbers from older versions
3. **Deploy 3 specialists, not 5** — one per mathematical domain of the proposal:
   e.g. harmonic analysis (standard-result verification), probability/geometric analysis
   (the novel scaling claim), gauge theory/ergodic theory (the theorem-upgrade claim).
   Each gets: reviewer MD (base64 images stripped) + current section text + adversarial
   context + domain-specific numbered questions + score axes.
4. **deepseek-chat, temperature=0.0, max_tokens=8192, incremental .part saves** (same
   engine constraints as full hybrid review; 3 sequential calls finish in ~2 min).
5. **Infrastructure feasibility check** (cheap, high-value): grep the MathCode INDEX.json
   for the proposal's key tools. Zero/near-zero hits (e.g. Matsushima=0, Ratner=2 out of
   113K entries) = the proposed proof chain cannot be formalized beyond honest-axioms —
   strong evidence for "conditional theorem at best".
6. **Synthesize into a verdict MD saved in the paper directory** (user preference: file
   delivery via MEDIA, not chat-only), answering the user's questions directly with a
   per-section score table and an "absorb / reject / compromise" action list.

## Detection patterns that fired in the verified run

- **Fabrication resurrection**: a previously-rejected formula reappears under a new name
  ("Bakry-Émery equipartition theorem" repackaging the rejected λ₀·dim/(dim+2λ₀) scaling).
  Detector: same target value + same domain-crossing + no citation for the load-bearing
  theorem. Counter-evidence to cite: log-concave projections only DECREASE the Poincaré
  constant (Bobkov 2003); Gaussian marginal counterexample.
- **Duplication masquerading as increment**: reviewer restates existing manuscript content
  and claims to "complete a missing pipeline". Detector: side-by-side extraction (step 1).
- **Stale companion stats**: reviewer MD cited "54 honest axioms / 82 total" (V50/V51 data)
  against a V52 file with 9 axioms/8 theorems/7 lemmas. Always verify against the live file.
- **Salvageable minority**: even a mostly-rejected proposal may contain genuinely new
  defensive material (here: 2PI-CTP division-of-labor + AZ Class DIII winding invariant) —
  route it to a robustness/discussion section instead of wholesale rejection.

## Outcome template
Q1 (rigor uplift): per-section verdict table (correctness / increment / net effect on honesty).
Q2 (theorem upgrade): three-way judgment — (A) unconditional theorem / (B) conditional theorem
within the formal axiom system / (C) remains postulate — with P0-resolution scorecard (n/6).
