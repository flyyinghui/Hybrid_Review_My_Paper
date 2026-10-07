# Hybrid Review 发现格式 + 分级训练数据提取

## 发现输出格式（V64 5agent Round 系列，最规范）

每个审稿人（`R0_EditorInChief` / `R1_FormalVerification` / ...）下：
- `#### P0 (blocking)` / `#### P1 (major)` / `#### P2 (minor)` / `#### P3 (optional)`
- 发现条目：`- **P1-A (new, §2 eq. (3) and §3.2):** 描述...`
- 每轮带独立的 **Prior-finding resolution table**：表格行 `| **P0-1** (...) | **FIXED** | 证据 |`

老格式（V50 及更早）是 `**C1. 描述**` 的 CRITICAL 编号，无 P 级。

## 历史报告中的结构化发现（可作分级器训练数据）

扫描桌面 `<projects>/` 下 483 个 md（163 审稿报告），提取粗体编号分级发现：

- 总数 **463 条**（31 个文件有结构化发现）
- 分布：P0=105 / P1=146 / P2=120 / P3=65 / C/CRITICAL=27
- 最大来源：V64 5agent Round2/3/4 = 64+81+71 = **216 条**（格式最干净）

## 关键陷阱：标签是 LLM 自评，不是人工 gold label

这些 P 级来自 LLM 审稿人，本身有噪声（v4-pro 单独审计不可靠、v4-flash false-positive）。
直接用它们训练分级器会继承 LLM 的 bias。

**去噪手段**：用跨轮 resolution table 筛高置信子集——
- 同一发现多轮被标同一 P 级 + 最终 FIXED/REJECT 佐证 → 标签可靠
- P 级在轮次间漂移（P0→P1）→ 标签存疑，剔除或降权
- 可从 463 条筛出约 200–300 条高置信样本

## 数据量评估（4 分类 P0/P1/P2/P3）

- baseline 分级器：每类 65–146 条够起步（Qwen 0.8B LoRA）
- 生产级（尤其 P0 高召回）：需 2000–5000 条 + 人工/半自动 gold label
- 数据不足时用 DeepSeek 同义改写/扰动增强扩到千条级（复用 augment_data 思路）

## 提取正则（复用）

```python
finding_re = re.compile(
    r'^[\s>-]*\*\*(?P<grade>P[0-3]|CRITICAL|C)(?P<id>[A-Za-z0-9._\-]*?)(?:\s*[.\-:]|\s*\(|\s*:|\s*\))',
    re.M
)
table_row_re = re.compile(r'^\s*\|\s*\*\*P[0-3]', re.M)  # resolution table，排除防重复计数
# 先 table_row_re.sub('', txt) 再去匹配 finding_re
```

⚠️ P 编号的「出现次数」≠「可标注条数」——正文引用、汇总表、版本号都会污染计数。
必须排除表格行（resolution table）才能数清真实发现条目。
