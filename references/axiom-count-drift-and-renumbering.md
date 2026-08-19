# Axiom-Count Drift & Continuous Renumbering (Paper ↔ Lean)

Verified case: CGICE V9.1 final review (2026-08-19). The paper claimed FOUR different
axiom counts — abstract "twenty-five", introduction "fourteen", §8.1 "fourteen",
conclusion "61" — while the Lean file actually had 69. This is a P0 that invalidates
the entire formal-verification narrative, and it is invisible unless you diff the paper's
count claims against the Lean file's ACTIVE axiom count.

## 1. Detection (automated, no LLM)

```python
import re

# (a) every count claim in the paper
for m in re.finditer(r'(twenty-five|fourteen|\b61\b|\b69\b|\d+ axiom|four theorems)[^.]*\.', md_txt):
    line = md_txt[:m.start()].count('\n') + 1
    print(line, m.group(0)[:90])

# (b) ACTIVE Lean counts — MUST exclude comment lines
active = [l for l in lean_txt.split('\n')
          if not l.strip().startswith('--') and not l.strip().startswith('/-')]
n_axiom   = sum(1 for l in active if re.match(r'^\s*axiom\b', l))
n_theorem = sum(1 for l in active if re.match(r'^\s*theorem\b', l))
n_lemma   = sum(1 for l in active if re.match(r'^\s*lemma\b', l))
n_sorry   = sum(1 for l in active if re.search(r'^\s*sorry\b', l))
```

Raw `grep -c axiom` over-counts badly (comments say "0 sorry", headers say "61 axiom").
Always filter `--` and `/-` lines first.

## 2. Continuous renumbering (old → new)

When the paper's numbering has gaps (A1-A25 missing A6/A17, A16 misplaced in §3.1),
build an old→new map and renumber BOTH files so the ranges are continuous and
paper↔Lean correspond (A1-A22 ↔ a1-a22).

```python
mapping = {  # old -> new  (CGICE V9.1 case)
    'A25':'A22','A24':'A21','A23':'A20','A22':'A19','A21':'A18','A20':'A17',
    'A19':'A16','A18':'A15','A16':'A7','A15':'A14','A14':'A13','A13':'A12',
    'A12':'A11','A11':'A10','A7':'A6',
}
# FUNCTIONAL re.sub — single pass, avoids ordering collision (A16→A7 vs A7→A6)
new_txt = re.sub(r'\bA(\d{1,2})\b', lambda m: mapping.get('A'+m.group(1), 'A'+m.group(1)), txt)
```

For Lean, axiom names are `a16_master_equation` — the number is followed by `_`, which
is a word char, so `\ba16\b` does NOT match. Use a lookahead instead:

```python
new_txt = re.sub(r'\ba(\d{1,2})(?=[_\s:(])',
                 lambda m: 'a' + mapping.get(m.group(1), m.group(1)), txt)
```

## 3. The four P0 patterns found alongside the drift

1. **Circular reverse-engineering.** η back-computed from g* via η = b₀(g*)²/(4π²),
   then claimed to "determine" g*. Fix: give η an independent first-principles source —
   e.g. η_k = C₂(adj)·h^∨/dim(M) = 12×6/35 = 72/35, then g* = √(4π²|η_k|/b₀) = √(24π²/35) ≈ 2.6015.
2. **Dimensional category error.** |ρ|² = 35 substituted into the position of |ρ| = √35,
   giving exp(−2·35·τ) ≈ 10⁻¹²² when the honest exp(−2·√35·τ) ≈ 2.5×10⁻²¹ — off 101 orders.
   The fix (Fokker-Planck covariance dissipation) legally uses 35 = λ_∥ = |ρ|² as a SPECTRAL
   GAP, not as the norm |ρ|. Rule: verify the dimension of every exponent argument.
3. **Zero-content axiom.** `axiom X : ∀ x, 0 ≤ x → True` — consequent is always true.
   Replace with a real assertion (e.g. `0 ≤ |∇V|² − hΔV`).
4. **Performative theorem name.** `theorem no_free_parameter` that only proves a constant ≠ 0.
   Rename to what it actually proves (`lambda_CC_relaxation_nonzero` via `Real.exp_ne_zero`).

## 4. Renumbering side-effects to expect

- Dropping cyclic/error axioms changes the count (CGICE: 69 → 64 after removing
  `jacobian_value`, `deltaR_value`, `eta_anomalous_value`, `g_star_value`,
  `witten_spectrum_nonneg`, and downgrading `a10_alpha_relation` axiom→def).
- The paper's count claim must be re-synced in the SAME pass (69→64, "twenty-one"→"twenty"
  core axioms) or the drift returns immediately.
- Downgrading `axiom X : P` to `def X : Prop := P` forces every lemma that used X to take
  an explicit `(hX : X t)` premise — recompile and fix each call site.

## 5. Lean gotchas hit during this work

- `10^(-122)` fails to synthesize (Nat ^ Int). Use `(10 : ℝ) ^ (-(122 : ℤ))`.
- `M_Pl`, `lambda_par`, `lambda_perp` were already declared earlier in the file —
  grep before adding a new def to avoid "has already been declared".
- `Real.sq_sqrt` + `positivity` proves `(Real.sqrt x)^2 = x`; `Real.exp_ne_zero` proves
  `exp x ≠ 0` (the honest non-trivial replacement for a norm_num constant-≠-0 theorem).
