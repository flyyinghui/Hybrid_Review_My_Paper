---
name: ars-awa-hybrid-review
description: >-
  Integrated academic paper review pipeline combining ARS (Academic Research Skills)
  full 10-stage workflow with AWA (Academic Writing Agents) granular parallel review
  at writing and revision stages. ARS provides structural pipeline management, integrity
  verification, and formal peer review. AWA injects 12-specialist-agent parallel review
  at Stage 2 (Writing) and Stage 4 (Revision) for fine-grained quality improvement.
  Triggers: hybrid review, ARS+AWA pipeline, integrated paper review, full review pipeline.
version: "1.0.0"
model: deepseek-v4-flash
tags: [academic-writing, peer-review, pipeline, multi-agent, hybrid]
depends_on:
  - academic-pipeline
  - academic-writing-agents
  - academic-paper-reviewer
---

# ARS + AWA Hybrid Review Pipeline v1.0

Integrated academic paper review pipeline: **ARS backbone** (structural management + formal peer review) × **AWA injection** (granular quality review at writing/revision stages).

```
ARS RESEARCH → WRITE +[AWA Review]→ INTEGRITY → FORMAL REVIEW → REVISE +[AWA Review]→ RE-REVIEW → FINALIZE
```

## Design Rationale

| Layer | Tool | Role |
|:--|:--|:--|
| **Backbone** | ARS `academic-pipeline` | 10-stage state machine, integrity gates, two-stage peer review, format output |
| **Injection 1** | AWA Stage 2a | After draft complete → 5-7 reviewer agents in parallel → granular prose/structure/math/consistency feedback → incorporate before integrity check |
| **Injection 2** | AWA Stage 4a | After revision complete → 3-5 reviewer agents on changed sections → verify fixes + catch new issues → incorporate before re-review |
| **Formal Gate** | ARS Stage 3 | 5-person panel (EIC + R1/R2/R3 + Devil's Advocate), editorial decision, revision roadmap |

## Hybrid Pipeline (12 Stages)

```
Stage 1:  RESEARCH          [ARS deep-research]
Stage 2:  WRITE             [ARS academic-paper full mode]
Stage 2a: AWA WRITE REVIEW  [AWA: 5-7 reviewer agents parallel]  ← INJECTION 1
Stage 2b: INCORPORATE       [apply AWA findings → revise draft]
Stage 2.5: INTEGRITY        [ARS integrity_verification_agent]
Stage 3:  FORMAL REVIEW     [ARS academic-paper-reviewer: 5-person panel]
Stage 4:  REVISE            [ARS academic-paper revision mode]
Stage 4a: AWA REV REVIEW    [AWA: 3-5 reviewer agents on changed sections] ← INJECTION 2
Stage 4b: INCORPORATE       [apply AWA findings → finalize revision]
Stage 3': RE-REVIEW         [ARS verification review]
Stage 5:  FINALIZE          [ARS format-convert]
Stage 6:  PROCESS SUMMARY   [ARS process record]
```

## Trigger Keywords

- "hybrid review my paper"
- "ARS + AWA pipeline"
- "integrated paper review"
- "full review pipeline with writing quality"
- "comprehensive paper review"
- "比较本文与...学术贡献度" / "compare contribution to existing literature"
- "contributions comparison" / "contribution benchmarking"
- "创新性工作" / "innovation assessment" / "从创新性角度" — triggers INNOVATION-FOCUSED review mode with 6-domain benchmarking
- "compare five versions" / "multi-version comparison" / "V{N} V{M} V{K} comparison" — triggers FIVE-VERSION COMPARATIVE REVIEW with 2 dimension-specialized agents (logic+math, testability+evolution). See `references/five-version-comparative-review.md`.
- "cross-check GW consistency" / "compare GW peaks" / "两篇论文GW表述" — triggers CROSS-PAPER GW CONSISTENCY AUDIT across papers sharing SL(6,C) foundation. See `references/cross-paper-gw-consistency-audit.md`.
- "启动Hybrid-review-my-paper技能" / "采用deepseek-v4-pro(最大tokens)推理" / "三篇论文相互推导结论的一致性" — triggers V4-PRO MULTI-PAPER CROSS-REVIEW. Single API call with 8-axis matrix + 5-section output. Use when user explicitly requests v4-pro or cross-paper consistency audit across 3+ papers. See `references/v4pro-multi-paper-cross-review.md`.
- "双模型对照审查" / "v4-pro + Qwen3.8 对照" / "同时调用 Qwen3.8 对照审查" — triggers DUAL-MODEL COMPARATIVE REVIEW (v4-pro high + Qwen3.8). Extract key content → dual-model calls → de-duplicate + cross-verify + reject false-positives. Key insight: models only see extracted fragments, so they MISS existing full derivations in the body — always grep the body before classifying a finding as real. See `references/dual-model-comparative-review.md`.

## J-space 预检层 (审查流程固定第一步, 2026-08-19)

任何 hybrid-review 审查启动前，先执行 J-space 预检（减少"漏掉正文推导"类误判）：

1. **deep-reasoning 追踪推导链**：在部署审查模型前，先沿关键推导链追踪中间步骤——
   - η_k → g_TC：确认 η_k = C₂(adj)·h^∨/dim(M) 的完整推导在正文位置（CGICE §7.3 行 602-610）
   - |ρ|² → λ_⊥：确认 A₅ 根系显式计算 + Freudenthal-de Vries 双重验证（§2.7）
   - τ_c → 122阶：确认是否已诚实标注为校准（§7.2 Step 3）
   - **原则**："中间步骤先于结论"——在断言"缺公式/来源不明"前，先 grep 正文确认推导链是否完整存在
2. **self-monitoring 置信度校准**：区分"已追踪验证"（grep 确认推导存在）vs "未追踪的猜测"（仅凭摘要印象）。审查模型输出"缺公式"时先 grep 正文，避免把"正文已有但审查者没看到"误判为 P0。
3. **broadcast hub set 追踪**：对跨论文共享参数（g_TC=2.60, λ_∥=35, λ_⊥=35/3, η_k=72/35, b₀=12）建立 hub set，追踪每个参数在四论文的引用位置，审查时检查一致性。

**验证案例**：CGICE 双模型审查中，v4-pro 误判"g_TC 缺公式"、Qwen3.8 追问"η_k 来源"，实际 §7.3 行 602-610 已有完整推导。若先执行 J-space 预检（grep 确认推导链），这两条误判可避免。

## 双模型交叉审查方式 (Dual-Model Cross-Review, 2026-08-19 固定方式)

用户要求"LLM双模型交叉审查"时，用两个模型独立审查同一篇论文，综合去重给出最优结论：

1. **v4-pro 主审**：`deepseek-v4-pro` (reasoning_effort=high, max_tokens=32768, temperature=0)，约 128s，深度数学推理，善于发现几何/维度错误。
2. **Qwen3.8 对照**：本地 `qwen3.8:27b-Q8_0` (chat_template_kwargs {"enable_thinking": False}, max_tokens=3000)，约 11min，独立视角，善于追问参数来源 + 计数映射。
3. **综合去重规则**：
   - 双模型共同发现 = 高置信真实问题（立即修复）
   - 单模型独有 = 需人工核实（可能是真实发现，也可能是误判）
   - **误判检测**：模型只看到"提取的摘要/关键片段"，可能漏掉正文完整推导（如 CGICE 的 η_k→g_TC 推导链在 §7.3 完整存在但摘要未写，导致双模型误判"缺公式"）
   - 已诚实标注的（如 τ_c=4.01 [honest-axiom]）无需改，在综合报告中标注"已处理"
4. **输出**：综合报告（P0 已修复/P1 需澄清/P1 误判 三栏）+ 两个模型的原始审查文件。

**已验证案例（CGICE 2026-08-19）**：v4-pro 发现 P0-1 维度混淆（SU(6)/SO(6) 20维 vs SL(6,C)/SU(6) 35维，真实，已修复摘要）+ Qwen3.8 发现公理计数冲突（73 vs 25/62，真实，已交叉校核）；双模型共同误判 η_k 来源/g_TC 公式（正文 §7.3 行 602-610 已有完整推导 C₂·h^∨/dim=72/35 → g*²=4π²|η_k|/b₀=24π²/35）。

## How It Works

### Stage 2a: AWA Write Review Injection

After ARS Stage 2 (WRITE) completes with a full paper draft:

**Step 1 — Load AWA**: Load `academic-writing-agents` skill and `principles/academic-writing.md` (30 principles).

**Step 2 — Present deployment plan**:
```
## AWA Write Review — Deployment Plan

Draft complete: [N] pages, [M] references, [K] figures

Deploying 5 agents in parallel:
├── consistency-checker → Terminology, cross-refs, structural coherence
├── logic-reviewer      → Argument flow, transitions, narrative arc
├── technical-reviewer  → Math notation, methodology, result validity
├── writing-reviewer    → Prose clarity, conciseness, academic tone
└── bibliography-auditor → Bib completeness, arXiv updates, venue consistency

Each agent reads the full draft. Expected output: prioritized issue lists.
Proceed? (y/n/add agents)
```

**Step 3 — Deploy**: Use `delegate_task` with `tasks` array (max 3 per batch, 2 batches for 5 agents).

**Step 4 — Synthesize**: Merge findings → Critical/Important/Minor → present to user.

**Step 5 — User decides**: Which issues to fix before Stage 2.5 integrity check.

### Stage 4a: AWA Revision Review Injection

After ARS Stage 4 (REVISE) completes:

**Step 1 — Identify changed sections**: Compare revised draft vs original draft.

**Step 2 — Deploy 3 agents** (lighter than Stage 2a):
```
├── consistency-checker → Verify fixes + cross-refs on changed sections
├── writing-reviewer    → Check revision prose quality
└── technical-reviewer  → Verify technical corrections
```

**Step 3 — Synthesize**: Verify that ARS review concerns were actually addressed, flag any new issues introduced by revision.

**Step 4 — User decides**: Which residual issues to fix before Stage 3' re-review.

## AWA Agent Deployment Patterns

### Full Draft Review (Stage 2a)

```
Batch 1 (parallel):
  delegate_task(tasks=[
    {goal: "consistency-checker: Review terminology, cross-refs, figure-text alignment in [FILE]",
     context: "Read [FILE]. Load principles A1,A3,D3,D7. Report Critical/Important/Minor issues with line references.",
     toolsets: ["terminal", "file"]},
    {goal: "logic-reviewer: Review argument flow, transitions, narrative arc in [FILE]",
     context: "Read [FILE]. Load principles A2,A4,A5,A6,A7. Check GPS rhythm, paragraph closers, claim-first exposition.",
     toolsets: ["terminal", "file"]},
    {goal: "technical-reviewer: Check math notation, methodology, citations in [FILE]",
     context: "Read [FILE]. Load principles C1,C2,C3,E1,E2. Verify all equations explained, all named entities cited.",
     toolsets: ["terminal", "file"]},
  ])

Batch 2 (parallel):
  delegate_task(tasks=[
    {goal: "writing-reviewer: Review prose clarity, conciseness, tone in [FILE]",
     context: "Read [FILE]. Load principles B1-B8. Flag AI-tell markers, negation-contrast, colloquial terms.",
     toolsets: ["terminal", "file"]},
    {goal: "bibliography-auditor: Audit bib completeness, arXiv updates, venue consistency",
     context: "Read [FILE]. Load principles E1,E2,E3. Check every citation exists, no arXiv-only when published version exists.",
     toolsets: ["terminal", "file"]},
  ])
```

### Revision Review (Stage 4a)

```
Batch 1 (parallel, 3 agents):
  delegate_task(tasks=[
    {goal: "consistency-checker: Verify fixes on changed sections [FILES]. Check no new cross-ref breaks.",
     context: "Read [FILES]. Compare against prior review findings. Load principles A1,A3. Flag: fixes not applied, new issues.",
     toolsets: ["terminal", "file"]},
    {goal: "writing-reviewer: Review revised prose in [FILES]. Check revision quality.",
     context: "Read [FILES]. Load principles B1-B8. Flag: prose regression, unfixed issues from prior review.",
     toolsets: ["terminal", "file"]},
    {goal: "technical-reviewer: Verify technical corrections in [FILES].",
     context: "Read [FILES]. Check all math/citation fixes from ARS reviewer concerns applied correctly. Flag regressions.",
     toolsets: ["terminal", "file"]},
  ])
```

## Synthesis Report Format

```markdown
## Hybrid Review — Stage [2a/4a] AWA Injection Report

### ARS Stage [2/4] Summary
- Draft: [N] pages, [M] references, [K] figures
- ARS self-assessment: [score if available]

### AWA Parallel Review Findings

#### Critical ([N] items)
1. **[Agent]** [Principle] [FILE:LINE] — Description → Suggested fix

#### Important ([N] items)
...

#### Minor ([N] items)
...

### Patterns
- [Cross-agent recurring themes]

### Comparison: AWA vs ARS Self-Assessment
- ARS found: [N] issues
- AWA found: [N] additional issues (not caught by ARS internal review)
- Overlap: [N] issues (both caught)

### Recommended Actions Before Next Stage
1. [Highest priority]
2. ...

### User Decision
- [ ] Fix all Critical + Important → proceed
- [ ] Fix Critical only → proceed (Important deferred)
- [ ] Bypass AWA findings → proceed directly
```

## Quality Gates

| Gate | Tool | Blocking? |
|:--|:--|:--|
| Stage 2a AWA findings | AWA reviewers | **Advisory** — user decides what to fix |
| Stage 2.5 Integrity | ARS integrity_verification_agent | **MANDATORY** — must PASS |
| Stage 3 Formal Review | ARS 5-person panel | **MANDATORY** — decision required |
| Stage 4a AWA findings | AWA reviewers | **Advisory** — user decides |
| Stage 4.5 Final Integrity | ARS integrity_verification_agent | **MANDATORY** — zero issues |

## Innovation-Correctness Gap Analysis (NEW v1.1)

When a paper shows divergent innovation and correctness scores (e.g., innovation 5.2 vs correctness 3.4), run a **meta-review** asking: "What correctness improvements would most elevate this innovation?" The gap reveals that the conceptual framework is strong but the mathematical execution lags. See `references/innovation-correctness-gap-analysis.md` for the 5-specialist meta-review protocol (proof gaps, D1 closure, gamma closure, axiom burden, improvement roadmap).

### Progressive Honesty and Score Trajectory

Making a paper MORE honest can REDUCE scores. This is NOT a regression — it reflects accurate assessment replacing inflated overclaim scores. See `proof-paper-cross-ref-revision/references/progressive-honesty-score-paradox.md`.

## Reference Files (NEW in v1.1)

| `references/review-verdict-application-and-axiom-recount.md` | **NEW — Review-verdict application + axiom-count drift** — 5-step workflow for applying cross-paper review verdicts (grep-scope first, skip non-applicable), the derivation-vs-assumption Table 1, axiom-count drift detection (MD 25/14/61 vs Lean 69), A-numbering continuity remap, and the docx run-splitting pitfall (2026-08-19). |

| File | Description |
|------|-------------|
| `references/cross-paper-sl6c-review-20260819.md` | **⭐ NEW — SL(6,C) 四论文跨论文综合审查** — 5 项标准 P0/P1 修改模板（Deng-Hani 删除/Atiyah-Singer 降级/分类表/Bourgain 局限声明）+ η_k=72/35 第一性原理 + Fokker-Planck 协方差耗散 + 公理序号统一 + DOCX run 级替换陷阱 (2026-08-19) |
| `references/axiom-count-drift-and-renumbering.md` | **⭐ NEW — Axiom-count drift & continuous renumbering** — paper-claims-vs-Lean axiom count diff, functional re.sub renumbering map, the 4 P0 patterns (circular reverse-engineering / dimensional category error / zero-content axiom / performative theorem name), Lean gotchas (2026-08-19) |
| `references/v4pro-multi-paper-cross-review.md` | **⭐ NEW — v4-pro Multi-Paper Cross-Review** — 6-step protocol for 3+ paper cross-review with v4-pro: extraction→prompt build (<50K chars)→v4-pro API (max_tokens=32768)→8-axis matrix→5-section output. ~160s. (2026-08-07) |
| `references/multi-paper-v4flash-thinking-review.md` | **⭐ NEW — Multi-paper V4-Flash Thinking Review** — Single-API-call alternative for 3+ paper cross-review. ~4 min, 48K reasoning. (2026-08-06) |
| `references/cross-paper-gw-consistency-audit.md` | **⭐ NEW — Cross-paper GW consistency audit** — 8-axis checklist for SL(6,C) trilogy, 3 common failure patterns, V63→V17 case study (2026-08-06) |
| `references/section-alignment-v4pro-docx.md` | **⭐ NEW — Section realignment workflow** — v4-pro rewrite + DOCX insertion for diverged papers, pitfall catalog (2026-08-06) |
| `references/v14-to-v16-iterative-fix-pipeline.md` | **⭐ NEW — V14→V15→V16 三版迭代修复** — regression引入检测、header-code漂移、尺度不匹配、双轨同步协议 (2026-08-06) |
| `references/cross-paper-consistency-review-protocol.md` | **⭐ NEW — 跨论文一致性审查协议** — V63 vs V16对比审查、六步对齐方法、4项关键陷阱 (2026-08-06) |
| `references/iterative-fix-regression-detection.md` | **⭐ NEW — 迭代修复回归检测** — 4类回归模式：Bourgain头注释陷阱、Stale定理旧值、观测比较漂移、尺度不匹配 (2026-08-06) |
| `references/v4pro-multi-paper-cross-review.md` | **⭐ NEW — v4-pro Multi-Paper Cross-Review** — 6-step protocol for 3+ paper cross-review with v4-pro: extraction→prompt build (<50K chars)→v4-pro API (max_tokens=32768)→8-axis matrix→5-section output. ~160s. (2026-08-07) |
| `references/multi-paper-v4flash-thinking-review.md` | **⭐ NEW — Multi-paper V4-Flash Thinking Review** — Single-API-call alternative for 3+ paper cross-review. ~4 min, 48K reasoning. (2026-08-06) |
| `references/cross-paper-gw-consistency-audit.md` | **⭐ NEW — 跨论文GW一致性审计** — 两篇SL(6,C)论文GW谱交叉审查，频率/机制/H₀诚实度8维比对 (2026-08-06) |
| `references/bourgain-header-claim-trap.md` | **⭐ NEW — Bourgain头注释陷阱** — 头声称已修但代码未删的检测模式 (2026-08-06) |
| `references/v14-review-fix-pipeline.md` | V14 Review-to-Fix Pipeline — Lean审计→双轨修复→交叉核查 (2026-08-06) |
| `references/three-agent-paper-lean-review.md` | **NEW — 三代理并行论文+Lean审阅** — 效率替代方案(3代理vs5+1)，含对抗性上下文注入、5种检测模式（2026-08-06） |
| `references/lean-arithmetic-audit-patterns.md` | **NEW — Lean算术审计模式** — norm_num假阳性、DOF计数溢出、定理=恒等展开、Bourgain替换为假代数、0 sorries+不可编译代码（2026-08-06） |
| `references/three-version-comparative-review.md` | **NEW — Three-Version Comparative Review** — 3 dimension-specialized agents (logic+math+testability), progressive honesty paradox, V13 warning case (2026-07-28) |
| `references/adversarial-context-sequential-review.md` | **NEW** — Multi-round review with prior findings as mandatory audit context |
| `references/innovation-focused-review-mode.md` | **NEW** — Innovation-only assessment with percentile rankings vs top papers |
| `references/innovation-correctness-gap-analysis.md` | **NEW** — Meta-review protocol: 5 specialists diagnose how to close the gap |
| `references/incremental-review-score-tracking.md` | **NEW** — Multi-version score tracking: V5→V6→V7, Δ<0.5 = cosmetic fixes, inject prior P0 as adversarial context |
| `references/comparative-three-version-review.md` | **NEW** — Comparative 3-version review: 3 parallel agents (consistency/math/testability), honesty-testability paradox detection (2026-07-28) |
| `references/brain-memory-knowledge-framework-synthesis.md` | **NEW** — Brain+memory→comprehensive MD: multi-source retrieval, 6-section structure, LaTeX+ASCII diagrams (2026-07-28) |
| `references/docx-translation-image-embedding-fix.md` | **NEW** — DOCX translation image loss fix: 5-step ZIP-level protocol to re-embed images after python-docx rebuild (2026-08-03) |
| `references/comparative-two-paper-review.md` | **NEW** — Comparative 2-paper review: 5 agents in 2 batches for cross-paper consistency, rigor, testability, publication strategy, and mutual learning assessment (2026-08-01) |
| `references/dual-path-theory-comparative-roadmap.md` | **NEW** — Dual-path theoretical framework comparative analysis+roadmap: 5-stage pipeline (load foundation→gather evidence→deep reasoning with v4-flash thinking→synthesis→deliver), 6-dimension scoring, cross-pollination mapping, moduli space contradiction detection (2026-08-04) |
| `references/paper-plus-lean-final-review.md` | **NEW** — Paper+Lean 6-agent final review: parallel deploy of consistency+logic+technical+writing+bibliography+lean-specialist. Multi-dimensional scoring, Deng-Hani framework compliance, prioritized P0-P3 fix checklist (2026-07-30) |
| `references/revision-landing-check-pattern.md` | **NEW** — Revision landing check: automated scan against prior review P0-P3 checklist, fix/partial/unfixed/new-issue classification, Lean stats conflict detection, residual version artifact scan (2026-07-30) |
| `references/v63-p0fix-final-review-pattern.md` | **NEW** — V63 P0Fix two-stage review: 26-check audit → 5-agent panel (2026-08-04) |
| `references/revision-landing-check-pattern.md` | Revision landing check: automated scan against prior review P0-P3 checklist (2026-07-30) |, fix/partial/unfixed/new-issue classification, Lean stats conflict detection, residual version artifact scan (2026-07-30) |

### V22→V25 Neutrino Condensation Paper (2026-07-06)

**Full multi-tier revision pipeline:**

```
Stage 2a (5 agents, 71 findings)
  → P0-P6 blocking fixes (provenance, no-free-params, falsifiability, citations, SB arithmetic)
  → P7-P10 quality fixes (AI markers, transitions, self-praise, g_TC dual role)
  → Stage 4a (3 agents, 4 residual issues found)
  → R1-R4 immediate fixes
  → Stage 3 formal panel (5 reviewers, PRD Major Revision)
  → R1-R6 editorial decision revisions
```

Key lessons:
1. **Tiered implementation**: P0-P4 are blocking → P5-P6 are technical → P7+ are prose. Fix in priority order, cross-audit after each tier.
2. **Stage 4a catches regressions**: 4 issues survived P0-P10 that only the verification review caught (R1 "no free parameters" in Abstract, R2 same in Introduction, R3 Σm_ν inconsistency, R4 ghost [cite] placeholders).
3. **Three-stage postulate → hypothesis repositioning**: definitional identity → bridging postulate (Stage 1, P21) → phenomenological hypothesis (Stage 2, P26). Triggered when formal peer review identifies the postulate as carrying the entire predictive weight. Full protocol in `proof-paper-cross-ref-revision/references/v24-v25-editorial-decision-revisions.md`.

### V20a Neutrino Condensation Paper (2026-07-05)
Full pipeline executed: 5 agents deployed, 12 Critical issues found and fixed, Stage 2.5 passed. See `proof-paper-cross-ref-revision/references/awa-hybrid-review-findings-v20.md` for full findings.

### Key Execution Lessons

1. **Bibliography is always the worst.** Every paper's reference list needs full audit — missing entries, wrong citation numbers, and duplicates are near-universal.
2. **Two competing axiom/numbering tables are a red flag.** Legacy tables must be labeled or removed.
3. **Dependency graphs fossilize predictably.** Always check range claims (A1–AN, L1–LN) against current reality.
4. **√2 convention splits are common in seesaw papers.** Check §1 vs §2.5 vs §3 for consistency.
5. **AWA catches what ARS misses.** In the V20a execution, ARS structural audits found 0/24 of the issues that AWA's parallel agent review discovered.

1. **AWA is advisory, ARS is blocking.** AWA provides granular quality feedback; ARS enforces structural/integrity gates.
2. **User always drives.** AWA review findings are presented with priorities; user chooses what to fix.
3. **Maximum 3 agents per delegate_task batch.** For 5+ agents, split into two parallel batches.
4. **Each AWA agent prompt must include**: file paths, principle categories (A-F), expected output format (Critical/Important/Minor with line references).
5. **Stage 2a deploys 5-7 agents** (full review). **Stage 4a deploys 3 agents** (lighter verification).
6. **Fix small AWA findings directly** (use `patch`/`write_file`). Deploy AWA action agents (prose-polisher) only for complex rewrites.
7. **Track AWA-ARS divergence.** When AWA catches issues ARS missed (bibliography collapse, narrative breaks, convention splits), note the pattern for pipeline improvement. See `references/awa-ars-divergence.md`.

## Verified Runs

| `references/comprehensive-rewrite-fix-pipeline.md` | **⭐ NEW — Comprehensive DeepSeek Rewrite for Bulk P0 Fixes** — 6-step protocol for applying 10+ P0 fixes in a single API call (64s vs 30min manual). CGICE V7→V8 case study. (2026-08-11) |

### CGICE V9→V10 R2 Review + Comprehensive Fix (2026-08-11) ← NEWEST

Eighteenth verified run. Second-round review of CGICE V9 found that prior "P0 fixes" were header notes appended without changing body text — the paper simultaneously made contradictory claims. 5-agent panel scored 2/10 consistency. V10 applied 9 REAL fixes via comprehensive DeepSeek rewrite (82s) + Lean surgical correction. v4-pro confirmed 9/10. Key pattern: header-only fixes ARE NOT fixes. See `references/cgice-v9-r2-header-only-fix-pattern.md`.

Seventeenth verified run. CGICE V7 paper with 12 P0 + 8 P1 issues from hybrid review. Used comprehensive DeepSeek rewrite protocol: classified fixes → built 12-item fix instruction with exact replacement text for §2.7 → single v4-flash API call (64.3s) → v4-pro audit (7/10). 10/12 P0 FIXED, 2 PARTIAL. Key pattern: replaced iterative patch with one-shot rewrite — dramatically faster and more consistent. Full protocol: `references/comprehensive-rewrite-fix-pipeline.md`.

### CGICE V7→V9 Multi-Round Evolution (2026-08-11) ← NEWEST

Eighteenth verified run. Three-round pipeline: V7(3.3, 12 P0)→comprehensive rewrite(64s)→V8(7.0)→P1 fixes→V9. Critical discovery: v4-pro single audit scored V9 9/10, but 5-agent panel found 4.7/10 with 8 undetected P0 issues. Added Pitfall 18 (v4-pro over-generosity) + `references/comprehensive-rewrite-fix-pipeline.md` + `references/cgice-v7-v9-evolution-case-study.md`. Full protocol in the case study reference.

### V63+V17+V16 Three-Paper Cross-Review with v4-pro (2026-08-07)

Sixteenth verified run. User explicitly requested "deepseek-v4-pro(最大tokens)推理" for 3-paper + 3-Lean cross-review. Prompt 47K chars, response 7,841 chars in 159.5s. 8-axis consistency matrix + 5-section output. Scores: V63=2/10, V17=3/10, V16=4/10 — all NOT READY.

Key findings: V63 internal g_TC contradiction (2.60 vs 0.5), V17 H₀ circularity + DM DOF ad-hoc construction (75≠70), V16 10⁸× dilution factor requires unobservable t_freeze. Cross-paper: DM mechanism conflict (neutrino condensate vs GW energy), GW frequency conflict, g_TC value conflict.

**v4-pro safe operating window confirmed**: v4-pro works reliably for prompts <50K chars with max_tokens=32768. Above 120K chars still hangs. Pattern and extraction methodology codified as `references/v4pro-multi-paper-cross-review.md`.

### Triple GW V5→V6→V7 (2026-07-25) ← NEW

Thirteenth verified run. Three consecutive reviews in single session with adversarial context injection. Scores: 1.3→1.4→1.7. Four P0 issues persisted across all versions, triggering the P0-persistence-across-versions detection rule. Key finding: surgical fixes cannot resolve framework-insufficient P0s — GW production from SL(6,C) geometry has no known derivation. See `references/triple-gw-v5-v6-v7-reviews.md` and `references/p0-persistence-across-versions.md`.

### Triple GW V11 — Formal Verification Trap (2026-07-25) ← NEWEST

Fourteenth verified run. V11 added Bakry-Émery explicit tactic proof, Bourgain slicing formalization, Ricci flow theorem (Lean 811 lines, 28 theorems, 0 sorries). **Score unchanged from V7: 1.7/10**. Demonstrates the "formal verification trap" — Lean proof upgrades do not improve review scores when the underlying physical derivation chain is broken. Five reviewers unanimously identified the same P0 issues as V7. Deeper mathematical errors (Ricci sign error, false axiom `ln(35/33)=160`) were later discovered by v4-pro deep analysis.

**Key lesson**: When 5-agent review scores stagnate despite formal proof upgrades, deploy single v4-pro deep mathematical analysis (Anthropic SDK, max_tokens=16384) to identify whether P0 issues are symptoms of mathematical impossibilities. See `references/triple-gw-v11-hybrid-review-record.md`.

### CDM Topological Kink Paper (2026-07-07)

Fourth verified run — 76-paragraph physics paper claiming to prove CDM:visible = 5:1 via SL(6,C) geometric crystallization. 5 agents in 2 batches. Scores: Consistency 3/10, Logic 2/10, Technical 2/10, Writing 6/10, Bibliography 3/10. Overall **3.2/10 — NOT READY**.

6 P0 showstoppers discovered:
1. Rank=90 in 70×70 matrix (mathematical impossibility)
2. 5:1 ratio hardcoded as axiom A5, not derived
3. Lean proof is empty shell (8 `exact trivial`, 5 `admit`, 31 undefined identifiers)
4. OllamaLens TEXTUAL_COOCCURRENCE is categorical error (LLM co-occurrence ≠ mathematical validation)
5. Reference [9] fabricated co-authorship (Eldan not co-author of cited paper)
6. KLS inequality misapplied to infinite-dimensional moduli space

Recommended path: downgrade from "formal proof" to "formalized conjecture" → target *Physics Letters B*. Full findings: `references/cdm-hybrid-review-20260707.md`.
Third real-world hybrid review — ~24,300 words, V38 final before PRD submission. 5 agents in 2 batches, all deployed in parallel. Scores: Consistency 5/10, Logic 6/10, Technical 3/10, Writing 3/10, Bibliography 2/10. Overall **3.8/10 — NOT READY for PRD**.

Key findings (6 P0 showstoppers):
1. SL(6,C)/SU(6) dimension error (26→35)
2. Self-identical ratio comparison after global 2.32→2.56 replacement (P52)
3. Citation numbering system collapse (~30% wrong)
4. Axiom catalog mismatch: body A1-A24 vs appendix A1-A28 (P53)
5. `:=True` stubs surviving in A6/A16/A28 despite claims of "zero stubs"
6. √2 convention untracked: Lean y_ν=0.50 vs paper y_ν=0.71 (41% discrepancy)

Submission recommendation: **Not ready for PRD.** Consider Physics Letters B (shorter, single-idea focus) or EPJC (higher tolerance for interdisciplinary methods). PRD requires higher writing and citation rigor. A full rewrite (abstract <250 words, CGICE→appendix, AI tools→supplement, ~12,000 word target) would be needed for PRD submission.

Agent deployment pattern refined:
```python
delegate_task(tasks=[
    {"goal": "consistency-checker: ...", "toolsets": ["terminal","file"]},
    {"goal": "logic-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "technical-reviewer: ...", "toolsets": ["terminal","file"]},
])  # Batch 1: 3 agents (structure + logic + math)
delegate_task(tasks=[
    {"goal": "writing-reviewer: ...", "toolsets": ["terminal","file"]},
    {"goal": "bibliography-auditor: ...", "toolsets": ["terminal","file"]},
])  # Batch 2: 2 agents (prose + refs)
```
Each agent reads the full paper from `/tmp/v38_paper.txt` + appendix from `/tmp/v38_appendix.txt`. Scores aggregated into 5-dimension radar with submission recommendation. 5 agents in 2 batches found **71 issues** (26 Critical / 22 Important / 23 Minor). Key findings: λ_KLS provenance misattributed to Klartag & Lehec (they prove positivity, not numerical value 11.7), "no free parameters" contradicted by internal admissions, "maximally falsifiable" for unmeasurable M_R ≈ 10¹⁴ GeV, bibliography system broken (duplicate [28], ghost [14], 11 uncited refs), §2.2.3→§2.3 zero transition. Prose score 5/10. Synthesized into P0-P6 prioritized fix list. See `references/v22-v23-hybrid-review-p0-p6-fix.md`.

### V56 Neutrino Condensation Paper — Final Hybrid Review + Contribution Comparison (2026-07-23)

Eleventh verified run. 6-agent panel. Unanimous REJECT at 3.0/10.

**Twelfth verified run — V55→V56 FOLLOW-UP REVIEW WITH ADVERSARIAL CONTEXT (2026-07-23)**:
User required V56 review to build on V55 findings. 6 agents received full V55 P0/P1 defect list as mandatory audit context. 5/6 MAJOR_REVISION, 1/6 REJECT, 3.9/10 (+0.8 from V55's 3.1). New pitfalls discovered: JSON unparseable from embedded quotes in detailed_comments (P0), .format() brace conflict with LaTeX (P0). Full pattern: `references/v56-vs-v55-followup-review-pattern.md`.

### V55 Neutrino Condensation Paper — Full Hybrid Review + C3-C6/C1-C2 Fix Pipeline (2026-07-22)

Tenth verified run. 5 rounds over 2 days: 3.1→4.3→5.5. EPJC recommendation. CN translation delivered. **New: Contribution Comparison Review mode** (3 domain experts: neutrino theory + cosmology + publication strategy) for benchmarking against literature. Triggers: "比较学术贡献度" / "compare contribution". See `references/v55-full-review-20260722.md`.

10 P0 showstoppers (initial):
1. Version chain break: paper V55 vs Lean V53 (2 versions behind)
2. Lean L379 compile error: `A_CS_QUANT]` illegal character `]`
3. g_TC² dual values: header ≈6.748 vs T_gTC_value proves 6.768 (0.3% diff)
4. D1 is definitional identity, not derivation
5. Dual-path "cross-validation" is an algebraic loop (shared |ρ|²=35 origin)
6. D1 epistemic status swings between 7+ contradictory labels (proved/conditional/postulate/conjecture)
7. Predictive degree drifts between −1 and −2 across sections
8. 23 references missing ([42]-[64]), numbering jump from 41→58
9. Abstract 384 words (limit 250) + contains LLM pipeline meta-info
10. |ρ|²=35 possible confusion with dim(SU(6))=35

**Venue recommendation**: NOT PRD/PRL. Target **Foundations of Physics** (highest tolerance for honest-axiom approach) or **Physics Letters B** (short format forces tightening).

### Pitfall 11: Follow-Up Review WITHOUT Prior Context — User Rejection (P0)

When running a review of V{N+1} after V{N} has already been reviewed, the user EXPECTS reviewers to build upon the prior review findings. Running without injecting the prior P0/P1 issue list causes rejection.

**Mandatory**: Load prior review → extract ALL P0/P1 IDs → inject as 【前次评审历史】 block → require "v55_issues_fixed" / "v55_issues_remain" in JSON output → include fix-status table in report.

### Pitfall 8: DOCX Extraction Loop Overwrites Target File (P0, 2026-07-22)

When iterating over multiple DOCX files in a directory to extract text to a single `/tmp/output.txt`, the LAST file in the loop silently overwrites all previous extractions. The consistency-checker and logic-reviewer received only §2.2 (13K chars) instead of the full 199K-char paper because `Section_22_Restructured_V55.docx` was processed last.

**Detection**: Compare extracted file size against expected. If `wc -c /tmp/output.txt` < 50K for a 60-page paper, the extraction was overwritten.

**Fix**: Either (a) filter to a single target file: `if 'EN_V55.docx' in f and 'Modifications' not in f and 'Section' not in f`, or (b) write each extraction to a uniquely-named file.

**Symptom**: Reviewers report "only §2.2 available" when the full paper was provided.

Sixth verified run — V51 paper + Lean with full Floquet-Equivariant framework. 5 agents in 2 batches. Key finding: the MD→DOCX+Lean upgrade pipeline successfully transformed the reviewer's Chinese markdown into a 55-OMML DOCX section + 11 new Lean axioms with zero conversion warnings. The cross-audit discovered 85/9/29 ground truth counts that were inconsistent across 4 DOCX files (old: 82/7/10). Fixed via XML-level bulk replacement without losing OMML formulas.

### V63 Neutrino → V17 Triple-GW Cross-Paper Alignment (2026-08-06) ← NEW

Fifteenth verified run. Cross-paper consistency audit between V63 neutrino condensation paper Section V and V16 triple GW paper. Deployed single consistency agent with 8-axis comparison matrix. **Score: 3.0/10 — CRITICAL inconsistencies found.**

Key findings:
1. GW peak count: V63=2 peaks, V16=3 peaks — DIVERGENT
2. GW frequencies: V63 (10⁻⁸/10⁻² Hz) vs V16 (4.5×10¹¹/1.71/10⁻⁹ Hz) — CONFLICT
3. H₀ status: V63 labeled as "derived", V16 corrected to [honest-axiom] — CONFLICT
4. V63 internal math: S₃/T formula claimed ≈35 but computes to ≈929
5. Missing honest-axiom declarations in V63 throughout Section V

Resolution: deepseek-v4-pro generated corrected Section V + Appendix E.5-E.6 text aligned to V16 ground truth. python-docx paragraph-level replacement in V63 DOCX → V63_V17.docx. 31 paragraphs changed across Section V, Appendix E, and cross-references in §§VII.C.

**Pattern codified as `references/cross-paper-consistency-review-protocol.md`** — six-step alignment protocol with 4 key pitfalls.

Seventh verified run — single-section focused evaluation using deepseek-v4-pro (max_tokens=16384, temp=0.0). Compared paper's Bakry-Émery curvature approach (§2.3.3) vs reviewer's Monge-Kantorovich optimal transport suggestion for deriving λ_KLS ≈ 11.7. **Finding**: Bakry-Émery formula is mathematically fabricated (2.35/10) — λ_KLS = λ₀·dim/(dim+2λ₀) appears in no published literature, the correct SL(6,ℂ)/SU(6) spectral gap is λ₁ = 35 not 35/3, and applying convex-body KLS to symmetric-space Laplacian is a category error. Monge-Kantorovich is rigorous (6.40/10) but can only give asymptotic bounds, not the precise numerical value. **Recommendation**: Acknowledge λ_KLS as phenomenological parameter, remove fabricated derivation, adopt optimal transport for qualitative support. Full evaluation in `proof-paper-cross-ref-revision/references/kls-method-comparison-v4pro.md`.

### Reviewer-Proposal Incremental Review (2026-07-17, ninth verified run)

When a reviewer MD proposes math upgrades to specific sections, do NOT run the full 5-agent
review. Use the targeted 3-specialist protocol: extract current section FIRST (proposal may
duplicate existing text), inject prior verdicts + known P0 issues as adversarial context,
check MathCode INDEX for formalization infrastructure (0 hits = honest-axiom-only chain),
deliver verdict MD to paper directory. Detected in run 9: fabrication resurrection under a
new theorem name, stale Lean stats (V50 numbers quoted against V52 file), 80% duplication
masquerading as increment. Full protocol: `references/reviewer-proposal-incremental-review.md`.

### Incremental-Value Review of Reviewer-Proposed Content (2026-07-17)

Ninth verified run — evaluating whether a reviewer MD improves specific paper sections (V52 §2.3.1–2.3.3) and whether it upgrades a postulate to a theorem. Pattern additions:

1. **Score TWO axes, not one**: correctness AND increment-vs-current-text. Reviewer content can be simultaneously correct and worthless — MD stages duplicating existing V52 text scored 8.5/10 correctness but 1.5/10 increment. Extract the CURRENT paper section (python-docx paragraph slice between heading anchors) and feed it alongside the reviewer MD so agents can diff.
2. **Adversarial context injection**: prepend all prior verdicts (fabrication rulings, P0 lists, actual Lean stats) to every agent prompt. This makes agents cross-check instead of re-litigating, and catches "new packaging of a judged-fabricated formula" (the λ₀/d equipartition claim was caught precisely because the prior λ₀·dim/(dim+2λ₀) ruling was in context).
3. **Specialists by claim domain** (3 agents mapped to the MD's claim clusters) beats 5 generic reviewers for single-section evaluation; embed known counterexamples in the targeted questions (e.g. Bobkov 2003 projection monotonicity, Gaussian marginal counterexample).
4. **Watch for stale statistics in reviewer MDs**: the 20260717 MD cited Lean stats from two versions back (54/82 axioms vs actual V52 9 axioms). Always verify reviewer-quoted file stats against current files before accepting their framing.
5. **Author self-flagged caveats go into the adversarial context** ("已知作者自警" item) — a subsequent 5-agent review then independently confirms or dismisses them, giving the caveat a verdict instead of leaving it hanging (the ρ∈F flag was confirmed fatal by 2/5 agents).

### Pitfall 8: Paper Extraction Overwrite — Wrong File Fed to Reviewers (2026-07-22)

When extracting DOCX text for hybrid review, loop-based file matching can silently
overwrite the full paper with a section-only fragment. **Symptom**: all 5 reviewers
report "missing chapters" despite the full paper existing. **Detection**: compare
`wc -c /tmp/paper.txt` against expected DOCX size. **Fix**: use exact filename
matching, not pattern-based loops. Full protocol: `references/hybrid-review-extraction-overwrite.md`.

### Pitfall: Interrupted delegate_task May Have Completed (Pitfall 6, 2026-07-15)

### Pitfall 7: Bibliography-Auditor 优化 (2026-07-16)

✅ **已解决**：四方案对比（Baseline / Few-shot / Manual / Two-stage），**Few-shot（3个真实审计案例注入）胜出**——零 JSON 破损，真实论文命中 21 条（Baseline 为 0）。SkillOpt ReflACT 不适用于结构化 JSON 输出场景（5 epoch 净改善 0）。详见 `references/bibliography-auditor-optimization.md`。

### Pitfall 9: DOCX Rebuild Corruption — Paper Text Silently Degraded (2026-07-25)

When a DOCX is rebuilt via raw XML manipulation (e.g., `str.replace()` on `word/document.xml`), the resulting file may pass ZIP integrity checks AND open in Word but contain drastically reduced text. **Symptom**: extracted paper text returns 494 chars from a file that should have 47,000+ chars. **Root cause**: XML-level modifications can corrupt OOXML structure in ways `zipfile.testzip()` doesn't catch — ZIP valid, XML semantics destroyed.

**Mandatory pre-deployment check:**
```python
paper_text = extract_docx(path)
assert len(paper_text) > 5000, f"DOCX may be corrupted: only {len(paper_text)} chars"
```

**Prevention**: Prefer python-docx paragraph-level edits over raw XML manipulation.

### Pitfall 8: DOCX Extraction Loop Overwrites Paper File (2026-07-22)

When a script loops over multiple DOCX files matching a version pattern and writes ALL to the SAME output path (`/tmp/v55_paper.txt`), the LAST (shorter) file overwrites the full paper. **Symptom**: Reviewers report "paper only contains §2.2 fragment". **Fix**: Break after FIRST match of the main paper pattern, or use unique output names per file. Verify output size > 100KB before deploying review.

When extracting DOCX text for hybrid review, loop-based file matching can silently
overwrite the full paper with a section-only fragment. **Symptom**: all 5 reviewers
report "missing chapters" despite the full paper existing. **Detection**: compare
`wc -c /tmp/paper.txt` against expected DOCX size. **Fix**: use exact filename
matching, not pattern-based loops. Full protocol: `references/hybrid-review-extraction-overwrite.md`.

### Pitfall: Interrupted delegate_task May Have Completed (Pitfall 6, 2026-07-15)

When `delegate_task` is interrupted by a session boundary or timeout (status='interrupted'), the subagent may have actually completed all file modifications before being killed. The `tool_trace` at the end of the result is the key signal — count the actual tool calls executed. If you see `write_file` or `terminal` commands with file paths in the trace, CHECK those files before re-running. A re-run will find "0 citations inserted" because the work was already done.

**Detection pattern**: `status: "interrupted"` + tool_trace shows many completed operations + verification finds the expected state.

**Fix**: Always run a verification pass after an interrupted delegate_task before deciding to re-run. The verification will either confirm completion or show exactly what's missing, allowing a targeted fix instead of a full redo.

### Pattern: Adversarial-Context Injection (2026-07-17, verified runs 9-10)

When reviewing material that has REVIEW HISTORY (prior verdicts, fabrication rulings, known
P0 lists, author self-warnings), prepend an 【对抗性历史上下文】 block to every reviewer
prompt and instruct "评审时必须逐条对照". Include: (a) prior fabrication/REJECT rulings with
scores, (b) unresolved P0 lists, (c) known counterexamples (e.g. Bobkov 2003 projection),
(d) scoring baselines from sibling routes ("Ratner=1.5, DH=4.0 — score relative to these"),
(e) the author's own pre-flagged caveats as explicit audit questions. Effects observed:
reviewers directly cross-referenced history, detected "new packaging of previously-judged
fabrication", confirmed the pre-flagged ρ∈F caveat as fatal, and produced calibrated
relative scores instead of free-floating ones.

### Pattern: Incremental-Value Review of a Reviewer MD (run 9, 2026-07-17)

When the user asks "does this reviewer MD improve section X?", do NOT review the MD in
isolation — extract the CURRENT manuscript section text first (python-docx, locate heading
boundaries e.g. 2.3.1→2.3.4) and feed BOTH to each reviewer with the explicit question
"what does the MD add that the manuscript does not already contain?" Frequent outcome:
the MD largely duplicates existing text (V52 case: stages 1-3 scored 1.5/10 incremental
despite 8.5/10 correctness) — correctness and increment are separate axes; score both.
Also check MD factual staleness against current artifacts (the 20260717 MD cited V50-era
Lean stats 54/82 vs actual V52 9 axioms).

### Pattern: Adversarial-Context Injection Review (2026-07-17, verified ×2)

When reviewing a NEW derivation/reviewer-proposal in a domain with prior review history, inject an explicit 【对抗性历史上下文】 block into every reviewer prompt containing:
1. Prior verdicts with scores (e.g. "旧公式 λ₀·dim/(dim+2λ₀) 被判捏造 2.35/10")
2. Known fatal issues from earlier rounds (P0 lists) the new material must be checked against
3. **Score baselines**: "Ratner路线1.5/10, DH路线4/10 — 若优于两者需给出高于4的分数并论证"
4. **Author self-flagged caveats** as mandatory audit items ("已知作者自警(须重点审查): ...")

Effects observed: reviewers calibrate scores against the baselines instead of drifting; pre-flagged caveats get explicitly adjudicated (the ρ∈F caveat was confirmed fatal by both EIC and R1); "new packaging of an old fabrication" gets caught (R2: "均分定理新版不应高于旧版1.8/10"). Without the context block, reviewers routinely miss that a proposal recycles a previously-rejected argument under new terminology.

Cost profile: 3-5 agents × deepseek-chat temp=0.0 max_tokens=8192 ≈ 30-65s each, sequential OK for ≤5 agents (total <5 min). Save each reviewer to `/tmp/<tag>_<name>.part` immediately.

### Pattern: v4-pro Single-Section Evaluation

When a reviewer challenges a specific mathematical derivation:
1. Extract the challenged section from paper DOCX → plain text
2. Extract the reviewer's suggested alternative from MD → plain text
3. Run brain recall for bridging concepts
4. Use `deepseek-chat` (NOT v4-pro — timing issues) with `max_tokens=16384, temperature=0.0`
5. Structure prompt with 5 weighted criteria (self-consistency 25%, framework alignment 25%, rigor 20%, heuristic 15%, acceptability 15%)
6. Output scored table + detailed analysis + actionable recommendation

### V51 Neutrino Condensation Paper — Full Hybrid Review + P0 Fix Pipeline (2026-07-15)

Eighth verified run — V51 paper, 155K chars, 474 paragraphs. 5 agents in 2 batches. Scores: Consistency 3/10, Logic 4/10, Technical 3/10, Writing 6.5/10, Bibliography 2/10. Overall **3.7/10 — REJECT**.

6 P0 showstoppers:
1. Lean proof stats completely fabricated (claimed 85/15/33 → actual 17/9/7)
2. Predictive degree self-contradiction (−1 in abstract, −2 in body)
3. λ_KLS = 35/3 uses unexplained factor of 3 (|ρ|²=35 derived, but 35/3 used)
4. 7 ghost citations [58]-[64] + fabricated ref [17] + commentary as [14]
5. |ρ|² normalization split: body=35, Appendix F=35/2
6. κ calibration circularity (claimed "m_τ" but actually calibrates to m_₃)

**Post-review fix pipeline**: All 6 P0 + P1-1 fixed in single session via 3-phase pipeline:
- Phase 1: Mechanical XML text replacements (59-66 changes/file across 4 DOCX)
- Phase 2a: Structural insertion (λ_KLS honest-scope disclosure paragraph in §2.3.3)
- Phase 2b: Bibliography rebuild (8 new refs [42]-[49], 3 removals, 1 journal fix)
- Phase 3: Python cross-audit verifying all fixes consistent across 4 DOCX + 1 Lean

Key lesson: **NTFS DOCX write corruption** — writing ZIP files directly to `/mnt/c/...` produces `BadZipFile`. Always write to `/tmp/` first, then copy back. See `proof-paper-cross-ref-revision/references/v51-p0-rapid-fix-pipeline.md`.

### V50 Neutrino Condensation Paper (2026-07-13)

Fifth verified run — V50 paper, 160K chars. 5 agents + Lean specialist. 3.6/10 — REJECT. Top findings: λ_KLS formula self-created, KO⁻³⁵(pt)=0, tautological verification, 17 :=True stubs. Full: `references/v50-neutrino-review-20260713.md`.

### V20a Neutrino Condensation Paper (2026-07-05)

## Pitfalls

### Pitfall 12: Version-Scope Discipline — Review the Requested Version, Not Its Transition (P0, 2026-08-06)

When the user says "review V14", review V14 **as-is**. Do NOT:
- Compare V14 against V15 fixes or analyze whether V15 changes landed
- Critique the V14→V15 transition pipeline
- Spend paragraphs proving that "V15 fixes weren't applied"

If the file has a V15 header but is named V14, just note the naming oddity in one sentence and move on. The user wants a review of the **content**, not a meta-analysis of the version history. The correction signal is clear: "没有让审阅V15啊" — the user named the version they want. Stick to it.

### Pitfall 13: Check Version Staleness Before Offering Fixes (P0, 2026-08-06)

When the user mentions a version number but the pipeline has already progressed further (e.g., "V14" when V16 exists), do NOT offer to fix the old version. Check what the latest version is in the directory first. Signal: "嗯不需要了，现在都V16版本了".

### 1. DeepSeek JSON Unparseable — detailed_comments with Embedded Quotes (P0)

When `detailed_comments` contains quoted phrases (e.g., `the "derived" value`), the generated JSON is unparseable by `json.loads()`. Two of six reviewers in the V56 session produced valid JSON that failed parsing. **Recovery**: Use regex field extraction (`re.search(r'"score":\s*([\d.]+)', text)`) instead of `json.loads()`. **Prevention**: Add to prompt: "Escape ALL double-quotes in detailed_comments as backslash-escaped."

### 2. Python .format() Brace Conflict with Paper Text (P0)

When paper text contains LaTeX math with curly braces (`\mathbb{C}`, `\{X\}`), using `str.format()` to inject paper text into a prompt template breaks with `KeyError`. **Fix**: Use `str.replace("__TOKEN__", value)` instead of `.format()`. Never use `.format()` with untrusted paper text.

### Pitfall 12: Version-Scope Discipline — Review the Requested Version, Not Its Transition (P0, 2026-08-06)

When the user says "review V14", review V14 **as-is**. Do NOT:
- Compare V14 against V15 fixes or analyze whether V15 changes landed
- Critique the V14→V15 transition pipeline
- Spend paragraphs proving that "V15 fixes weren't applied"

If the file has a V15 header but is named V14, just note the naming oddity in one sentence and move on. The user wants a review of the **content**, not a meta-analysis of the version history. The correction signal is clear: "没有让审阅V15啊" — the user named the version they want. Stick to it.

### Pitfall 13: Check Version Staleness Before Offering Fixes (P0, 2026-08-06)

When the user mentions a version number but the pipeline has already progressed further (e.g., "V14" when V16 exists), do NOT offer to fix the old version. Check what the latest version is in the directory first. Signal: "嗯不需要了，现在都V16版本了".

### 1. DeepSeek JSON Unparseable — detailed_comments with Embedded Quotes (P0)

When `detailed_comments` contains quoted phrases (e.g., `the "derived" value`), the generated JSON is unparseable by `json.loads()`. Two of six reviewers in the V56 session produced valid JSON that failed parsing. **Recovery**: Use regex field extraction (`re.search(r'"score":\s*([\d.]+)', text)`) instead of `json.loads()`. **Prevention**: Add to prompt: "Escape ALL double-quotes in detailed_comments as backslash-escaped."

### 2. Python .format() Brace Conflict with Paper Text (P0)

When paper text or Lean stats contain curly braces (LaTeX math like `\mathbb{C}`, JSON templates in the prompt), using `str.format()` to inject content fails with `KeyError`. Observed twice in V56 review script builds. **Fix**: Use `str.replace("__TOKEN__", value)` instead of `.format()`. Never use `.format()` with untrusted paper text or Lean code.

### Pitfall 19: "P0 Fix Header Notes" — AI Rewrites Add Disclaimers Instead of Changing Text (2026-08-11)

When DeepSeek rewrites a paper to apply fixes, it often appends banner notes (e.g., `[V9.1 P0 FIXES: ...]`) to headers and adds inline notes like `N_e = 161 is a calibration result` but LEAVES the original overclaim text unchanged in the body. The result: a paper that simultaneously says "prediction" in 5 locations and "calibration" in 1 banner note. The CGICE R2 review found 8/8 "fixes" from R1 were only partially applied — banner notes existed but body text was untouched.

**Detection**: After every rewrite pass, grep for the OLD text patterns. If `grep -c "within an order of magnitude"` > 0 after the fix was supposed to remove it, the rewrite failed. DO NOT trust the banner notes.

**Key signal**: A paper header containing `[V9.1 P0 FIXES 2026-08-11]` with a list of claimed fixes is a RED FLAG — it means the AI writer appended a fix manifest rather than fixing the actual text. Fix manifests in headers should be treated as TODO lists, not as evidence of completion.

**Fix approach**: In the rewrite prompt, explicitly say "Do NOT add header notes or banner disclaimers. Change the ACTUAL body text. The fix must survive a grep for the old text returning zero."

v4-pro single-API-call audits consistently score papers 2-5 points HIGHER than 5-agent adversarial panels. CGICE V9 case: v4-pro scored 9/10; 5-agent panel found 4.7/10 with 8 P0 issues (phantom predictions, Lean algebra bug, Λ_CC contradiction, RG arithmetic error). The single audit missed all of these.

**Root cause**: v4-pro reads linearly and trusts framing. Multi-agent panels with adversarial context + specialized roles (consistency/logic/math/writing/bibliography) produce cross-verification that catches inconsistencies no single reader would.

**Rule**: v4-pro single = DIRECTIONAL CHECK only. Always follow with ≥3-agent panel for gate decision.

**Detection signal**: If v4-pro gives ≥8/10 but no "CRITICAL" findings → re-audit with multi-agent panel.

### Pitfall 14: v4-pro 全尺寸挂死 + v4-flash Content 空 (2026-08-07)

v4-pro 对 5.5K chars 的 prompt 也会挂死——0% CPU、6+ 分钟无响应。旧假设"仅 >120K 挂死"不成立。**v4-pro 对所有审查任务不可靠**。

**替代**: 深度推理用 v4-flash thinking。但可能 token 耗尽致 `content=""`(71K reasoning/0 content)。从 `reasoning_content` 提取结论回退。

**决策树**: 短 prompt→v4-flash thinking | 中长→v4-flash+thinking=disabled | 任何长度+v4-pro→❌

DeepSeek v4-pro has a sharp reliability cliff around prompt size:

| Zone | Prompt Size | Behavior | Recommendation |
|------|------------|----------|----------------|
| **Safe** | <50K chars | Reliable, ~160s, deep math reasoning | ✅ Use for cross-paper reviews |
| **Risky** | 50-100K chars | May hang intermittently | ⚠️ Test first, have v4-flash fallback |
| **Unsafe** | >120K chars | Silently hangs (no error, no timeout) | ❌ Use v4-flash instead |

**Symptoms of hang**: Zero stdout for >300s, process killed with exit code 143, report file not created.

**When user explicitly requests v4-pro**: Limit prompt to <50K chars by extracting only key sections (abstract + core derivations + conclusions + Lean stats + numerical claims). Do NOT include full paper text. For papers >100K chars, use the extraction pattern in `references/v4pro-multi-paper-cross-review.md`.

### 2. Process Kill Before File Write — Incremental Save

When running 5-agent review via `terminal(background=true, timeout=600)`, the timeout may kill the process AFTER all API calls complete but BEFORE the final `open().write()` saves the compiled report. All review text is lost.

**Fix**: Write each reviewer's output to a separate `.part` file IMMEDIATELY:

```python
with open(f'/tmp/review_{name}.part', 'w') as f:
    f.write(content)
```

Final compilation reads `.part` files — idempotent and recoverable even if killed mid-compile.

### 4. Lean Stats Regex Trap (V50, 2026-07-13)

When counting `axiom`, `theorem`, `sorry` in Lean files for review purposes, simple regex/grep matches comments and header strings. Example: `grep -c 'sorry' proof.lean` returned 9, but all 9 were in header comments saying "0 sorry". The actual active sorry count was 0. Similarly, `grep -c 'axiom'` returned 237 when the real count was 80.

**Fix**: Always filter out comment lines: `grep -v '^--' file.lean | grep -v '/-' | grep -c 'sorry'`. Or use Python with regex that excludes lines starting with `--`.

### 5. :=True Stub Disclosure (V50, 2026-07-13)

In Lean, `:= True` is syntactically distinct from `sorry` — it typechecks as a complete proof. But for verification purposes, it's equivalent to a hidden sorry (empty proof body). Papers that claim "zero sorry" must also disclose the `:= True` stub count. V50 had 17 stubs undisclosed.

When running hybrid review via `execute_code`, the 300s hard timeout is insufficient for 5 sequential API calls. Always use `terminal(background=true, notify_on_complete=true)` with timeout≥600s, or split into separate foreground calls.
