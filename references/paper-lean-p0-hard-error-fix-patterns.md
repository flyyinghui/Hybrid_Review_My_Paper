# 论文-Lean P0 硬错误修复模式 + 投稿适配性终审配方（V18 FoP 案例，2026-09-20）

## 一、5 代理投稿适配性终审配方（Foundations of Physics / 期刊投稿）

当用户要求「评估论文手稿 + 形式化证明是否适合投稿某期刊」时，5 代理角色改为（区别于通用 consistency/logic/technical/writing/bibliography）：

1. **consistency** —— 论文自报 Lean 统计 vs 机器实测（grep 剥离注释后行首锚定计数）+ 证据等级标注(K/C/A/P/O)前后一致性（同一量被标 A 又标 C = 矛盾）
2. **technical** —— 独立重算每个 P0 的算术（导数残差/比例方向/谱界），逐条 fixed/remain/partial
3. **logic** —— 逻辑闭环 + 诚实性（状态升级过度声称/校准伪装成推导/预测度声明是否一致）
4. **lean_specialist** —— 公理构成审计（研究公理 vs 零内容/占位/数值断言）+ opaque 桥接是否空转（纯命题符号无实际对象）
5. **publication** —— 期刊作者指南合规（摘要词数 150-250/关键词数 4-6/章节层级/是否有 .tex/AI 辅助披露）+ 科学门槛（是否有真实动力学工作包）

**执行配方**：terminal + Python 脚本直调 `deepseek-flash`（`extra_body={"thinking":{"type":"disabled"}}`, max_tokens=8192, temp=0.0, timeout=600），串行 5 代理，每个输出立即写 `/tmp/<name>.part` 防超时丢失，background + notify_on_complete。**对抗性上下文 = 上一轮二审报告的完整 P0/P1 清单**（逐条 fixed/remain/partial，禁止重新凭空评审）。

**编译独立复现**：lake build 验证论文自报的 jobs 数是否属实（V18 自报 "8725 jobs" 经独立编译完全一致 = 编译声明真实）。`export HOME=/root`（lake 内部调 `$HOME/.local/bin/env`）+ `rm -f .lake/build/lib/lean/<module>.*` 强制重编。

**评分分裂模式**：诚实性（7.5/10 高水平）与技术严谨性（3.5-4.5/10）的分裂 = 诚实化只落正文文字层、未传导到 Lean 代码层。这是"过度声称已解决，但诚实标注与代码语义脱节"的新阶段。

## 二、P0 硬错误五类修复模式（编译通过但数学错误）

核心原则：**编译通过 ≠ 数学正确**。0 sorry 是源码卫生条件，不能替代命题语义审查。以下五类全是编译通过但数学/语义错误。

### 类型 A：正文-Lean 双向脱节
- 症状：正文公式已写对（`e^{−2ℓt}`），Lean 定义未同步（`exp(-ell*t)`）。
- 检测：对比正文公式 vs Lean def，残差非零（ℓ(C−D/ℓ)≠0）；反例 ℓ=D=1,C₀=2,t=0 时导数 −1 而方程要求 −2。
- 修复：改 Lean 定义（`exp(-2*ell*t)`）+ 补导数验证定理（HasDerivAt 验证 C'=−2ℓC+2D）。初值/稳态定理的 `simp [ouCov]` 对任意指数都成立，改定义后不用改证明体。
- 案例：ouCov 因子 2。

### 类型 B：公理伪装谱定理
- 症状：`axiom perron_frobenius_dominant_eigen : ... → DominantEigenvalue M = 5.47` 把观测输入(Ω_c/Ω_b≈5.44)包装成数学结论（保守 Metzler 生成元列和为零 → 谱界=0，主特征值不可能=5.47）。
- 检测：检查公理断言数值是否有独立数学来源。
- 修复：删除公理链（公理 + 包装定理 + 孤立 opaque）→ 改 `def targetRatio : ℝ := 547/100`（诚实观测输入常量）。**删除前先 grep 下游引用确认零悬空**（包装定理无下游 = 可安全删）。
- 案例：PF 主特征值公理。

### 类型 C：比例/方向写反
- 症状：metzler 稳态比例注释写 v/u，实际 D/B = u/v（稳态向量 [v,u] 即 B=v, D=u）。
- 检测：用具体数值代入验证（u=2,v=1 → 稳态(B,D)=(1,2) → D/B=2=u/v）。
- 修复：改注释 + 显式标注分量顺序（"B=v, D=u"）。
- 案例：metzler 稳态比例。

### 类型 D：隐含假设未披露（正定性）
- 症状：trace_pairing B(X,Y)=Re tr(XY) 非正定但注释声称"深化 Casimir 守恒数学基础"（隐含正定性假设）。
- 检测：构造反例 H=diag(1,-1,0,0,0,0)→B(H,H)=2>0、K=iH→B(K,K)=−2<0、E₁₂→0。
- 修复：**不删定理**（ad-不变性代数结果本身正确，对全部 6×6 复矩阵成立），只删"过度声称"措辞——在定义处加非正定警告（正定内积需限制 𝔰𝔲(6) 用 ⟨X,Y⟩=−Re tr(XY)），在定理处改为"只证 ad-不变性不证正定性"，论文 MD 同步"Casimir conservation is a provable theorem"→"remains an honest-axiom"。
- 案例：迹配对不正定。

### 类型 E：历史方程残留（基准对齐）
- 症状：桥接命名空间 opaque 注释回到历史版本旧方程（拓扑荷源项 Q_CS、循环熵 ∮dS=0），与当前基准（CGICE v10 §4）不符。
- 检测：grep 旧方程特征串（Q_CS/dτ、dS_info、拓扑荷守恒、信息循环闭合）。
- 修复：opaque 声明不变（只改注释），注释对齐当前基准（dX=(−∇V+F)dt+BdW / Ċ=−HC−CHᵀ+2𝔇 / j̇=−g[a,j] Casimir / KL′=−D∫p‖∇log(p/μ)‖²）+ 历史块注释加"HISTORICAL V11 formulation, NOT v10 §4 baseline"标注 + honest-axiom 注释加"independent extension, NOT v10 baseline"标注。
- 案例：PhaseCgiceBridge CGICE-3/4 旧方程。

## 三、通用教训

- **删除公理链三步**：grep 下游引用（确认零悬空）→ 删公理 + 包装定理 + 孤立 opaque → 新增诚实 def（观测输入常量）。
- **注释修复不改声明计数**：只改注释不改代码语义 → axiom/theorem/opaque/def 计数不变、lake build jobs 数不变（仍 8725 jobs）。
- **论文 MD 统计同步**：删除声明后必须同步附录 A 的计数（116→114 axiom、174→173 thm、73→71 opaque、125→126 def）+ honest_axiom 104→98（删 2 个 honest-axiom 后）。
- **honest_axiom 装饰器分行陷阱**：`@[honest_axiom]` 单独一行 + `axiom` 下一行（分行）会导致同行正则 `@\[\w+\]\s*axiom` 漏计数；统计脚本必须同时处理分行和同行两种形式。论文自报 104 vs 实测 100 的口径差异即源于此。
- **终审发现的核心元观察**：论文诚实化（预测度≈0、三峰撤回、λ_⊥=35/3 标注独立输入）已达高水平，但诚实化只落在正文文字层，未传导到 Lean 代码层——正文写对（−2ℓt）但 Lean 定义错（−ℓt）、正文承认 5.47 是观测输入但 Lean 公理仍当谱定理。修复时二者必须双向同步。
