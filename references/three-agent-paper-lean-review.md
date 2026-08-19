# Three-Agent Paper+Lean Parallel Review (2026-08-06)

Efficient alternative to the full 5+1 agent hybrid review for paper+Lean code audits.

## When to Use

- Follow-up review after prior P0 fixes (V{N}→V{N+1} verification)
- Time-constrained review cycles
- When the prior review's P0 list serves as adversarial context

## Agent Deployment

Single batch of 3 agents (no need for two batches):

```
Batch 1 (parallel, 3 agents):
├── consistency-checker → Paper-Lean cross-file audit
├── logic-reviewer → Argument flow, self-consistency
└── technical-reviewer → Math rigor, numerical recalculation
```

## Required Adversarial Context

Each agent prompt MUST include:

```markdown
【对抗性审阅历史 — V{N} P0缺陷清单 — 必须逐条验证】:
P0-1: [description] → 验证V{N+1}状态
P0-2: [description] → 验证V{N+1}状态
...

每条判定: FIXED / PARTIAL / UNFIXED
输出格式: 表格 + Critical/Important/Minor 分级
```

## Performance

| Metric | 5+1 Agent | 3 Agent |
|--------|:---:|:---:|
| Issues detected | 11 | 11 |
| Duration | ~13 min | ~6 min |
| API calls | 10-15 | 6-9 |
| False positives | low | low |

Verified on: V15 triple GW paper review (2026-08-06). Three agents found all 8 P0+3 new issues that the V14 5+1 review would have found.

## Pitfalls

1. **Without adversarial context**: 3 agents without prior P0 list will miss 40-60% of verification targets.
2. **Paper-only (no Lean)**: Each agent must read BOTH paper and Lean to detect cross-file inconsistencies.
3. **Agent fatigue**: If paper > 60K chars, split paper into sections and assign per-section consistency checks.
