# Venue-fit 5-agent final review (SL(6,C) Lean-formalized physics papers)

When a physics paper carries a companion Lean formalization (0 axiom / 0 sorry / 0 admit,
compiled EXIT=0), the standard FINAL review is a **venue-fit 5-agent panel** — NOT the
AWA writing/bibliography config. This is distinct from `academic-paper-reviewer`'s
EIC+3-reviewers+Devil's-Advocate panel; both are valid but venue-fit is the established
pattern for this user's CGICE / three-spacetime-phase / triple-GW / neutrino corpus.

## Agent config (venue-fit, non-AWA)

1. **consistency** — 计数 / 命名空间清单完整性 / 编译状态声明前后一致 / 数值常量跨节漂移 / 公式编号悬空 / 定理名对齐（改名残留检测）
2. **technical** — 数学推导正确性、硬算术错误（因子 2、比例方向写反、谱定理伪装观测输入、量纲不匹配）
3. **logic** — 条件模型定位 [F]/[A]/[O]/[M] 标签、循环论证检测、摘要防火墙（摘要声称 vs 正文）、诚实标注是否传导到 Lean 层
4. **lean_specialist** — 形式化实质质量、定义重言式陷阱（V64 教训：`unfold` 后只剩 `rw [定义]+linarith`）、实质定理分层占比估计、覆盖 vs 声称一致性
5. **publication_strategist** — JCAP / PRD / CQG 适配性 + READY / MAJOR REVISION / NOT READY + 推荐投稿顺序 + 修改路线图

## Execution parameters (deepseek-flash)

- `model="deepseek-flash"`, `temperature=0.0`, `extra_body={"thinking":{"type":"disabled"}}`
- **`max_tokens=16384`** — NOT 8192. 8192 truncates the technical reviewer, dropping its
  score and conclusion. (deepseek-v4-pro hangs on large prompts; only use flash for full-text review.)
- `timeout=900`; 全文 ~200K chars 可整篇喂入（deepseek-flash 128K context 可容纳）
- 5 个 agent 用 terminal `background=true` + `notify_on_complete=true` 并行跑，各写
  `/tmp/<review>/<agent>.md`；~40s 完成（thinking disabled 快模式）

## Three injected blocks (essential — each review must rebuild them)

1. **LEAN_GROUND_TRUTH** — machine-level stats, grep-computed on comment-stripped source
   (`re.sub(r'/-.*?-/', '', lean, flags=re.S)` then strip `--`). Count theorem/lemma/def/
   abbrev/structure/namespace (dedupe namespaces!) + 0 axiom/sorry/admit + compile EXIT=0.
   **Recompute fresh every review** — a prior session held "303 thm" while the actual source
   had already grown to 382/329. Stale counts poison the consistency agent's whole report.
2. **PRIOR_REVIEW_HISTORY** — the previous round's待修改清单, injected so each agent outputs
   a `vN_issues` fixed/remain/partial table. This is how the review closes the loop across rounds.
3. **已核验误判清单** — explicitly tell the technical agent "these prior factor-claims were
   human-verified as misjudgments, do NOT repeat them" (see reviewer-factor-dimension-recalc-false-positives.md).

## Compiled-status unification (recurring pre-review sweep)

These papers often carry a stale "not compiled / has not been compiled / source only /
not a successful build" wording left over from a "no compilation requested" review task,
even though the Lean source actually compiled EXIT=0 afterward. Before (or during) review,
sweep the paper for every such phrasing and unify to
`compiled with 0 error / 0 sorry / 0 admit / 0 axiom`. Also check reference-list entries —
a stale "the edited R9 file has not been compiled" can hide inside a bibliography item.
Honest exception: keep `#print axioms` as "not separately claimed" unless it was actually run.

## Cross-agent agreement signal (distinguish real issues from false positives)

When **two agents independently flag the same factor/dimension discrepancy** (e.g. logic P0-3
and technical P2-6 both pointing at "§7.4 factor 2 vs §7.8.1 1/12 oscillation average"), that
is NOT the single-agent false-positive pattern — it is a **signal to human-verify by
re-deriving the source-term chain**. Single-agent factor claims are usually convention
misreads; cross-agent agreement on one spot is usually worth a real look.

## Aggregation

- Per-agent score (X.X/10) + P0/P1/P2/P3 tiered issues + vN_issues table.
- Separate **实质层** (needs author re-derivation or Lean evidence) from **表述层**
  (wording/inline qualifiers) — do NOT dock points for honest labels ("not a spectral
  theorem", "different models, not simultaneous assumptions", "not an exact UV-complete EFT").
- Final: a score table, a "无阻断级 P0" determination, and a journal recommendation
  (this user's corpus usually lands on "JCAP MAJOR REVISION, close to READY; complete
  A-group mechanical fixes + B-group P0 fixes then submit").
