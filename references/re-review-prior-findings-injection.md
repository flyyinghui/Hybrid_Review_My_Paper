# Re-review Must Inject Prior Findings（复审必须注入前轮 P0/P1 对照清单）

> 来源：V56 终审教训（2026-07-23）+ V64 两轮终审（2026-09-26）。
> 用户对"复审推翻前次意见"零容忍。

## 核心规则

**任何版本升级后的复审（round 2+），必须：**

1. 加载前版审稿报告
2. 提取全部 P0/P1 缺陷 ID（如 P0-1, P0-2, P1-1 ...）
3. 注入为 prompt 里的【前次评审历史】块
4. 要求评审逐条判断 `FIXED / PARTIALLY FIXED / NOT FIXED`
5. 输出格式强制包含 "Prior-finding resolution table"

## 注入块的格式

```
【前次评审历史 — 上轮 5-agent 终审的 P0/P1 缺陷清单，本轮必须逐条判断 fixed/remain】

上轮 P0（阻断级）：
- P0-1 [R1/R2/R3/R4一致] 瞬子 bound ... 是循环论证 ...
- P0-2 [R2/R4] CP 源 ... 非 derived ...

上轮 P1（重大）：
- P1-1 [R0] c=2 度量尺度 ...
...

请逐条判断上述 P0/P1 在本轮修改后的状态（FIXED / PARTIALLY FIXED / NOT FIXED），
并在 "Prior-finding resolution table" 中列出。
```

## SYSTEM prompt 必须追加的格式要求

```
### Prior-finding resolution table
- | Finding ID | Status (FIXED / PARTIALLY FIXED / NOT FIXED) | Evidence |
```

## 为什么重要

- V56：第一次复审未注入前轮意见 → 用户明确拒绝（"否则就推翻之前审稿意见了"）→ 重跑带对照清单，评分 3.0→3.7。
- V64：注入对照清单后，审稿人自动逐条判断修复状态，评分 5.4→6.5，且能精确指出"PARTIALLY FIXED"的残留层次（如"construct 动词仍暗示推导"）。

## 修复状态判断的常见结果

| 状态 | 含义 | 处理 |
|---|---|---|
| FIXED | 缺陷完全消除 | 无需再动 |
| PARTIALLY FIXED | 主缺陷消除，但残留更深层次（如改了 derived 但标识符名仍 constructed）| 继续挖 |
| NOT FIXED | 未动 | 说明是结构性选择（如 matching dictionary 太大）|

PARTIALLY FIXED 是最有价值的信号——它指向"修复不彻底"的层次（措辞层→标识符层→审计层→摘要层），是下一轮修复的精确靶点。
