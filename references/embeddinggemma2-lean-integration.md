# EmbeddingGemma-2-Lean 接入 Hybrid-review（方案 A 落地 + 方案 B 迁移验证）

> 日期：2026-10-20
> 状态：方案 A 已落地；方案 B 已验证通过（迁移效果良好）

---

## 一、背景与定位

`embeddinggemma2-lean`（flyyinghui/embeddinggemma-2-lean）是**全精度**（bf16/fp32）transformers 版
EmbeddingGemma-2，在 openai_math 的 37.7 万对 Lean 依赖上微调，768 维。

Hybrid-review v1.5.0 原本集成的 `litert-community/embeddinggemma-2-740m-litert-lm`
是 **int4 QAT 量化版**（LiteRT-LM 格式），区分度窄带（学术文本相似度挤在 0.68–0.80）。

**核心价值**：把 cross_paper_semantic.py 的语义后端从 int4 窄带升级为全精度，
并对用户 SL(6,C) 系列论文的 Lean 声明库提供语义一致性核对能力。

---

## 二、方案 A（已落地）：cross_paper_semantic 后端升级

### 改动清单

| 文件 | 位置 | 作用 |
|---|---|---|
| `lean_encode_cli.py` | `<EMBEDDINGGEMMA_LEAN_DIR>/` | 独立 venv 跑，stdin JSON → stdout JSON，加载全精度模型编码 |
| `embeddinggemma_lean.py` | `ars-awa-hybrid-review/scripts/` | subprocess 封装，接口对齐 `embeddinggemma.py`（embed/cosine/semantic_match） |
| `cross_paper_semantic.py` | `ars-awa-hybrid-review/scripts/` | `_import_embeddinggemma()` 改为优先 lean 后端、降级 int4 后端 |

### 后端优先级

```
embeddinggemma_lean（全精度 bf16，优先）
  → 降级 embeddinggemma（int4 LiteRT-LM）
  → 都失败 → 返回 available=False（不阻塞审稿）
```

### 关键设计决策

1. **subprocess 架构**：lean 模型需 transformers 5.19 + torch 2.6，而 Hermes 主 venv 的
   torch 2.5.1 较脆弱。故独立 venv 跑 `lean_encode_cli.py`，由 `embeddinggemma_lean.py`
   用 subprocess 调用，**不污染主 venv**。
2. **dtype 自动检测**：`torch.cuda.is_bf16_supported()` → RTX 4000 用 bf16，P620（Pascal 6.1）用 float32。
3. **max_seq_length=1024**：论文主题文本（6000 字符）会被截断，但模型在短文本微调，
   长文本属任务迁移（见诚实边界）。

### 端到端验证（2026-10-20，P620）

- 模型加载 118s（1376 张量），4 条测试文本全部编码出 768 维向量，EXIT=0 ✅

---

## 三、方案 B（已验证）：跨命名空间迁移效果

### 验证方法

对 `cgice_proof_v10.lean`（486 theorem / 9 lemma / 198 def，共 691 声明）：
1. 解析声明库（名字 + kind + signature + body）
2. 提取依赖：每个 theorem/lemma 的 body 里词边界匹配到其他声明名（共 997 依赖）
3. 编码声明（增强文本口径：名字词化 + 签名）
4. 测 recall@k：给定定理名（纯名字口径），召回 top-k，命中真实依赖的比例

### 验证结果

| 指标 | 本验证（CGICE 跨命名空间） | openai_math 同分布基线（纯名字） |
|---|---|---|
| recall@1 | 0.1505 | — |
| recall@3 | 0.2718 | — |
| recall@5 | 0.3240 | — |
| **recall@10** | **0.4112** | 0.4663 |

**结论**：recall@10 = 0.4112，接近同分布水平（-5.5pp）。**跨命名空间迁移效果良好**——
模型在 openai_math 上微调的语义判别力，能有效迁移到用户 CGICE 自制命名空间。

### 落地建议（F3 方法-代码对齐的语义辅助层）

- 用 `parse_lean_declarations.py` 重新解析用户 SL(6,C) 系列 Lean 文件（CGICE / 三大时空相 /
  右手中微子 / 三峰引力波 / 光速分界面）→ 建自定义声明库
- 用 embeddinggemma2-lean 编码建索引
- 审稿一致性代理核对「正文定理名 ↔ Lean 定理名」时，做语义召回（top-10），发现
  「名字不同但语义相近」的错位（现有 F3 是字面核对，无法发现这类不一致）
- **不替代**字面核对与 live-search（F2），只做辅助排序

---

## 四、诚实边界

1. **长文本迁移未验证**：模型在短文本（~45 token）微调，方案 A 的论文主题相似度用
   max_seq_length=1024，长文本语义质量未单独验证（recall 验证用的是短声明口径）。
2. **docstring 缺失**：用户 Lean 文件基本无 `/-- ... -/` docstring，增强文本只有
   「名字词化 + 签名」，比训练口径少 docstring 成分，可能小幅影响召回。
3. **单文件验证**：方案 B 只验了 cgice_proof_v10.lean，其余四篇论文的 Lean 文件未逐一测
   （预计同构，recall 应同量级，但未证）。
4. **不替代 F2 live-search**：embedding 只能语义排序，不能证伪幻觉引用。

---

## 五、复现命令

```bash
# 方案 A 验证（独立 venv 加载 + 编码）
cd <EMBEDDINGGEMMA_LEAN_DIR>
echo '{"texts":["...","..."],"normalize":true,"max_seq_length":128}' \
  | ./venv/bin/python lean_encode_cli.py

# 方案 B 跨命名空间验证
./venv/bin/python verify_cross_namespace.py "~/Desktop/papers/cgice/cgice_proof_v10.lean"

# cross_paper_semantic（自动优先 lean 后端）
/usr/local/lib/hermes-agent-v14/venv/bin/python \
  ars-awa-hybrid-review/scripts/cross_paper_semantic.py --papers a.md b.md
```
