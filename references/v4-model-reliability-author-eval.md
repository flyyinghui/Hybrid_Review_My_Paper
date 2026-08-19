# 作者回应评估 + v4 模型可靠性 (2026-08-07)

## 触发词

"评估作者回应"、"是否合理"、"检查统一框架"、"review the author response"

## 工作流

1. 加载前序审查报告 → 提取P0/P1矛盾清单
2. 读取作者回应MD → 提取核心桥接参数和统一方程组
3. 六步评估协议 → 见 `references/author-response-evaluation-pattern.md`
4. 输出评分(0-10) + 逐项分析 + 修改建议

## v4 模型可靠性 (2026-08-07)

- **v4-pro**: 对任何长度prompt都可能挂死(实测5.5K→6分钟无响应)。不可靠。
- **v4-flash thinking**: 可靠但可能token耗尽致content为空→从reasoning_content回退
- **推荐**: 所有审查任务用v4-flash(thinking或disabled按需选择)
