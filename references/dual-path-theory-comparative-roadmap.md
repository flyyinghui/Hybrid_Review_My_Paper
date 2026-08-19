# Dual-Path Theoretical Framework Comparative Analysis & Roadmap

Pipelines for comparing two competing theoretical physics paths (e.g., different moduli spaces under the same parent theory), producing argumentation roadmaps, improvement suggestions, and optimality assessments.

## Trigger

- "dual-path comparison" / "SU(6) vs SU(3,3)" / "compare two frameworks"
- "论证路线图" / "双路径对比" / "最优合理性评估"
- User provides two papers sharing a mathematical base but diverging on a key choice

## Pipeline (5 Stages)

### Stage 1: Load Foundation (parallel)

```
skill_view(name='physics-proof-engine')   # proof framework
skill_view(name='neural-memory-brain')    # concept retrieval
skill_view(name='proof-paper-cross-ref-revision')  # pitfall knowledge
skill_view(name='ars-awa-hybrid-review')  # review protocol
```

### Stage 2: Gather Evidence (parallel)

1. **Read comparative review** — if an existing cross-review exists (e.g., `Hybrid_Review_V17_vs_V61_Comparative.md`), read it first for existing findings
2. **Extract both papers** — python-docx → plain text, record paragraph count and char count
3. **Brain recall** — query 5-6 concept groups relevant to both paths (e.g., "SL(6,C) moduli space", "KLS spectral gap", "Stern-Brocot flavor charge", "D1 coherence correspondence")
4. **Read review history** — load any prior hybrid reviews of each paper

### Stage 3: Deep Reasoning (background)

Use `deepseek-v4-flash` with thinking mode:
- `model="deepseek-v4-flash"`
- `max_tokens=32768`
- `extra_body={"thinking": {"type": "enabled"}}`
- `timeout=300+`
- Handle fallback: if `content` is empty, use `reasoning_content`

Key prompt structure:
```
Inputs:
  - Comparative review (full text)
  - Prior review summaries
  - Brain concept retrieval results
  - Paper key excerpts

Output sections:
  1. 双路径论证路线图 (Argumentation Roadmap)
  2. Path A deepening suggestions (P0-P3 tiered)
  3. Path B deepening suggestions (P0-P3 tiered)
  4. 最优合理性评估 (Multi-dimensional scoring)
  5. 协同演进路线图 (Co-evolution timeline)
```

**Pitfall**: `deepseek-v4-pro` hangs on large prompts (>40K chars). Always use v4-flash for full-paper analysis.

### Stage 4: Human-Readable Synthesis

While DeepSeek runs in background, compose an intermediate summary from:
- The comparative review findings already read
- Brain recall results
- Paper structure analysis (paragraph counts, Lean stats, axiom/theorem ratios)

This gives the user immediate value while the deep analysis completes.

### Stage 5: Deliver

- Save DeepSeek output to the paper directory as `SU6_SU33_DualPath_Roadmap_YYYYMMDD.md`
- Notify user on completion via `notify_on_complete=true`
- Present both the intermediate summary and the saved file path

## Reusable Analysis Dimensions

For any dual-path theoretical comparison, score on these axes:

| Dimension | Weight | What to check |
|:--|:--:|:--|
| 数学自洽性 | 25% | Internal consistency, axiom/theorem ratio, Lean sorries |
| 物理可检验性 | 25% | Falsifiable predictions, experimental channels, explicit thresholds |
| 推导完备性 | 20% | Derivation chain completeness, honest-scope declarations |
| 简约性 | 15% | Occam's razor — axiom count vs output predictions |
| 发表成熟度 | 10% | Journal readiness, structural integrity, readability |
| 统一潜力 | 5% | Unification breadth, cross-domain explanatory power |

## Key Pattern: Moduli Space Contradiction Detection

When comparing two paths under the same parent theory (e.g., SL(6,C)):
1. Identify the **moduli space choice** (which isotropy subgroup)
2. Compare: symmetric space type, rank, restricted root system, curvature, spectral properties
3. If the two choices are mathematically incompatible (different Cartan type), flag as **P0 irreconcilable contradiction**
4. Propose resolution paths: (A) subsumption, (B) energy-scale separation, (C) honest tension admission

## Cross-Pollination Pattern

When both paths have complementary strengths:
- Path A has strong phenomenology but weak mathematical verification
- Path B has strong mathematical verification but weak phenomenology
- → Map specific techniques from each path to the other

Example from V17↔V61:
- V17 → V61: Witten Laplacian dual verification of λ_KLS
- V61 → V17: Honest-axiom template, Lean streamlining, Stern-Brocot combinatorics

## Pitfalls

1. **v4-pro hang on large prompts**: >40K chars → v4-pro silent hang (0% CPU). Always use v4-flash.
2. **thinking mode content fallback**: v4-flash thinking may put output in `reasoning_content` field, not `content`. Always check both.
3. **Wrong paper version**: User may point to "六维流形时空理论模型.docx" (9.2MB old version) instead of the current V17. Verify version before analysis. Per memory: "旧版'六维流形时空理论模型.docx'（9.2MB/1298段）非V17，不可混用"
4. **Brain recall method**: `brain.recall()` returns dict list (NOT object list). Use `r.get('content','')` not `getattr()`. Single-load for multiple queries (60-170s load, then ~0.8s/query) vs per-query subprocesses (15min for 9 queries).
