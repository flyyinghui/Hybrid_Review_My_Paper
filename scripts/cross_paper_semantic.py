#!/usr/bin/env python3
"""
cross_paper_semantic.py — 多论文语义相似度（EmbeddingGemma-2 集成）
====================================================================
用于 ars-awa-hybrid-review 的交叉审稿前置：计算多篇论文的语义相似度矩阵，
帮助审稿人聚焦「最相关的论文对」（共享概念 / 可能矛盾 / 可能重复）。

依赖: embeddinggemma_lean.py（全精度 embeddinggemma2-lean，优先）或
      embeddinggemma.py（int4 LiteRT-LM 版，降级）

Usage:
  python cross_paper_semantic.py --papers a.txt b.txt c.txt [--top 5] [--output /tmp/cross_sem.json]
  # 也支持 docx: --papers a.docx b.docx
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_EMBEDDING_MODULE_DIR = os.environ.get("EMBEDDINGGEMMA_MODEL_DIR", "<dir>/embeddinggemma-2-740m")
_TOPIC_CHARS = 6000  # 每篇论文取前 N 字符作为主题代表


def _import_embeddinggemma():
    """加载语义后端：优先全精度 embeddinggemma2-lean，降级 int4 LiteRT-LM。"""
    # 优先：全精度 embeddinggemma2-lean（sentence-transformers，subprocess 调独立 venv）
    try:
        if _SCRIPT_DIR not in sys.path:
            sys.path.insert(0, _SCRIPT_DIR)
        import embeddinggemma_lean
        if embeddinggemma_lean.available():
            return embeddinggemma_lean
    except Exception:
        pass
    # 降级：int4 LiteRT-LM 版（原后端）
    try:
        if _EMBEDDING_MODULE_DIR not in sys.path:
            sys.path.insert(0, _EMBEDDING_MODULE_DIR)
        import embeddinggemma
        return embeddinggemma
    except Exception:
        return None


def _read_text(path: str) -> str:
    """读取 txt/md/docx 文本，返回前 _TOPIC_CHARS 字符。"""
    p = Path(path)
    if p.suffix.lower() == ".docx":
        try:
            from docx import Document
            doc = Document(str(p))
            paras = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
            text = "\n".join(paras)
        except Exception as e:
            text = f"(docx 解析失败: {e})"
    else:
        text = p.read_text(encoding="utf-8", errors="replace")
    # 去掉纯数字/符号噪声，保留正文
    text = re.sub(r'\s+', ' ', text)
    return text[:_TOPIC_CHARS]


def cross_paper_similarity(paper_texts, labels=None):
    """计算多篇论文的两两余弦相似度。

    paper_texts: list[str]（论文文本）
    labels: list[str]（论文标签，默认 Paper1..N）
    返回: {matrix, top_pairs}
    """
    eg = _import_embeddinggemma()
    if eg is None:
        return {
            "available": False,
            "note": "EmbeddingGemma-2 不可用（未安装 litert-lm-api 或模型缺失）",
        }
    n = len(paper_texts)
    if labels is None:
        labels = [f"Paper{i+1}" for i in range(n)]

    vecs = eg.embed(paper_texts, normalize=True)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(round(eg.cosine(vecs[i], vecs[j]), 4))
        matrix.append(row)

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((labels[i], labels[j], matrix[i][j]))
    pairs.sort(key=lambda t: -t[2])

    return {
        "available": True,
        "labels": labels,
        "matrix": matrix,
        "top_pairs": [{"a": a, "b": b, "score": s} for a, b, s in pairs],
    }


def main():
    ap = argparse.ArgumentParser(description="Cross-paper semantic similarity (EmbeddingGemma-2)")
    ap.add_argument("--papers", nargs="+", required=True, help="论文文件路径（txt/md/docx）")
    ap.add_argument("--top", type=int, default=5, help="输出的最相似论文对数量")
    ap.add_argument("--output", default=None, help="输出 JSON 路径")
    args = ap.parse_args()

    labels = [Path(p).stem for p in args.papers]
    texts = [_read_text(p) for p in args.papers]
    report = cross_paper_similarity(texts, labels)

    out_path = args.output or "/tmp/cross_paper_semantic.json"
    Path(out_path).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print("=" * 60)
    print("Cross-Paper Semantic Similarity (EmbeddingGemma-2)")
    print("=" * 60)
    if not report.get("available"):
        print(f"  note: {report.get('note')}")
        return 0
    print(f"  papers: {len(labels)}")
    print(f"\n  相似度矩阵:")
    header = "        " + " ".join(f"{l[:10]:>10}" for l in labels)
    print(header)
    for i, l in enumerate(labels):
        row = " ".join(f"{v:>10.3f}" for v in report["matrix"][i])
        print(f"  {l[:10]:>8} {row}")
    print(f"\n  Top {args.top} 相似论文对:")
    for p in report["top_pairs"][: args.top]:
        print(f"    {p['a']} <-> {p['b']}: {p['score']:.4f}")
    print(f"\n  Report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
