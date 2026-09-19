# Lean Axiom-Consistency Audit — False-Proof Compilation & Performative Honesty

Verified 2026-08-16 in the CGICE V9.1 review (and reused across V16/V17). When a paper
claims "0 sorry / 0 active sorry", that only proves the *file compiles* — it says nothing
about whether the **axioms are mutually consistent**. An inconsistent axiom set is WORSE
than `sorry`: by explosion (ex falso), every theorem *and its negation* becomes provable,
so the formal verification is vacuous. A "0 sorry" file can still prove `False`.

## 1. The core technique — compile `False` to confirm inconsistency

If you suspect axioms A and B jointly imply `X = Y` while axiom C asserts `X ≠ Y`,
DON'T just argue it in prose. Write a minimal standalone Lean file that abstracts the
axioms to their exact logical structure and compile two `False` proofs. If they both
typecheck, the inconsistency is proven, not merely suspected.

Minimal reproducible pattern (works in `lean4` core, no Mathlib needed):

```lean
-- /tmp/false_proof.lean
opaque V_eff : ℝ → ℝ
opaque I_cycle : ℝ → ℝ
opaque Λ_CC : ℝ → ℝ
opaque I_eq : ℝ → ℝ → ℝ
opaque λ₁ : ℝ

-- A6: I_cycle = V_eff · (2π/λ₁)
axiom a6 (t : ℝ) : I_cycle t = V_eff t * (2 * Real.pi / λ₁)
-- A10: V_eff · (2π/(35/3)) = (35/3)(V_eff/Λ_CC) = I_eq
axiom a10 (t : ℝ) : V_eff t * (2 * Real.pi / (35/3)) = I_eq (V_eff t) (Λ_CC t)
-- A17: I_cycle ≠ I_eq  ("prevent trivial solution")
axiom a17 (t : ℝ) : I_cycle t ≠ I_eq (V_eff t) (Λ_CC t)
-- A9: initial condition I_cycle 0 = I_eq
axiom a9 : I_cycle 0 = I_eq (V_eff 0) (Λ_CC 0)
-- plus the fact that λ₁ is defined as 35/3 (making A6 RHS = A10 LHS)

theorem false1 : False := by
  -- A6 + A10 (with λ₁ = 35/3) ⟹ I_cycle = I_eq; contradicts A17
  ...

theorem false2 : False := by
  -- A9 (t=0) directly contradicts A17 at t=0 — no A6/A10 needed
  ...
```

Key insight from CGICE V9.1: the SIMPLEST contradiction is often the most damning —
`a9 : I_cycle 0 = I_eq` vs `a17 : ∀t, I_cycle t ≠ I_eq` contradicts at t=0 **without
needing the whole derivation chain**. Always check the initial-condition axiom against
the "non-triviality" axiom first; it's a one-line contradiction.

Also check: does the value used in the axiom actually equal the `def`? CGICE had
`def λ₁ := 35/3`, so `V_eff·(2π/λ₁)` and `V_eff·(2π/(35/3))` are definitionally the
same term — that identity is what closed the contradictory loop. Verify reciprocals
with Python: `2π/λ₁ = 6π/35 ≈ 0.5386`, `λ₁/(2π) = 35/(6π) ≈ 1.8568`, product = 1.

## 2. Performative honesty — commented-out `@[honest_axiom]` tags

A paper/Lean file that "declares axioms as `@[honest_axiom]` or `@[phenomenological]`"
may be faking it. Detection:

```bash
grep -c '^@\[honest_axiom\]'  file.lean    # real attribute lines
grep -c '^-- @\[honest_axiom\]' file.lean   # commented-out (decorative) lines
```

In CGICE V9.1: **26 `@[honest_axiom]` + 8 `@[phenomenological]` were ALL commented-out**
(`-- @[...]`), i.e. zero real Lean attributes, yet the abstract claimed "declared as
@[honest_axiom]". Comment text is invisible to the compiler and un-auditable — it is
documentation-level honesty masquerading as a machine-checkable mechanism.

Rule: "document-level honesty ≠ mechanism-level honesty". A paper is only honestly
disclosing its axioms if either (a) the tags are real Lean attributes that `#print axioms`
can enumerate, or (b) the paper explicitly says "documented in source comments" rather
than "declared as attribute".

## 3. Contradiction migration — a "fix" that introduces a new contradiction

When a review flags "axioms A+B force X=Y (trivial solution)", the naive author fix is
to *add* an axiom asserting X≠Y to "prevent the trivial solution". This does NOT resolve
the contradiction — it MIGRATES it: the axiom set is now inconsistent (proves False)
instead of trivial. The correct fix is to change A or B's coefficients so the loop
doesn't close, making X≠Y a *consequence of the master equation's solution* rather than
a contradictory decree.

Signature to flag: an axiom named `*_nontrivial` / `*_nondegenerate` / `*_prevents_trivial`
whose body is a bare `≠` statement, combined with a comment "to avoid the trivial
solution". That is almost always a contradiction-migration red flag.

## 4. Axiom-count contradiction (recurring P0)

Papers routinely claim one axiom count while the Lean file has another. CGICE V9.1 had
THREE mutually exclusive counts: abstract "25 axioms", §1 "fourteen axioms", Lean actual
**39**. Always grep the ground truth:

```bash
grep -c '^\s*axiom\s' file.lean          # active axiom declarations
grep -c '^\s*theorem\s' file.lean        # active theorems
wc -l file.lean                          # actual line count
```

And check the header comment's self-reported count against these — the header frequently
carries a stale count from 3 versions ago (e.g. "~1101 lines · 14 axioms" on a 1979-line,
66-axiom file). The "transparent disclosure" paper whose own axiom count is wrong in
three places has a credibility problem independent of the math.

## 5. Ghost theorem claims — "fully verified" but absent from Lean

A paper section may claim `theorem t4_topological_charge_conservation` is "fully
verified in Lean" while the .lean file has only a comment `-- UNDER DEVELOPMENT`.
Grepping the claimed theorem name and finding nothing (or only a comment) is a
fabrication-level finding. This is distinct from a sorry — it's a claim about the
formalization that is simply false. Check every theorem name the paper names against
the file before believing any "verified" claim.
