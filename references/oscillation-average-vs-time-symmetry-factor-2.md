# Oscillation-average ½ vs |t−s|-symmetry factor 2 vs modulus |∫|² — three distinct factor-2 mechanisms (reviewer false-positive category #4)

**Where this bit us (2026-10-18, 三峰引力波 paper_triple_gw_v20.md R9 第三轮终审):** `logic` (P0-3) and `technical` (P2-6) both independently flagged a "possible factor-2 inconsistency" between §7.4 (7.9) `I_T(K)=2∫₀^T(T-u)e^{-Γu}cos(Ku)du` (contains a factor 2) and §7.8.1 (7.25d) `|A_pq|²` (no factor 2), noting both sections claim "1/12 includes the oscillation average 1/2". Independent re-derivation along the source chain showed **both are correct; there is no inconsistency.**

## The three mechanisms that each legitimately produce or absorb a factor 2 in a GW UETC spectrum

1. **|t−s| symmetry of the double time integral** — `∫₀^T ds ∫₀^T ds' → 2∫₀^T(T−u)du` with `u=|s−s'|`. This is the factor 2 *inside* `I_T`. It is **not** an oscillation average and has nothing to do with the ½.

2. **Oscillation average** — `cos[K(η−s)]cos[K(η−s′)] → ½cos[K(s−s′)]` (dropping the fast `cos[K(2η−s−s′)]` term). This ½ cancels the prefactor `4/(2π²)=2/π²` carried by (7.3), yielding the clean `K³/(π²M⁴)` in (7.13).

3. **Modulus structure** — `|A_pq|² = |∫ u_p u_q e^{iKt} dt|²` already encodes the double time integral via the modulus; no extra symmetry factor 2 is needed.

## The verification that closes it

Both sections end at the **same Ω prefactor `K³/(12π²M⁴H²)`**:

- §7.4: `P_ḣ = K³/(π²M⁴)·C_sp·I_T`, then `Ω = P_ḣ/(12H²)`. The "12" is the (7.4) energy-density definition; the oscillation ½ was already absorbed by the prefactor `2 × ½`.
- §7.8.1: `Ω = K³/(6π²M⁴H²)·½·∫…` where `1/6` is the (7.3)+(7.4) prefactor combination `4/(2π²·12)` and `1/2` is the oscillation average. So `1/12 = (1/6)·(1/2)`.

**Same final number, different provenance of the "12".** That is exactly why the reviewer's "factor 2 doubled/missing" flag is a false positive.

## Rule for future review sessions

When a reviewer flags "factor 2 / oscillation-average ½ missing or doubled", do NOT accept it. Independently re-derive along the source-term chain — (7.3)→(7.4)→(7.9)/(7.13) for the maintained-kernel route, or (7.24)→(7.25)→(7.25d) for the mode-evolved route — and classify every factor 2 into one of the three mechanisms above. "`I_T` has factor 2 but `|A_pq|²` doesn't" is **not** an inconsistency: they are different time-response structures (maintained OU kernel `C_Π∝e^{-Γ|t-s|}` vs mode-evolved covariance `C_φ=P_i u_p(t)u_p(s)`).

## Related false-positive categories (see reviewer-factor-dimension-recalc-false-positives.md)

1. conformal vs physical time (source term differs by a²)
2. Itô vs Stratonovich mixing (phantom −12DC term)
3. dropped oscillation-average ½
4. **(this)** |t−s| symmetry factor 2 vs modulus |∫|² structure
