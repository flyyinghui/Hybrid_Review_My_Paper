# ars-awa-hybrid-review v1.7.0 — 部署说明

> Hybrid-review-my-paper 技能：ARS（10 阶段工作流）+ AWA（多专家并行审稿）混合论文审稿管线，
> 5-agent 并行审稿（consistency / logic / technical / writing / bibliography）+ F1/F2/F3 审计。

## 依赖的模型权重（**不在本包内**，需从 HuggingFace 下载）

### embeddinggemma2-lean（语义后端，优先）

| 项 | 值 |
|---|---|
| HF 仓库 | `flyyinghui/embeddinggemma-2-lean`（public，Apache 2.0） |
| 大小 | ~1.49 GB（740M 参数，bf16） |
| 用途 | 多论文交叉审稿语义相似度 + Lean 语义一致性核对（F3 辅助层） |

下载（国内镜像）：

```bash
export HF_ENDPOINT=https://hf-mirror.com
pip install -U "huggingface_hub[cli]"
huggingface-cli download flyyinghui/embeddinggemma-2-lean --local-dir <model_dir>/embeddinggemma-2-lean
```

依赖（独立 venv，避免污染主 venv 的 torch）：

```bash
python3.12 -m venv <venv>
<venv>/bin/pip install "sentence-transformers>=6.1" "transformers>=5.19" "torch>=2.6"
```

### embeddinggemma-2（int4 LiteRT-LM 版，降级后端，可选）

| 项 | 值 |
|---|---|
| HF 仓库 | `litert-community/embeddinggemma-2-740m-litert-lm` |
| 用途 | cross_paper_semantic.py 的后端降级（当 lean 版不可用时） |

## 环境变量配置

```bash
export EMBEDDINGGEMMA_LEAN_DIR=<model_dir>/embeddinggemma-2-lean     # 权重目录
export EMBEDDINGGEMMA_LEAN_VENV=<venv>/bin/python                     # 独立 venv python
export EMBEDDINGGEMMA_LEAN_CLI=<本包>/scripts/lean_encode_cli.py     # 编码 CLI
export EMBEDDINGGEMMA_MODEL_DIR=<dir>/embeddinggemma-2-740m          # int4 降级后端目录（可选）
```

## 验证

```bash
# 1. 语义后端自检
python scripts/embeddinggemma_lean.py   # 打印 available=True

# 2. 跨命名空间召回验证（可选）
<venv>/bin/python scripts/verify_cross_namespace.py <your_lean_file.lean>

# 3. 多论文相似度矩阵
python scripts/cross_paper_semantic.py --papers a.md b.md c.md
```

## 审稿模型

5 个审稿代理默认用 `deepseek-flash`（`extra_body={"thinking":{"type":"disabled"}}`），
API key 从 `~/.hermes/.env` 读取 `DEEPSEEK_API_KEY`。
