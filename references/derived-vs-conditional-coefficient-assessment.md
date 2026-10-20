# Derived vs conditional coefficient — reviewer assessment heuristic

When a paper claims a "derived" quantity (e.g., "derived relaxation rate 6mκ"), the reviewer must
decompose it into two independent questions:

  (a) the numerical PREFACTOR — is it genuinely computed from the framework's own data?
  (b) the DIMENSIONFUL inputs — are they still free / specified / matched parameters?

The single test that separates honest from overclaim:
  "Did the author compute a coefficient they did not put in, or is it a combination of
   still-specified inputs?"

## Canonical case (round 9, LightSpeed_Phase_Boundary)

`derivedRate m k = 6*m*k`:
- factor **6** IS derived — `root_frame_identity : Σ_{i<j}(x_i−x_j)² = 6·norm6 x − (trace6 x)²`
  on the traceless slice gives Hessian 6κI. The 6 is a real combinatorial consequence of the A₅
  root system, not inserted.
- **m** (mobility) and **k** (stiffness) are STILL declared inputs [M].
- ⇒ the rate is "6 × (two free inputs)" — a derived PREFACTOR, not a parameter-free prediction.

## Assessment ladder for "does this close the no-dynamics-work-package P0?"

| stage | content | verdict on P0-A |
|---|---|---|
| round N | no dynamics at all (hand-picked rate ratio) | NOT closed |
| round N+1 | conditional dynamics + one derived prefactor | PARTIALLY closed |
| (unreached) | parameter-free prediction from framework data | CLOSED |

## Sub-checks that flag the residual overclaim

- `matching_35_requires_scale : derivedRate m k = 35 ↔ m*k = 35/6` — this is the HONEST move: it
  explicitly demotes "35" from a derived rate to a calibration choice. Credit it, and require the
  same calibration caveat to appear in the abstract, not just buried in §V.P.5.
- "root-derived" in the TITLE is an overclaim when only the prefactor 6 is root-derived and m,k
  are inputs. Flag title/abstract/body mismatch: body says "inputs [M]", title says "derived".
- A "spectral gap lower bound" that is proved term-by-term on a finite Hermite coefficient core
  (with an attaining witness, `first_mode_saturates` / `exact_core_gap`) is SUBSTANTIVE, not a
  tautology — but it is a *finite-core coefficient* theorem, not a full-manifold operator theorem.
  The Gaussian realization / Hermite completeness / operator closure are analytical steps; the
  abstract must say "finite-core" and not "established analytically" for the parts that are not.

## Verdict framing

- "+1 conditional on scale fixing" — honest.
- "derived rate" (unqualified) — overclaim.
- The paper has gone from "no dynamics" to "a conditional dynamics package with one computed
  coefficient"; that is a REAL improvement but does NOT reach a physics venue's bar (PRD/CQG/SciPost
  want a parameter-free prediction). FoP/JMP tolerate it if framed as an effective-model construction.
