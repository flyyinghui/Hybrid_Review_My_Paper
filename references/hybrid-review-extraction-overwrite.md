# Hybrid Review: 论文提取覆盖陷阱

## 症状

部署 5-agent hybrid review 时，审阅员报告发现大量缺失章节（如 "Stern-Brocot §2.5.1 不在提供文件中"、"摘要不可见"），而实际上完整论文是存在的。

## 根因

提取脚本在循环中按文件名匹配提取多个文件，最后一个匹配的文件覆盖了 `/tmp/v55_paper.txt`：

```python
# BUG: 最后一个匹配项覆盖先前提取
for f in os.listdir(d):
    if 'V55' in f.upper() and f.endswith('.docx'):
        # 每次循环都写入同一文件！
        with open('/tmp/v55_paper.txt', 'w') as out:
            out.write(text)
```

结果：完整的 EN_V55.docx（199K 字符）被 Section_22_Restructured_V55.docx（13K 字符，仅 §2.2）覆盖。

## 检测

审阅员报告中出现以下信号：
1. "论文文件仅 13K 字符（§2.2 片段）"
2. "关键章节缺失：Stern-Brocot 味荷、中微子质量预测"
3. 多个审阅员独立报告相同的内容缺失

## 修复

```python
# 精确匹配目标文件名，避免覆盖
target = "Neutrino_Condensation_Reviewed_Optimized_EN_V55.docx"
fp = os.path.join(d, target)
with zipfile.ZipFile(fp) as zf:
    xml = zf.read('word/document.xml').decode('utf-8')
text = re.sub(r'<[^>]+>', ' ', xml)
with open(f'/tmp/{target.replace(".docx", ".txt")}', 'w') as out:
    out.write(text)
```

## 预防清单

- [ ] 提取脚本使用精确文件名，不依赖循环匹配
- [ ] 验证输出文件大小：`wc -c /tmp/paper.txt` 应接近源 DOCX 大小
- [ ] 部署审阅前运行快速检查：`grep -c 'Abstract\|Conclusion\|References' /tmp/paper.txt`
- [ ] 若审阅员报告 "内容缺失"，**首先怀疑提取脚本**，而非论文本身
