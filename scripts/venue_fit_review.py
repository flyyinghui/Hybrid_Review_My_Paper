#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-paper 5-agent venue-fit final review executor.

Distinct from multi_paper_review.py: this runs the *5-agent venue-fit panel*
(consistency / technical / logic / lean_specialist / publication_strategist),
each with a behavior-specific disposition, against ONE paper + ONE Lean file.

Two things this does that the naive regex in multi_paper_review.py does NOT:
  1. Machine-level Lean ground truth via *nested block-comment stripping* then
     *line-anchored* declaration counts — the only way to get authoritative
     theorem/def/abbrev/axiom/sorry counts when the .lean file contains
     `/- ... -/` block comments (possibly nested) and `--` line comments.
  2. thinking=disabled (extra_body) so deepseek-flash writes to `content`
     instead of dumping into `reasoning_content`.

Usage (run all 5 in parallel via a bash wrapper):
  for a in consistency technical logic lean_specialist publication_strategist; do
      python venue_fit_review.py --agent $a --paper paper.md --lean proof.lean \
          --prior prior_review.md > /tmp/run_$a.log 2>&1 &
  done; wait
"""
import argparse, os, re, time
from openai import OpenAI

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    for p in ["~/.hermes/.env",
              os.path.expanduser("~/.hermes/.env")]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8", errors="ignore"):
                line = line.strip()
                if line.startswith("DEEPSEEK_API_KEY="):
                    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

MODEL = "deepseek-flash"
BASE_URL = "https://api.deepseek.com"


def strip_nested_block_comments(s: str) -> str:
    """Remove `/- ... -/` block comments, handling nesting. This is what makes
    the declaration counts authoritative — a naive regex like
    `(?<![/-])\btheorem\b` miscounts whenever 'theorem' appears inside a
    nested block comment or a '--' line comment."""
    out, depth, i, n = [], 0, 0, len(s)
    while i < n:
        if depth == 0 and s[i:i+2] == "/-":
            depth, i = 1, i + 2
            continue
        if depth > 0:
            if s[i:i+2] == "/-":
                depth, i = depth + 1, i + 2
                continue
            if s[i:i+2] == "-/":
                depth, i = depth - 1, i + 2
                continue
            i += 1
            continue
        out.append(s[i]); i += 1
    return "".join(out)


def lean_ground_truth(lean_path: str) -> str:
    src = open(lean_path, encoding="utf-8").read()
    stripped = strip_nested_block_comments(src)
    lines = stripped.split("\n")
    def count(kw):
        pat = re.compile(r"^\s*(?:noncomputable\s+)?(?:private\s+)?(?:protected\s+)?" + kw + r"\b")
        return sum(1 for l in lines if pat.search(l))
    namespaces = re.findall(r"^\s*namespace\s+(\S+)", stripped, re.M)
    counts = {kw: count(kw) for kw in
              ["theorem", "lemma", "def", "abbrev", "structure", "axiom", "sorry", "admit",
               "noncomputable"]}
    sorry_any = len(re.findall(r"\bsorry\b", stripped))
    admit_any = len(re.findall(r"\badmit\b", stripped))
    gt = ["MACHINE-LEVEL LEAN GROUND TRUTH (line-anchored counts, nested block comments stripped):"]
    for k, v in counts.items():
        gt.append(f"- {k}: {v}")
    gt.append(f"- sorry (anywhere): {sorry_any}")
    gt.append(f"- admit (anywhere): {admit_any}")
    gt.append(f"- namespace ({len(namespaces)}): " + ", ".join(namespaces))
    return "\n".join(gt)


# Behavior-specific dispositions — see references/five-agent-venue-fit-review-script.md
AGENTS = {
  "consistency": ("一致性审计 consistency auditor",
    "字面主义 literalism：只信机器级验证，逐字核对每一个计数/编号/数值/定理名/参考文献，绝不接受「应该没问题」。唯一武器是 grep/Python 机器计数。",
    "论文自报计数是否与机器级 Lean ground truth 一致；公式编号是否连续；正文引用定理名是否真实存在；参考文献编号是否一一对应；编译状态声明是否与 EXIT=0 事实一致。"),
  "technical": ("技术/数学审计 technical auditor",
    "怀疑主义 skepticism：默认作者写错了因子 2、比例方向、或隐藏了假设。每条核心推导链独立重算。first-pass 因子 2/量纲指控先自己重算确认再下结论。",
    "核心证据链的算术/符号/因子正确性；是否存在「定义恒等式伪装公理」或「rw def + linarith」浅层重言式；是否存在观测输入伪装谱定理。"),
  "logic": ("逻辑自洽审计 logic auditor",
    "高度怀疑 adversarial：主动构造反例、找循环论证、区分「语言借用」与「方程被遵循」。最对抗的人格。",
    "核心结论是否暗中依赖待证命题；每个 matched input 是否显式标注 [M]；「语言借用」与「方程跟随」是否被诚实区分；多条证据链是否互相矛盾。"),
  "lean_specialist": ("Lean 形式化专家 Lean specialist",
    "字面主义最严 strictest literalism：只信编译结果、#print axioms、grep 计数，绝不信任文件头注释的「0 sorry / compiled」。凡 rw [def] + linarith 一律怀疑为重言式。",
    "定理中是否存在「定义重述伪装定理」；新模块定理是否实质证明；#print axioms 是否干净；noncomputable def 是否说明物理意义；是否存在 native_decide 在 R 上的假精确等式。"),
  "publication_strategist": ("投稿策略顾问 publication strategist",
    "共情 empathy：代入敌对审稿人/编辑立场，判断各目标期刊容忍度与最低验收项。按期刊格式合规清单逐项核对。",
    "期刊格式合规（摘要词数/关键词数/章节层级/.tex 源/AI 披露）；科学门槛（是否有真实动力学工作包；净预测度是否≈0）；READY/MAJOR/NOT READY 三级判定 + 首选/备选/暂缓期刊 + 最低验收清单。"),
}


def build_prompt(agent, paper, gt, prior):
    role, disp, focus = AGENTS[agent]
    return f"""You are the {role} on a 5-agent venue-fit final-review panel for a theoretical-physics manuscript with an accompanying Lean 4 formalization.

YOUR DISPOSITION (adopt strictly): {disp}

YOUR FOCUS AREAS: {focus}

=== MACHINE-LEVEL LEAN GROUND TRUTH (authoritative; trust over the paper's self-report) ===
{gt}

=== PRIOR REVIEW HISTORY (judge each item fixed/remain/partial with evidence) ===
{prior if prior else "(none)"}

=== MANUSCRIPT (full text) ===
{paper}

=== YOUR TASK ===
Produce a Markdown report with EXACTLY these sections:
## Score (0-10)  — one number + one-line justification
## Verdict  — READY / MAJOR REVISION / NOT READY
## P0 findings (submission-blocking)  — each: [P0-x] claim — evidence — why it blocks
## P1 findings (major)
## P2/P3 findings (minor/optional)
## Prior-item disposition  — fixed/remain/partial per prior item
## Submission recommendation (publication_strategist ONLY)
Be specific and adversarial. Trust the machine-level ground truth over the paper's self-reported counts."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, choices=list(AGENTS))
    ap.add_argument("--paper", required=True)
    ap.add_argument("--lean", default=None)
    ap.add_argument("--prior", default=None)
    ap.add_argument("--max-tokens", type=int, default=16384)
    ap.add_argument("--out-dir", default="/tmp")
    args = ap.parse_args()

    paper = open(args.paper, encoding="utf-8").read()
    gt = lean_ground_truth(args.lean) if args.lean and os.path.exists(args.lean) else "(no lean file)"
    prior = open(args.prior, encoding="utf-8").read() if args.prior and os.path.exists(args.prior) else ""

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=900.0, max_retries=2)
    t0 = time.time()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(args.agent, paper, gt, prior)}],
        max_tokens=args.max_tokens,
        temperature=0.0,
        extra_body={"thinking": {"type": "disabled"}},
    )
    msg = resp.choices[0].message
    content = msg.content or ""
    if not content:
        content = getattr(msg, "reasoning_content", "") or ""
    out = os.path.join(args.out_dir, f"review_{args.agent}.md")
    open(out, "w", encoding="utf-8").write(content)
    print(f"[{args.agent}] done in {time.time()-t0:.0f}s, {len(content)} chars -> {out}")
    if not content:
        print(f"[{args.agent}] WARNING: empty content")


if __name__ == "__main__":
    main()
