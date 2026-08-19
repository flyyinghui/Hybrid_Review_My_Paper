# Stage 3 Formal Panel Integration with AWA Hybrid Review

## Deployment Pattern

When running the full AWA hybrid review pipeline (Stages 2a + 3), deploy the 5-person formal peer review panel in two batches due to the 3-agent parallel limit:

**Batch 1** (3 agents parallel):
- EIC (Editor-in-Chief): journal fit, originality, significance, overall assessment, honest scope evaluation
- R1 (Methodology/Formal Verification): axiom system design, Lean proof claims, ℝ-algebraic scope validity
- R2 (Domain Expert): neutrino phenomenology, seesaw mechanism, experimental constraints, flavor hierarchy

**Batch 2** (2 agents parallel):
- R3 (Cross-Disciplinary): geometric-physics bridge evaluation, mathematical depth, broader impact across fields
- DA (Devil's Advocate): core argument challenges, logical gap detection, alternative explanations, strongest counter-arguments

## Editorial Decision Synthesis

After all 5 reports are collected, the synthesizer:

1. **Identifies consensus** (5/5 agree): issues all reviewers independently flagged
2. **Identifies disagreement**: where reviewers diverge (e.g., EIC values originality while R2 finds it insufficient)
3. **Issues editorial decision** with explicit revision requirements

### Decision Matrix

| Scenario | Decision |
|:--|:--|
| 1+ reviewer finds fatal flaws (DA: "FATAL") | Major Revision with explicit bar |
| 2+ reviewers effectively reject but EIC values originality | Major Revision (not Reject) |
| All reviewers recommend Major/Minor Revision | Revision as recommended |
| 4+ reviewers recommend Accept | Accept with minor corrections |

### Explicit Revision Bar Pattern

When issuing a Major Revision against reviewer recommendation, include an explicit N-item bar:

> The following N requirements must ALL be met. Failure on any single item will result in rejection on resubmission.

This gives the author clear, measurable targets and protects the journal from endless revision cycles.

## Proven Execution: V24 Neutrino Condensation Paper (2026-07-06)

- **5 reviewers**, 2 batches
- **Consensus** (5/5): D1 is the sole load-bearing element, honest scope is exemplary, ℝ-algebraic verification is trivial
- **Disagreement**: EIC recommends Major Revision (values originality 8/10 + honesty 9/10), R2 effectively recommends reject (total 3.3/10), DA says FATAL
- **Decision**: Major Revision with 6 explicit requirements (R1-R6)
- **Outcome**: V25→V26 addressed all 6 requirements
