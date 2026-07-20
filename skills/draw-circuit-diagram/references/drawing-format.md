# 绘图 JSON 格式

坐标单位为 SVG 用户单位。建议网格间距 40，水平或垂直放置元件。

```json
{
  "width": 640,
  "height": 360,
  "title": "一阶 RC 电路（重绘）",
  "components": [
    {"id": "Vs", "type": "voltage_source", "from": [120, 260], "to": [120, 100], "label": "u_s", "value": "10 V", "polarity": "+-"},
    {"id": "R1", "type": "resistor", "from": [120, 100], "to": [360, 100], "label": "R", "value": "2 kOhm"},
    {"id": "C1", "type": "capacitor", "from": [360, 100], "to": [360, 260], "label": "C", "value": "10 uF"}
  ],
  "wires": [
    {"points": [[120, 260], [360, 260]]}
  ],
  "nodes": [
    {"at": [120, 100], "label": "n1"},
    {"at": [360, 100], "label": "n2"}
  ],
  "annotations": [
    {"kind": "current", "from": [180, 70], "to": [260, 70], "label": "i"},
    {"kind": "voltage", "from": [400, 110], "to": [400, 250], "label": "u_C"}
  ]
}
```

支持的 `type`：`resistor`、`capacitor`、`inductor`、`voltage_source`、`current_source`、`diode`、`switch`、`short`。所有元件的 `from` 和 `to` 必须不同，且必须水平或垂直。

`voltage_source.polarity` 必须是 `+-` 或 `-+`，字符顺序对应 `from -> to` 两端；省略时默认为 `+-`。二极管方向同样按 `from`（阳极）到 `to`（阴极）解释。
