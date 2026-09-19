# Reviewer Arithmetic False-Positive — Verify Before Relaying (2026-09-04)

## When to use

When multiple review agents (especially a unanimous 5-agent panel) flag a
"numerical contradiction" / "arithmetic error" in a sentence — most often in
the **abstract** or a grammatically **garbled/ambiguous** sentence.

## The meta-lesson

**Independently recompute the flagged arithmetic BEFORE relaying it as a P0.**
Two failure modes discovered in the V17 final review (both were agent
misdiagnoses, not paper defects):

### Case 1 — Ambiguous sentence splices two chains (the "0.46%" case)

The abstract read (garbled):

> "5.00 evolves to 5.47: 0.46% of baryonic matter collapses into black holes..."

All 5 agents read this as "0.46% transmutation drives 5.00 → 5.47" and flagged
it as a math error: `5.47/5.00 = +9.4% ≠ 0.46%`.

Independent recomputation showed **two separate chains**:
- `5.00 → 5.47`: DM/baryon ratio evolution via black-hole transmutation (a
  *different* mechanism).
- `0.46% → Ω_DE`: `0.0046 × (1+z_eff)³ = 0.0046 × 148 ≈ 0.68 ≈ Ω_DE` — this
  chain is **arithmetically self-consistent**.

The real defect was **WRITING CLARITY** (an ambiguous colon splicing two
unrelated chains), not arithmetic. Correct severity: **P1 (writing), not P0
(math error)**. The fix was to split the sentence and add "(Note: this 0.46% →
Ω_DE chain is distinct from the 5.00 → 5.47 evolution…)".

This case *corrects* a misdiagnosis recorded earlier in
`math-calculation-accuracy-review.md` §7 (which listed "0.46% transmutation →
5.02" as a circular-calibration error). The "0.46%" is NOT the 5.00→5.47
transmutation rate; it is the Ω_DE generation chain, which is self-consistent.

### Case 2 — Agent's own convention error (the "b₀" case)

The numerical reviewer flagged `b₀ = 12` as wrong, recomputing
`(11/3)·6 − (4/3)·15 = 82/3 ≈ 27.3`. But the correct one-loop β-function
coefficient uses the fundamental index `T_F = 1/2`:

```
b₀ = (11/3)·C_A − (4/3)·N_f·T_F = 22 − 10 = 12   ✓
```

The reviewer **dropped the `T_F = 1/2` factor**. The paper's `b₀ = 12` was
correct; the reviewer's own recalculation was wrong.

## Rule

1. Never relay an agent's "arithmetic error" as P0 without independently
   recomputing it yourself (Python precise calc).
2. If the flagged sentence is grammatically garbled (ambiguous colon / comma
   splice / "A: B and C"), check whether the numbers belong to **separate
   chains** before declaring a math error.
3. Verify agent findings against **your own** calculation — agents make
   convention errors (T_F index, normalization factors, dim vs rank, Dirac vs
   Weyl) exactly like papers do. A unanimous panel can still be unanimously
   wrong about a shared misreading.
4. Classify the finding honestly: an ambiguous sentence that *causes* a
   collective misread is a writing defect (P1), not an arithmetic defect (P0) —
   even though the *symptom* looks arithmetic.

## Distinction from `math-calculation-accuracy-review.md`

That reference's core insight ("definitional arithmetic is almost always right;
physical-prediction numbers are where errors cluster") remains valid. This
reference adds the **reciprocal guard**: when the flagged number is inside a
garbled sentence, first check whether the "contradiction" is real or is a
splice of two chains, and re-derive any convention-dependent value (T_F, C₂,
normalization) yourself before trusting the agent's recomputation.
