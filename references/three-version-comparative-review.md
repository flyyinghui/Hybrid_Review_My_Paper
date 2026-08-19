# Three-Version Comparative Hybrid Review

## Purpose

Compare three versions (V11, V13, V15) of the same paper across three independent dimensions to identify the best version and generate prioritized improvement recommendations.

## When to Use

Triggered by: "评估三个版本", "对比 V{N} V{M} V{K}", "multi-version comparative review"

## Three-Dimensional Agent Deployment

Deploy 3 specialist agents in parallel via `delegate_task(tasks=[...])` — one per review dimension:

| Agent | Dimension | Sub-criteria | Weight |
|-------|-----------|-------------|--------|
| **logic-reviewer** | 论述逻辑自洽性 | Internal argument coherence, absence of self-contradiction, cross-section consistency, honesty of claims vs derivation strength | scored separately |
| **technical-reviewer** | 数学推导完备性 | Derivative rigor, moduli space handling, key formula derivation honesty, Lean proof alignment | scored separately |
| **testability-reviewer** | 物理参数可检验性 | Falsifiability, observational data connection, parameter count honesty, prediction/post-diction distinction | scored separately |

Each agent reads ALL THREE version texts (extracted to `/tmp/6d_V{N}.txt`) plus the Lean ground truth stats.

## Agent Prompt Template

```
context: "You are reviewing three versions of [PAPER_TITLE]. File paths: /tmp/6d_V11.txt (...), /tmp/6d_V13.txt (...), /tmp/6d_V15.txt (...). Lean ground truth: [STATS]. Review for [DIMENSION] only: [DETAILED_CRITERIA]. Read all three files, compare them, produce structured report in Chinese with scores and rankings. Max 4 sentences per finding."
goal: "Comparative review of three versions across dimension [DIMENSION]. Score each version 1-10 on [SUB_CRITERIA]. Identify the best version for this dimension. Output structured report."
```

## Synthesis and Composite Ranking

After all three agents return, compute weighted composite:

```
Composite = logic × 0.40 + math × 0.35 + testability × 0.25
```

## Key Patterns Discovered (6D Spacetime V11/V13/V15 Session)

### Pattern: V13 Regression Warning

V13 introduced important honesty innovations (parameter accounting table, net predictive degree concept) but **created new fatal contradictions that V11 didn't have**:

1. Bakry-Émery paradox: claimed Ric=(35/2)g>0 while simultaneously citing Helgason's Ric≤0 theorem
2. GW sum rule cross-section contradiction: abstract said "removed", body still listed as "derived quantity"

**Lesson**: Improving form (adding honesty labels) without fixing underlying math errors can REDUCE logical consistency. Always fix mathematical foundations before adding formal accounting.

### Pattern: Progressive Honesty vs Testability Tension

V15 was the most scientifically honest version (downgraded predictions to post-dictions, explicit P1 conjecture labeling) but also the **least testable** — honesty paradoxically reduced the theory's empirical vulnerability. The optimal future version (V16+) needs to restore testability without sacrificing honesty.

### Pattern: Convergent Mathematical Ground Truth

When two independent mathematical methods (Witten Laplacian §III.B and Riemannian needle decomposition §III.E) converge on the same value (λ_KLS=35/3), document this as cross-validation strength rather than claiming either as a "proof."

## Verified Run

**6D Spacetime Phase Emergence — V11 vs V13 vs V15 (2026-07-28):**
- 3 agents deployed in single `delegate_task(tasks=[...])` batch
- V13: worst logical consistency (4.00) and math completeness (3.60) due to fatal contradictions
- V15: best overall (6.75 composite) — strongest logic (8.25) and math (7.0), weakest testability (5.0)
- V11: middle-ground (4.92) — no fatal contradictions but weak derivations
- Led to P0/P1/P2 prioritized fix pipeline → V15→V16→V17 evolution
