# 拓扑输出格式

```yaml
source: 原图或 PDF 页
states:
  - name: t<0
    switch_positions: [S1=左]
nodes:
  - id: n0
    aliases: [ground]
    confidence: high
components:
  - id: R1
    type: resistor
    terminals: [n1, n0]
    value: 2
    unit: kOhm
    voltage_reference: n1 -> n0
    current_reference: n1 -> n0
    confidence: high
branches:
  - id: b1
    path: [n1, R1, n0]
ambiguities:
  - item: crossing near R1
    alternatives: [connected, not_connected]
    impact: changes node count and KCL equations
```

对受控源增加 `control` 和 `gain`。对耦合电感增加 `dot_terminal`。对二极管增加 `anode`、`cathode` 和采用的模型。未读出的字段填 `unknown`，不要删除字段来掩盖不确定性。
