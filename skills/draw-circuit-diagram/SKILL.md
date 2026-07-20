---
name: draw-circuit-diagram
description: Draw clear, reproducible circuit schematics as SVG from a verified JSON topology or textual circuit description, using standard electrical symbols, labeled nodes, reference directions, and switch states. Use when a circuit must be redrawn for explanation, topology verification, equivalent transformations, or exam-solution presentation.
---

# 绘制电路图

从已核验拓扑绘图，不把绘图过程当作修复未知连接的机会。优先生成可缩放 SVG，并保留输入 JSON 作为可编辑源。

## 工作流

1. 若输入是图片，先调用 `$recognize-circuit-diagram`。
2. 选择横向或纵向布局，使主信号流从左到右、参考地位于下方、跨线最少。
3. 按 [drawing-format.md](references/drawing-format.md) 建立 JSON。坐标使用整齐网格；元件端点必须与导线端点完全重合。
4. 运行：

```powershell
python scripts/render_circuit.py circuit.json circuit.svg
```

5. 打开 SVG 进行视觉检查：标签无遮挡、导线不穿过文字、节点连接明确、方向与原题一致。
6. 将 SVG 与 JSON 一同交付。若用于解题，在图注中说明这是重绘图，不冒充教材原图。

## 绘图规范

- 使用白底、黑色导线与元件；仅用红色表示电压参考，蓝色表示电流参考。
- 电阻采用 IEC 矩形符号，与教材常见符号一致。
- 连接点用实心圆；无连接跨线不得加圆点。
- 电压源正负号、二极管方向、受控源菱形、开关状态必须清楚。
- 标签不压线；元件名称和值分行或放在元件外侧。
- 不为美观改变节点顺序、极性、方向或开关状态。
- 多时段动态电路分别绘制 `t<0` 与 `t>0`，不要把两个拓扑叠在一张图上。

脚本支持常用二端符号。复杂器件超出支持范围时，仍提供结构化拓扑，并采用成熟电路绘图库或 LaTeX `circuitikz`；不要手画含义不明的新符号。
