#!/usr/bin/env python3
"""
lean_encode_cli.py — embeddinggemma2-lean 编码 CLI（用独立 venv 运行）
=====================================================================
用 sentence-transformers 加载「全精度」embeddinggemma-2-lean 模型，
作为 ars-awa-hybrid-review 的 cross_paper_semantic.py 的语义后端。

为什么独立 venv：模型需 transformers 5.19 + torch 2.6，而 Hermes 主
venv 的 torch 2.5.1 较脆弱，故用本机 EmbeddingGemma2 独立 venv 跑，
由 embeddinggemma_lean.py（subprocess 封装）调用，避免污染主 venv。

协议（一次性模式）：
  stdin : {"texts": [...], "normalize": true, "max_seq_length": 512}
  stdout: {"vectors": [[...], ...]}  或  {"error": "..."}

用法（在 EmbeddingGemma2 独立 venv 下）：
  .../venv/bin/python lean_encode_cli.py < req.json
"""

import json
import os
import sys


def _build_model(model_dir: str, max_seq_length: int):
    import torch
    from sentence_transformers import SentenceTransformer

    # 设备与 dtype 自动检测：支持 bf16 的卡（RTX 4000）用 bf16，否则（P620 Pascal）用 float32
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32
    else:
        device = "cpu"
        dtype = torch.float32

    model = SentenceTransformer(
        model_dir, device=device, model_kwargs={"torch_dtype": dtype}
    )
    model.max_seq_length = max_seq_length
    return model


def main():
    try:
        req = json.load(sys.stdin)
    except Exception as e:
        json.dump({"error": f"stdin 解析失败: {e}"}, sys.stdout)
        return 1

    texts = req.get("texts", [])
    if not texts:
        json.dump({"vectors": []}, sys.stdout)
        return 0

    normalize = req.get("normalize", True)
    max_seq_length = req.get("max_seq_length", 512)
    model_dir = req.get("model_dir") or os.environ.get(
        "EMBEDDINGGEMMA_LEAN_DIR",
        "<model_dir>/embeddinggemma-2-lean",  # huggingface-cli download flyyinghui/embeddinggemma-2-lean
    )

    try:
        model = _build_model(model_dir, max_seq_length)
        vecs = model.encode(
            texts,
            normalize_embeddings=normalize,
            batch_size=8,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        json.dump({"vectors": [v.tolist() for v in vecs]}, sys.stdout)
        return 0
    except Exception as e:
        json.dump({"error": f"{type(e).__name__}: {e}"}, sys.stdout)
        return 1


if __name__ == "__main__":
    sys.exit(main())
