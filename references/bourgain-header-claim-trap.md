# Bourgain Header-Claims-Fix Trap (P0-6a Pattern)

*Captured from V15→V16 Lean fix session (2026-08-06)*

## Symptom

The Lean file header changelog declares "P0-6 FIX: Removed mathematically false Bourgain 'theorems'", but the actual code body **still contains** the false theorems — `Bourgain_slicing_conservation`, `time_explosion`, and `Bourgain_differential`.

## Detection

```python
# Compare header claims against actual code
header_claims = grepped from the top-of-file comment block
active_code = sub(r'--.*|/-.*?-\/', '', file_content, flags=DOTALL)
for theorem_name in header_claimed_removed:
    if theorem_name in active_code:
        print(f"HEADER LIE: {theorem_name} still present in active code")
```

## Root Cause

The file went through multiple iterative edit rounds:
1. V14 originally contained the false theorems
2. V15 header was updated to claim removal
3. The actual deletion patch was **never applied** — only the header comment was updated

## Fix Protocol

1. **Never trust header changelogs alone** — always grep the active code
2. When "removing" a theorem, verify with: `assert 'theorem_name' not in active_code`
3. When a header claim contradicts code, the code is the ground truth

## V16 Case

The false `Bourgain_slicing_conservation` theorem claimed `A * B ≥ 1` from `A > 0, B > 0`, "proved" with `nlinarith`. This is mathematically false (counterexample: 0.1 × 0.1 = 0.01 < 1). The fix was to replace the entire block with a single `[honest-axiom: physical-analogy]` placeholder.
