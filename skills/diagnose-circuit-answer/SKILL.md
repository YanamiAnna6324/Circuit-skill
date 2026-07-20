---
name: diagnose-circuit-answer
description: Diagnose, explain, correct, and independently verify wrong or uncertain circuit-analysis answers using textbook-grounded evidence. Use when a user provides an answer for grading, asks where a solution went wrong, wants a corrected solution, challenges an agent answer, or when the agent must self-check its own circuit solution before finalizing it.
---

# 电路答案诊断

把候选答案当作待验证对象，不把它当作正确基线。先独立求得检查基线，再逐步比较；不要用“重新读一遍原推导”冒充自检。

## 选择模式

- **错题诊断**：用户提供题目和自己的答案。定位第一个实质错误，解释错误传播，并给出完整修正解答。
- **答案审阅**：用户提供参考答案、他人答案或多个答案。分别验证，不以“答案一致”代替正确性检查。
- **自我诊断**：检查 agent 刚生成的答案。隐藏原答案的最终结论，先从题目与教材独立重建基线，再比较。

缺少题目、题图、答案步骤或参考方向时，先列出能检查的范围。只有缺失信息会改变结论时才询问用户；不要猜图中连接或省略的初值。

## 强制诊断流程

1. **冻结输入**：抄录题意、候选答案、单位、参考方向、时段与假设。把题目事实和候选答案的主张分开。
2. **核验拓扑**：题目含图时调用 `$recognize-circuit-diagram`。拓扑存在关键歧义时停止数值判定。
3. **建立教材基线**：调用 `$search-circuit-textbook`，核验方法、公式和适用条件。遵循 [diagnosis-protocol.md](references/diagnosis-protocol.md) 的证据规则。
4. **独立求解**：不沿用候选答案的中间量和方程。优先采用教材中的方法，得到符号结果、数值结果与物理预期。
5. **逐步对照**：按拓扑 → 参考方向 → 模型/定理条件 → 初值 → 方程 → 代数 → 单位 → 结果表达的顺序检查。定位“第一个实质错误”，不要只指出后续连锁错误。
6. **检验假设**：为 3-5 个可能根因列出预测，并用最小检查逐个证伪。简单明显错误可以缩减为 1-2 个，但说明为什么无需更多假设。
7. **修正答案**：从第一个错误处重新推导，不只替换最终数值。保留正确步骤并说明它们为何仍然成立。
8. **独立复验**：从 [independent-checks.md](references/independent-checks.md) 选择至少一种与主解不同的检查。高风险题使用两种。
9. **给出判定**：只能使用“通过”“修正后通过”“无法判定”三种结论，并报告剩余不确定性。
10. 调用 `$review-circuit-exam`，把根因转化为知识点、规律、考试要点、易错点和快速自检。

## 自我诊断隔离规则

检查自己的答案时：

1. 不把原答案的最终值当输入条件。
2. 更换解题表述或方法；例如节点法主解用回路法、戴维南等效、KCL/KVL 回代或功率守恒复验。
3. 重新读取题图和教材页，不复用未经核验的识图结论。
4. 对每个关键公式重新核对适用条件、符号和单位。
5. 发现错误后修正一次，再完整复验一次；不要无限递归调用本 skill。
6. 如果无法构造独立检查，结论必须是“无法判定”，不得写“自检通过”。

## 输出契约

先将下列 `scripts/` 路径解析为相对于本 `SKILL.md` 所在目录的绝对路径；不要假设当前工作目录位于 skill 根目录。

严格按 [diagnosis-template.md](references/diagnosis-template.md) 输出。完成后运行：

```powershell
python scripts/check_diagnosis.py diagnosis.md
```

不能写临时文件时，将 Markdown 通过标准输入传入。在 Windows PowerShell 5.1 中先设置 `$OutputEncoding = [Text.UTF8Encoding]::new($false)`，再运行 `Get-Content -Raw -Encoding UTF8 diagnosis.md | python scripts/check_diagnosis.py -`；其他终端可直接管道传入 UTF-8。

结构检查通过不等于数学正确；它只保证诊断证据没有遗漏。最终“通过”还必须满足：教材依据已核验、没有未解决的关键拓扑歧义、独立复验成功。

比较带单位的标量时，使用确定性检查：

```powershell
python scripts/compare_values.py --expected 5 --expected-unit mA --actual 5 --actual-unit A
```

脚本支持常用 SI 前缀，并会拒绝不同物理量单位之间的比较。

## 与总控 skill 配合

由 `$solve-circuit-textbook` 调用时，只诊断当前草稿一次。若发现错误，修正后再复验一次并返回总控；不要重新调用总控造成循环。
