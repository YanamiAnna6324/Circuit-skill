---
name: solve-circuit-textbook
description: Solve Chinese circuit-analysis questions for postgraduate entrance exam preparation with mandatory priority given to Zhou Wei's Circuit Analysis Fundamentals, 2nd edition. Use for calculations, proofs, concept questions, textbook exercises, circuit images, solution checking, or requests that require knowledge points and exam takeaways after every answer.
---

# 教材优先电路解题

把教材证据、拓扑核验、规范求解和考点复盘串成完整流程。不要仅凭通用知识声称“教材中指出”。

## 强制流程

1. 复述已知量、待求量、参考方向、开关时刻和稳态条件。保留题目单位与符号。
2. 如输入含电路图，调用 `$recognize-circuit-diagram`。先得到元件表、节点表、支路表和歧义清单；存在影响答案的歧义时，不要继续数值求解。
3. 调用 `$search-circuit-textbook`。按概念、定理、公式、相似例题四类检索，至少视觉核对一个正文页；只命中目录不算正文证据。
4. 写入教材证据记录。遵循 [evidence-policy.md](references/evidence-policy.md)。教材没有覆盖或扫描缺页时，明确说明，不得伪造页码或原文。
5. 选择教材使用的方法并求解。先列适用条件，再列方程，最后化简并代入单位。
6. 用至少一种独立方法自检：量纲、KCL/KVL、初终值、功率守恒、极限情况、数量级或回代。
7. 仅在重绘能消除歧义、说明等效变换或展示切换状态时调用 `$draw-circuit-diagram`。
8. 调用 `$review-circuit-exam`，始终在答案末尾输出知识点、规律总结、考试要点、易错点和快速自检。

## 方法优先级

1. 教材正文明确出现且适用的方法。
2. 教材例题展示的同类方法。
3. 从教材定义和定理直接推导的方法，标记为“由教材内容推导”。
4. 教材外方法，只能放入“补充方法”区，且不得替代教材主解。

教材方法较长但可靠时，仍以它作为主解。若用户明确要求其他方法，同时保留教材主解并对照结果。

## 输出契约

按照 [answer-template.md](references/answer-template.md) 的顺序作答。引用格式统一为：

`[教材，第4章4.2节，书页78（PDF 87）]`

使用转述，不大段抄录。区分正文已核验、仅目录定位、教材未覆盖三个证据等级。完成后运行：

```powershell
python scripts/check_answer.py answer.md
```

脚本失败表示答案不完整，补齐缺少的区段。

## 失败处理

- 教材路径不可用：请用户设置 `CIRCUIT_TEXTBOOK_PDF` 或传入 PDF 路径，同时可给出标为“待教材核验”的临时分析。
- 扫描页模糊：渲染相邻页或提高 DPI，再视觉核对；不要猜测公式上下标。
- 题图模糊：列出已确认内容与歧义，提出一个最小澄清问题。
- 教材与常见约定不同：采用教材约定，并指出差异。
