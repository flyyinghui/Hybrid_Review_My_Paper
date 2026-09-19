# Version-Commentary Strip + PRD Reconstruction (Pre-Review Cleanup)

## When to use

The user has an iterated physics paper (V15/V16/V17…) whose manuscript has accumulated
version-fix commentary — `[V17 FIX]`, `[WITHDRAWN]`, `[2026-08-16]` date stamps,
`[C-2]`/`[CROSS-PAPER]` cross-refs, `[honest-axiom]` notes, inline `**[P0-2/3/4 深度形式化证明]**`
blocks, and Chinese fix-explanation prose inside English text. They ask to "删除修正过去
错误版本内容的论述" → "按 PRD 体例重构" → "优化文字" → then run hybrid review.

Verified on 三峰引力波 V17→V18 (84 KB → 30.7 KB, −64%).

## Step 1 — Backup first

`cp paper.md paper.md.bak_pre_prd_refactor_$(date +%Y%m%d_%H%M%S)` — never edit in place.

## Step 2 — Strip these categories (DELETE entirely, not "convert")

| Category | Example |
|---|---|
| Version-number tags | `[V16]`, `[V17]`, `V15 P0-4 FIX` |
| Date stamps | `2026-08-16`, `2026-09-02` |
| Withdrawal banners | `[Target T2 WITHDRAWN…]`, `撤回「DM=GW」…` |
| Cross-paper refs | `[C-2]`, `[CROSS-PAPER C-2]`, `[FRAMEWORK ALIGNMENT]` |
| Review-audit notes | `[CIRCULAR-REASONING AUDIT 2026-08-07]` |
| Proof-methodology blocks | `**[P0-2/3/4 深度形式化证明]** … Lean 编译 0 sorry` |
| Chinese fix-prose in English body | `[V17 P0-1 FIX: 此 10⁻²/10⁻¹⁴ 层级标度是 V16 旧值…]` |

Also delete **redundant duplicate honest declarations** — the same "三峰频率是校准非推导"
caveat repeated 6+ times collapses to ONE clean sentence.

## Step 3 — KEEP, but convert to clean prose (NOT banner notes)

The honest boundary is the paper's *value*, not noise — keep it, but as a **Table I
(derived / calibrated / postulated boundary matrix)** plus natural-language statements:

- Core withdrawal → positive restatement: "DM=GW withdrawn" → "co-produced but not identified; separate continuity equations".
- Normalization clarifications → one sentence: "|ρ|² = 35 under the doubled Killing normalization B=2·Tr; the standard trace form gives 35/2".
- `[honest-axiom]` → plain "postulate"/"assumption" (never keep "honest" as a technical modifier).

## Step 4 — Resolve contradictions the commentary was MASKING

The version commentary frequently hides unresolved self-contradictions. After stripping, grep for:

- "fossilized gravitational wave" vs withdrawn "DM=GW" → unify to co-production.
- Two numeric values for the same quantity (8.6% vs 0.35% BH transmutation) → keep the LATEST only.
- Process meta leaking into physics ("Brain ON model calibrates H₀") → delete.

## Step 5 — Standard PRD skeleton

Title → Abstract (≤250 words, NO pipeline meta like "the formalization establishes…")
→ I. Introduction → II. Framework → III. Results → IV/V. Cosmological/Observational
→ VI. Formal Verification (COMPRESSED — Lean/sorry/namespace jargon moves to appendix)
→ VII. Conclusion → Acknowledgments → Appendix → References.

## Step 6 — Expect these findings when the 5-agent review runs afterward

These recur across the user's papers; pre-fix them in the same pass if time allows:

1. **References is just "see supplementary"** → P0. Build a real list (Planck 2018, Helgason,
   Lichnerowicz, Obata, Harish-Chandra, NANOGrav, LISA…). This is the #1 score-killer (3.5/10).
2. **Boundary Table I self-contradicts** → g_TC² and DM:B=5.00 listed "derived" but actually
   "conditional on Ansatz / DOF-counting" → move to Postulated/Calibrated.
3. **AI-methodology appendix** (neural-memory-brain, LLM pipeline, SNN neuron counts) → REMOVE
   from PRD body/appendix; reviewers consistently flag it as non-physical (0/3 keep it).
4. **Redundant "for completeness" derivations** (e.g. f₀=9.61×10⁴⁴ Hz unused) → delete.
5. **"honest" as technical modifier** throughout → replace with postulate/assumption.
6. **Line-count / number drift** vs Lean ground truth (2389 vs 2390) → always re-verify with
   the comment-stripped Lean audit, not `wc -l`/grep (see lean-stats traps in SKILL.md).

## Execution notes

- The rewrite is a MANUAL authoring pass by the orchestrating agent (not DeepSeek batch
  translate) — the judgment "which commentary is process noise vs which is the honest boundary"
  requires reading the whole argument chain.
- Strip resolves the *history*; the 5-agent review then finds the *remaining* scientific gaps
  (co-production source-term coupling, GW Peak III cosmic-string mechanism vs π₁=0, etc.).
