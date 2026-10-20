# 衔接/桥接论文审稿 — Devil's Advocate 的核心挑战模式

当论文定位为「衔接论文 / bridging paper」（把母框架的推导衔接到具体唯象）时，审稿重点是「独有增量是否充分」+「衔接是否正确」，而非「是否独立推导了母框架」。Devil's Advocate 对这类论文反复命中三个核心挑战（V65 中微子衔接论文终审实测，评分 6.5/10 与其它 4 代理的 7.6-7.8 拉开差距）。

## 挑战 1：「前向预测」措辞的诚实化（forward → conditional forward evaluation）

- **反论**：摘要写 "produces a forward mass scale M_R≈X GeV without fitting a target neutrino mass" 时，字面为真但物理上误导——M_R 是 EFT 输入（正则化尺度 + 耦合）的函数，这些输入**未被任何实验数据固定**。改变正则化尺度一个量级，M_R 相应改变，论文中无机制排除。
- **本质**：这不是 "prediction"，而是 "**a representative point in an unconstrained parameter space**"。
- **修复要求**：(a) 写出 M_R 对参数的显式依赖 (b) 给误差带而非单点 (c) "forward" → "**conditional forward evaluation at a specified parameter point**"。

## 挑战 2：「事后选择」（post-hoc selection）识别 = "falsification theater"

- **反论**：主假设 H（R=0.03985）**被否证**（历史数据排除），随后推广两个"通过"的候选斜率（R=0.03089/0.03042）——这是**逻辑倒置**。若 H 是 "the hypothesis"，它失败了；若候选是 "candidates"，H 就不是 hypothesis 而是被否证的中间产物。
- **本质**：先展示一个失败的主假设以证明诚实，再用事后拟合的候选挽救叙事 = "falsification theater"（证伪剧场），不是真正的证伪协议。
- **修复要求**：(a) 诚实披露候选是"在知道约束后从参数组合枚举得到"（含枚举空间大小）(b) 或给先验选择原则（如"最小分母"）(c) 否则把章节标题从 "falsification tests" 改为 "**post-hoc compatibility scan**"。

## 挑战 3：衔接论文缺「独立可证伪预言」

- **反论**：衔接论文的合法性依赖"产生母框架无法单独产生的、可证伪的预言"。若增量（热力学、味谱）是"条件 EFT 内的自洽演化"或"被自身数据排除的假设"，则价值退化为"**母框架的数值后处理**"。
- **修复**：明确写出 H 的可证伪内容（如"若 JUNO/DUNE 测到 R>0.034，H 被排除"），把"独立假设"从"事后拟合"提升为"可证伪假设"。区分「H 的失败模式定位到 barrier 层级」vs「桥接核心被否证」。

## 通用结论

对衔接/桥接论文，Devil's Advocate 的 3 个挑战本质是**「诚实化的最后一公里」**——要求进一步明确边界：数值是"条件性评估"而非"前向预测"，候选是"事后兼容性扫描"而非"独立假设"，增量是"条件性诊断"而非"独立可证伪预言"。这与"诚实降级悖论"一脉相承，是"诚实但正面"的第三条路（措辞用肯定式功能定位，避免反复否定句）。

修复优先级：挑战 1 可立即改措辞（零成本）；挑战 2/3 触及认识论根基（需重构定位）。
