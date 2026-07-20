---
name: recognize-circuit-diagram
description: Recognize circuit diagrams from textbook scans, photos, screenshots, or hand drawings and convert them into a verified component-node-branch topology with reference directions and confidence levels. Use before solving any image-based circuit question, when OCR may confuse labels, or when a schematic must be reconstructed or checked.
---

# 识别电路图

先识别连接关系，再识别参数，最后识别文字题意。不要把导线交叉自动视为连接，也不要仅凭版面距离推断串并联。

## 识别流程

1. 裁剪到电路主体并保持题号、图注和极性标记可见。低清图先放大或提高 PDF 渲染 DPI。
2. 建立节点：以连续理想导线为同一节点；有实心连接点的交叉线合并；无连接点的跨线默认不合并，但标为待核验。
3. 建立元件：为每个元件分配唯一标识，记录类型、两端节点、数值、单位、方向、极性和置信度。
4. 建立支路：同一电流贯穿的一组串联元件可组成支路，但保留原始元件级连接。
5. 单独记录开关位置、受控源控制量、耦合电感同名端、运放端子和二极管方向。
6. 执行 [verification-checklist.md](references/verification-checklist.md) 中的拓扑检查。
7. 按 [topology-schema.md](references/topology-schema.md) 输出；不要在识图阶段偷偷补上题目未给出的假设。

## 置信度

- `high`：符号、端点和标注清楚，可直接读取。
- `medium`：拓扑清楚但字符或方向略模糊。
- `low`：连接点、元件类型、极性或数值存在多种解释。

任何 `low` 项影响方程或数值答案时，停止求解并询问用户。若多个解释均可继续，分别命名为方案 A/B，说明各自结果将如何变化。

## 视觉规则

- “同一水平线”不等于同一节点，必须追踪连续导线。
- 导线交叉只有在连接点、T 形接入或图形语义明确时才合并。
- 电压正负号给出参考极性，不必代表实际正负。
- 电流箭头给出参考方向；算得负值表示实际方向相反。
- 受控源必须同时识别输出端、源类型、控制量和比例系数。
- 开关题必须区分 `t<0`、`t=0`、`t>0` 的拓扑。
- 动态电路必须标出电容电压和电感电流的参考方向。

完成识别后，把结构化拓扑交给 `$draw-circuit-diagram` 重绘；用重绘图与原图逐支路对照能发现漏支路和错误节点。
