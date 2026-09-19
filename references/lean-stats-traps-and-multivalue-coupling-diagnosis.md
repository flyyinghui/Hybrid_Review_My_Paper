# Lean Stats Traps + Multi-Value Coupling-Constant Diagnosis (2026-08-29)

Four-paper SL(6,C) joint review (CGICE V9.1 / Spacetime V17 / Neutrino V63 / Triple-GW V16)
surfaced two NEW proof-audit bugs and one reusable diagnosis pattern. All extend Pitfall 4
(Lean Stats Regex Trap) and the cross-paper consistency protocol.

## 1. Nested block-comment false-positive (`sorry` miscount)

**Symptom**: `proof_consistency_audit.py` reported Neutrino V63 `sorry=4` → GATE BLOCK, but
`grep -n 'sorry'` showed all 4 were inside `/- ... -/` block comments ("0 active sorry" claims,
CHANGELOG table rows). True count = 0 active sorry.

**Root cause**: the block-comment stripper `re.sub(r'/-.*?-/', '', lean, flags=re.S)` uses a
**non-greedy** `.*?`. When a block comment *nests* another `/-` (common in these long proofs:
a section header `/- ... -/` containing a quoted `/- ... -/` example), the non-greedy match
terminates at the FIRST `-/`, leaving the inner `/-`/`-/` pair un-paired. Subsequent block
comment interior lines leak into the "active" list and their `sorry` words get counted.

**Fix**: confirm ANY non-zero sorry/admit/trivial count with `grep -n` line context BEFORE
reporting a P0 (already in Pitfall 4). For a robust stripper, use a bracket-counting scanner
or `re.sub(r'/-.*?-/', ...)` is NOT safe for nested comments — replace with an explicit
state-machine that tracks `/-`/`-/` depth. Detection signal: a "sorry" line whose surrounding
lines are English prose ("ZERO-sorry status", "✓ ZERO SORRY:") rather than Lean code.

## 2. active-sorry counted but NOT gated (audit-gate failure)

**Symptom**: `proof_consistency_audit.py` computed `n_sorry` and wrote it into
`report["stats"]["active_sorry"]`, but NEVER appended it to `blocks`/`warns`. A proof with
active `sorry` therefore returned `gate=PASS` (no other defect fired) — the audit gate was
silent on the single most important defect.

**Fix (landed 2026-08-29, GitHub review)**: add a "检测 0" highest-priority check right after
blocks/warns init:
```python
if n_sorry > 0:
    msg = f"{n_sorry} 处 active 'sorry'（未完成证明）。gate 必须为 BLOCK。"
    blocks.append(msg)
    findings.append({"type": "active_sorry", "severity": "BLOCK", "count": n_sorry, "msg": msg})
```
Plus a gate/stats consistency assert in the orchestrator:
```python
assert (report["stats"]["active_sorry"] == 0) or report["gate"] == "BLOCK", \
    "gate/stats inconsistency: active_sorry>0 but gate!=BLOCK"
```

**General lesson**: any metric that is *counted into stats* but *never feeds the gate decision*
is a silent audit-gate hole. When auditing an audit script, cross-check every `stats[...]`
key against a corresponding `blocks.append`/`warns.append` path.

## 3. Multi-value coupling-constant trace (g_TC four-value case)

**The paper series claimed 4 different g_TC values**. Independent recomputation traced each
to a DIFFERENT λ_KLS choice, instantly exposing the contradiction's root:

| g_TC value | g_TC² | source | λ_KLS implied |
|---|---|---|---|
| 2.60 | 6.76 ≈ 24π²/35 | D1 duality g_TC²=8π²/λ_KLS | λ_KLS=35/3 |
| 1.50 | 2.26 ≈ 8π²/35 | same D1 duality | λ_KLS=35 |
| 0.5 | 0.25 | none (unexplained phenomenological) | — |
| 2.83 | 8.0 | mass-ratio / WKB sections | — |

**Reusable diagnosis**: when a shared coupling/spectral constant appears with multiple values
across a paper series, DON'T just flag "inconsistent". For each value, invert the defining
relation (e.g. `g_TC² = 8π²/λ_KLS` → solve for λ_KLS) and see which parameter choice each
value corresponds to. The multi-value mystery almost always reduces to a **multi-choice
parameter** (here λ_KLS = 35/3 vs 35) — and then you can pinpoint that the real contradiction
is the parameter, not the coupling.

## 4. Non-compact symmetric space spectral-gap error (λ_KLS = 35/3)

`λ_KLS = 35/3` (V17) is a **mathematical error**: SL(6,C)/SU(3,3) is a NON-COMPACT real form
(SU(3,3) Killing form is indefinite), so its Witten Laplacian has CONTINUOUS spectrum with no
positive gap. KLS/log-Sobolev constants require a COMPACT (or strongly convex) manifold. V17
transplanted the compact-dual SU(6)/SO(6) Harish-Chandra result (λ = |ρ|² = 35) to the
non-compact space without proof. Correct options: use the compact dual λ_KLS = 35, or admit
no gap exists. Also note |ρ|² = 35 only under the root-length²=2 normalization; standard
Killing normalization gives |ρ|² = 70/4 = 17.5 — normalization MUST be stated.

## Four-paper scores (for continuity)

| paper | derivation-completeness | calc-accuracy | contribution-30yr | editor |
|---|---|---|---|---|
| CGICE V9.1 | 4.2 | 6.5 | 3.5 | 5.5 |
| Spacetime V17 | 5.8 | 5.5 | 4.0 | 6.0 |
| Neutrino V63 | 6.5 | 7.5 | 5.5 | 6.5 |
| Triple-GW V16 | — | 6.0 | 4.5 | 5.0 |

V63's neutrino masses m₁/m₂/m₃ = 0.0030/0.0091/0.0505 eV were independently recomputed and
match NuFIT 5.3 (m₂=0.00912 ✓, m₃=0.05016 ✓). V16's N_e=(35/6)·ln(1+10⁶)=80.59≈80.6 is
arithmetically correct but is a [CALIBRATION], not a derivation.
