# Magicskills CLI Guide

本文档是 Magicskills 的使用文档，旨在详细介绍 Magicskills 项目的从安装到使用的一系列 CLI 命令。

## 1. 安装项目

方式一：从源码安装

```bash
git clone https://github.com/Narwhal-Lab/MagicSkills.git
cd MagicSkills
python -m pip install -e .
```

方式二：通过 PyPI 安装

```bash
pip install MagicSkills
```

当然你也可以安装在你的 conda 或者 uv 环境下，笔者使用的就是 conda 环境，当你安装成功后可以使用 `magicskills -h` 或 `magicskills --help` 来验证安装是否成功，安装成功时会出现如下信息。

```bash
(cli-guide) PS D:\example> magicskills -h
usage: magicskills [-h]
                   {listskill,readskill,execskill,syncskills,install,addskill,createskill_template,uploadskill,deleteskill,showskill,addskills,listskills,loadskills,deleteskills,saveskills,changetooldescription,changeclidescription,skill-tool}
                   ...

positional arguments:
  {listskill,readskill,execskill,syncskills,install,addskill,createskill_template,uploadskill,deleteskill,showskill,addskills,listskills,loadskills,deleteskills,saveskills,changetooldescription,changeclidescription,skill-tool}
    listskill           List skills from Allskills or one named skills collection
    readskill           Read by file path or skill name
    execskill           Execute command
    syncskills          Sync skills into AGENTS.md
    install             Install skills or skill from source or by skill name
    addskill            Register one skill into one collection
    createskill_template
                        Create a standard skill scaffold
    uploadskill         Upload one skill to repository (default settings)
    deleteskill         Delete a skill by one target (name or path)
    showskill           Show all content for one skill from Allskills
    addskills           Create a named skills collection
    listskills          List named skills collections
    loadskills          Load registry from disk
    deleteskills        Delete one or more named skills collections
    saveskills          Persist registry to disk
    changetooldescription
                        Update tool description on a skills collection
    changeclidescription
                        Update CLI description on a skills collection
    skill-tool          Run skill_tool action

options:
  -h, --help            show this help message and exit
```



## 2. CLI 命令总览与使用

| **命令**                  | **使用场景**                       | **主要能力**                                |
| ----------------------- | ------------------------------ | --------------------------------------- |
| `listskill`             | 查看当前内置技能集合里有哪些 skill           | 列出 skill 名称、描述、`SKILL.md` 路径            |
| `readskill`             | 读取 skill 说明或任意本地文本文件           | 按 skill 名称或文件路径输出内容                     |
| `execskill`             | 在当前工作目录执行命令                    | 支持流式输出、JSON 输出、无 shell 模式、自定义 skills 路径 |
| `syncskills`            | 把命名 skills 集合同步进 `AGENTS.md`   | 生成或替换 `<skills_system>` 区块              |
| `install`               | 从本地目录、Git 仓库或默认技能仓库安装 skill    | 复制 skill 文件并注册到 `Allskills`             |
| `addskill`              | 把一个现成的 skill 注册到某个集合中          | 不复制文件，只注册元数据                            |
| `createskill_template`  | 创建一个 skill 的简易模板               | 生成后可修改其中内容                              |
| `uploadskill`           | 把本地 skill 提交到默认 MagicSkills 仓库 | 自动走 fork、push、PR 流程                     |
| `deleteskill`<br />     | 从某个集合中删除一个 skill，或全局删除         | 从命名集合中移除，或从 `Allskills` 删除目录并清理引用       |
| `showskill`             | 审查一个 skill 的完整内容               | 显示元信息和 skill 目录下所有文件内容                  |
| `addskills`             | 创建一个命名 skills 集合               | 为 agent 或团队建立独立 skill 集合                |
| `listskills`            | 查看所有命名 skills 集合               | 普通文本或 JSON 输出                           |
| `loadskills `           | 列出指向的 `JSON` 文件中的 `skills` 信息  | 普通文本或 JSON 输出                           |
| `deleteskills`          | 删除一个命名 skills 集合               | 只删除集合注册，不删除 skill 文件                    |
| `  saveskills   `       | 将 skills 集合，保存到 JSON 文件        | 复制 Allskills 的信息                        |
| `changetooldescription` | 修改集合的 `tool_description` 元数据   | 更新面向 tool 的描述，便于后续查询与外部集成               |
| `changeclidescription`  | 修改集合的 `cli_description` 元数据    | 更新面向 CLI 的描述，便于后续查询与外部集成                |
| `skill-tool`            | 以 tool function 风格调用 skill 能力  | 用统一 JSON 输出做 list/read/exec 分发          |

### 注意

以下命令的使用，必须在安装了 skill 的前提下进行，即，最起码你已经创建了 Allskills【记录所有你通过 install 命令安装的 skill，本质上是一个 json 文件，保存在 \~/.magicskills/collection.json 中】，如果你未安装任何 skill ，请先阅读 `2.5 install `

### 2.1 listskill&#x20;

**作用**：列出某个命名（已注册）的 skills 集合里的 skill，依次列出每个 skill 的name、description、path（指向该 skill 的 SKILL.md），输出结果按 skill 名称字母顺序排序

**格式**：

```bash
magicskills listskill [--name <collection-name>]
```

* `--name <collection-name>`：注册的 skills 集合的名称。可以传入你自己用 addskills 命令创建的 skills，当然可以不传，此时使用 `Allskills`

**使用实例：**

```bash
(cli-guide) PS D:\example> magicskills listskill
1. name: algorithmic-art
   description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.
   path: C:\Users\13978\allskills\algorithmic-art\SKILL.md

......（篇幅有限，此处省略 30 余行）

13. name: doc-coauthoring
   description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
```

例如，example-skills 是笔者使用 addskills 命令 (2.11 addskills)创建的 skills 集合，同样可以使用 listskill 列出其中的 skill

```bash
(cli-guide) PS D:\example> magicskills listskill --name example-skills
1. name: c_2_ast
   description: Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).
   path: D:\example\.agent\skills\c_2_ast\SKILL.md
2. name: xlsx
   description: Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
   path: C:\Users\13978\allskills\xlsx\SKILL.md
```

### 2.2 readskill&#x20;

**作用：**&#x5F53;你知道某个 skill 名称，或者是其 `SKILL.md` 的路径，想直接查看它的 `SKILL.md` 的内容；或者你想借这个命令顺手读取任意一个本地文件，可以使用 readskill 命令，相当于是 cat 命令

**格式：**

```bash
magicskills readskill <path>
```

* `<path>`：可以是文件路径，也可以是 `Allskills` 中的 skill 名称。

  * 当传入 skill 名称时，命令会读取对应 skill 目录下的 `SKILL.md`。

  * 如果出现多个同名 skill ，必须改为传具体文件路径，例如 `./skills/demo/SKILL.md`。

  * 当传入的是显式路径时，目标必须是文件，不能是目录。

**使用实例：**

出于篇幅限制，省略了如下命令的输出内容，只保留首尾几行内容

```bash
(cli-guide) PS D:\example> magicskills readskill docx
---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

## Overview

A .docx file is a ZIP archive containing XML files.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `pandoc` or unpack for raw XML |
| Create new document | Use `docx-js` - see Creating New Documents below |
| Edit existing document | Unpack → edit XML → repack - see Editing Existing Documents below |

......（此处省略 400 余行）

## Dependencies

- **pandoc**: Text extraction
- **docx**: `npm install -g docx` (new documents)
- **LibreOffice**: PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for images
```

同样的，你也可以传入其具体的 SKILL.md 文件路径，笔者是 `magicskills readskill "D:\\example\\.claude\\skills\\docx\\SKILL.md"`，输出内容和上文一致，不赘述

### 2.3 execskill&#x20;

**作用**：保持调用方式和 MagicSkills 体系一致的同时，在当前工作目录执行一条命令；这条命令也适合给 agent 或自动化脚本暴露统一的执行入口。

**格式：**

```bash
magicskills execskill [--no-shell] [--json] [--paths [PATHS ...]] -- <command>
```

* `<command>`：要执行的子命令字符串，建议写在 `--` 后面，如果没写 `--` 仍然可以执行，但是一定要在前三个参数列表的后面。

* `--no-shell`：默认是通过系统 shell 执行命令，使用时，关闭 shell 模式，内部会对命令做 `shlex.split()`，更适合直接执行可执行文件及其参数。

* `--json`：不直接流式打印终端输出，而是返回 JSON，字段包含 `command`、`returncode`、`stdout`、`stderr`。

* `--paths [PATHS ...]`：指定自定义 skill 搜索路径，使用后会加载这些路径下的 skill 构建临时的 `Skills` 集合，然后再执行命令。

**使用实例：**

笔者使用的是Windows系统

```bash
(cli-guide) PS D:\example> magicskills execskill -- dir
 驱动器 D 中的卷是 新加卷
 卷的序列号是 105E-7D2B

 D:\example 的目录

2026/03/24  16:04    <DIR>          .
2026/03/23  20:44    <DIR>          .agent
2026/03/23  20:38    <DIR>          .claude
2026/03/23  21:30    <DIR>          c_2_ast
2026/03/23  21:26    <DIR>          exa_skills
2026/03/24  16:04                20 hello.py
               1 个文件             20 字节
               5 个目录 273,338,122,240 可用字节
```

```bash
(cli-guide) PS D:\example> magicskills execskill --no-shell -- python hello.py
hello world
```

```sql
(cli-guide) PS D:\example> magicskills execskill --json --no-shell -- python hello.py
{
  "command": "python hello.py",
  "returncode": 0,
  "stdout": "hello world\n",
  "stderr": ""
}
```

```bash
(cli-guide) PS D:\example> magicskills execskill --paths ./.claude/skills  -- python hello.py
hello world
```

```sql
(cli-guide) PS D:\example> magicskills execskill --paths ./.claude/skills --no-shell --json -- python hello.py
{
  "command": "python hello.py",
  "returncode": 0,
  "stdout": "hello world\n",
  "stderr": ""
}
```

### 2.4 syncskills&#x20;

**作用：**&#x5BF9;于你已经创建好&#x7684;**&#x20;**&#x73;kills 集合，此命令可以帮助你把它同步到某个 `AGENTS.md` 文件里，主要用于让 agent（如 ClaudeCode、Cursor等） 在系统提示中感知这些 skills

**格式：**

```bash
magicskills syncskills <name> [-o OUTPUT] [--mode {none,cli_description}] [-y]
```

* `<name>`：使用的 skills 集合名称。

* `-o, --output`：AGETNS.md 的输出文件路径，不传时使用该集合自己的 `agent_md_path`。

* `--mode`：同步渲染模式，默认为 `none`模式

  * `none`：保持 `<usage> + <available_skills>` 结构。适合能够根据 `AGENTS.md` 中给出的 skill 信息列表直接发现并使用对应 skill 的 agent

  * `cli_description`：只输出 `<usage>`，内容来自集合的 `cli_description`，适合不能根据 `AGENTS.md` 中给出的 skill 信息列表直接使用 skill、需要通过 `magicskills skill-tool` 的 CLI 说明来使用 skill 的 agent

* `-y, --yes`：命令会跳出是否继续的确认，使用 `-y` 跳过交互确认，直接同步。

**使用实例：**

```bash
(cli-guide) PS D:\example> magicskills syncskills example-skills
Sync 2 skills to D:\example\AGENTS.md? [y/N] y
Synced to D:\example\AGENTS.md

(cli-guide) PS D:\example> magicskills syncskills example-skills -y
Synced to D:\example\AGENTS.md
```

此时 `AGETNS.md` 的内容如下：

```markdown
# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively.

How to use skills:
First, read the SKILL.md file in the corresponding path of the skill. Then, based on its content, decide whether to read more related docs or execute the relevant command or script.

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
</usage>

<available_skills>

<skill>
<name>c_2_ast</name>
<description>Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).</description>
<path>D:\example\.agent\skills\c_2_ast</path>
</skill>

<skill>
<name>xlsx</name>
<description>Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.</description>
<path>C:\Users\13978\allskills\xlsx</path>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
```

`magicskills syncskills example-skills --mode cli_description` 执行后，

`AGETNS.md` 内容如下：

```markdown
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Whenever you receive a task, you must first run "magicskills skill-tool listskill --name example-skills" to view all available skills.
Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's SKILL.md file by path.
Based on that documentation, either continue reading more files with "magicskills skill-tool readskill --arg <file_path>" or run the needed command with "magicskills skill-tool execskill --arg <command>".
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>
```

当然你也可以指定输出的文件路径

```bash
(cli-guide) PS D:\example> magicskills syncskills example-skills -o ./target_path/AGENT.md
Sync 2 skills to ./target_path/AGENT.md? [y/N] y
Synced to D:\example\target_path\AGENT.md
```



### 2.5 install&#x20;

**作用**：把 skill 安装到当前项目或全局目录中，在安装的同时，安装好的 skill 路径会同步在 Allskills 中。skill 可以来源于内置的默认仓库，也可以指定远程仓库（下载此仓库中的所有 skill），也可以你本地目录下的 skill

**格式**：

```bash
magicskills install <source> [--global] [--universal] [-t TARGET] [-y]
```

* `<source>`：skill 的来源地址

  * skill 名称：例如 `c_2_ast`。此时会克隆默认仓库 `https://github.com/Narwhal-Lab/MagicSkills.git`，然后安装同名 skill 到目标路径。

  * GitHub 仓库短写：例如 anthropics 的官方skill 仓库`anthropics/skills`，命令会转成 `https://github.com/anthropics/skills.git` 并安装仓库内所有包含 `SKILL.md` 的 skill 目录到目标路径。

  * Git URL：例如 https://github.com/anthropics/skills.git 或 git@github.com:anthropics/skills.git。

  * 本地路径：可以是单个 skill 目录（例如 c\_2\_ast)，也可以是包含多个 skill 的根目录（例如 exa\_skills，里面笔者放置了 c\_2\_ast 和 brand-guidelines 两份 skill)，命令会递归查找所有含 `SKILL.md` 的 skill 目录

* 目标目录：

  * `--global`：把安装根目录切到用户 Home，即，\~\\.claude\skills 的文件夹中。

  * `--universal`：当前路径下的 `.agent/skills` 文件夹中。

  * `-t, --target`：自定义安装目录；**不能和 `--global` 或 `--universal` 同时使用**。

* `-y, --yes`：如果目标目录中已经存在同名 skill，不管该目录下的具体代码是否相同，直接覆盖；但当同名 skill 存在在目标目录下，若不使用`-y , --yes`，会报错

**使用实例**：

1. `<source>` 指定 skill 名称：`magicskills install c_2_ast`

```bash
(cli-guide) PS D:\example> magicskills install c_2_ast
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmpq9idgolo'...
remote: Enumerating objects: 190, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (144/144), done.
remote: Total 190 (delta 53), reused 130 (delta 36), pack-reused 0 (from 0)
Receiving objects: 100% (190/190), 4.98 MiB | 4.11 MiB/s, done.
Resolving deltas: 100% (53/53), done.
Installed: D:\example\.claude\skills\c_2_ast
```

```bash
(cli-guide) PS D:\example> magicskills install c_2_ast --global
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmpg6q1zed1'...
remote: Enumerating objects: 190, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (144/144), done.
remote: Total 190 (delta 53), reused 130 (delta 36), pack-reused 0 (from 0)
Receiving objects: 100% (190/190), 4.98 MiB | 1.47 MiB/s, done.
Resolving deltas: 100% (53/53), done.
Installed: C:\Users\13978\.claude\skills\c_2_ast
```

```bash
(cli-guide) PS D:\example> magicskills install c_2_ast --universal
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmpss8kgzrd'...
remote: Enumerating objects: 190, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (144/144), done.
remote: Total 190 (delta 53), reused 130 (delta 36), pack-reused 0 (from 0)
Receiving objects: 100% (190/190), 4.98 MiB | 2.89 MiB/s, done.
Resolving deltas: 100% (53/53), done.
Installed: D:\example\.agent\skills\c_2_ast
```

```bash
(cli-guide) PS D:\example> magicskills install c_2_ast -t ~/allskills
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmph6jskr37'...
remote: Enumerating objects: 190, done.
remote: Counting objects: 100% (190/190), done.
remote: Compressing objects: 100% (144/144), done.
remote: Total 190 (delta 53), reused 130 (delta 36), pack-reused 0 (from 0)
Receiving objects: 100% (190/190), 4.98 MiB | 2.93 MiB/s, done.
Resolving deltas: 100% (53/53), done.
Installed: C:\Users\13978\allskills\c_2_ast
```

* `<source>`指定 Github 仓库短写： `anthropics/skills`

```bash
(cli-guide) PS D:\example> magicskills install anthropics/skills
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmpkyxz4ig4'...
remote: Enumerating objects: 323, done.
remote: Counting objects: 100% (323/323), done.
remote: Compressing objects: 100% (248/248), done.
remote: Total 323 (delta 56), reused 290 (delta 56), pack-reused 0 (from 0)
Receiving objects: 100% (323/323), 3.03 MiB | 4.62 MiB/s, done.
Resolving deltas: 100% (56/56), done.
Installed: D:\example\.claude\skills\algorithmic-art
Installed: D:\example\.claude\skills\brand-guidelines
Installed: D:\example\.claude\skills\canvas-design
Installed: D:\example\.claude\skills\claude-api
Installed: D:\example\.claude\skills\doc-coauthoring
Installed: D:\example\.claude\skills\docx
Installed: D:\example\.claude\skills\frontend-design
Installed: D:\example\.claude\skills\internal-comms
Installed: D:\example\.claude\skills\mcp-builder
Installed: D:\example\.claude\skills\pdf
Installed: D:\example\.claude\skills\pptx
Installed: D:\example\.claude\skills\skill-creator
Installed: D:\example\.claude\skills\slack-gif-creator
Installed: D:\example\.claude\skills\theme-factory
Installed: D:\example\.claude\skills\web-artifacts-builder
Installed: D:\example\.claude\skills\webapp-testing
Installed: D:\example\.claude\skills\xlsx
Installed: D:\example\.claude\skills\template
```

\--global、--universal、-t 的使用与实例 1 大致相同，不赘述；



* `<source>`指定 Github 仓库：https://github.com/anthropics/skills.git 或者 git@github.com:anthropics/skills.git

```bash
(cli-guide) PS D:\example> magicskills install https://github.com/anthropics/skills.git
Cloning into 'C:\Users\13978\AppData\Local\Temp\tmpcnew8zfh'...
remote: Enumerating objects: 323, done.
remote: Counting objects: 100% (323/323), done.
remote: Compressing objects: 100% (248/248), done.
remote: Total 323 (delta 56), reused 290 (delta 56), pack-reused 0 (from 0)
Receiving objects: 100% (323/323), 3.03 MiB | 7.32 MiB/s, done.
Resolving deltas: 100% (56/56), done.
Installed: D:\example\.claude\skills\algorithmic-art
Installed: D:\example\.claude\skills\brand-guidelines
Installed: D:\example\.claude\skills\canvas-design
Installed: D:\example\.claude\skills\claude-api
Installed: D:\example\.claude\skills\doc-coauthoring
Installed: D:\example\.claude\skills\docx
Installed: D:\example\.claude\skills\frontend-design
Installed: D:\example\.claude\skills\internal-comms
Installed: D:\example\.claude\skills\mcp-builder
Installed: D:\example\.claude\skills\pdf
Installed: D:\example\.claude\skills\pptx
Installed: D:\example\.claude\skills\skill-creator
Installed: D:\example\.claude\skills\slack-gif-creator
Installed: D:\example\.claude\skills\theme-factory
Installed: D:\example\.claude\skills\web-artifacts-builder
Installed: D:\example\.claude\skills\webapp-testing
Installed: D:\example\.claude\skills\xlsx
Installed: D:\example\.claude\skills\template
```

git@github.com:anthropics/skills.git 的输入结果和 https 格式的结果一致，不赘述；

\--global、--universal、-t 的使用与实例 1 大致相同，不赘述；



* `<source>` 指定本地路径："D:\example\c\_2\_ast"（可以不用双引号），以及 "D:\example\exa\_skills"

```bash
(cli-guide) PS D:\example> magicskills install "D:\example\c_2_ast"
Installed: D:\example\.claude\skills\c_2_ast
```

```bash
(cli-guide) PS D:\example> magicskills install "D:\example\exa_skills"
Installed: D:\example\.claude\skills\brand-guidelines
Installed: D:\example\.claude\skills\c_2_ast
```

\--global、--universal、-t 的使用与实例 1 大致相同，不赘述；



* `-y , --yes`

```bash
(cli-guide) PS D:\example> magicskills install "D:\example\c_2_ast"
install failed: Skill 'c_2_ast' already exists at D:\example\.claude\skills\c_2_ast
Hint: rerun with -y/--yes to overwrite the existing skill directory.
Hint: use -t/--target to install into a different directory.
(cli-guide) PS D:\example> magicskills install "D:\example\c_2_ast" -y
Installed: D:\example\.claude\skills\c_2_ast
```

### 2.6 `addskill`

**作用：**&#x628A;现成的 skill，注册进某个 `skills` 集合中，注册成功后可以通过 `listskill`命令查看

**格式：**

```bash
magicskills addskill <target> [--source SOURCE] [--name COLLECTION]
```

* `<target>`：可以是 skill 目录路径（该路径可以不在 `Allskills`中），也可以是内置 `Allskills` 中已可解析的 skill 名称。

* `--source`：可选，给这个 skill 记录来源信息；不传时默认记录 skill 所在父目录的绝对路径。

* `--name`：可选，目标 skills 集合名称；不传时默认注册到内置 `Allskills`。

**使用实例：**

由于未指定 `--name` 的内容，所以效果相当于是将 `skill`注册到 `Allskills` 中

```bash
(cli-guide) PS D:\example> magicskills addskill ./.claude/skills/docx
Registered: D:\example\.claude\skills\docx
```

可以使用 --source 传递来源，此时依然是注册到 `Allskills` 中

```bash
(cli-guide) PS D:\example> magicskills addskill ./.claude/skills/docx --source https://github.com/anthropics/skills.git
Registered: D:\example\.claude\skills\docx
```

或者注册到指定的、你已经用 `addskills` 命令创建好的 `skills` 集合中

```bash
(cli-guide) PS D:\example> magicskills addskill ./.claude/skills/docx --source https://github.com/anthropics/skills.git --name example-skills
Registered: D:\example\.claude\skills\docx
```

### 2.7 `createskill_template`

**作用：**&#x521B;建一个 skill 的简易模板

**格式：**

```bash
magicskills createskill_template <name> <base_dir>
```

* `name`：位置参数，意为要创建的 skill 的名称

* `base_dir`：位置参数，意为 skill 要存放的根目录，可以传入相对或绝对路径

**使用实例：**

创建一个名为 name 的 skill 在 exa\_skills 目录下

```bash
(cli-guide) PS D:\example> magicskills createskill_template  name  exa_skills
Created template: exa_skills\name
```

当 `name` 和 `base_dir` 中包含空格时，需要使用 ""&#x20;

```bash
(cli-guide) PS D:\example> magicskills createskill_template  "na me"  exa_skills
Created template: exa_skills\na me

(cli-guide) PS D:\example> magicskills createskill_template  "na me"  "D:\example\exa_ski lls"
Created template: D:\example\exa_ski lls\na me
```

### 2.8 `uploadskill`

**作用**：将本地的 skill，创建 Pull Request，把它自动提交到默认 [MagicSkills 仓库](https://github.com/Narwhal-Lab/MagicSkills)

**格式：**

```bash
magicskills uploadskill <source>
```

* `<source>`：可以是 `Allskills` 中的 skill 名称，也可以是本地 skill 目录路径。如果同名 skill 在 `Allskills` 中有多个，必须改传 skill 目录路径。

**使用实例：**

如果你之前没有安装过 gh ，你会先遇到如下情况，安装完成后你需要刷新你的 PATH 或者直接新开一个终端

```bash
(cli-guide) PS D:\example> magicskills uploadskill "D:\\example\\.claude\\skills\\pdf"
GitHub CLI (gh) is missing. Install now and continue upload? [Y/n] y
已找到 GitHub CLI [GitHub.cli] 版本 2.88.1
此应用程序由其所有者授权给你。
Microsoft 对第三方程序包概不负责，也不向第三方程序包授予任何许可证。
正在下载 https://github.com/cli/cli/releases/download/v2.88.1/gh_2.88.1_windows_amd64.msi
  ██████████████████████████████  13.6 MB / 13.6 MB
已成功验证安装程序哈希
正在启动程序包安装...
已成功安装
Failed to auto-install gh. Details: winget: install command completed but gh still not found
GitHub CLI (gh) is not installed yet.
`gh` CLI not found. Install GitHub CLI and run `gh auth login` first.
```

然后重新输入上传指令，按照引导登录你的 Github 账号，即可 PR 成功

### 2.9 `deleteskill`

**作用：**&#x628A;某个 skill 从某个集合里移除，或者从内置 `Allskills` 里彻底删除

**格式：**

```bash
magicskills deleteskill <target> [--name COLLECTION]
```

* `<target>`：可以是 skill 名称，也可以是 skill 目录路径。

  * 当指向的 skills 集合中有多个同名的 skil，必须传入具体路径

* `--name`：可选，目标 skills 集合名称；不传时默认作用于 `Allskills`

  * 当作用于 `Allskills` 时，删除会直接移除实际 skill 目录下的具体文件，且不会二次确认。

  * 从 `Allskills` 删除成功，而其他 skills 集合里也引用了同一路径的 skill，这些集合中的对应项也会一起被剔除。

  * 当作用于其他 skills 集合时，只会把 skill 从该集合中移除；skill 目录下的文件和 `Allskills` 中的记录都会保留。

**实例使用：**

执行如下命令后，可以看到相应的 `skill` 文件夹已经删除，且在 `Allskills` 中也删除了对应路径（你可以直接进入 \~\\.magicskills\collections.json 中查看）

```bash
(cli-guide) PS D:\example> magicskills deleteskill "D:\\example\\.claude\\skills\\brand-guidelines"
Deleted: D:\example\.claude\skills\brand-guidelines
(cli-guide) PS D:\example> cd D:\example\.claude\skills\brand-guidelines
cd : 找不到路径“D:\example\.claude\skills\brand-guidelines”，因为该路径不存在。
```

执行如下命令后，可见文件路径依然保留

```bash
(cli-guide) PS D:\example> magicskills deleteskill "D:\\example\\.claude\\skills\\docx" --name example-skills
Deleted: D:\example\.claude\skills\docx
(cli-guide) PS D:\example> cd D:\example\.claude\skills\docx
(cli-guide) PS D:\example\.claude\skills\docx>
```

### 2.10 `showskill`

**作用：**&#x5BA1;查一个 skill 中的所有文件，这在 code review、提交流程、排查二进制文件或检查脚本入口时很有用

**格式：**

```bash
magicskills showskill <target>
```

* `<target>`：可以是 skill 名称，也可以是 skill 目录路径

  * 必须是注册进 `Allskills`中的 `skill`，且有多个同名 `skill`，则必须传入 `skill`的目录路径

**实例使用：**

命令会先展示 skill 概览，包括名称、描述、skill 目录、base\_dir、`SKILL.md` 路径和安装来源，然后会展示 skill 目录下的所有文件内容。如果遇到二进制文件，会显示 `[binary file omitted: <size> bytes]`，不会直接打印乱码。

例如笔者在 `2.7 createskill_template` 创建的名为 `name`的 `skill`，展示信息如下，将命令中的 name 改为 D:\example\exa\_skills\name 或 "D:\example\exa\_skills\name" 是一样的效果

```yaml
(cli-guide) PS D:\example> magicskills showskill name
+----------------------------------------------------------------------------------------------+
| Skill Overview                                                                               |
+----------------------------------------------------------------------------------------------+
| Skill: name                                                                                  |
| Description:                                                                                 |
| Skill directory: D:\example\exa_skills\name                                                  |
| Skills root (base_dir): D:\example\exa_skills                                                |
| SKILL.md path: D:\example\exa_skills\name\SKILL.md                                           |
| Install source: D:\example\exa_skills\name                                                   |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Files                                                                                        |
+----------------------------------------------------------------------------------------------+
| Total files: 1                                                                               |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| File 1/1: SKILL.md                                                                           |
+----------------------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------------------+
---
name: name
description:
---

# Overview

Describe the skill here.

------------------------------------------------------------------------------------------------
```

### 2.11 `addskills`

**作用：**&#x521B;建 skills 集合

**格式：**

```bash
magicskills addskills <name> [--skill-list [SKILLS ...]] [--paths [PATHS ...]] [--tool-description TEXT] [--cli-description TEXT] [--agent-md-path PATH]
```

* `<name>`：新 skills 集合名称

* `--skill-list [SKILLS ...]`：显式指定要纳入集合的 skill，每一项都可以是 skill 名称或 skill 目录路径，底层会从 `Allskills` 里解析。

  * 当有多个同名 skill 时必须传入目标路径（此时和 `--paths` 的效果是一样的）

* `--paths [PATHS ...]`：把这些路径对应的 skills 或者是 skill 纳入新集合。

  * 传某个 skill 目录路径，例如 `./.claude/skills/demo`

  * 传某个 skills 根目录，例如 `./.claude/skills`

  * **注意**：`--skill-list` 和 `--paths` 不能同时使用

* `--tool-description`：覆盖该集合的 `tool_description` 元数据。

* `--cli-description`：覆盖该集合的 `cli_description` 元数据。

* `--agent-md-path`：指定该集合在使用默认 `syncskills` 同步到哪个 `AGENTS.md` 文件。

  * 不使用时，默认是记录你输入命令时所处目录下的 `AGENTS.md` 路径

**实例使用：**

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
```

使用 `--skill-list` 传入名字和路径

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills --skill-list docx name
Created skills instance: example-skills
Skills count: 2
(cli-guide) PS D:\example> magicskills deleteskills example-skills
Deleted skills instance: example-skills
(cli-guide) PS D:\example> magicskills addskills example-skills --skill-list "D:\\example\\.claude\\skills\\pdf" "D:\\example\\.claude\\skills\\pptx"
Created skills instance: example-skills
Skills count: 2
```

使用`--paths [PATHS ...]`

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills --paths "D:\\example\\.claude\\skills\\pdf" "D:\\example\\.claude\\skills\\pptx"
Created skills instance: example-skills
Skills count: 2
(cli-guide) PS D:\example> magicskills deleteskills example-skills
Deleted skills instance: example-skills
(cli-guide) PS D:\example> magicskills addskills example-skills --paths "D:\\example\\.claude\\skills\\pdf" "D:\\example\\.claude\\skills"
Created skills instance: example-skills
Skills count: 18
```

在不使用 `--tool-description` 和 `--cli-description` 和 `--agent-md-path` 时，创建的 example-skills 中对应元数据内容如下：

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
 {
  "collections": {
    "example-skills": {
      "paths": [],
      "tool_description": "Unified skill tool. First use \"listskill\" to find relevant skills. \nThen use \"readskill\" to read the selected skill's SKILL.md or related docs. \nIf needed, use \"execskill\" to run the command.\n\n\nInput format:\n{\n    \"action\": \"<action_name>\",\n    \"arg\": \"<string argument>\"\n}\n\nActions:\n- listskill\n- readskill: arg = file path\n- execskill: arg = full command string",
      "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
      "agent_md_path": "D:\\example\\AGENTS.md"
    }
  }
}
```

使用后，对应信息会进行修改

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills  --tool-description "Just a test for tool description" --cli-description "Just test for cli description" --agent-md-path ./test/AGENTS.md
Created skills instance: example-skills
Skills count: 0
{
  "collections": {
    "example-skills": {
      "paths": [],
      "tool_description": "Just a test for tool description",
      "cli_description": "Just test for cli description",
      "agent_md_path": "D:\\example\\test\\AGENTS.md"
    }
  }
}
```

### 2.12 `listskills`

**作用：**&#x5217;出已经注册了的 skills 集合

**格式：**

```bash
magicskills listskills [--json]
```

* `--json`：以 JSON 数组输出；不传时输出人类可读的盒状文本。

**实例使用：**

```bash
(cli-guide) PS D:\example> magicskills listskills
+----------------------------------------------------------------------------------------------+
| MagicSkills Collections                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 2                                                                         |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Collection Allskills                                                                         |
+----------------------------------------------------------------------------------------------+
| - name: Allskills                                                                            |
| skills: 39                                                                                   |
| agent_md_path: D:\example\AGENTS.md                                                          |
| paths: C:\Users\13978\allskills\algorithmic-art, C:\Users\13978\allskills\brand-guidelines,  |
| C:\Users\13978\allskills\canvas-design, C:\Users\13978\allskills\claude-api,                 |
| C:\Users\13978\allskills\doc-coauthoring, C:\Users\13978\allskills\frontend-design,          |
| C:\Users\13978\allskills\internal-comms, C:\Users\13978\allskills\mcp-builder,               |
| C:\Users\13978\allskills\pdf, C:\Users\13978\allskills\pptx,                                 |
| C:\Users\13978\allskills\skill-creator, C:\Users\13978\allskills\slack-gif-creator,          |
| C:\Users\13978\allskills\theme-factory, C:\Users\13978\allskills\web-artifacts-builder,      |
| C:\Users\13978\allskills\webapp-testing, C:\Users\13978\allskills\xlsx,                      |
| C:\Users\13978\allskills\template, C:\Users\13978\.claude\skills\c_2_ast,                    |
| D:\example\.agent\skills\c_2_ast, C:\Users\13978\allskills\c_2_ast,                          |
| D:\example\.claude\skills\algorithmic-art, D:\example\.claude\skills\canvas-design,          |
| D:\example\.claude\skills\claude-api, D:\example\.claude\skills\doc-coauthoring,             |
| D:\example\.claude\skills\frontend-design, D:\example\.claude\skills\internal-comms,         |
| D:\example\.claude\skills\mcp-builder, D:\example\.claude\skills\pdf,                        |
| D:\example\.claude\skills\pptx, D:\example\.claude\skills\skill-creator,                     |
| D:\example\.claude\skills\slack-gif-creator, D:\example\.claude\skills\theme-factory,        |
| D:\example\.claude\skills\web-artifacts-builder, D:\example\.claude\skills\webapp-testing,   |
| D:\example\.claude\skills\xlsx, D:\example\.claude\skills\template,                          |
| D:\example\.claude\skills\c_2_ast, D:\example\.claude\skills\docx,                           |
| D:\example\exa_skills\name                                                                   |
| tool_description: Unified skill tool. First use "listskill" to find relevant skills.         |
|   Then use "readskill" to read the selected skill's SKILL.md or related docs.                |
|   If needed, use "execskill" to run the command.                                             |
|                                                                                              |
|                                                                                              |
|   Input format:                                                                              |
|   {                                                                                          |
|       "action": "<action_name>",                                                             |
|       "arg": "<string argument>"                                                             |
|   }                                                                                          |
|                                                                                              |
|   Actions:                                                                                   |
|   - listskill                                                                                |
|   - readskill: arg = file path                                                               |
|   - execskill: arg = full command string                                                     |
| cli_description: Unified skill CLI tool. Whenever you receive a task, you must first run     |
| "magicskills skill-tool listskill --name {skills_name}" to view all available skills.        |
|   Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's |
|  SKILL.md file by path.                                                                      |
|   Based on that documentation, either continue reading more files with "magicskills          |
| skill-tool readskill --arg <file_path>" or run the needed command with "magicskills          |
| skill-tool execskill --arg <command>".                                                       |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Collection example-skills                                                                    |
+----------------------------------------------------------------------------------------------+
| - name: example-skills                                                                       |
| skills: 0                                                                                    |
| agent_md_path: D:\example\test\AGENTS.md                                                     |
| paths: (none)                                                                                |
| tool_description: Just a test for tool description                                           |
| cli_description: Just test for cli description                                               |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Summary                                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 2                                                                         |
| Total skills across collections: 39                                                          |
+----------------------------------------------------------------------------------------------+
```

```bash
(cli-guide) PS D:\example> magicskills listskills --json
[
  {
    "name": "Allskills",
    "skills_count": 39,
    "paths": [
      "C:\\Users\\13978\\allskills\\algorithmic-art",
      "C:\\Users\\13978\\allskills\\brand-guidelines",
      "C:\\Users\\13978\\allskills\\canvas-design",
      "C:\\Users\\13978\\allskills\\claude-api",
      "C:\\Users\\13978\\allskills\\doc-coauthoring",
      "C:\\Users\\13978\\allskills\\frontend-design",
      "C:\\Users\\13978\\allskills\\internal-comms",
      "C:\\Users\\13978\\allskills\\mcp-builder",
      "C:\\Users\\13978\\allskills\\pdf",
      "C:\\Users\\13978\\allskills\\pptx",
      "C:\\Users\\13978\\allskills\\skill-creator",
      "C:\\Users\\13978\\allskills\\slack-gif-creator",
      "C:\\Users\\13978\\allskills\\theme-factory",
      "C:\\Users\\13978\\allskills\\web-artifacts-builder",
      "C:\\Users\\13978\\allskills\\webapp-testing",
      "C:\\Users\\13978\\allskills\\xlsx",
      "C:\\Users\\13978\\allskills\\template",
      "C:\\Users\\13978\\.claude\\skills\\c_2_ast",
      "D:\\example\\.agent\\skills\\c_2_ast",
      "C:\\Users\\13978\\allskills\\c_2_ast",
      "D:\\example\\.claude\\skills\\algorithmic-art",
      "D:\\example\\.claude\\skills\\canvas-design",
      "D:\\example\\.claude\\skills\\claude-api",
      "D:\\example\\.claude\\skills\\doc-coauthoring",
      "D:\\example\\.claude\\skills\\frontend-design",
      "D:\\example\\.claude\\skills\\internal-comms",
      "D:\\example\\.claude\\skills\\mcp-builder",
      "D:\\example\\.claude\\skills\\pdf",
      "D:\\example\\.claude\\skills\\pptx",
      "D:\\example\\.claude\\skills\\skill-creator",
      "D:\\example\\.claude\\skills\\slack-gif-creator",
      "D:\\example\\.claude\\skills\\theme-factory",
      "D:\\example\\.claude\\skills\\web-artifacts-builder",
      "D:\\example\\.claude\\skills\\webapp-testing",
      "D:\\example\\.claude\\skills\\xlsx",
      "D:\\example\\.claude\\skills\\template",
      "D:\\example\\.claude\\skills\\c_2_ast",
      "D:\\example\\.claude\\skills\\docx",
      "D:\\example\\exa_skills\\name"
    ],
    "tool_description": "Unified skill tool. First use \"listskill\" to find relevant skills. \nThen use \"readskill\" to read the selected skill's SKILL.md or related docs. \nIf needed, use \"execskill\" to run the command.\n\n\nInput format:\n{\n    \"action\": \"<action_name>\",\n    \"arg\": \"<string argument>\"\n}\n\nActions:\n- listskill\n- readskill: arg = file path\n- execskill: arg = full command string",
    "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
    "agent_md_path": "D:\\example\\AGENTS.md"
  },
  {
    "name": "example-skills",
    "skills_count": 0,
    "paths": [],
    "tool_description": "Just a test for tool description",
    "cli_description": "Just test for cli description",
    "agent_md_path": "D:\\example\\test\\AGENTS.md"
  }
]
```

### 2.13 `loadskills `

**作用：**&#x548C; `listskills` 类似，列出指向的 `JSON` 文件中的 `skills` 信息

**格式：**

```bash
magicskills loadskills [path] [--json]
```

* `--json`：以 JSON 数组输出；不传时输出人类可读的盒状文本。

* `path`：要输出的 `JSON` 文件，不传入时使用 `~/.magicskills/collections.json`

  * 且无论该 JSON 文件中是否包含 `Allskills`，`loadskills` 方法在加载完成后都会自动创建 `Allskills` 实例

**实例使用：**

null.json 文件是笔者创建的 空文件，使用 loadskills 加载结果如下

```sql
(cli-guide) PS D:\example> magicskills loadskills .\null.json
+----------------------------------------------------------------------------------------------+
| MagicSkills Collections                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 1                                                                         |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Collection Allskills                                                                         |
+----------------------------------------------------------------------------------------------+
| - name: Allskills                                                                            |
| skills: 0                                                                                    |
| agent_md_path: D:\example\AGENTS.md                                                          |
| paths: (none)                                                                                |
| tool_description: Unified skill tool. First use "listskill" to find relevant skills.         |
|   Then use "readskill" to read the selected skill's SKILL.md or related docs.                |
|   If needed, use "execskill" to run the command.                                             |
|                                                                                              |
|                                                                                              |
|   Input format:                                                                              |
|   {                                                                                          |
|       "action": "<action_name>",                                                             |
|       "arg": "<string argument>"                                                             |
|   }                                                                                          |
|                                                                                              |
|   Actions:                                                                                   |
|   - listskill                                                                                |
|   - readskill: arg = file path                                                               |
|   - execskill: arg = full command string                                                     |
| cli_description: Unified skill CLI tool. Whenever you receive a task, you must first run     |
| "magicskills skill-tool listskill --name {skills_name}" to view all available skills.        |
|   Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's |
|  SKILL.md file by path.                                                                      |
|   Based on that documentation, either continue reading more files with "magicskills          |
| skill-tool readskill --arg <file_path>" or run the needed command with "magicskills          |
| skill-tool execskill --arg <command>".                                                       |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Summary                                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 1                                                                         |
| Total skills across collections: 0                                                           |
+----------------------------------------------------------------------------------------------+
```

example-cli.json同样也是笔者新创建的文件，内容如下：

```json
{
  "collections": {
    "example-skills": {
      "paths": [],
      "tool_description": "Just a test for tool description",
      "cli_description": "Just test for cli description",
      "agent_md_path": "D:\\example\\test\\AGENTS.md"
    }
  }
}
```

使用 loadskills 的加载结果如下

```sql
(cli-guide) PS D:\example> magicskills loadskills .\example-cli.json
+----------------------------------------------------------------------------------------------+
| MagicSkills Collections                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 2                                                                         |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Collection Allskills                                                                         |
+----------------------------------------------------------------------------------------------+
| - name: Allskills                                                                            |
| skills: 0                                                                                    |
| agent_md_path: D:\example\AGENTS.md                                                          |
| paths: (none)                                                                                |
| tool_description: Unified skill tool. First use "listskill" to find relevant skills.         |
|   Then use "readskill" to read the selected skill's SKILL.md or related docs.                |
|   If needed, use "execskill" to run the command.                                             |
|                                                                                              |
|                                                                                              |
|   Input format:                                                                              |
|   {                                                                                          |
|       "action": "<action_name>",                                                             |
|       "arg": "<string argument>"                                                             |
|   }                                                                                          |
|                                                                                              |
|   Actions:                                                                                   |
|   - listskill                                                                                |
|   - readskill: arg = file path                                                               |
|   - execskill: arg = full command string                                                     |
| cli_description: Unified skill CLI tool. Whenever you receive a task, you must first run     |
| "magicskills skill-tool listskill --name {skills_name}" to view all available skills.        |
|   Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's |
|  SKILL.md file by path.                                                                      |
|   Based on that documentation, either continue reading more files with "magicskills          |
| skill-tool readskill --arg <file_path>" or run the needed command with "magicskills          |
| skill-tool execskill --arg <command>".                                                       |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Collection example-skills                                                                    |
+----------------------------------------------------------------------------------------------+
| - name: example-skills                                                                       |
| skills: 0                                                                                    |
| agent_md_path: D:\example\test\AGENTS.md                                                     |
| paths: (none)                                                                                |
| tool_description: Just a test for tool description                                           |
| cli_description: Just test for cli description                                               |
+----------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------+
| Summary                                                                                      |
+----------------------------------------------------------------------------------------------+
| Total collections: 2                                                                         |
| Total skills across collections: 0                                                           |
+----------------------------------------------------------------------------------------------+
```

```sql
(cli-guide) PS D:\example> magicskills loadskills .\example-cli.json --json
[
  {
    "name": "Allskills",
    "skills_count": 0,
    "paths": [],
    "tool_description": "Unified skill tool. First use \"listskill\" to find relevant skills. \nThen use \"readskill\" to read the selected skill's SKILL.md or related docs. \nIf needed, use \"execskill\" to run the command.\n\n\nInput format:\n{\n    \"action\": \"<action_name>\",\n    \"arg\": \"<string argument>\"\n}\n\nActions:\n- listskill\n- readskill: arg = file path\n- execskill: arg = full command string",
    "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
    "agent_md_path": "D:\\example\\AGENTS.md"
  },
  {
    "name": "example-skills",
    "skills_count": 0,
    "paths": [],
    "tool_description": "Just a test for tool description",
    "cli_description": "Just test for cli description",
    "agent_md_path": "D:\\example\\test\\AGENTS.md"
  }
]
```

### 2.14 `deleteskills`

**作用：**&#x5220;除注册的` skills` 集合（`skill` 的具体文件会保留，且不会影响 `Allskills` 中的信息）

**格式：**

```bash
magicskills deleteskills <name> [<name> ...]
```

* `<name>`：要删除的一个或多个命名 skills 集合名称。

**实例使用：**

删除一个

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
(cli-guide) PS D:\example> magicskills deleteskills example-skills
Deleted skills instance: example-skills
```

删除多个

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
(cli-guide) PS D:\example> magicskills addskills example-cli
Created skills instance: example-cli
Skills count: 0
(cli-guide) PS D:\example> magicskills deleteskills example-skills example-cli
Deleted skills instances: example-skills, example-cli
```

### 2.15 `saveskills  `

**作用：**&#x5C06;当前已注册的 skills 集合，保存到指定目录下的 JSON 文件

**格式：**

```bash
magicskills saveskills [path]
```

* `path`：可选，保存到的目标文件路径。不传入时使用默认路径（\~/.magicskills/collections.json）

**实例使用：**

```bash
(cli-guide) PS D:\example> magicskills saveskills
C:\Users\13978\.magicskills\collections.json

(cli-guide) PS D:\example> magicskills saveskills ./output.json
output.json

(cli-guide) PS D:\example> cat .\output.json
{
  "collections": {
    "Allskills": {
      "paths": [
        "C:\\Users\\13978\\allskills\\algorithmic-art",
        "C:\\Users\\13978\\allskills\\brand-guidelines",
        "C:\\Users\\13978\\allskills\\canvas-design",
        "C:\\Users\\13978\\allskills\\claude-api",
        "C:\\Users\\13978\\allskills\\doc-coauthoring",
        "C:\\Users\\13978\\allskills\\frontend-design",
        "C:\\Users\\13978\\allskills\\internal-comms",
        "C:\\Users\\13978\\allskills\\mcp-builder",
        "C:\\Users\\13978\\allskills\\pdf",
        "C:\\Users\\13978\\allskills\\pptx",
        "C:\\Users\\13978\\allskills\\skill-creator",
        "C:\\Users\\13978\\allskills\\slack-gif-creator",
        "C:\\Users\\13978\\allskills\\theme-factory",
        "C:\\Users\\13978\\allskills\\web-artifacts-builder",
        "C:\\Users\\13978\\allskills\\webapp-testing",
        "C:\\Users\\13978\\allskills\\xlsx",
        "C:\\Users\\13978\\allskills\\template",
        "C:\\Users\\13978\\.claude\\skills\\c_2_ast",
        "D:\\example\\.agent\\skills\\c_2_ast",
        "C:\\Users\\13978\\allskills\\c_2_ast",
        "D:\\example\\.claude\\skills\\algorithmic-art",
        "D:\\example\\.claude\\skills\\canvas-design",
        "D:\\example\\.claude\\skills\\claude-api",
        "D:\\example\\.claude\\skills\\doc-coauthoring",
        "D:\\example\\.claude\\skills\\frontend-design",
        "D:\\example\\.claude\\skills\\internal-comms",
        "D:\\example\\.claude\\skills\\mcp-builder",
        "D:\\example\\.claude\\skills\\pdf",
        "D:\\example\\.claude\\skills\\pptx",
        "D:\\example\\.claude\\skills\\skill-creator",
        "D:\\example\\.claude\\skills\\slack-gif-creator",
        "D:\\example\\.claude\\skills\\theme-factory",
        "D:\\example\\.claude\\skills\\web-artifacts-builder",
        "D:\\example\\.claude\\skills\\webapp-testing",
        "D:\\example\\.claude\\skills\\xlsx",
        "D:\\example\\.claude\\skills\\template",
        "D:\\example\\.claude\\skills\\c_2_ast",
        "D:\\example\\.claude\\skills\\docx",
        "D:\\example\\exa_skills\\name"
      ],
      "tool_description": "Unified skill tool. First use \"listskill\" to find relevant skills. \nThen use \"readskill\" to read the selected skill's SKILL.md or related docs. \nIf needed, use \"execskill\" to run the command.\n\n\nInput format:\n{\n    \"action\": \"<action_name>\",\n    \"arg\": \"<string argument>\"\n}\n\nActions:\n- listskill\n- readskill: arg = file path\n- execskill: arg = full command string",
      "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
      "agent_md_path": "D:\\example\\AGENTS.md"
    }
  }
}
```

### 2.16 `changetooldescription`

**作用：**&#x8C03;整某个已注册的 skills 集合上的 `tool_description` 元数据

**格式：**

```bash
magicskills changetooldescription <name> <description>
```

* `<name>`：命名 skills 集合名称。

* `<description>`：新的工具描述文本；如果包含空格，记得加引号。

**实例使用：**

输入如下命令，可以发现前后 tool\_description 发生了变化

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
(cli-guide) PS D:\example> magicskills changetooldescription example-skills "test the changetooldescription command"
Updated tool description for skills instance: example-skills
```

```bash
# 修改前
    {
    "name": "example-skills",
    "skills_count": 0,
    "paths": [],
    "tool_description": "Unified skill tool. First use \"listskill\" to find relevant skills. \nThen use \"readskill\" to read the selected skill's SKILL.md or related docs. \nIf needed, use \"execskill\" to run the command.\n\n\nInput format:\n{\n    \"action\": \"<action_name>\",\n    \"arg\": \"<string argument>\"\n}\n\nActions:\n- listskill\n- readskill: arg = file path\n- execskill: arg = full command string",
    "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
    "agent_md_path": "D:\\example\\AGENTS.md"
  }
  
# 修改后
  {
    "name": "example-skills",
    "skills_count": 0,
    "paths": [],
    "tool_description": "test the changetooldescription command",
    "cli_description": "Unified skill CLI tool. Whenever you receive a task, you must first run \"magicskills skill-tool listskill --name {skills_name}\" to view all available skills.\nThen use \"magicskills skill-tool readskill --arg <file_path>\" to read the selected skill's SKILL.md file by path.\nBased on that documentation, either continue reading more files with \"magicskills skill-tool readskill --arg <file_path>\" or run the needed command with \"magicskills skill-tool execskill --arg <command>\".",
    "agent_md_path": "D:\\example\\AGENTS.md"
  }
```

### 2.17 `changeclidescription`

**作用：**&#x6574;某个命名 skills 集合上的 `cli_description` 元数据

**注意：**&#x4F7F;用  `syncskills` 且  `--mode cli_description` 时，`changeclidescription` 会影响输出。

**格式：**

```bash
magicskills changeclidescription <name> <description>
```

* `<name>`：命名 skills 集合名称。

* `<description>`：新的 CLI 描述文本；如果包含空格，记得加引号。

实例使用：

```bash
(cli-guide) PS D:\example> magicskills addskills example-skills
Created skills instance: example-skills
Skills count: 0
(cli-guide) PS D:\example> magicskills syncskills example-skills --mode cli_description -y
Synced to D:\example\AGENTS.md
```

生成的 AGETNS.md 内容如下

```markdown
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Whenever you receive a task, you must first run "magicskills skill-tool listskill --name example-skills" to view all available skills.
Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's SKILL.md file by path.
Based on that documentation, either continue reading more files with "magicskills skill-tool readskill --arg <file_path>" or run the needed command with "magicskills skill-tool execskill --arg <command>".
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

```

执行修改命令

```bash
(cli-guide) PS D:\example> magicskills changeclidescription example-skills "test for the changeclidescription command"
Updated CLI description for skills instance: example-skills
(cli-guide) PS D:\example> magicskills syncskills example-skills --mode cli_description -y
Synced to D:\example\AGENTS.md
```

修改内容后，生成的文档内容如下：

```xml
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
test for the changeclidescription command
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

```

### 2.18 `skill-tool`

**作用：**&#x9762;向 agent/tool-call 的 CLI 包装层，提供了一个统一的接口，将不同的动作（`listskill`、`readskill`、`execskill`）分发到对应的处理函数，统一成 JSON 返回结构，并用退出码表示成功或失败

**格式：**

```bash
magicskills skill-tool <action> [--arg ARG] [--name NAME]
```

* `<action>`：动作名，支持以下主动作和别名。

  * `listskill`、`list`、`list_metadata`：列出集合中的 skill

  * `readskill`、`read`、`read_file`：读取某个 skill

  * `execskill`、`exec`、`run_command`：执行可执行命令

* `--arg ARG`：动作参数。

  * 对 `listskill` 可留空，或使用` --name` 传入`skills` 名称

  * 对 `readskill`，传 skill 名称或 SKILL.md 文件路径，当有重名情况出现时，必须使用文件路径

  * 对 `execskill`，可传普通命令字符串、JSON 字符串，或旧格式 `name::command`

* `--name NAME`：指定要使用哪个命名 skills 集合；不传时默认使用 `Allskills`。

**实例使用：**

对 `listskill` 的使用

```sql
(cli-guide) PS D:\example> magicskills skill-tool listskill
{
  "ok": true,
  "action": "listskill",
  "result": [
    {
      "name": "algorithmic-art",
      "description": "Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.",
      "path": "C:\\Users\\13978\\allskills\\algorithmic-art\\SKILL.md"
    },

......（此处省略100余行）

    {
      "name": "xlsx",
      "description": "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \\\"the xlsx in my downloads\\\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.",
      "path": "D:\\example\\.claude\\skills\\xlsx\\SKILL.md"
    }
  ]
}

(cli-guide) PS D:\example> magicskills skill-tool listskill --name example-skills
{
  "ok": true,
  "action": "listskill",
  "result": []
}
```

对 `readskill` 的使用：

````bash
(cli-guide) PS D:\example> magicskills skill-tool readskill --arg xlsx --name example-skills
{
  "ok": false,
  "error": "readskill: skill name 'xlsx' is duplicated; please pass an explicit file path (for example: <skill-path>/SKILL.md).\n\"Multiple skills named 'xlsx' found. Provide path. Candidates: D:\\\\example\\\\.claude\\\\skills\\\\xlsx, C:\\\\Users\\\\13978\\\\allskills\\\\xlsx\""
}
# 此时出现重名情况，必须传入 SKILL.md 路径
(cli-guide) PS D:\example> magicskills skill-tool readskill --arg "C:\\Users\\13978\\allskills\\xlsx\\SKILL.md" --name example-skills
{
  "ok": true,
  "action": "readskill",
  "result": "---\nname: xlsx\ndescription: \"Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \\\"the xlsx in my downloads\\\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.\"\nlicense: Proprietary. LICENSE.txt has complete terms\n---\n\n# Requirements for Outputs\n\n## All Excel files\n\n### Professional Font\n- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user\n\n### Zero Formula Errors\n- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)\n\n### Preserve Existing Templates (when updating templates)\n- Study and EXACTLY match existing format, style, and conventions when modifying files\n- Never impose standardized formatting on files with established patterns\n- Existing template conventions ALWAYS override these guidelines\n\n## Financial models\n\n### Color Coding Standards\nUnless otherwise stated by the user or existing template\n\n#### Industry-Standard Color Conventions\n- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios\n- **Black text (RGB: 0,0,0)**: ALL formulas and calculations\n- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook\n- **Red text (RGB: 255,0,0)**: External links to other files\n- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated\n\n### Number Formatting Standards\n\n#### Required Format Rules\n- **Years**: Format as text strings (e.g., \"2024\" not \"2,024\")\n- **Currency**: Use $#,##0 format; ALWAYS specify units in headers (\"Revenue ($mm)\")\n- **Zeros**: Use number formatting to make all zeros \"-\", including percentages (e.g., \"$#,##0;($#,##0);-\")\n- **Percentages**: Default to 0.0% format (one decimal)\n- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)\n- **Negative numbers**: Use parentheses (123) not minus -123\n\n### Formula Construction Rules\n\n#### Assumptions Placement\n- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells\n- Use cell references instead of hardcoded values in formulas\n- Example: Use =B5*(1+$B$6) instead of =B5*1.05\n\n#### Formula Error Prevention\n- Verify all cell references are correct\n- Check for off-by-one errors in ranges\n- Ensure consistent formulas across all projection periods\n- Test with edge cases (zero values, negative numbers)\n- Verify no unintended circular references\n\n#### Documentation Requirements for Hardcodes\n- Comment or in cells beside (if end of table). Format: \"Source: [System/Document], [Date], [Specific Reference], [URL if applicable]\"\n- Examples:\n  - \"Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]\"\n  - \"Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]\"\n  - \"Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity\"\n  - \"Source: FactSet, 8/20/2025, Consensus Estimates Screen\"\n\n# XLSX creation, editing, and analysis\n\n## Overview\n\nA user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.\n\n## Important Requirements\n\n**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `scripts/recalc.py` script. The script automatically configures LibreOffice on first run, including in sandboxed environments where Unix sockets are restricted (handled by `scripts/office/soffice.py`)\n\n## Reading and analyzing data\n\n### Data analysis with pandas\nFor data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:\n\n```python\nimport pandas as pd\n\n# Read Excel\ndf = pd.read_excel('file.xlsx')  # Default: first sheet\nall_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict\n\n# Analyze\ndf.head()      # Preview data\ndf.info()      # Column info\ndf.describe()  # Statistics\n\n# Write Excel\ndf.to_excel('output.xlsx', index=False)\n```\n\n## Excel File Workflows\n\n## CRITICAL: Use Formulas, Not Hardcoded Values\n\n**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.\n\n### ❌ WRONG - Hardcoding Calculated Values\n```python\n# Bad: Calculating in Python and hardcoding result\ntotal = df['Sales'].sum()\nsheet['B10'] = total  # Hardcodes 5000\n\n# Bad: Computing growth rate in Python\ngrowth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']\nsheet['C5'] = growth  # Hardcodes 0.15\n\n# Bad: Python calculation for average\navg = sum(values) / len(values)\nsheet['D20'] = avg  # Hardcodes 42.5\n```\n\n### ✅ CORRECT - Using Excel Formulas\n```python\n# Good: Let Excel calculate the sum\nsheet['B10'] = '=SUM(B2:B9)'\n\n# Good: Growth rate as Excel formula\nsheet['C5'] = '=(C4-C2)/C2'\n\n# Good: Average using Excel function\nsheet['D20'] = '=AVERAGE(D2:D19)'\n```\n\nThis applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.\n\n## Common Workflow\n1. **Choose tool**: pandas for data, openpyxl for formulas/formatting\n2. **Create/Load**: Create new workbook or load existing file\n3. **Modify**: Add/edit data, formulas, and formatting\n4. **Save**: Write to file\n5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the scripts/recalc.py script\n   ```bash\n   python scripts/recalc.py output.xlsx\n   ```\n6. **Verify and fix any errors**: \n   - The script returns JSON with error details\n   - If `status` is `errors_found`, check `error_summary` for specific error types and locations\n   - Fix the identified errors and recalculate again\n   - Common errors to fix:\n     - `#REF!`: Invalid cell references\n     - `#DIV/0!`: Division by zero\n     - `#VALUE!`: Wrong data type in formula\n     - `#NAME?`: Unrecognized formula name\n\n### Creating new Excel files\n\n```python\n# Using openpyxl for formulas and formatting\nfrom openpyxl import Workbook\nfrom openpyxl.styles import Font, PatternFill, Alignment\n\nwb = Workbook()\nsheet = wb.active\n\n# Add data\nsheet['A1'] = 'Hello'\nsheet['B1'] = 'World'\nsheet.append(['Row', 'of', 'data'])\n\n# Add formula\nsheet['B2'] = '=SUM(A1:A10)'\n\n# Formatting\nsheet['A1'].font = Font(bold=True, color='FF0000')\nsheet['A1'].fill = PatternFill('solid', start_color='FFFF00')\nsheet['A1'].alignment = Alignment(horizontal='center')\n\n# Column width\nsheet.column_dimensions['A'].width = 20\n\nwb.save('output.xlsx')\n```\n\n### Editing existing Excel files\n\n```python\n# Using openpyxl to preserve formulas and formatting\nfrom openpyxl import load_workbook\n\n# Load existing file\nwb = load_workbook('existing.xlsx')\nsheet = wb.active  # or wb['SheetName'] for specific sheet\n\n# Working with multiple sheets\nfor sheet_name in wb.sheetnames:\n    sheet = wb[sheet_name]\n    print(f\"Sheet: {sheet_name}\")\n\n# Modify cells\nsheet['A1'] = 'New Value'\nsheet.insert_rows(2)  # Insert row at position 2\nsheet.delete_cols(3)  # Delete column 3\n\n# Add new sheet\nnew_sheet = wb.create_sheet('NewSheet')\nnew_sheet['A1'] = 'Data'\n\nwb.save('modified.xlsx')\n```\n\n## Recalculating formulas\n\nExcel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `scripts/recalc.py` script to recalculate formulas:\n\n```bash\npython scripts/recalc.py <excel_file> [timeout_seconds]\n```\n\nExample:\n```bash\npython scripts/recalc.py output.xlsx 30\n```\n\nThe script:\n- Automatically sets up LibreOffice macro on first run\n- Recalculates all formulas in all sheets\n- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)\n- Returns JSON with detailed error locations and counts\n- Works on both Linux and macOS\n\n## Formula Verification Checklist\n\nQuick checks to ensure formulas work correctly:\n\n### Essential Verification\n- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model\n- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)\n- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)\n\n### Common Pitfalls\n- [ ] **NaN handling**: Check for null values with `pd.notna()`\n- [ ] **Far-right columns**: FY data often in columns 50+ \n- [ ] **Multiple matches**: Search all occurrences, not just first\n- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)\n- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)\n- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets\n\n### Formula Testing Strategy\n- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly\n- [ ] **Verify dependencies**: Check all cells referenced in formulas exist\n- [ ] **Test edge cases**: Include zero, negative, and very large values\n\n### Interpreting scripts/recalc.py Output\nThe script returns JSON with error details:\n```json\n{\n  \"status\": \"success\",           // or \"errors_found\"\n  \"total_errors\": 0,              // Total error count\n  \"total_formulas\": 42,           // Number of formulas in file\n  \"error_summary\": {              // Only present if errors found\n    \"#REF!\": {\n      \"count\": 2,\n      \"locations\": [\"Sheet1!B5\", \"Sheet1!C10\"]\n    }\n  }\n}\n```\n\n## Best Practices\n\n### Library Selection\n- **pandas**: Best for data analysis, bulk operations, and simple data export\n- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features\n\n### Working with openpyxl\n- Cell indices are 1-based (row=1, column=1 refers to cell A1)\n- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`\n- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost\n- For large files: Use `read_only=True` for reading or `write_only=True` for writing\n- Formulas are preserved but not evaluated - use scripts/recalc.py to update values\n\n### Working with pandas\n- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`\n- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`\n- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`\n\n## Code Style Guidelines\n**IMPORTANT**: When generating Python code for Excel operations:\n- Write minimal, concise Python code without unnecessary comments\n- Avoid verbose variable names and redundant operations\n- Avoid unnecessary print statements\n\n**For Excel files themselves**:\n- Add comments to cells with complex formulas or important assumptions\n- Document data sources for hardcoded values\n- Include notes for key calculations and model sections"
}
````

对 `execskill` 的使用：

```sql
(cli-guide) PS D:\example> magicskills skill-tool exec --arg "dir"
{
  "ok": true,
  "action": "exec",
  "result": {
    "command": "dir",
    "returncode": 0,
    "stdout": " 驱动器 D 中的卷是 新加卷\n 卷的序列号是 105E-7D2B\n\n D:\\example 的目录\n\n2026/03/25  01:22    <DIR>          .\n2026/03/23  20:44    <DIR>          .agent\n2026/03/23  20:38    <DIR>          .claude\n2026/03/24  16:04                20 hello.py\n               1 个文件             20 字节\n               3 个目录 272,956,874,752 可用字节\n",
    "stderr": ""
  }
}

(cli-guide) PS D:\example> magicskills skill-tool exec --arg "python ./hello.py"
{
  "ok": true,
  "action": "exec",
  "result": {
    "command": "python ./hello.py",
    "returncode": 0,
    "stdout": "hello world\n",
    "stderr": ""
  }
}

(cli-guide) PS D:\example> magicskills skill-tool execskill --arg "echo hello"
{
  "ok": true,
  "action": "execskill",
  "result": {
    "command": "echo hello",
    "returncode": 0,
    "stdout": "hello\n",
    "stderr": ""
  }
}
```

