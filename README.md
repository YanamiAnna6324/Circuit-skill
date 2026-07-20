# Circuit-skill

面向电路分析专业课与考研复习的 Codex skill 集合。默认以周围主编《电路分析基础（第2版）》为首要知识来源，并把教材证据、题图拓扑、电路重绘、规范求解和考点复盘组合为一条可核验流程。

## 包含的 skills

| Skill | 用途 |
|---|---|
| `solve-circuit-textbook` | 总控解题流程，强制教材优先、独立自检和考点复盘 |
| `search-circuit-textbook` | 定位扫描教材、渲染正文页并记录证据等级 |
| `recognize-circuit-diagram` | 从图片提取元件、节点、支路、方向和歧义 |
| `draw-circuit-diagram` | 从 JSON 拓扑生成可编辑、可复核的 SVG 电路图 |
| `review-circuit-exam` | 提炼知识点、规律、考试要点、易错点和快速自检 |

## 教材设置

教材 PDF 不包含在本仓库中。请保留自己的合法本地副本，并设置环境变量：

```powershell
$env:CIRCUIT_TEXTBOOK_PDF = "C:\path\to\电路分析基础（第2版）.pdf"
```

也可以在运行教材渲染脚本时传入 `--pdf`。已适配的扫描版本 SHA-256 为：

```text
24C6AE612A3969F9A4032B1CCEE6ED0333B672A042DC6441650CC05A57E6C62E
```

该版本正文书页 1 对应 PDF 第 10 页，换算式为 `PDF页 = 书页 + 9`。扫描正文在书页 331（PDF 340）后结束，PDF 341 为空白页，不包含目录所列的部分习题参考答案和参考资料。

## 安装

将仓库克隆到本地，然后在 Codex 中安装/加载插件目录。也可以把 `skills/` 下的单个 skill 目录复制到 `$CODEX_HOME/skills`。

运行脚本需要 Python 3；教材页面渲染需要 Poppler 的 `pdfinfo` 与 `pdftoppm`。

## 使用

```text
使用 $solve-circuit-textbook 解答这道题。先核验教材依据，最后列出知识点、规律、考试要点、易错点和快速自检。
```

含图片的题目会先调用 `$recognize-circuit-diagram`。查教材时，目录索引只能定位候选页，公式与适用条件必须通过正文扫描页视觉核验。

## 验证

```powershell
$env:PYTHONUTF8 = "1"
python C:\path\to\skill-creator\scripts\quick_validate.py skills\solve-circuit-textbook
python C:\path\to\plugin-creator\scripts\validate_plugin.py .
```

## 版权说明

本仓库只提供工作流、目录导航和工具脚本，不分发教材内容。教材页只在用户本机临时渲染，且 `.gitignore` 排除所有 PDF、临时页面和输出目录。
