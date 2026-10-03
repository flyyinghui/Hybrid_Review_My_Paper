# ARS + AWA Hybrid Review Pipeline

**Integrated academic paper review pipeline** combining ARS (Academic Research Skills)
10-stage workflow with AWA (Academic Writing Agents) granular parallel review.

```
ARS RESEARCH → WRITE +[AWA Review] → INTEGRITY → FORMAL REVIEW → REVISE +[AWA Review] → RE-REVIEW → FINALIZE
```

- **ARS backbone** — structural pipeline management, integrity verification, formal peer review
- **AWA injection** — 12-specialist-agent parallel review at writing & revision stages
- **BootLoops frame-audit** — implicature + prose-honesty + number-discipline pre-audit (v1.3)
- **Version**: v1.3.0

---

## Design Rationale

| Layer | Tool | Role |
|:--|:--|:--|
| **Backbone** | ARS `academic-pipeline` | 10-stage state machine, integrity gates, two-stage peer review |
| **Injection 1** | AWA Stage 2a | After draft → 5-7 reviewer agents in parallel → granular prose/structure/math/consistency feedback |
| **Injection 2** | AWA Stage 4a | After revision → 3-5 reviewer agents on changed sections → verify fixes + catch new issues |
| **Formal Gate** | ARS Stage 3 | 5-person panel (EIC + R1/R2/R3 + Devil's Advocate), editorial decision, revision roadmap |

---

## Hybrid Pipeline (13 Stages)

```
Stage 0:  FRAME PRE-AUDIT   [BootLoops referee-sim: implicature audit]      ← v1.3
Stage 1:  RESEARCH          [ARS deep-research]
Stage 2:  WRITE             [ARS academic-paper full mode]
Stage 2a: AWA WRITE REVIEW  [5-7 reviewer agents parallel]                  ← INJECTION 1
Stage 2b: INCORPORATE       [apply AWA findings → revise draft]
Stage 2.5: INTEGRITY        [ARS integrity_verification_agent]
Stage 3:  FORMAL REVIEW     [5-person panel: EIC + R1/R2/R3 + Devil's Advocate]
Stage 4:  REVISE            [ARS revision mode]
Stage 4a: AWA REV REVIEW    [3-5 reviewer agents on changed sections]       ← INJECTION 2
Stage 4b: INCORPORATE       [apply AWA findings → finalize revision]
Stage 3': RE-REVIEW         [verification review]
Stage 5:  FINALIZE          [format-convert]
Stage 6:  PROCESS SUMMARY   [process record]
```

**Stage 0 (frame pre-audit, v1.3)** — before any 5-agent fact-check review, run a
`referee-sim` implicature audit: audit *what conclusion a reader will draw*, not *whether
sentences are true*. Fact-checking and frame-checking are orthogonal audits that catch
non-overlapping failure classes: abstract-firewall, unanswered-answer, hedge-blur,
missing-audience, novelty-correctness conflation, friendly-reader/strawman.

---

## Trigger Keywords

The pipeline is keyword-triggered. A few representative triggers (full list in `SKILL.md`):

| Trigger | Mode |
|---|---|
| "hybrid review my paper" / "启动Hybrid-review-my-paper技能" | 5-agent hybrid review |
| "ARS + AWA pipeline" / "integrated paper review" | Full 13-stage pipeline |
| "框架预审" / "referee-sim" / "frame audit" | Stage 0 frame pre-audit |
| "deepseek-v4-pro推理，deepseek-v4-flash撰写" / "双LLM模式" | Dual-LLM review mode |
| "诚实性tell" / "number discipline" / "舍入方向" | Honesty tells + number discipline |
| "计数不一致" / "定理名不一致" | Lean-inventory regex + symbol false-positive check |
| "适不适合投 X 期刊" / "venue-fit" | Publication-strategist venue review |
| "复审" / "带前轮P0清单复审" | Re-review with adversarial defect-list injection |
| "评分收敛" / "复审何时收尾" | Review-convergence stopping rule |
| "参考文献核验" / "幻影引用" | Reference-list machine verification |

The skill encodes **50+ specialized review patterns** as reference documents — one per
recurring failure mode discovered across real multi-round review campaigns
(CGICE / Triple-GW / neutrino condensation / SL(6,C) family papers).

---

## Key Review Patterns (references/)

Selected patterns, one file per failure mode:

- **`referee-sim-frame-pre-audit.md`** — BootLoops implicature audit (Stage 0)
- **`prose-lint-honesty-number-discipline.md`** — sentence-level honesty tells (B6) + 13 number-discipline contradictions (N)
- **`reviewer-arithmetic-false-positive-verification.md`** — recompute flagged arithmetic before relaying as P0
- **`reviewer-false-positive-lean-regex-and-symbol-errors.md`** — truncated Unicode identifiers → phantom count mismatches
- **`performative-honesty-detection.md`** — comment-only `@[honest_axiom]` tags vs real attributes
- **`competing-proposal-evaluation.md`** — 3-axis comparative evaluation of competing fix proposals
- **`venue-fit-publication-strategist-review.md`** — journal format compliance + science-threshold gate
- **`prose-layer-infinite-loop-judgment.md`** — when to stop re-reviewing (P2/P3 infinite recursion)
- **`dual-llm-v4pro-reason-v4flash-write.md`** — v4-pro reasoning + v4-flash report writing
- **`v4pro-multi-paper-cross-review.md`** — single-API-call cross-review for 3+ papers

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/multi_paper_review.py` | Multi-paper cross-review (DeepSeek v4-flash thinking mode) |

---

## Dependencies

| Skill | Role |
|---|---|
| `academic-pipeline` | ARS 10-stage backbone |
| `academic-writing-agents` | AWA 12-specialist parallel review |
| `academic-paper-reviewer` | 5-person formal panel |

LLM backend: DeepSeek (`v4-pro` for reasoning, `v4-flash` with `thinking=disabled` for report writing).

---

## Directory Layout

```
ars-awa-hybrid-review/
├── SKILL.md                    # Hermes skill definition (trigger keywords + pipeline spec)
├── README.md                   # this file
├── scripts/
│   └── multi_paper_review.py   # multi-paper cross-review driver
└── references/                 # 160+ review patterns (one file per failure mode)
```

## License

Released for open-source distribution. See the parent project for license terms.
