# Manuscript Version-Comparison for Physical Self-Consistency

## When to use
User asks to compare two versions/drafts of the *same* framework paper (or two related
manuscripts) and judge **which gives a better physical interpretation / self-consistency** —
e.g. "对比 SL6C_Unified...V2.md 和原版，宇宙演化自洽性哪个更有优势". This is a distinct task from
hybrid review (single-version critique) and from paper↔Lean cross-ref revision.

## Method: diff the *strategy*, not just the prose

First locate both files, dump section headings (`grep -nE '^#{1,3} '`), then read the
Abstract, the newly-added sections, and both Discussion/Conclusions. The decisive signal is
almost always a *structural* change (new sections, new Propositions) rather than wording.

### Five criteria — apply in order

1. **Avoidance vs construction (回避 vs 构造).**
   Does the newer version *fill* the identified gap with a conditional theorem, or merely
   *rename/avoid* it? "A separate requirement" / "needs further geometric structure" = avoidance
   (gap remains). "Proposition G4: under conditions (i)(ii)(iii), the quotient is Lorentzian" =
   construction. Construction wins, even when its hypotheses are strong.

2. **Circular-reasoning elimination (循环论证消除).**
   Cosmological frameworks are prone to using a 4D EFT result (condensate, light cone) to
   *justify the 4D Lorentzian spacetime it lives in*. The stronger version states this as an
   explicit red line, e.g. "no subsequent condensate or light-cone calculation is used to infer
   its own Lorentzian premises" and "instability thresholds do not themselves establish a change
   of spacetime signature". Grep for this; its presence is a major plus.

3. **Input/derivation boundary (输入/推导边界).**
   Does the version carry an explicit two-column table separating "Derived in the specified
   model" from "Additional input / unresolved construction"? This is the honest-engineering
   signature. Its absence means inputs are silently smuggled as results.

4. **Honest-but-positive framing (诚实但不自贬).**
   The preferred register is "constructive conditional bridges and explicit obstructions" —
   NOT "we do not predict X" (self-deprecating) and NOT "we derive X" (overclaim). Falsifiable
   parameter relations stated positively.

5. **Exposed difficulty = falsifiability (暴露难点=可证伪性).**
   A version that names the remaining *input* (e.g. the "signature selector" / rank-two
   localization matrix) is *stronger* than one that hides it behind "later work will construct
   it". Any single input being refuted must point to a precise place to patch, not collapse the
   whole framework.

## Case study: SL6C Unified Framework V1 → V2 (2026-10)

V1 treated the 6D→4D reduction as "separate requirements" (avoidance) — a logical gap. V2 added
§2.4 (logical order of the emergence problem) + §4.5–4.10 and Propositions G1–G5:

- **G1** exact Gaussian stochastic-localization Riccati solution `C_τ=(C₀⁻¹+τB)⁻¹` (rank is input)
- **G2** positive precision cannot generate time: `C>0 ⇒ C⁻¹>0`
- **G3** unimodular endpoint obstruction: `det(I₆)=+1 ≠ det(η_{1,5})=−1`, so no SL(6,ℂ)
  determinant-preserving complex congruence reaches the single-negative real endpoint
- **G4** conditional quotient theorem: signature (1,5) + positive projectable internal 2-bundle ⇒ (1,3)
- **G5** torus KK spectrum + radius matching + finite low-energy window, composing G1+G4

Verdict: V2 wins decisively on self-consistency because it converts the gap into checkable
conditional bridges, blocks circularity, and exposes the "signature selector" as an explicit
input. The cost — more exposed assumptions — is itself a falsifiability gain, not a weakness.

## Pitfalls
- Don't score a version higher just because it is longer or more "rigorous-looking"; verify the
  new content is *construction* (criterion 1) not elaboration of the same gap.
- A version that only *adds* "we do not claim X" sentences without adding theorems is
  self-deprecation without substance — flag it (criterion 4), don't reward it.
- When the two manuscripts share large verbatim blocks (both Discussions here were near-identical
  after the first paragraph), focus the comparison on the *delta* sections only.
