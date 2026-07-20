---
name: search-circuit-textbook
description: Locate and visually verify definitions, formulas, theorems, methods, and similar examples in Zhou Wei's scanned Circuit Analysis Fundamentals, 2nd edition PDF. Use whenever a circuit answer must prioritize the textbook, cite book and PDF pages, inspect a scanned page, or determine whether the provided scan covers a requested topic.
---

# 检索电路分析教材

把目录索引用于导航，把正文页面用于证据。该 PDF 是扫描版且没有可靠文字层，不要依赖 `pdftotext`。

## 定位教材

按顺序解析 PDF 路径：

1. 命令参数 `--pdf`；
2. 环境变量 `CIRCUIT_TEXTBOOK_PDF`；
3. 当前目录中唯一包含“电路分析基础”和“第2版”的 PDF。

若存在多个候选文件，要求用户指定，不要任意选择。使用 `scripts/render_textbook_pages.py --info` 核验教材身份、页数和哈希。哈希与已知版本不同时，将页码映射视为待核验。

## 检索流程

1. 从题目提取标准术语、符号和同义词。例如“叠加”还应查“叠加定理”，“零输入”还应查“自由响应”。
2. 在 [textbook-index.md](references/textbook-index.md) 中定位候选章节和起始书页。目录命中仅为 B 级证据。
3. 将书页换算为 PDF 页。当前版本为 `PDF页 = 书页 + 9`。
4. 渲染候选页及前后各一页：

```powershell
python scripts/render_textbook_pages.py --pdf "教材.pdf" --book-pages 74-80 --output tmp/textbook
```

5. 使用视觉工具查看生成的 PNG。核对页眉书页、节标题、定义或公式、适用条件和上下文。
6. 若需例题，再沿正文向后浏览到例题或习题；不要从目录推断例题内容。
7. 返回简短转述和证据记录，不大段抄录。

## 返回格式

对每条证据给出：

```text
主题：
用途：定义 / 定理 / 公式 / 例题
定位：第x章x.x节，书页y（PDF z）
等级：A 正文已核验 / B 仅目录定位 / C 教材未覆盖
适用条件：
内容转述：
```

至少提供一条 A 级证据，才可把主解标为“教材已核验”。

## 扫描边界

当前文件共 341 个 PDF 页，正文书页 1 位于 PDF 10，书页 331 位于 PDF 340，PDF 341 为空白页。目录列出的“部分习题参考答案（书页332）”和“参考资料（书页342）”不在扫描中。遇到这些内容时返回 C 级，不要猜答案。

## OCR 使用限制

可用 OCR 生成候选关键词，但必须视觉核对原页。OCR 对公式、希腊字母、上下标、参考方向和电路图拓扑不具有证据效力。
