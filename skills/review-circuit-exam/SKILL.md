---
name: review-circuit-exam
description: Turn a completed circuit-analysis solution into an exam-focused review containing textbook knowledge points, transferable patterns with boundary conditions, common question forms, scoring steps, pitfalls, and rapid checks. Use at the end of every solved problem or when reviewing mistakes, chapters, or recurring postgraduate entrance exam methods.
---

# 电路考点复盘

只从已经核验的题意、教材证据和解题步骤提炼，不凭一道题制造“万能结论”。每条规律必须附适用条件或失效边界。

## 强制输出

按以下五部分输出，即使某部分只有一条：

### 知识点

列出本题直接使用的教材定义、定理、模型、公式和适用条件。附章节与页码引用；不重复完整推导。

### 规律总结

每条使用“识别线索 → 操作 → 适用条件 → 失效边界”结构。例如：

`端口求等效且含受控源 → 保留受控源并加测试源 → 线性单口网络 → 不适用于把受控源直接置零。`

只总结可迁移规律。仅由本题特殊数值导致的巧合不得写成规律。

### 考试要点

列出常见设问、关键得分步骤、应写出的中间量和合理的时间策略。优先指出阅卷可见的参考方向、初值、等效模型、方程和单位。

### 易错点

使用“错误 → 后果 → 预防动作”结构。聚焦本题实际风险，不罗列通用口号。

### 快速自检

给出 1-3 个可在数十秒内完成的检查，并写明期待观察到什么，例如功率代数和为零、初值连续、极限频率下元件趋于开路或短路。

## 规律质量门槛

- 区分定义、定理、经验规律和仅用于自检的启发式。
- 不把充分条件写成必要条件，也不省略定理适用条件。
- 正弦稳态结论不得直接用于瞬态；直流稳态的电容开路、电感短路不得用于换路瞬间。
- 关联参考方向下吸收功率为正；非关联参考方向必须相应调整符号。
- 线性、稳态、零初始条件、对称三相等前提必须显式写出。

## 错题复盘

用户提供错误答案时，额外按 [mistake-taxonomy.md](references/mistake-taxonomy.md) 分类根因。优先修复最早发生的错误，不把后续代数错误当作唯一原因。给出一道最小变式题，用于检验该错误是否真正改正，但不要直接给出变式题答案。
