#!/usr/bin/env python3
"""
verify_cross_namespace.py — 验证 embeddinggemma2-lean 跨命名空间迁移效果
========================================================================
背景：embeddinggemma2-lean 在 openai_math（OAI 命名空间）的 37.7 万依赖对上
微调，recall@10 = 0.4663（纯名字）/ 0.5505（增强文本）。本脚本验证它迁移到
用户 SL(6,C) 自制命名空间（CGICE 等）后的引理召回命中率。

流程：
  1. 解析用户 Lean 文件 → 声明库（名字 + kind + signature + body）
  2. 提取依赖：每个 theorem/lemma 的 body 里引用的其他声明名（词边界匹配）
  3. 用 embeddinggemma2-lean 编码声明（增强文本口径：名字词化 + 签名）
  4. 测 recall@k：给定定理名（纯名字口径），召回 top-k，命中真实依赖的比例
  5. 对比 openai_math 的 0.4663（纯名字），判断迁移是否退化

用法（独立 venv 下）：
  .../venv/bin/python verify_cross_namespace.py <lean_file> [lean_file2 ...]
"""

import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 解析 Lean 声明库
# ---------------------------------------------------------------------------

KINDS = ("theorem", "lemma", "def", "abbrev", "structure", "class", "inductive", "opaque", "instance")
DECL_RE = re.compile(
    r'^\s*(theorem|lemma|def|abbrev|structure|class|inductive|opaque|instance)\s+'
    r'([A-Za-z_α-ωΑ-Ω0-9][\wα-ωΑ-Ω.\'’]*)\b'
)
NS_RE = re.compile(r'^\s*namespace\s+([A-Za-z_][\w.]*)')
END_RE = re.compile(r'^\s*end\b')
IDENT_RE = re.compile(r"[A-Za-z_α-ωΑ-Ω][\wα-ωΑ-Ω.'’]*")


def name_to_text(name: str) -> str:
    """Lean 标识符 → 可读文本（与训练口径一致）。"""
    s = re.sub(r'_+', ' ', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s)
    return s.strip()


def parse_file(path: str):
    """返回 {短名: {kind, signature, body, namespace}}。"""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    n = len(lines)

    # 第一遍：定位所有声明起始行 + namespace 追踪
    decl_lines = []  # (start_line, full_name, kind)
    namespace = []
    for i, line in enumerate(lines):
        m_ns = NS_RE.match(line)
        if m_ns:
            namespace.append(m_ns.group(1))
            continue
        if END_RE.match(line):
            if namespace:
                namespace.pop()
            continue
        m = DECL_RE.match(line)
        if m:
            decl_lines.append((i, m.group(2), m.group(1)))

    decls = {}
    for idx, (start, full_name, kind) in enumerate(decl_lines):
        name = full_name.split('.')[-1]
        end = decl_lines[idx + 1][0] if idx + 1 < len(decl_lines) else n
        body = "\n".join(lines[start:end])
        # 签名：声明行名字之后，到第一个 := 或 where
        sig = body
        sig = re.split(r':=|\bwhere\b', sig)[0]
        sig = re.sub(r'\s+', ' ', sig).strip()
        ns_full = '.'.join(namespace) if namespace else ''
        if name not in decls:
            decls[name] = {"kind": kind, "signature": sig, "body": body, "namespace": ns_full}
    return decls


def extract_deps(decls):
    """对每个 theorem/lemma，找 body 中引用的其他声明名（词边界匹配）。"""
    all_names = set(decls.keys())
    deps = {}
    for name, d in decls.items():
        if d["kind"] not in ("theorem", "lemma"):
            continue
        idents = set(IDENT_RE.findall(d["body"]))
        found = {x.split('.')[-1] for x in idents if x.split('.')[-1] in all_names}
        found.discard(name)
        if found:
            deps[name] = found
    return deps


# ---------------------------------------------------------------------------
# 2. 编码 + 召回评估
# ---------------------------------------------------------------------------

def enrich(name, decls, sig_chars=120):
    """增强文本口径：名字词化 + 类型签名（用户文件基本无 docstring）。"""
    parts = [name_to_text(name)]
    d = decls.get(name)
    if d and d.get("signature"):
        parts.append("type " + d["signature"][:sig_chars])
    return " | ".join(parts)


def main():
    files = sys.argv[1:] or [
        "~/Desktop/papers/cgice/cgice_proof_v10.lean"
    ]

    t0 = time.time()
    # 解析所有文件
    decls = {}
    for f in files:
        d = parse_file(f)
        decls.update(d)
        print(f"[parse] {Path(f).name}: {len(d)} 声明", flush=True)

    deps = extract_deps(decls)
    n_theorems = sum(1 for d in decls.values() if d["kind"] in ("theorem", "lemma"))
    n_with_deps = len(deps)
    print(f"[deps] 声明总数 {len(decls)}，theorem/lemma {n_theorems}，有依赖的 {n_with_deps}", flush=True)

    if n_with_deps == 0:
        print("[deps] 无依赖可测，退出")
        return 0

    # 加载模型
    print("[model] 加载 embeddinggemma2-lean ...", flush=True)
    import numpy as np
    import torch
    from sentence_transformers import SentenceTransformer

    model_dir = os.environ.get("EMBEDDINGGEMMA_LEAN_DIR", "<model_dir>/embeddinggemma-2-lean")
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32
    else:
        device = "cpu"
        dtype = torch.float32
    model = SentenceTransformer(model_dir, device=device, model_kwargs={"torch_dtype": dtype})
    model.max_seq_length = 64  # 紧凑口径（与训练一致）
    print(f"[model] 加载完成 ({time.time()-t0:.0f}s), device={device}, dtype={dtype}", flush=True)

    # 编码所有声明（增强文本口径）
    all_names = list(decls.keys())
    cand_texts = [enrich(n, decls) for n in all_names]
    print(f"[encode] 编码 {len(all_names)} 条候选声明 ...", flush=True)
    cand_emb = model.encode(cand_texts, normalize_embeddings=True, batch_size=64,
                            convert_to_numpy=True, show_progress_bar=False)
    print(f"[encode] 候选编码完成 ({time.time()-t0:.0f}s)", flush=True)

    # 编码查询（纯名字口径，与训练评估的"纯名字"口径一致）
    query_names = list(deps.keys())
    query_texts = [name_to_text(n) for n in query_names]
    print(f"[encode] 编码 {len(query_names)} 条查询（纯名字口径）...", flush=True)
    query_emb = model.encode(query_texts, normalize_embeddings=True, batch_size=64,
                             convert_to_numpy=True, show_progress_bar=False)

    # 相似度矩阵（query × candidate）
    sim = query_emb @ cand_emb.T  # 已归一化，点积即余弦
    # 排除自身
    name_to_idx = {n: i for i, n in enumerate(all_names)}
    for qi, qn in enumerate(query_names):
        if qn in name_to_idx:
            sim[qi, name_to_idx[qn]] = -1.0

    # 计算 recall@k
    ks = [1, 3, 5, 10]
    hits = {k: 0 for k in ks}
    total_deps = 0
    per_query_recall = {k: [] for k in ks}
    for qi, qn in enumerate(query_names):
        true = deps[qn]
        total_deps += len(true)
        topk = np.argsort(-sim[qi])[:10]
        topk_names = [all_names[i] for i in topk]
        for k in ks:
            hit = len(set(topk_names[:k]) & true)
            hits[k] += hit
            per_query_recall[k].append(hit / len(true))

    print("\n" + "=" * 60)
    print(f"跨命名空间迁移验证结果（{len(files)} 文件，{len(deps)} 查询）")
    print("=" * 60)
    print(f"  总依赖数: {total_deps}")
    for k in ks:
        r = hits[k] / total_deps
        print(f"  recall@{k:2d} = {r:.4f}  (命中 {hits[k]}/{total_deps})")
    print(f"\n  参考基线（openai_math 同分布）:")
    print(f"    纯名字 recall@10 = 0.4663")
    print(f"    增强文本 recall@10 = 0.5505")
    print(f"\n  结论判读:")
    r10 = hits[10] / total_deps
    if r10 >= 0.40:
        print(f"    recall@10={r10:.4f} ≥ 0.40 → 迁移效果良好（接近同分布水平）")
    elif r10 >= 0.25:
        print(f"    recall@10={r10:.4f} ∈ [0.25, 0.40) → 迁移有损失但可用")
    else:
        print(f"    recall@10={r10:.4f} < 0.25 → 迁移显著退化，建议重训或放弃")
    print(f"\n  总耗时 {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
