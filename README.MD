# Hybrid-Review-My-Paper

一个面向学术论文的**混合审查（Hybrid Review）技能**，融合 ARS（学术研究技能）全流程管线、AWA（学术写作代理）多代理并行审查、J-space 预检层与双模型交叉审查，输出可操作的 P0/P1/P2 问题清单、跨论文一致性矩阵、数值验证与发表就绪评估。

> 该技能从 Hermes Agent 的个人技能库（`ars-awa-hybrid-review`）整理而来，可独立部署为 GitHub 仓库供任何 AI 编码代理 / 审查代理使用。

---

## 一、整体功能

Hybrid-Review-My-Paper 解决学术论文审查中的四个核心问题：

1. **结构性盲区**：单模型审查只看到"提取的摘要/关键片段"，漏掉正文完整推导，导致"缺公式"类误判。
2. **单模型置信度失控**：单模型给分与真实质量偏差大（v4-pro 给 9/10 时，5 代理对抗面板只给 4.7/10）。
3. **跨论文一致性缺失**：多篇共享同一理论框架（如 SL(6,C)）的论文，参数/机制/数值互相矛盾却无人发现。
4. **形式化验证口径不一**：论文声称"0 sorry"但实际含 `:= True` 空壳证明或自指公理。

对应地，本技能提供：**J-space 预检层**（减少误判）→ **双模型交叉审查**（去重 + 交叉验证）→ **ARS 完整性门控**（阻断级检查）→ **AWA 多代理并行**（细粒度质量反馈）。

---

## 二、审查架构与流程

```
┌─────────────────────────────────────────────────────────────┐
│  Step 0: J-space 预检层 (固定第一步)                          │
│    deep-reasoning 追踪推导链 · self-monitoring 置信度校准      │
│    broadcast hub-set 跨论文参数追踪                           │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: 双模型交叉审查                                       │
│    deepseek-v4-pro (high, 32768 token) 主审                  │
│    Qwen3.8:27b-Q8_0 对照 (本地, 独立视角)                     │
│    → 综合去重: 共同发现=高置信 / 单模型独有=需核实 / 误判=剔除 │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: ARS 10 阶段骨架                                      │
│    RESEARCH → WRITE →[AWA Review]→ INTEGRITY → FORMAL REVIEW  │
│    → REVISE →[AWA Review]→ RE-REVIEW → FINALIZE               │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: AWA 多代理并行审查                                    │
│    Stage 2a: 5-7 代理 (consistency/logic/technical/writing/   │
│              bibliography) 全稿审查                           │
│    Stage 4a: 3-5 代理 修订验证                                 │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: 形式化验证交叉校核                                    │
│    Lean 4: axiom/theorem/lemma/sorry 精确计数                  │
│    公理分类映射 (核心/研究前提/状态变量/数值/技术)              │
│    假公理检测 (≈偷换成=) · 零内容公理检测 (1×1=1)              │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
                   最优审查结论输出
      P0(已修复) / P1(需澄清) / P1(误判) / 发表就绪评估
```

---

## 三、各功能模块

### 1. J-space 预检层（`SKILL.md` → "J-space 预检层"）

审查流程的**固定第一步**，减少"漏掉正文推导"类误判。

| 子模块 | 作用 |
|--------|------|
| `deep-reasoning` | 追踪关键推导链的中间步骤（η_k→g_TC、\|ρ\|²→λ_⊥、τ_c→122阶），原则"中间步骤先于结论" |
| `self-monitoring` | 区分"已追踪验证"vs"未追踪的猜测"，审查模型输出"缺公式"前先 grep 正文 |
| `broadcast` | 对跨论文共享参数（g_TC=2.60、λ_∥=35、λ_⊥=35/3、η_k=72/35、b₀=12）建立 hub-set 追踪一致性 |

**已验证效果**：CGICE 双模型审查中，v4-pro 误判"g_TC 缺公式"、Qwen3.8 追问"η_k 来源"，实际 §7.3 已有完整推导。若先执行 J-space 预检（grep 确认推导链），这两条误判可避免。

### 2. 双模型交叉审查（`SKILL.md` → "双模型交叉审查方式"）

| 模型 | 角色 | 配置 |
|------|------|------|
| deepseek-v4-pro | 主审（深度数学推理）| reasoning_effort=high, max_tokens=32768, ~128s |
| Qwen3.8:27b-Q8_0 | 对照（参数来源追问）| enable_thinking=False, max_tokens=3000, ~11min |

**综合去重规则**：双模型共同发现 = 高置信真实问题；单模型独有 = 需人工核实；正文已有但审查者没看到 = 误判剔除。

### 3. ARS 骨架（Academic Research Skills）

10 阶段状态机 + 完整性门控 + 两阶段同行评审 + 格式输出。**阻断级门控**：Stage 2.5 完整性验证（MANDATORY）、Stage 3 五人评审面板（MANDATORY）。

### 4. AWA 多代理并行（Academic Writing Agents）

- **Stage 2a**（写作后）：5-7 代理并行——consistency-checker / logic-reviewer / technical-reviewer / writing-reviewer / bibliography-auditor
- **Stage 4a**（修订后）：3-5 代理验证修复 + 捕获新引入问题
- 每批最多 3 个 `delegate_task` 并行，5+ 代理分两批

### 5. 形式化验证交叉校核（Lean 4）

- 精确计数：`axiom`/`theorem`/`lemma`/`sorry`（排除注释行）
- 公理分类映射：核心公理 / 研究级前提 / 状态变量 / 数值公理 / 技术条件
- 假公理检测：`e^{-280.7}=10^{-122}`（把 ≈ 偷换成 =）
- 零内容公理检测：`1×1=1`、`1=1`
- 自指公理检测：`theorem T := by exact axiom_A`（公理即定理）

---

## 四、主要引用

本技能的审查方法论与形式化验证经验，参考以下体系：

| 引用 | 用途 |
|------|------|
| ARS（Academic Research Skills）| 结构管线管理、完整性验证、正式同行评审 |
| AWA（Academic Writing Agents）| 12 代理并行审查、写作/修订阶段质量注入 |
| J-Space（Gurnee et al., Anthropic, 2026）| 内部工作空间控制、深度推理、自我监控 |
| deepseek-v4-pro / deepseek-v4-flash | 主审 / 快速数值校核模型 |
| Qwen3.8:27b-Q8_0（本地 llama.cpp）| 对照审查、陈述批量生成 |
| Lean 4 + mathlib 4 | 形式化证明验证（0 sorry 交叉校核）|

**技能已验证案例**（18+ 轮）：V22→V25 中微子凝聚、V38 CDM 拓扑扭结、V50-V56 中微子凝聚、V63/V17/V16 三论文跨审查、CGICE V7→V9.1 多轮演化等。

---

## 五、目录结构

```
hybrid-review-my-paper/
├── SKILL.md                  # 技能主文件（审查架构 + 流程 + 陷阱目录）
├── references/               # 83 个参考文档（审查协议/案例/陷阱）
│   ├── v4pro-multi-paper-cross-review.md     # v4-pro 多论文审查协议
│   ├── multi-paper-v4flash-thinking-review.md
│   ├── cross-paper-gw-consistency-audit.md   # 跨论文 GW 一致性审计
│   ├── cross-paper-sl6c-review-20260819.md   # SL(6,C) 四论文综合审查
│   ├── axiom-count-drift-and-renumbering.md  # 公理计数漂移 + 重编号
│   ├── lean-arithmetic-audit-patterns.md     # Lean 算术审计模式
│   └── ... (共 83 个)
└── scripts/
    └── multi_paper_review.py  # 多论文审查辅助脚本
```

---

## 六、许可证

本项目采用 **MIT 开放协议**。详见 [LICENSE](LICENSE)。

核心条款：
- ✅ 允许：商用、修改、分发、私用、再许可
- ✅ 唯一要求：保留版权声明与许可声明
- ⚠️ 免责：软件按"现状"提供，无任何担保

---

## 七、快速开始

1. 将本仓库克隆到 AI 代理的技能目录（或 Hermes Agent 的 `~/.hermes/skills/`）
2. 审查单篇论文：`启动 Hybrid-review-my-paper 技能` + 指定论文路径
3. 审查多篇论文（共享框架）：触发词"三篇论文相互推导结论的一致性"
4. 固定流程自动执行：J-space 预检 → 双模型交叉审查 → ARS/AWA → 形式化校核 → 最优结论

**触发关键词**：`hybrid review my paper`、`ARS + AWA pipeline`、`integrated paper review`、`LLM双模型交叉审查`、`启动Hybrid-review-my-paper技能` 等。
