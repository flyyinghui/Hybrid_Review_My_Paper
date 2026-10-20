# Re-review score-drop + the "conditional effective model vs parameter-free prediction" line

## The pattern that makes re-review scores DROP (not rise)

Three rounds of the same paper (LightSpeed_Phase_Boundary) showed scores go 5.5 → 4.7 → 3.9 while
the author was actively fixing P0/P1s. Two causes, both reusable:

1. **Cosmetic relabeling reads as regression.** Fixes that only reword ("fixed by" → "consistent
   with", "full formal parity" → "formal parity on finite-algebra fragments") get judged as
   relabeling, not substantive repair. The reviewer's literalism disposition then re-derives and
   finds the SAME structural overclaim under the new verb.

2. **The repositioning itself introduces new P0s.** When you change the paper's framing (e.g. add a
   new "derived dynamics" module and retitle the paper), the new text is NOT reconciled with the
   stale boilerplate already in the file (old "not compiled" claims, old section cross-refs, old
   count sentences). The re-review flags these as fresh P0s. See
   `proof-paper-cross-ref-revision/references/repositioning-compilation-sweep.md`.

## The core judgment line reviewers apply (physics/foundations papers)

The single most load-bearing question in rounds 7–9 was:

> Is the new "derived coefficient" a **computed number the author did NOT put in by hand**, or is it
> a **conditional combination of still-specified inputs**?

Concrete case: the O1 module derived the factor **6** (from the A5 root sum `Σ(xᵢ−xⱼ)² = 6|x|²`),
but the "derived rate" was `6·m·κ` where mobility `m` and stiffness `κ` were still free `[M]`
inputs. Five agents independently landed on the same verdict: **"6 is derived; 6mκ is 6 × two free
inputs — a real but *conditional* work package, PARTIAL closure of 'no dynamics work package'."**

Lesson to encode in the PAPER (not just the review): when the headline is a derived coefficient,
state up front in the abstract *what is derived vs what remains input*. The honest formulation that
survived review: "the factor six in a_E/(mκ) is the computed root-frame coefficient; the absolute
physical rate remains dependent on mκ and on a map to proper time." Buried in §V.P.5, it cost a P1;
in the abstract it would have closed it.

Net-predictive-content language that worked: "≈0" → "+1 conditional on scale fixing (mκ=35/6)";
never claim "parameter-free prediction" when inputs remain.

## write_file JSON quote-escaping trap — Chinese-text variant

The existing `references/five-agent-venue-fit-review-script.md` documents the `\"` trap for English
quotes. It ALSO fires on Chinese-text ASCII double quotes inside Python dict strings, e.g.
`"区分"导出"与"匹配""` — the inner `"导出"` uses ASCII `"`, which terminates the Python string and
yields `SyntaxError: invalid decimal literal` / `forgot a comma`. Fix: use corner brackets 「」
(`区分「导出」与「匹配」`) instead of ASCII quotes for inner emphasis, then re-parse with
`ast.parse` to catch any remaining occurrence before launching the parallel agents.
