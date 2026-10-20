# embeddinggemma2-lean 对 Hybrid-review 的融合评估

> 日期：2026-10-20。评估既有 `flyyinghui/embeddinggemma-2-lean`（Lean 引理检索微调模型）
> 对 Hybrid-review-my-paper 技能（本 skill）的帮助与融合方案。

## 一、关键前提：本 skill 已有一个「劣化版」embedding 后端

本 skill **v1.5.0 已集成 EmbeddingGemma-2**，但用的是
`litert-community/embeddinggemma-2-740m-litert-lm`——**int4 QAT 量化版**（LiteRT-LM 格式）。
SKILL.md 自述精度限制：「int4 量化区分度有限（学术文本相似度挤在 0.68–0.80 窄带）」。
用途是 `scripts/cross_paper_semantic.py` 的多论文两两语义相似度矩阵（已接入
`scripts/multi_paper_review.py`，EmbeddingGemma 不可用时优雅降级）。

## 二、embeddinggemma2-lean 是什么

- 基座 `google/embeddinggemma-2`（740M 多模态三塔），**全参微调**（非 LoRA），bf16 全精度。
- 微调任务：给定 Lean 定理名，召回其依赖 DAG 中的引理/定义（openai_math 依赖对 377,098 对）。
- recall@10 = 0.5505（增强文本口径：名字词化 + 类型签名 120 + docstring 60），纯名字 0.4663。
- HF repo `flyyinghui/embeddinggemma-2-lean`（public，1.49GB，sentence-transformers 完整格式）。
- 关键实验结论：①必须配增强文本（纯名字掉 0.08）；②勿引入 mined hard negatives（劣化 19%）；
  ③增强文本要紧凑（~45 token，长了单卡 page fault）。

## 三、融合方案（按价值排序）

| 优先级 | 帮助点 | 价值 | 说明 |
|---|---|---|---|
| **P2** | 替换现有 embedding 后端（精度升级） | ✅ 最实在 | `cross_paper_semantic.py` 从 int4 窄带 → 全精度 bf16 |
| **P3** | 新增 Lean 语义一致性核对 | ⚠️ 新能力，需验证 | F3「方法-代码对齐」目前字面核对，可补语义召回 |
| **P4** | F2 引用核查辅助 | ❌ 收益很小 | F2 用 live-search 逐条验证，embedding 只能排序不能证伪 |

### 方案 A（推荐，低风险）：替换 cross_paper_semantic 后端

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("flyyinghui/embeddinggemma-2-lean", device="cuda")
sim = model.encode(papers, normalize_embeddings=True)   # 替换原 LiteRT-LM 后端
```

- 收益：多论文「共享概念/可能矛盾/可能重复」区分度从 0.68–0.80 窄带拉开。
- 成本：需 transformers 5.19 + sentence-transformers 6.1 + torch≥2.6（比 LiteRT-LM 重）；
  740M bf16 ≈ 1.5GB 显存（RTX 4000 无压力，P620 需 float32 加载）。
- **保持原有优雅降级逻辑不变**（EmbeddingGemma 不可用时降级不阻塞）。

### 方案 B（可选）：Lean 语义一致性核对

1. 用 `parse_lean_declarations.py` 解析**用户 SL(6,C) 系列论文的 Lean 文件**（CGICE / 三大时空相 /
   右手中微子 / 三峰引力波）建自定义声明库（**非** openai_math）。
2. embeddinggemma2-lean 编码建索引。
3. 一致性代理核对「正文定理名 ↔ Lean 定理名」时做语义召回，发现名字不同但语义相近的错位。

**关键风险（接入前必验证）**：模型微调数据全来自 openai_math（OAI 命名空间），对用户自制
命名空间（`CGICE.Deepening20261019` 等）迁移效果**未测**。须先跑 20–50 条用户定理名的召回
看命中率，否则这层是负资产。

### 不建议

**替代 F2 的 live-search 引用核查**——F2 价值在「外部真实性验证」（能证伪幻觉引用），
embedding 只能排序、不能证伪，替代即降级。

## 四、一句话结论

embeddinggemma2-lean 对 Hybrid-review 是 **P2–P3 级增强**：核心 = 把现有 int4 劣化 embedding
后端升级为全精度版（方案 A，直接做）；可选 = Lean 语义一致性核对（方案 B，需先验证跨命名
空间迁移）。不改变 5-agent 审稿 + F2/F3 核心机制。
