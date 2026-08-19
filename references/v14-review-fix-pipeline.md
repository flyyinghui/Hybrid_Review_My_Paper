# Review-to-Fix Rapid Pipeline — V14 Triple GW Case Study

*Captured from the V14 Hybrid Review → V15 Lean+Paper fix session (2026-08-06)*

## Trigger

User says: "根据[Review Report]提出的修改意见，对应修改意见一步一步通过数学推导补充到论文和对应的Lean文件中"

## Pipeline Steps

### Phase 1: Audit the Lean File

1. **Map all missing identifiers**: Run `grep` to find every symbol used in `def`/`theorem`/`lemma` bodies that is never defined. The V14 case had 10 undefined symbols despite claiming "0 sorries."

2. **Detect false theorems**:
   - `rfl` tautologies (`unfold X; rfl` — proves definition equals itself)
   - False arithmetic (`norm_num` claiming `x=y` when `x≠y`)
   - Category errors (named after deep theorems but proved with `nlinarith`)
   - Conflicting definitions (same symbol defined twice with different values)

3. **Count duplicates**: Sections copy-pasted during iterative editing create duplicated definitions that mask underlying inconsistency.

### Phase 2: Fix Lean (Priority Order)

Fix in dependency order — definitions must exist before they are used:

1. **P0-2 first**: Insert all missing definitions in one block before first use
2. **P0-8 second**: Remove conflicting definitions (keep one, delete others)
3. **P0-5 third**: Fix false arithmetic — either correct values or recast as calibration
4. **P0-6 fourth**: Replace false "theorems" with honest-axioms
5. **P0-3 fifth**: Replace `rfl` tautologies with honest-axiom declarations
6. **P0-4 sixth**: Downgrade unsupportable derivation claims
7. **P0-1 last**: Address numerical inconsistencies between paper and Lean

### Phase 3: Generate Paper Fix Checklist

After all Lean fixes are complete, produce a structured checklist mapping each Lean change to the corresponding DOCX modification. Include:
- Old text → New text
- Exact section/paragraph locations
- Table cell updates (for appendix summary tables)

### Phase 4: Cross-Audit

Verify consistency:
- Are all numerical values in the paper matched in Lean?
- Are all theorem/axiom counts in the header correct?
- Does the paper's "honest scope" language match the Lean annotations?

## Key Lessons

1. **Lean "0 sorries" is NOT synonymous with "verified"**: A file with 10 undefined identifiers has `sorry=0` but cannot type-check. The `sorry` keyword count ignores missing definitions.

2. **`norm_num` can't fix arithmetic**: If the underlying values are wrong, `norm_num` won't magically correct them. Always independently verify claimed equalities.

3. **`unfold; rfl` is a smell**: Any theorem body ending in `rfl` that only unfolds a definition is proving `X = X`, not deriving X from deeper principles.

4. **DOF counting must sum exactly**: If a "representation-theoretic derivation" produces DOF totals exceeding the parent representation dimension, it's not a derivation — it's reverse-engineering.

5. **Named theorems need their content**: If a theorem is named after a deep result (Bourgain, Bakry-Émery) but the proof is `nlinarith` from trivial axioms, the theorem name is decorative.
