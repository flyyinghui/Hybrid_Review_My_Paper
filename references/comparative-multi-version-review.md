# Comparative Multi-Version Review Pattern

## Trigger
When asked to compare multiple paper versions (e.g., V11 vs V13 vs V15) across specific review dimensions.

## Protocol: M Agents × N Versions (not N×M)

For N versions × M dimensions, deploy **M specialist agents** (one per dimension), each reviewing ALL versions across ONE dimension — NOT N×M agents.

## Agent Assignment

```
delegate_task(tasks=[
  {goal: "LOGICAL-CONSISTENCY reviewer: Compare V11/V13/V15",
   context: "Read all three paper files. Score each 1-10 on: (a) internal argument coherence, (b) absence of self-contradiction, (c) cross-section consistency, (d) honesty of claims vs derivation strength. Output comparative table with rankings."},
  {goal: "MATHEMATICAL-COMPLETENESS reviewer: Compare V11/V13/V15",
   context: "Read all three plus Lean ground truth. Score on: (a) derivation rigor, (b) moduli space handling, (c) key constant justification, (d) Lean proof alignment. Output comparative table."},
  {goal: "PHYSICAL-TESTABILITY reviewer: Compare V11/V13/V15",
   context: "Read all three. Score on: (a) falsifiability, (b) observational connection, (c) parameter count honesty, (d) prediction vs post-diction distinction. Output comparative table."},
])
```

## Key Insight: Honesty-Testability Tension

When a paper becomes MORE honest (downgrading predictions to post-dictions), its testability score DROPS. The most honest version is often the least testable. This paradox needs explicit acknowledgment — it is NOT a regression.

## Verified Run
- **2026-07-28**: 6D spacetime V11/V13/V15 comparison. V15 won logic (8.25) and math (7.0); V13 won testability (5.5). Overall: V15 (6.75). V13 paradox: highest testability but lowest logic due to introduced contradictions.
