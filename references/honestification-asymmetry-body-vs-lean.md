# Honestification Asymmetry: Body Text vs Lean Code Divergence

## The meta-pattern (V18 final review 2026-09-20)

A paper can score HIGH on honesty (7.5/10) in its prose layer while the Lean
formalization still carries the OLD overclaims. The honestification landed in
body text but was NOT propagated to the `.lean` code. This is a distinct failure
mode from plain overclaiming — the prose is already honest, so a naive
honesty audit passes, but the code layer is silently stale.

Symptom signature: **honesty score ≈ 2× the technical/formalization score**
(real case: logic 7.5 vs technical 4.5 / lean_specialist 3.5). When you see this
gap, the next action is NOT more prose honesty — it is propagating the honest
labels INTO the Lean code (delete/replace the stale axioms) and fixing the
arithmetic errors the code still encodes.

## Detection: for every "corrected" value/claim in the body, grep the Lean for the OLD value

- Body §IV.C writes correct `C_t = D/ℓ + (C₀−D/ℓ)e^{−2ℓt}` (exponent −2ℓt)
- Lean `def ouCov ... := (C0 - D/ell) * Real.exp (-ell * t) + D/ell` (exponent −ℓt) ← STALE
- Fix: after every body correction, grep the .lean for the OLD numeric/operator
  form (`exp (-ell`, `= 5.47`, `v/u`) — not just the new form. Body/Lean
  bidirectional divergence is a P0 even when the body text is correct.

## Concrete math verification facts (reusable across the SL(6,C) series)

1. **Conservative Metzler generator spectral bound = 0.** A column-sum-zero
   Metzler matrix satisfies M^T·1 = 0, so 0 is an eigenvalue; by Perron–Frobenius
   the dominant eigenvalue is 0. Any axiom asserting `DominantEigenvalue M = 5.47`
   is MATHEMATICALLY FALSE. 5.47 (Ω_c/Ω_b) is an observation input → must be
   `def targetRatio : ℚ := 547/100`, NOT a spectral-theorem conclusion.

2. **Trace pairing B(X,Y)=Re tr(XY) is INDEFINITE on sl(6,C).** Counterexamples:
   H=diag(1,-1,0,0,0,0) → B(H,H)=2>0; K=iH → B(K,K)=−2<0; E₁₂ → B(E₁₂,E₁₂)=0.
   For a positive-definite invariant inner product, restrict to the compact real
   form su(6) with ⟨X,Y⟩=−Re tr(XY) (= tr(X*X) for skew-Hermitian).

3. **Steady-state ratio order.** For the 2-state conservative matrix
   M(u,v)=[[−u,v],[u,−v]], the steady vector is (v,u) in (B,D) ordering →
   D/B = u/v, NOT v/u. Comment-order errors are a recurring P0 — verify the
   component ordering before trusting any ratio written in a comment.

## Lean declaration-count refinement

- `noncomputable section` is a SECTION marker, not a def. Count
  `^noncomputable\s+def` (exclude `\s+section`), else you inflate the def count
  (real case: 36 defs inflated to 51 by 15 sections).
- `@[honest_axiom]` decorators are usually on a SEPARATE line from the `axiom`
  declaration. Count BOTH same-line (`@\[\w+\]\s*axiom`) AND previous-line
  (`prev.strip().startswith("@[honest_axiom]")`) forms, else you undercount
  honest_axiom (real case: 4 same-line vs 100 total).

## Review execution note

5-agent serial `deepseek-flash` (thinking disabled, `extra_body={"thinking":{"type":"disabled"}}`,
max_tokens=8192, temp=0.0, timeout=600) via `terminal(background=true, notify_on_complete=true)`,
each agent's output written to `/tmp/v18_review_<name>.part` immediately. Do NOT use
delegate_task (children inherit the parent model). Inject the full P0/P1 list as adversarial
context and require `fixed/remain/partial` per defect — this prevents re-litigating and
produces calibrated relative verdicts.
