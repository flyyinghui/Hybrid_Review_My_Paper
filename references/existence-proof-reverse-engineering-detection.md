# Existence-Proof Reverse-Engineering Detection (分支比解耦 / ∃-参数陷阱)

When a reviewer OR the author proposes "introduce a parameter X to close two observables simultaneously", the naive implementation writes the target observation into the parameter's definition — reverse engineering disguised as derivation. The resulting `∃`-theorem is mathematically trivial, yet it often compiles clean (0 sorry) and survives review unless the narrative overclaim is separately flagged.

## Verified case — V18 三大时空相, 修改意见 20260919_1 (2026-09-19)

Reviewer proposal: "introduce a branching ratio f_DM to decouple the 0.46% (DE) vs 8.59% (DM-ratio) discrepancy (18.7×)."

Naive implementation:
```lean
def f_DE : ℝ := 0.682 / ((47:ℝ)/547 * 148.036)   -- 0.682 = the OBSERVED Ω_DE
theorem resolved_transmutation_fraction_existence :
    ∃ model, model.total_baryon_loss = 47/547 ∧ |model.late_time_DE_fraction - 0.682| < 0.005
```

Why it is reverse engineering:
1. **The numerator 0.682 is the observation being explained.** You write the answer into the parameter, then claim the parameter "predicts" the answer. This is 校准伪装成推导 (rule B3) in its purest form.
2. **The ∃-theorem is trivial.** Any target value is reachable by adjusting one free parameter f_DE. Existence ≠ derivation ≠ physical closure.
3. **A clean Lean proof does NOT rescue the physics.** The norm_num/field_simp proof is genuinely 0-sorry (algebraically correct) — but algebraic cleanliness is orthogonal to whether the parameter is physically derived.

## Five-agent consensus verdict (4/5 agents flagged it independently)

- `resolved_transmutation_fraction_existence` is an **existence proof**, not a **dynamics closure**.
- f_DE ≈ 0.0536 is a **reverse-engineered phenomenological free parameter**, not derived from Γ_b/Γ_trans + PBH evaporation particle species.
- Narrative overclaim: "This shifts the mechanism from a numerical coincidence to a **covariant mass-transfer dynamic**" — should read "a free parameter that absorbs the observation".
- f_DE was NOT registered in the paper's own K/C/A/P/O classification table → P1 (self-inconsistency with "net predictive degree = 0" self-assessment).

Score impact: the closure attempt DROPPED the score (6.5 → 6.20, phase3 agent gave 5.0) versus the prior honest-downgrade round.

## Detection checklist (add to rule B3 / B4)

- Does the parameter's definition contain the observation value in its numerator/input? → reverse engineering
- Is the theorem an `∃` (existence) statement rather than a derivation? → trivial; existence ≠ closure
- Is the parameter registered in the K/C/A/P/O (honest-axiom) table? → if missing, P1
- Does the narrative use "dynamic / mechanism / covariant" for what is actually "a fitted parameter"? → status escalation (B4)

## Honest-downgrade paradox — third confirmed instance

Round 4 scored **6.5 by honest downgrade** ("INDEPENDENT single-redshift benchmark, must NOT be conflated"). Round 5 dropped to **6.20 by attempting closure** via branching ratio (overclaim). Pattern: *honest labeling beats overclaimed closure — every time.* (Prior instances in `references/honesty-downgrade-paradox.md`.)

## Execution detail — smoke-test assertion

In the 5-agent serial review script, `assert 'OK' in smoke` FAILS because deepseek-flash does not echo "OK" literally — it returns a polite greeting ("好的，请问有什么我可以帮您的？"). Assert content **non-empty** (`assert smoke`), never literal echo. The smoke test's purpose is only to confirm the model name is valid + `thinking=disabled` returns non-empty `content`.
