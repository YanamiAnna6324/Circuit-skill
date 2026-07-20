# Circuit-skill 安装教程

本文面向 Windows 用户，分别说明：

1. 使用标准 Codex CLI 或 ChatGPT 桌面版安装整个插件；
2. 为 Codex IDE 扩展直接安装 6 个 skills；
3. 使用 CC-Switch 图形界面发现、安装、同步和更新 skills。

仓库地址：<https://github.com/YanamiAnna6324/Circuit-skill>

> 教材 PDF 不包含在仓库中。你需要持有自己的本地教材副本，并在安装后设置路径。

## 一、先确认使用哪种安装方式

| 使用环境 | 推荐方式 | 安装结果 |
|---|---|---|
| Codex CLI | 标准版插件安装 | 一次安装整个 `circuit-skill` 插件及其 6 个 skills |
| ChatGPT 桌面版中的 Codex | 标准版插件安装 | 从 Circuit Skill marketplace 安装插件 |
| VS Code / JetBrains Codex IDE 扩展 | 标准版 skills 直装 | 将 6 个 skill 目录放入用户级 skills 目录 |
| 已使用 CC-Switch | CC-Switch 版 | 图形界面逐个安装并同步 6 个 skills |

插件是这套仓库的推荐分发方式。IDE 扩展当前不支持插件浏览和安装，因此 IDE 用户应使用 skills 直装方式。无论采用哪种方式，不要同时安装同名插件和同名用户 skills，否则选择器里可能出现重复项。

## 二、共同前置条件

### 2.1 先做安装工具预检

打开 PowerShell，运行：

```powershell
$commands = "winget", "node", "npm", "git", "codex", "python", "pdfinfo", "pdftoppm"
$commands | ForEach-Object {
  [PSCustomObject]@{
    Command = $_
    Available = [bool](Get-Command $_ -ErrorAction SilentlyContinue)
  }
}
```

`False` 表示对应命令尚不可用。按下面各节补齐后，重新打开 PowerShell 并再次运行预检。

本教程优先使用 Windows 自带的 `winget`。如果 `winget` 不存在，请先在 Microsoft Store 安装或更新 **应用安装程序（App Installer）**；无法使用 Microsoft Store 时，从各软件官网下载安装包：

- Node.js LTS：<https://nodejs.org/en/download>
- Git for Windows：<https://git-scm.com/download/win>
- Python：<https://www.python.org/downloads/windows/>
- Poppler for Windows：<https://github.com/oschwartz10612/poppler-windows/releases>

使用官网安装包时，勾选把命令加入 `PATH` 的选项。安装完成后必须打开一个新的 PowerShell。

### 2.2 安装 Node.js、Git 和 Codex

Codex 的 npm 安装方式需要 Node.js 和 npm。先检查：

```powershell
node --version
npm --version
git --version
```

缺少 Node.js 或 Git 时运行：

```powershell
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Git.Git -e
```

重新打开 PowerShell，再安装或升级 Codex：

```powershell
npm install -g @openai/codex@latest
```

本教程按 Codex CLI `0.144.x` 验证，要求 `0.144.0` 或更高版本。确认版本和插件子命令都可用：


```powershell
codex --version
codex plugin --help
codex plugin marketplace --help
```

如果版本低于 `0.144.0`，或帮助中没有 `marketplace`、`add`、`list`、`remove` 子命令，请重新执行上面的升级命令后再继续。首次使用需登录：

```powershell
codex login
```

### 2.3 安装 Python

脚本需要 Python 3.9 或更高版本，推荐当前 Python 3：

```powershell
python --version
python -c "import sys; assert sys.version_info >= (3, 9), 'Python 3.9 or newer is required'"
```

如果 `python` 命令不存在，或第二条命令出现 `AssertionError`：

```powershell
winget install --id Python.Python.3.13 -e
```

安装后重新打开 PowerShell，并再次运行上面的两条检查。若 `python --version` 仍显示旧版本，打开 Windows 的 **管理应用执行别名**，关闭旧的 `python.exe` 别名，或把新版 Python 调整到用户 `PATH` 中旧版本之前；必须等版本断言无输出且退出成功后再继续。

### 2.4 安装 Poppler

扫描教材的页面定位与渲染需要 `pdfinfo` 和 `pdftoppm`：

```powershell
pdfinfo -v
pdftoppm -h
```

如果命令不存在：

```powershell
winget install --id oschwartz10612.Poppler -e
```

安装后重新打开 PowerShell，再运行上面的检查命令。

### 2.5 准备教材

本项目默认教材是周围主编、人民邮电出版社出版的《电路分析基础（第2版）》。将自己合法持有的 PDF 放在稳定位置，不要放进 `Circuit-skill` Git 仓库。例如：

```text
D:\Books\电路分析基础（第2版）周围.pdf
```

检查文件存在：

```powershell
$textbook = "D:\Books\电路分析基础（第2版）周围.pdf"
Test-Path -LiteralPath $textbook
```

应输出 `True`。为当前 PowerShell 临时设置教材路径：

```powershell
$env:CIRCUIT_TEXTBOOK_PDF = $textbook
```

永久写入当前 Windows 用户环境变量：

```powershell
[Environment]::SetEnvironmentVariable(
  "CIRCUIT_TEXTBOOK_PDF",
  $textbook,
  "User"
)
```

永久设置后必须完全关闭并重新打开 Codex、VS Code、CC-Switch 和终端，旧进程不会自动获得新变量。

本仓库适配的扫描版 SHA-256 为：

```text
24C6AE612A3969F9A4032B1CCEE6ED0333B672A042DC6441650CC05A57E6C62E
```

检查自己的文件：

```powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath $textbook).Hash
```

哈希一致时，书页与 PDF 页映射可以直接使用。哈希不一致不代表教材无效，但它不属于本仓库已经验证的扫描文件。此时仍可让 agent 使用教材，但必须先核对书名、版次、正文起始 PDF 页和正文末页，并在回答中把证据标为“版本待核验”；不要直接采用仓库预设页码。

## 三、正常版：安装完整插件

此方式适合 Codex CLI 和 ChatGPT 桌面版中的 Codex。

### 3.1 添加 Circuit Skill marketplace

在 PowerShell 中运行：

```powershell
codex plugin marketplace list
codex plugin marketplace add YanamiAnna6324/Circuit-skill --ref main
```

第一条命令用于检查是否已经添加。如果列表中已有 `circuit-skill`，不要重复添加，直接进入 3.2 节。如果添加命令报告同名 marketplace 已存在，也按此方式处理。

确认 marketplace 已加入：

```powershell
codex plugin marketplace list
```

列表中应出现名称 `circuit-skill`。

### 3.2 安装插件

先查看可安装插件：

```powershell
codex plugin list --available --json
```

若 `codex plugin list --json` 已把 `circuit-skill@circuit-skill` 显示为 `installed: true`，不要重复安装，直接进入验证步骤。

安装：

```powershell
codex plugin add circuit-skill@circuit-skill
```

确认安装状态：

```powershell
codex plugin list --json
```

应能看到 `pluginId` 为 `circuit-skill@circuit-skill`，且 `installed`、`enabled` 均为 `true`。该安装已经过隔离环境端到端测试，安装缓存中应包含全部 6 个 `SKILL.md`。

### 3.3 重新启动并验证

关闭当前 Codex 会话，启动一个新会话：

```powershell
codex
```

在交互界面中输入 `/skills`，或者输入 `$` 后搜索：

```text
solve-circuit-textbook
diagnose-circuit-answer
search-circuit-textbook
recognize-circuit-diagram
draw-circuit-diagram
review-circuit-exam
```

执行最小验证：

```text
使用 $diagnose-circuit-answer 检查：10 V 电源串联 2 kΩ 电阻，某答案认为电流为 5 A。定位错误并修正。
```

预期：指出遗漏 `k` 前缀导致 1000 倍错误，正确结果为 `5 mA`，并给出独立复验。

再验证教材路径：

```text
使用 $search-circuit-textbook 核验欧姆定律所在章节与书页，并报告教材文件哈希是否匹配。
```

### 3.4 在 ChatGPT 桌面版安装

1. 完成上面的 marketplace 添加操作。
2. 完全退出并重新打开 ChatGPT 桌面版。
3. 切换到 Codex，打开 **Plugins**。
4. 在来源中选择 **Circuit Skill**。
5. 打开 `circuit-skill`，选择 **Install** 或 **安装**。
6. 新建对话，在 skill 选择器中确认 6 个 skills 可用。

如果桌面版中没有 **Plugins** 入口，先使用 3.1 和 3.2 节的 CLI 命令安装，再完全重启桌面版；不要改用 IDE 直装步骤覆盖同名技能。

### 3.5 更新插件

先刷新远程 marketplace：

```powershell
codex plugin marketplace upgrade circuit-skill
```

如果已安装版本没有自动更新，重新安装：

```powershell
codex plugin remove circuit-skill@circuit-skill
codex plugin add circuit-skill@circuit-skill
```

随后重启 Codex。此插件没有账号连接器或远程状态，重新安装不会删除教材 PDF。

### 3.6 卸载插件

```powershell
codex plugin remove circuit-skill@circuit-skill
```

如果以后也不再使用该来源：

```powershell
codex plugin marketplace remove circuit-skill
```

教材环境变量需要单独删除：

```powershell
[Environment]::SetEnvironmentVariable(
  "CIRCUIT_TEXTBOOK_PDF",
  $null,
  "User"
)
```

## 四、正常版：IDE 扩展直接安装 skills

Codex IDE 扩展可以使用 skills，但不安装插件。当前 Codex 的用户级 skills 标准目录是：

```text
%USERPROFILE%\.agents\skills\
```

### 4.1 克隆仓库

如果没有 Git：

```powershell
winget install --id Git.Git -e
```

重新打开 PowerShell，然后运行：

```powershell
Set-Location $env:USERPROFILE
git clone https://github.com/YanamiAnna6324/Circuit-skill.git
```

若 `$env:USERPROFILE\Circuit-skill` 已存在，不要再次克隆；进入该目录运行 `git pull --ff-only` 后继续。

### 4.2 复制 6 个 skills

```powershell
$source = "$env:USERPROFILE\Circuit-skill\skills"
$target = "$env:USERPROFILE\.agents\skills"
$skillNames = @(
  "solve-circuit-textbook",
  "diagnose-circuit-answer",
  "search-circuit-textbook",
  "recognize-circuit-diagram",
  "draw-circuit-diagram",
  "review-circuit-exam"
)

New-Item -ItemType Directory -Force -Path $target | Out-Null

foreach ($name in $skillNames) {
  $sourcePath = Join-Path $source $name
  $destination = Join-Path $target $name
  if (-not (Test-Path -LiteralPath (Join-Path $sourcePath "SKILL.md"))) {
    throw "源 skill 无效：$sourcePath"
  }
  if (Test-Path -LiteralPath $destination) {
    throw "目标已存在，请先按 4.3 节更新，或按 4.4 节卸载：$destination"
  }
}

# 先完成全部检查，再复制，避免发现冲突时只装了一部分。
foreach ($name in $skillNames) {
  Copy-Item -LiteralPath (Join-Path $source $name) `
    -Destination (Join-Path $target $name) -Recurse
}
```

确认安装：

```powershell
$skillNames | ForEach-Object {
  $path = Join-Path $target $_
  [PSCustomObject]@{
    Skill = $_
    Valid = Test-Path -LiteralPath (Join-Path $path "SKILL.md")
  }
}
```

应显示 6 行且 `Valid` 全为 `True`。重启 VS Code 或 JetBrains IDE，并新建 Codex 对话。输入 `$` 或打开 skills 选择器确认技能可见。

### 4.3 更新直装 skills

进入克隆目录并拉取更新：

```powershell
Set-Location "$env:USERPROFILE\Circuit-skill"
git pull --ff-only
```

只备份并替换这 6 个目录：

```powershell
$source = "$env:USERPROFILE\Circuit-skill\skills"
$target = "$env:USERPROFILE\.agents\skills"
$backupRoot = Join-Path $env:USERPROFILE (
  "circuit-skill-backup-" + (Get-Date -Format "yyyyMMdd-HHmmss")
)
$skillNames = @(
  "solve-circuit-textbook",
  "diagnose-circuit-answer",
  "search-circuit-textbook",
  "recognize-circuit-diagram",
  "draw-circuit-diagram",
  "review-circuit-exam"
)

New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
foreach ($name in $skillNames) {
  $sourcePath = Join-Path $source $name
  if (-not (Test-Path -LiteralPath (Join-Path $sourcePath "SKILL.md"))) {
    throw "更新源无效：$sourcePath"
  }
}

foreach ($name in $skillNames) {
  $destination = Join-Path $target $name
  if (Test-Path -LiteralPath $destination) {
    Move-Item -LiteralPath $destination -Destination $backupRoot
  }
  Copy-Item -LiteralPath (Join-Path $source $name) `
    -Destination $destination -Recurse
}

Write-Output "备份位置：$backupRoot"
```

执行完后重新运行 4.2 节的六项验证。不要删除整个 `.agents\skills`，其中可能还有其他技能。更方便的长期更新方式是改用插件安装，或者使用下一节的 CC-Switch。

### 4.4 卸载直装 skills

先关闭 Codex 和 IDE，再只删除这 6 个已知目录：

```powershell
$target = [IO.Path]::GetFullPath("$env:USERPROFILE\.agents\skills")
$skillNames = @(
  "solve-circuit-textbook",
  "diagnose-circuit-answer",
  "search-circuit-textbook",
  "recognize-circuit-diagram",
  "draw-circuit-diagram",
  "review-circuit-exam"
)

foreach ($name in $skillNames) {
  $path = [IO.Path]::GetFullPath((Join-Path $target $name))
  if (-not $path.StartsWith($target + [IO.Path]::DirectorySeparatorChar)) {
    throw "拒绝删除目标目录外的路径：$path"
  }
  if (Test-Path -LiteralPath $path) {
    Remove-Item -LiteralPath $path -Recurse -Force
  }
}
```

教材 PDF、仓库克隆和环境变量不会被该命令删除。需要删除环境变量时，使用 3.6 节末尾的命令。

## 五、CC-Switch 版

以下步骤按 CC-Switch v3.13.0 及以上编写；建议使用最新版。v3.13.0 开始支持 skill 内容哈希更新检测、批量更新和源存储位置切换。

### 5.1 安装或升级 CC-Switch

只从以下官方来源下载：

- 官方网站：<https://ccswitch.io>
- GitHub Releases：<https://github.com/farion1231/cc-switch/releases>

Windows x64 用户选择：

- `CC-Switch-v{版本号}-Windows.msi`，正常安装版；或
- `CC-Switch-v{版本号}-Windows-Portable.zip`，绿色版。

启动 CC-Switch 后，在 **设置 → 关于** 中检查版本，并确认 Codex CLI 已被检测到。如果没有检测到，可以在该页面安装 Codex，或者先按本文 2.1 节安装。

### 5.2 确认 Codex 配置目录

1. 打开 **设置**，快捷键为 `Ctrl + ,`。
2. 找到 **高级 → 配置目录覆盖 → Codex 配置目录**。这里填写的是配置目录，不是 `codex.exe` 所在目录。
3. Codex 配置目录通常保持默认：

```text
C:\Users\你的用户名\.codex
```

4. 如果你设置了自定义 Codex 目录，确保启动 Codex 时也使用相同的 `CODEX_HOME`。
5. 修改目录后重启 CC-Switch 和 Codex。

检查当前终端使用的 Codex Home：

```powershell
if ($env:CODEX_HOME) {
  $env:CODEX_HOME
} else {
  "$env:USERPROFILE\.codex"
}
```

CC-Switch 显示的 Codex 目录与该结果不一致时，skills 可能被安装到另一个环境。

### 5.3 选择 skill 存储与同步方式

在 CC-Switch 的 **设置** 页面找到 **Skills 存储位置** 和 **Skills 同步方式**：

1. **源存储位置**推荐选择 `~/.agents/skills`，便于其他兼容 agent 共用；默认的 `~/.cc-switch/skills` 也可以。
2. **Skills 同步方式**优先选择 **软连接 / Symlink**。
3. Windows 因权限导致软链接失败时，改为 **复制 / Copy**。

这里有两层目录，作用不同：

| 目录 | 作用 |
|---|---|
| `~/.agents/skills` 或 `~/.cc-switch/skills` | CC-Switch 保存 skill 主副本的源存储，只选其中一个 |
| `<Codex 配置目录>/skills`，默认 `~/.codex/skills` | CC-Switch 为 Codex 分发出的应用目录 |

选择 `~/.agents/skills` 不会把 Codex 应用目录改名为 `.agents`；CC-Switch 仍会按同步方式分发到 `.codex/skills`。这是 CC-Switch v3.17 的兼容分发模型；手动直装仍应使用第 4 节的 Codex 标准用户目录 `.agents/skills`。不要手动修改 `~/.cc-switch/cc-switch.db`。

### 5.4 添加 Circuit-skill 仓库

1. 在 CC-Switch 顶部应用切换器中选择 **Codex**。
2. 打开顶部 **Skills** 页面。
3. 点击 **仓库管理**。
4. 点击 **添加仓库**。
5. CC-Switch v3.17 的 **仓库 URL** 填写：

```text
https://github.com/YanamiAnna6324/Circuit-skill
```

6. Branch 填写：

```text
main
```

7. 点击 **添加**。
8. 返回 Skills 页面，点击 **刷新**。

CC-Switch v3.13 至 v3.16 的旧界面可能显示 `Owner`、`Name`、`Branch` 和可选的 `Subdirectory`，此时分别填写：

```text
Owner: YanamiAnna6324
Name: Circuit-skill
Branch: main
Subdirectory: skills
```

CC-Switch 会递归扫描仓库中包含 `SKILL.md` 的目录，应报告“识别到 6 个技能”。v3.17 的 URL 表单不需要填写子目录；旧版若提供 `Subdirectory`，填写 `skills` 可以缩小扫描范围。

### 5.5 安装 6 个 skills

保持顶部应用切换器为 **Codex**，在发现页面的仓库过滤器中选择 `YanamiAnna6324/Circuit-skill`，然后逐个点击 **安装**：

| Skill | 主要用途 |
|---|---|
| `solve-circuit-textbook` | 教材优先总控解题 |
| `diagnose-circuit-answer` | 错题诊断与 agent 自检 |
| `search-circuit-textbook` | 教材定位、渲染和证据核验 |
| `recognize-circuit-diagram` | 题图拓扑识别 |
| `draw-circuit-diagram` | JSON 拓扑生成 SVG 电路图 |
| `review-circuit-exam` | 知识点、规律和考点复盘 |

`solve-circuit-textbook` 会调用其他 skills，因此建议全部安装。只安装总控而缺少依赖技能，会使完整工作流无法执行。

CC-Switch 的三个状态含义如下：

| 状态 | 判断位置 | 含义 |
|---|---|---|
| 已发现 | Skills 发现页面显示卡片 | 只说明远程仓库扫描成功 |
| 已安装 | 卡片显示“已安装”，主 Skills 面板出现该项 | 主副本已写入源存储 |
| Codex 已启用 | 主 Skills 面板中该 skill 的 **Codex** 开关已打开 | 已同步到 Codex 应用目录 |

从顶部选择 **Codex** 后安装，CC-Switch 会默认启用该 skill 的 Codex 开关。安装完成后返回主 Skills 面板，逐项确认 **Codex** 开关仍为打开；若关闭，手动打开。只有“已发现”而没有“已安装”不能使用，只有“已安装”但 Codex 开关关闭也不能在 Codex 中使用。

### 5.6 检查 CC-Switch 同步结果

以下命令检查 CC-Switch 的 Codex 应用目录，而不是 5.3 节的源存储目录：

```powershell
$codexHome = if ($env:CODEX_HOME) {
  $env:CODEX_HOME
} else {
  "$env:USERPROFILE\.codex"
}
$appSkillRoot = Join-Path $codexHome "skills"
$skillNames = @(
  "solve-circuit-textbook",
  "diagnose-circuit-answer",
  "search-circuit-textbook",
  "recognize-circuit-diagram",
  "draw-circuit-diagram",
  "review-circuit-exam"
)

if (-not (Test-Path -LiteralPath $appSkillRoot)) {
  throw "Codex skill 目录不存在；请检查 Codex 配置目录和 Codex 启用开关：$appSkillRoot"
}

$results = @($skillNames | ForEach-Object {
  $path = Join-Path $appSkillRoot $_
  $item = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue
  [PSCustomObject]@{
    Skill = $_
    Valid = Test-Path -LiteralPath (Join-Path $path "SKILL.md")
    LinkType = $item.LinkType
    Target = $item.Target
  }
})

$results | Format-Table -AutoSize
$missing = @($results | Where-Object { -not $_.Valid })
if ($missing.Count -gt 0) {
  throw "缺少或无效的 skills：$($missing.Skill -join ', ')"
}

Write-Output "CC-Switch 同步验证通过：6/6"
```

软链接方式通常会显示 `LinkType` 和 `Target`，复制方式这两列可能为空。成功条件不是“至少看到一项”，而是最后输出 `CC-Switch 同步验证通过：6/6`。

### 5.7 重启和功能验证

1. 完全关闭 Codex、VS Code 和相关终端。
2. 确认已设置 `CIRCUIT_TEXTBOOK_PDF`。
3. 重新启动 Codex。
4. 输入 `/skills`，或输入 `$` 搜索 `solve-circuit-textbook`。
5. 执行本文 3.3 节的单位错误测试和教材路径测试。

### 5.8 使用 CC-Switch 更新

1. 打开 **Skills** 页面。
2. 点击 **刷新** 重新扫描仓库，再点击 **检查更新**。
3. 出现 **有新版本** 标识后，点击单项 **更新**。
4. 有多个更新时，点击 **全部更新**。
5. 复制同步方式下确认应用目录已更新；软链接方式通常立即生效。
6. 新建 Codex 会话；仍显示旧内容时重启 Codex。

### 5.9 使用 CC-Switch 卸载与恢复

1. 在主 Skills 面板找到目标 skill。
2. 点击 **卸载** 并确认。
3. CC-Switch 会在 `~/.cc-switch/skill-backups/` 创建备份，并从所启用的应用目录移除该 skill。
4. 需要恢复时，使用 **从备份恢复**，选择对应名称和日期。

由于 6 个 skills 互相配合，完整卸载时应全部卸载。只卸载某个被总控依赖的 skill 会导致部分流程缺失。

全部卸载后若不再使用此来源，打开 **仓库管理**，删除 `YanamiAnna6324/Circuit-skill`。删除仓库配置不会自动卸载已安装技能，因此顺序应是先卸载 6 个 skills，再删除仓库。

## 六、常见问题

### 6.1 `$solve-circuit-textbook` 搜索不到

按顺序检查：

1. 新建 Codex 会话或重启 Codex。
2. 确认目标目录包含 `SKILL.md`。
3. 确认 Codex 与 CC-Switch 使用相同 `CODEX_HOME`。
4. 检查是否把整个仓库复制成一个 skill。正确结构必须是：

```text
skills\solve-circuit-textbook\SKILL.md
skills\diagnose-circuit-answer\SKILL.md
...
```

5. 正常插件版运行 `codex plugin list --json`。
6. CC-Switch 版确认 skill 对 Codex 已启用，而不是只对 Claude 或 Gemini 启用。

### 6.2 Agent 提示找不到教材

```powershell
$textbook = [Environment]::GetEnvironmentVariable(
  "CIRCUIT_TEXTBOOK_PDF",
  "User"
)

$textbook
Test-Path -LiteralPath $textbook
```

若最后一条返回 `False`，重新设置正确绝对路径。不要只设置包含教材的目录，变量值必须是 PDF 文件本身。若这里返回 `True`、但 agent 仍找不到教材，说明当前进程还没有读到新的用户变量；完全关闭并重新打开 Codex、IDE 和终端。

### 6.3 `pdftoppm` 或 `pdfinfo` 不存在

重新安装 Poppler并打开新终端：

```powershell
winget install --id oschwartz10612.Poppler -e
```

如果仍不存在，使用 `Get-Command pdftoppm` 检查是否已加入 `PATH`。官网下载 ZIP 的用户需要把包含 `pdftoppm.exe` 和 `pdfinfo.exe` 的 `Library\bin` 目录加入 Windows 用户 `PATH`，然后重新打开终端；不要只把 ZIP 解压后停在那里。

### 6.4 CC-Switch 添加仓库后显示 0 个 skills

1. 检查仓库 URL 拼写和网络连接。
2. Branch 必须为 `main`；旧版界面的 Subdirectory 填 `skills`。
3. 在浏览器打开 <https://github.com/YanamiAnna6324/Circuit-skill>，确认当前网络可访问 GitHub。
4. 点击 **刷新**。
5. 删除错误仓库配置后重新添加。
6. 更新到最新版 CC-Switch；若出现 HTTP 403/429，等待 GitHub 限流恢复，或在 **设置 → 代理** 配置可用代理。

### 6.5 Windows 软链接失败

在 CC-Switch 设置中把 Skills 同步方式改为 **复制 / Copy**。不需要为了安装 skills 关闭 Windows 安全功能或授予整个程序不必要的管理员权限。

### 6.6 出现两份同名 skill

通常是同时安装了插件版、`.agents\skills` 直装版或 CC-Switch 同步版。保留一种方式即可：

- 使用插件：删除或卸载用户级同名 skills；
- 使用 CC-Switch：卸载插件和手动复制版本，让 CC-Switch 作为单一管理入口；
- 使用 IDE 直装：卸载插件，并只保留 `.agents\skills` 中的一份。

用下面的命令定位可能的副本；它只读取文件，不会删除内容：

```powershell
$roots = @(
  "$env:USERPROFILE\.agents\skills",
  "$env:USERPROFILE\.codex\skills",
  "$env:USERPROFILE\.cc-switch\skills"
)

$roots | Where-Object { Test-Path -LiteralPath $_ } | ForEach-Object {
  Get-ChildItem -LiteralPath $_ -Directory -ErrorAction SilentlyContinue |
    Where-Object Name -in @(
      "solve-circuit-textbook",
      "diagnose-circuit-answer",
      "search-circuit-textbook",
      "recognize-circuit-diagram",
      "draw-circuit-diagram",
      "review-circuit-exam"
    ) |
    Select-Object -ExpandProperty FullName
}
```

注意：CC-Switch 选择 `.agents\skills` 作为源存储并软链接到 `.codex\skills` 时，两处路径是同一套受管安装，不应手动删掉其中一端。只有同时存在插件安装和独立直装、或存在不受 CC-Switch 管理的额外副本时才需要卸载。

### 6.7 marketplace 或 npm 下载失败

先分别测试 GitHub 和 npm：

```powershell
git ls-remote https://github.com/YanamiAnna6324/Circuit-skill.git HEAD
npm view @openai/codex version
```

第一条失败通常是 GitHub 网络、代理或证书问题；第二条失败通常是 npm registry 或代理问题。先修复网络后再重试，不要在下载未完成时手动拼装插件缓存。若 `npm install -g` 报权限错误，优先使用 Node.js 官方安装程序为当前用户修复安装，不要把整个终端长期以管理员身份运行。

### 6.8 marketplace 已添加但插件仍不可用

```powershell
codex plugin marketplace list
codex plugin list --available --json
codex plugin list --json
```

第一条必须列出 `circuit-skill`。未安装时，第二条应列出 `circuit-skill@circuit-skill`；安装后，它会从 `available` 移到第三条的 `installed` 列表。若 marketplace 指向错误来源，先运行 `codex plugin marketplace remove circuit-skill`，再按 3.1 节重新添加。

## 七、安装后推荐提示词

完整解题：

```text
使用 $solve-circuit-textbook 解答这道题。先识别并核验拓扑，优先使用教材方法，给出教材页码和独立自检，最后列出知识点、规律、考试要点、易错点和快速自检。
```

错题诊断：

```text
使用 $diagnose-circuit-answer 检查我的答案。定位第一个实质错误，区分错误传播与独立错误，从错误处重新解答，并用不同方法复验。
```

仅查询教材：

```text
使用 $search-circuit-textbook 查找戴维南定理。目录只用于定位，必须查看正文扫描页后再总结适用条件。
```

## 八、参考资料

- Codex Skills：<https://learn.chatgpt.com/docs/build-skills>
- Codex Plugins：<https://learn.chatgpt.com/docs/build-plugins>
- CC-Switch 官方仓库：<https://github.com/farion1231/cc-switch>
- CC-Switch Skills 文档：<https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/zh/3-extensions/3.3-skills.md>
- CC-Switch 安装文档：<https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/zh/1-getting-started/1.2-installation.md>

本文核对基准：Codex CLI `0.144.6`，CC-Switch `v3.17.0`（2026-07-13 发布）。标准插件流程已在隔离的 `CODEX_HOME` 中完成 marketplace 添加、插件安装和 6 个 `SKILL.md` 检查；CC-Switch 的界面名称、递归发现和目录行为已对照 v3.17.0 源码及官方手册核验。
