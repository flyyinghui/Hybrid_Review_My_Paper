#!/usr/bin/env python3
"""
embeddinggemma_lean.py — embeddinggemma2-lean 封装（全精度 sentence-transformers 后端）
====================================================================================
接口对齐 embeddinggemma.py（LiteRT-LM int4 版）：embed / cosine / semantic_match。
内部通过 subprocess 调用独立 venv 的 lean_encode_cli.py，避免污染 Hermes 主 venv。

模型: flyyinghui/embeddinggemma-2-lean（740M，bf16/fp32，768 维）
  - 全精度 transformers 版（对比 LiteRT-LM int4 版的窄带区分度）
  - 在 37.7 万对 Lean 依赖上微调，数学文本判别力更强

用法（同 embeddinggemma.py）:
  import embeddinggemma_lean as eg
  v = eg.embed("text")                        # -> list[float] (768-dim)
  vs = eg.embed(["a", "b", "c"])              # -> list[list[float]]
  s = eg.cosine(v1, v2)                       # -> float [-1, 1]
  top = eg.semantic_match(q, cands, top_k=3)  # -> [(idx, score)]

注意：每次 embed() 都会 subprocess 加载模型（本机 P620 约 110-124s）。
      适用于「一次性编码多篇论文」的交叉审稿前置场景，非高频调用。
"""

import json
import math
import os
import subprocess

_VENV_PY = os.environ.get("EMBEDDINGGEMMA_LEAN_VENV", "<venv>/bin/python")
_CLI_PATH = os.environ.get("EMBEDDINGGEMMA_LEAN_CLI", "<dir>/lean_encode_cli.py")


def available() -> bool:
    return os.path.exists(_VENV_PY) and os.path.exists(_CLI_PATH)


def embed(texts, normalize: bool = True, max_seq_length: int = 1024, timeout: int = 900):
    """生成 embedding（全精度 embeddinggemma2-lean）。

    texts: str 或 list[str]
    normalize: 是否 L2 归一化（默认 True）
    max_seq_length: 模型截断长度（论文主题文本较长，默认 1024）
    返回: list[float]（单条）或 list[list[float]]（批量）
    """
    single = isinstance(texts, str)
    seq = [texts] if single else list(texts)
    if not seq:
        return None if single else []

    req = {"texts": seq, "normalize": normalize, "max_seq_length": max_seq_length}
    proc = subprocess.run(
        [_VENV_PY, _CLI_PATH],
        input=json.dumps(req, ensure_ascii=False),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"lean_encode_cli 返回非零 ({proc.returncode}): {proc.stderr[-2000:]}")

    out = json.loads(proc.stdout)
    if "error" in out and out["error"]:
        raise RuntimeError(f"lean_encode_cli 报错: {out['error']}")

    vecs = out.get("vectors", [])
    return vecs[0] if single else vecs


def cosine(a, b) -> float:
    """余弦相似度（对已归一化向量等价于点积）。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def semantic_match(query: str, candidates, top_k: int = 3):
    """语义检索：返回与 query 最相似的 top_k 个候选 (index, score)。"""
    q = embed(query)
    cs = embed(list(candidates))
    scored = sorted(
        ((i, cosine(q, c)) for i, c in enumerate(cs)),
        key=lambda t: -t[1],
    )
    return scored[:top_k]


if __name__ == "__main__":
    print(f"venv python : {_VENV_PY}  (exists={os.path.exists(_VENV_PY)})")
    print(f"cli script  : {_CLI_PATH}  (exists={os.path.exists(_CLI_PATH)})")
    print(f"available   : {available()}")
