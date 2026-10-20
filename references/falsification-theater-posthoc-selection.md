# Devil's Advocate 批评模式：falsification theater（事后选择 vs 先验预测）

当论文「诚实展示失败」时，审稿人（尤其 Devil's Advocate）会质疑一个隐蔽的逻辑倒置。

## 核心模式

论文结构常见于候选修正/证伪协议类稿件：
1. 主假设 $H_0$ 被数据排除（如 R=0.03985 被 NuFIT R<0.03380 排除）
2. 论文诚实报告这个失败
3. 然后推广两个「通过」的候选假设（如斜率 38/35、12/11）

Devil's Advocate 会把 2+3 判定为 **falsification theater**（证伪剧场）：
> 先展示一个失败的主假设以证明诚实，再用两个事后拟合的候选来挽救叙事。真正的证伪协议应该预先注册候选，而非在知道约束后从参数组合中挑选。

**判断标准**：候选假设是「先验预测」还是「事后选择」？关键问题是「为什么是 38/35 和 12/11，而不是 37/34 或 13/12？」——如果答案只是「它们恰好通过矩形」，那就是 post-hoc selection，不是独立假设。

## 三个可复用的 Devil's Advocate 挑战

1. **「forward prediction」措辞**：报告数值是「前向预测」还是「参数空间里选点后报数值」？若参数未被独立观测固定，应改「conditional forward evaluation at a specified parameter point」+ 给误差带而非单点。
2. **「new hypothesis」声称**：候选是「新假设」还是「事后拟合」？若是在知道约束后枚举得到，应改「compatibility scan」+ 披露枚举空间大小。
3. **「falsification protocol」标题**：展示失败主假设 + 推广事后候选 = falsification theater。应改「post-hoc compatibility scan」，或给出先验选择原则（如最小分母、与谱对象的代数关系）。

## 修复模式（本会话 V65 实际采用）

在候选斜率段落插入 **Selection history (disclosed)** 块：
- 明确候选提出的日期 + 触发事件（响应主假设失败）
- 明确「post-hoc selections」「compatibility scan」「no independent prior motivation」
- 声明「defensible test requires preregistering slopes before comparison with data not used in selection」

并加 **Falsifiable content** 块（把「失败」转为「可操作的约束」）：
- 明确假设的可证伪边界（如 JUNO/DUNE 测 R>0.034 即排除）
- 明确「failure mode is sharply localized to its barrier hierarchy, not to the bridging core」

## 关键教训

诚实 ≠ 自贬，但诚实展示失败 + 推广事后候选 = 新的逻辑问题。两条路：
- **诚实降级**：把候选降级为「compatibility scan」，披露事后选择
- **诚实但正面**：把失败定位为「可操作的约束」，给出可证伪的边界

不诚实的是「未披露事后选择」+「把候选当先验预测」。披露了就是可接受的「条件性可证伪参数关系」。
