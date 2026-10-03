# Reviewer Unit-Conversion & Prefactor False Positives (V19 final review, 2026-09-21)

Two concrete instances where reviewers reported "numerical contradictions" that were
**false positives** — the paper was CORRECT and the reviewer(s) dropped a factor.
Both were caught by independent re-derivation BEFORE relaying as P0.

## Instance 1: β-function fixed point — reviewer dropped the 1/2 in β(g)=ηg/2

- Paper: β(g) = ηg/2 + bg³/(8π²), η=−36/35, b=12 → g*² = −η·4π²/b = **12π²/35**.
- `technical-reviewer` claimed g*² = **24π²/35** (used −η·8π²/b, i.e. dropped the 1/2 in ηg/2).
- `consistency-checker` independently derived **12π²/35** — the two agents contradicted each other.
- Lesson: when one reviewer's arithmetic contradicts another's on the SAME quantity, re-derive
  the fixed point yourself. The disagreement is itself the signal that one is wrong.

## Instance 2: §9.3 f₀ — two reviewers dropped the ℏ (natural-unit → Hz) conversion

- Paper: f₀ = (T₀/T*)(g_s0/g_s*)^(1/3)(1/2π)√(π²g*/90)·T*²/M̄_P, then explicitly
  "Converting the natural-unit frequency with ℏ=6.582×10⁻²⁵ GeV·s … gives ≈2.65×10⁻⁸ (T*/GeV) Hz".
- TWO reviewers (`technical` F-07 and `consistency` F-006) recomputed the natural-unit value
  1.744×10⁻³²·T* [GeV] and reported a "10²⁴ discrepancy" — they **dropped the explicit ℏ conversion**.
- Check: 1.744×10⁻³² × (1/ℏ = 1.519×10²⁴ Hz/GeV) = **2.65×10⁻⁸ Hz** ✓ paper correct.

### Detection signal (high-value)
A reported **"10^N discrepancy"** (especially ~10²⁴) is almost always a **missing unit
conversion**, not a real arithmetic error. Before relaying any such finding, grep the paper
text for the conversion sentence and apply the factor yourself. Common dropped conversions:
ℏ (GeV→Hz, 1/ℏ ≈ 1.519×10²⁴), c, k_B, G, and prefactors 1/2, T_F, normalization.

## Reusable technique: Lean theorem-name diff for cross-paper derivation assessment

To quantify "does paper B derive from paper A" **mechanically** (instead of narrative):

```python
import re
def names(f):
    return set(re.findall(r'^(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_\.\']*)',
                          open(f, encoding='utf-8').read(), re.M))
A = names("paperA.lean"); B = names("paperB.lean")
transcribed     = A & B   # same-name theorems/lemmas = transcribed baseline
new             = B - A   # paper B's additions
not_transcribed = A - B   # paper A results B did NOT carry over
```

- V19 case: CGICE v10 (161 thm/lemma) vs V19 (260) → **71 transcribed / 189 new / 90 not-transcribed**.
- This yields an OBJECTIVE `follows / partial / language_only` baseline before LLM adjudication:
  same-name = follows (transcription), new = language_only (conditional model, not derived),
  not-transcribed = a transparency gap (paper B should disclose it didn't carry them over).
- **Caveat**: Unicode identifiers get truncated by `[A-Za-z0-9_]` (ξ → empty, so
  `sum_ξ_indicator_s` → `sum_`); already documented in
  `lean-unicode-identifier-reviewer-false-positive.md`.

## Rule reinforcement

- "10^N discrepancy" → look for dropped unit conversions (ℏ/c/k_B) or prefactors (1/2, T_F) FIRST.
- Cross-paper derivation = transcription (set intersection of theorem names) vs new
  (set difference), not the paper's narrative "follows CGICE" claim.
- Two agents disagreeing on the same arithmetic → re-derive yourself; one is wrong.
