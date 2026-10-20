#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reusable 5-agent venue-fit review executor (deepseek-flash).
Copy this file, fill in LEAN_GT and PRIOR constants, then run one agent at a time:

    python venue_fit_review_exec.py --agent consistency
    python venue_fit_review_exec.py --agent technical
    ... (logic, lean_specialist, publication_strategist)

Run all in parallel via a bash wrapper + background=true + notify_on_complete:
    for a in technical logic lean_specialist publication_strategist; do
        python venue_fit_review_exec.py --agent $a > /tmp/run_$a.log 2>&1 &
    done; wait

Each agent writes /tmp/review_<agent>.md. 25s/agent typical for a ~230KB manuscript.

Key parameters (verified): deepseek-flash + extra_body={"thinking":{"type":"disabled"}}
(else content is empty / reasoning_content holds the chain), max_tokens=16384 (8192
truncates the technical agent mid-P2 and loses its score/verdict), temperature=0.0,
timeout=900.  Feed the FULL manuscript in one prompt — deepseek-flash handles 170-260KB.
Do NOT use deepseek-v4-pro for reviewer agents (hangs on full-manuscript prompts).
"""
import argparse, os, time
from openai import OpenAI

# ---- Fill in: DeepSeek key (value never hardcoded here; read from your .env) ----
def load_key():
    for p in ["~/.hermes/.env",
              "/root/.hermes/.env"]:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8", errors="ignore"):
                line = line.strip()
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("no DEEPSEEK_API_KEY found")

API_KEY = load_key()
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-flash"

# ---- Fill in: machine-level Lean ground truth (authoritative; trust this over paper) ----
#   Report def / abbrev / structure as THREE SEPARATE columns. Authors write "N definitions"
#   while silently folding abbrevs into def — the conflation itself is a common P0.
LEAN_GT = """MACHINE-LEVEL LEAN GROUND TRUTH (grep line-anchored counts, nested block comments stripped):
- theorem: <N>  |  lemma: <N>  |  def: <N>  |  abbrev: <N>  |  structure: <N>
- axiom: <N>  |  sorry: <N>  |  admit: <N>  |  noncomputable: <N>
- namespace (<N>): <comma-separated list>
- Compilation: EXIT=<0/1> against pinned Mathlib version.
- Golden gate (#print axioms) on main theorems: only [propext, Classical.choice, Quot.sound].
"""

# ---- Fill in: prior review history (rounds 1..N-1), as adversarial context ----
#   Do NOT treat a prior "ACCEPT" as ground truth. Prior panels overclaim; verify each
#   prior "fixed" item against the CURRENT body text, not the prior report.
PRIOR = """PRIOR REVIEW HISTORY (rounds 1..N-1):
Score trajectory: <...>.
Prior venue recommendation: <...>.
Prior key findings (judge each fixed / remain / partial against CURRENT manuscript): <...>
Persistent caveats: <...>.
"""

AGENTS = {
 "consistency": {
   "role": "一致性审计 (consistency auditor)",
   "disp": "字面主义 literalism：只信机器级验证，逐字核对每一个计数/编号/数值/定理名/参考文献，绝不接受「应该没问题」。你的唯一武器是 grep/Python 机器计数，不是印象。",
   "focus": "论文自报的定理/定义/公理计数是否与机器级 Lean ground truth 一致；公式编号是否连续；正文引用的定理名是否真实存在于 Lean；参考文献编号是否与文献表一一对应；编译状态声明是否与 EXIT 事实一致；附录统计段是否与 ground truth 一致。",
 },
 "technical": {
   "role": "技术/数学审计 (technical auditor)",
   "disp": "怀疑主义 skepticism：默认作者写错了因子 2、比例方向、或隐藏了假设。对每条核心推导链独立重算。对 first-pass 因子 2/量纲/漏项指控，先自己重算确认再下结论。",
   "focus": "核心证据链的算术/符号/因子正确性；是否存在「定义恒等式伪装公理」或「rw def + linarith」浅层重言式；是否存在观测输入伪装谱定理；每个系数（如 24、35/2 vs 35）是否有推导或标注。",
 },
 "logic": {
   "role": "逻辑自洽审计 (logic auditor)",
   "disp": "高度怀疑 adversarial：主动构造反例、找循环论证、区分「语言借用」与「方程被遵循」。最对抗的人格。",
   "focus": "核心结论是否暗中依赖待证命题（循环）；每个 matched input 是否显式标注 [M]；「语言借用」与「方程跟随」是否被诚实区分；是否存在把匹配输入伪装成推导的切分错误；多条证据链之间是否互相矛盾；附录「closes the gaps」与正文「remains open」是否自相矛盾。",
 },
 "lean_specialist": {
   "role": "Lean 形式化专家 (Lean specialist)",
   "disp": "字面主义最严 strictest literalism：只信编译结果、#print axioms 输出、grep 计数，绝不信任文件头注释的「0 sorry / compiled」声明。凡 rw [def] + linarith 的浅层证明一律怀疑为重言式。",
   "focus": "定理中是否存在「定义重述伪装定理」（unfold 后只剩 rw+linarith）；新模块定理是否为实质证明还是 native_decide/有限代数内容；#print axioms 是否干净；编译声明是否与 ground truth 一致；noncomputable def 是否说明物理意义；是否存在 native_decide 在 R 上的假精确等式。",
 },
 "publication_strategist": {
   "role": "投稿策略顾问 (publication strategist)",
   "disp": "共情 empathy：代入敌对审稿人/编辑立场，判断每个目标期刊的容忍度与最低验收项。按期刊格式合规清单逐项核对。",
   "focus": "期刊格式合规（摘要 150-250 词、关键词 4-6 个、章节层级、.tex 源、AI 使用披露）；科学门槛（是否至少一个真实动力学工作包；净预测度是否≈0）；READY / MAJOR REVISION / NOT READY 三级判定 + 首选/备选/暂缓/不建议期刊 + 最低验收项清单。",
 },
}

def build_prompt(agent, paper):
    a = AGENTS[agent]
    return f"""You are the {a['role']} on a 5-agent venue-fit final-review panel for a theoretical-physics manuscript with an accompanying Lean 4 formalization.

YOUR DISPOSITION (adopt strictly): {a['disp']}

YOUR FOCUS AREAS: {a['focus']}

=== MACHINE-LEVEL LEAN GROUND TRUTH (authoritative, trust this over the paper's self-report) ===
{LEAN_GT}

=== PRIOR REVIEW HISTORY (adversarial context; judge each item fixed/remain/partial) ===
{PRIOR}

=== MANUSCRIPT (full text) ===
{paper}

=== YOUR TASK ===
Produce a review report in Markdown with EXACTLY these sections:

## Score (0-10)
One number + one-line justification.

## Verdict
READY / MAJOR REVISION / NOT READY, one line.

## P0 findings (submission-blocking)
Each: [P0-x] claim — evidence (quote/line/theorem name) — why it blocks.

## P1 findings (major, should fix before submit)
## P2/P3 findings (minor / optional)
## Prior-item disposition
For each prior-history item: fixed / remain / partial + evidence from CURRENT manuscript.

## Submission recommendation (publication_strategist ONLY; others may give one line)
Be specific and adversarial. Trust machine ground truth over the paper's self-reported counts.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--paper", required=True)
    ap.add_argument("--max-tokens", type=int, default=16384)
    args = ap.parse_args()
    paper = open(args.paper, encoding="utf-8").read()
    prompt = build_prompt(args.agent, paper)
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=900.0, max_retries=2)
    t0 = time.time()
    resp = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}],
        max_tokens=args.max_tokens, temperature=0.0,
        extra_body={"thinking": {"type": "disabled"}},
    )
    msg = resp.choices[0].message
    content = msg.content or ""
    if not content:
        content = getattr(msg, "reasoning_content", "") or ""
    out = f"/tmp/review_{args.agent}.md"
    open(out, "w", encoding="utf-8").write(content)
    print(f"[{args.agent}] done {time.time()-t0:.0f}s {len(content)} chars -> {out}")

if __name__ == "__main__":
    main()
