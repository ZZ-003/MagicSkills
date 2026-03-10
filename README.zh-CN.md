<div align="center">

<img src="./image/Logo.png" alt="MagicSkills" width="360" />

<br/>
<br/>

<p align="center">
  <a href="https://www.pku.edu.cn">
    <img src="./image/image4.png" alt="Peking University" height="42" />
  </a>
  <a href="https://github.com/Narwhal-Lab">
    <img src="./image/image5.png" alt="Narwhal-Lab" height="42" />
  </a>
</p>


# 🪄 MagicSkills: **一次构建技能，供每个 Agent 复用**

<br/>

为多 Agent 项目打造的**本地优先** Skill 基础设施

将分散的 `SKILL.md` 沉淀为可复用 · 可组合 · 可同步 · 可调用的共享能力库

<br/>

<table>
<tr>
<td align="center"><b>🤖 Agent 应用</b></td>
<td align="center"><b>🧩 Agent 框架</b></td>
</tr>
<tr>
<td align="center">Claude Code · Cursor · Windsurf · Aider · Codex<br/><sub>任何读取 AGENT.md 的 Agent 应用</sub></td>
<td align="center">AutoGen · CrewAI · LangChain · LangGraph · Haystack<br/>Semantic Kernel · smolagents · LlamaIndex<br/><sub>任何具备 tool / function 适配能力的 Agent 框架</sub></td>
</tr>
</table>

<br/>

<p>
  <a href="https://github.com/Narwhal-Lab/MagicSkills"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10‑3.13"/></a>
  &nbsp;
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License: MIT"/></a>
  &nbsp;
  <a href="https://github.com/Narwhal-Lab/MagicSkills"><img src="https://img.shields.io/github/stars/Narwhal-Lab/MagicSkills?style=for-the-badge&logo=github" alt="GitHub stars"/></a>
</p>


<br/>
<br/>


[English](./README.md)&ensp;|&ensp;简体中文

<br/>

[**概览**](#overview-cn)&ensp;·&ensp;[**快速开始**](#quick-start-cn)&ensp;·&ensp;[**工作原理**](#how-it-works-cn)&ensp;·&ensp;[**CLI 命令**](./doc/cli.zh-CN.md)&ensp;·&ensp;[**Python API**](./doc/python-api.zh-CN.md)&ensp;·&ensp;[**使用建议**](#tips-cn)

</div>

<br/>

---

<a id="overview-cn"></a>

## 🧭 概览

MagicSkills 是面向多 Agent 项目的本地优先 Skill 基础设施层。

它把零散的 `SKILL.md` 目录整理成一套可以：

- 安装到共享 skill 库
- 按 agent 组合成独立的 `Skills` 集合
- 同步到 `AGENTS.md`
- 通过稳定 API 直接暴露为工具

核心模型很简单：

- `Skill`：一个具体的 skill 目录
- `ALL_SKILLS()`：访问当前内置的 `Allskills` 视图
- `Skills`：某个 agent 或工作流实际使用的 skill 子集
- `SkillsRegistry`：跨运行持久化的命名集合

MagicSkills 特别适合这些场景：

- 你维护多个需要复用同一套 skill 库的 agent
- 你已经有 `SKILL.md` 内容，但还没有安装和选配流程
- 某些 agent 读取 `AGENTS.md`，另一些 agent 需要直接接工具接口
- 你希望 skill 管理保持透明、基于文件且可追踪

## 🤔 为什么需要 MagicSkills

没有 skill 层时，多 Agent 项目通常会逐渐滑向以下状态：

- 同一个 skill 被复制到多个 agent 目录里，很快产生分叉
- `SKILL.md` 明明已经存在，但仍然只是文档，而不是可操作单元
- 每个 agent 都加载了过多无关 skill
- `AGENTS.md`、提示词拼接层和框架工具接口各自演化、彼此脱节
- 一旦更换框架，就要把整套集成方式重做一遍

MagicSkills 通过分离以下几层来解决这些问题：

- 总体已安装 skill 池
- 每个 agent 实际应该看到的 skill 子集
- 负责保存命名集合的持久化层

<a id="quick-start-cn"></a>

## 🚀 快速开始

推荐的最短流程如下：

1. 安装 MagicSkills。
2. 安装一个或多个 skill 到本地技能库。
3. 为某个 agent 创建一个命名 `Skills` 集合。
4. 把这个集合同步到 `AGENTS.md`，或直接以工具方式暴露出来。

### 1. 📦 安装项目

从源码安装：

```bash
git clone https://github.com/Narwhal-Lab/MagicSkills.git
cd MagicSkills
python -m pip install -e .
magicskills -h
```

或通过 PyPI 安装：

```bash
pip install MagicSkills
magicskills -h
```

### 2. ⬇️ 安装 skill

```bash
magicskills install anthropics/skills
```

默认情况下，安装的 skill 会被复制到 `./.claude/skills/`，随后就能在内置的 `Allskills` 视图中被发现。

### 3. 🧩 创建一个 Agent 集合

```bash
magicskills createskills agent1_skills --skill-list pdf docx --agent-md-path /agent_workdir/AGENTS.md
```

这条命令的含义是：

- 从 `Allskills` 中解析 `pdf` 和 `docx`
- 创建一个名为 `agent1_skills` 的集合
- 记住 `/agent_workdir/AGENTS.md` 作为它的默认同步目标

### 4. 🔄 同步到 `AGENTS.md`

```bash
magicskills syncskills agent1_skills
```

如果目标文件中已经包含 skills 区块，就会替换；否则会在文件末尾追加新的区块。

### 5. 🛠️ 或直接使用工具接口

如果某些 agent 不读取 `AGENTS.md`，可以直接使用统一的 CLI 工具入口：

```bash
magicskills skill-tool listskill --name agent1_skills
magicskills skill-tool readskill --name agent1_skills --arg pdf
magicskills skill-tool execskill --name agent1_skills --arg "echo hello"
```

## 🐍 Python 示例

如果你要把 MagicSkills 接入某个 agent 框架，Python 侧可以尽量保持简洁：

```python
import json

from langchain_core.tools import tool
from magicskills import ALL_SKILLS, Skills

skill_a = ALL_SKILLS().get_skill("pdf")
skill_b = ALL_SKILLS().get_skill("docx")

agent1_skills = Skills(
    name="agent1_skills",
    skill_list=[skill_a, skill_b],
)


@tool("_skill_tool", description=agent1_skills.tool_description)
def _skill_tool(action: str, arg: str = "") -> str:
    return json.dumps(agent1_skills.skill_tool(action, arg), ensure_ascii=False)
```

如果你的运行时会读取 `AGENTS.md`，用 `syncskills`。如果不会，直接使用 `skill_tool` 或 Python API 即可。

## 🧪 示例与生态集成

MagicSkills 已提供多种集成示例，覆盖既能直接读取 `AGENTS.md` 的 Agent / IDE，也覆盖通过 tool / function 调用接入的主流 Agent 框架。

### 可直接读取 `AGENTS.md` 的 Agent / IDE

- [Claude Code](./ClaudeCode_example/README.md)
- [Cursor](./Cursor_example/README.md)
- [Windsurf](./Windsurf_example/README.md)
- [Aider](./Aider_example/README.md)
- [Codex](./Codex_example/README.md)

### 通过 Tool / Framework 接入的示例

- [AutoGen](./autogen_example/README.md)
- [CrewAI](./crewai_example/README.md)
- [LangChain](./langchain_example/README.md)
- [LangGraph](./langgraph_example/README.md)
- [Haystack](./haystack_example/README.md)
- [Semantic Kernel](./semantic_kernel_example/README.md)
- [smolagents](./smolagents_example/README.md)
- [LlamaIndex](./llamaindex_example/README.md)


## 🗺️ 文档导航

- [工作原理](#how-it-works-cn)：架构与对象模型
- [CLI 命令](./doc/cli.zh-CN.md)：逐条命令参考
- [Python API](./doc/python-api.zh-CN.md)：对象与函数参考
- [使用建议](#tips-cn)：接入方式与实践建议

<a id="how-it-works-cn"></a>

# ⚙️ 工作原理

## 🧠 核心思想

MagicSkills 的核心不是“把一堆命令堆在一起”，而是把 skill 管理拆成三层稳定模型：

- `Skill`：描述一个单独的 skill 目录及其元数据
- `Skills`：描述一组可操作的 skills 集合
- `SkillsRegistry`：描述多个命名 skills 集合的注册、加载和持久化

CLI 和 Python API 都只是这三层能力的不同入口。无论你执行的是 `readskill`、`install`、`syncskills` 还是 `skill_tool`，最终都会落到同一套核心对象和命令实现上。

从推荐的运行流程看，MagicSkills 更接近下面这条链路：

1. 先通过 `install` 把相关 skill 安装到本地 skills 目录
2. 安装过程中，MagicSkills 会扫描这些 skill 目录，解析 `SKILL.md` frontmatter，并把它们构造成 `Skill`
3. 所有已安装并被发现的 skill，都会先汇总进入内置 `Allskills` 视图
4. 再通过 `ALL_SKILLS()` 或 `REGISTRY.get_skills("Allskills")` 从这个视图里挑选一部分 skill，组合成某个具体 agent 要使用的 `Skills` 集合
5. 最后把这个命名的 `Skills` 集合注册进 `SkillsRegistry`，并按需持久化、同步到 `AGENTS.md`

## 🧱 Skill 层

在 MagicSkills 里，一个 skill 的最小成立条件很简单：它必须是一个目录，并且目录内存在 `SKILL.md`。

典型目录结构如下：

```text
demo-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

其中：

- `SKILL.md` 是 skill 的入口说明文件，也是元数据来源
- `references/`、`scripts/`、`assets/` 是常见约定目录，不是强制要求

代码里，单个 skill 会被表示为一个 `Skill` 对象，核心字段包括：

- `name`：skill 名称，通常就是目录名
- `description`：从 `SKILL.md` frontmatter 中提取
- `path`：该 skill 的目录路径
- `base_dir`：该 skill 所在的 skills 根目录
- `source`：这个 skill 来自哪里，例如本地路径或 Git 仓库
- `is_global` / `universal`：用于标记它来自哪类安装位置

这一层解决的是“单个 skill 是什么”的问题，不负责管理整组 skill，也不负责持久化注册表。

围绕单个 skill 的常见能力有：

- `readskill`：读取某个 skill 的 `SKILL.md`
- `showskill`：查看 skill 目录下的完整文件内容
- `createskill_template`：创建标准 skill 骨架
- `createskill`：把一个已存在的 skill 目录注册进集合

## 🧩 Skills 集合层

`Skills` 层解决的是“如何把多个 skill 组织成一个可操作的工作集合”。

一个 `Skills` 对象可以通过两种方式构建：

- 直接传入 `skill_list`
- 传入 `paths`，由系统自动扫描这些路径下的 skill 目录

构造完成后，这个集合就拥有统一的高层能力：

- `listskill()`：列出集合里的所有 skill
- `readskill(target)`：读取 skill 文件内容
- `showskill(target)`：展示完整 skill 内容
- `execskill(command, ...)`：执行命令并返回结构化结果
- `uploadskill(target)`：上传 skill 到默认仓库工作流
- `deleteskill(target)`：从集合中移除 skill；如果作用于 `Allskills`，还会删除磁盘目录
- `syncskills(output_path=None)`：把当前集合写入 `AGENTS.md`
- `skill_tool(action, arg="")`：以 tool function 风格统一分发 list/read/exec

这一层有两个关键设计：

- `Skills` 既支持按名称找 skill，也支持按路径找 skill；当名称重复时，路径是最终判定标准
- `Skills` 是运行时视图，不等于安装目录本身；同一个 skill 可以被多个命名集合引用

需要特别注意的是，`execskill()` 当前是在当前进程的工作目录中执行命令，而不是自动切换到 skill 目录执行。这意味着 MagicSkills 统一了执行入口，但不会偷偷改你的运行上下文。

## 🗃️ Registry 持久化层

`SkillsRegistry` 层解决的是“如何保存和恢复多个命名 skills 集合”。

这一层的职责包括：

- 维护全局注册表单例 `REGISTRY`
- 保证内置集合 `Allskills` 一直存在
- 创建、查询、删除命名 skills 集合
- 把集合信息写入 JSON 文件，并在后续重新加载

默认情况下，注册表存储在：

```text
~/.magicskills/collections.json
```

这里保存的不是每个 skill 的完整文件内容，而是集合恢复所需的最小信息：

- `paths`
- `tool_description`
- `agent_md_path`

也就是说，Registry 保存的是“集合配置”和“skill 路径引用”，而不是 skill 内容副本。真正的 skill 内容仍然在文件系统里。

这一层的典型工作流是：

1. 通过 `createskills` 创建一个命名集合
2. 通过 `saveskills` 或 `REGISTRY.saveskills()` 持久化
3. 通过 `loadskills` 或进程启动时的默认加载恢复这些集合
4. 通过 `syncskills` 把某个集合同步到目标 `AGENTS.md`

因此，Registry 层本质上是 MagicSkills 的“项目级配置中心”。`Skill` 定义单体，`Skills` 组织集合，`SkillsRegistry` 负责让这些集合在不同运行周期之间持续存在。

<a id="cli-cn"></a>

# 🛠️ CLI 命令

完整 CLI 参考文档已迁移至 [doc/cli.zh-CN.md](./doc/cli.zh-CN.md)。
英文版见 [doc/cli.md](./doc/cli.md)。


<a id="python-api-cn"></a>

# 🐍 Python API

完整 Python API 参考文档已迁移至 [doc/python-api.zh-CN.md](./doc/python-api.zh-CN.md)。
英文版见 [doc/python-api.md](./doc/python-api.md)。


<a id="tips-cn"></a>

# 💡 使用建议

## 🧾 依赖 `AGENTS.md` 的接入方式

更推荐把所有 skill 先集中安装或维护到同一个 skills 根目录下，再从中挑选出某个 agent 真正需要的那一部分，组成一个命名 skills 集合，最后把这个集合同步到目标 `AGENTS.md`。

这样做有几个好处：

- skill 的物理存储位置统一，便于维护、升级和排查
- 不同 agent 可以复用同一批底层 skill，但只暴露各自需要的子集
- `AGENTS.md` 只保留当前 agent 真正需要看到的 skills，减少上下文噪音

推荐流程如下：

1. 把 skill 安装到统一目录，例如 `~/allskills/` 或 `./.claude/skills` 或 `~/.claude/skills`
2. 用 `createskills` 创建一个只包含部分 skill 的命名集合
3. 用 `syncskills` 把这个集合写入目标 `AGENTS.md`
4. 让 agent 只读取这个目标 `AGENTS.md`

示例：

```bash
magicskills install anthropics/skills  -t  ~/allskills/
magicskills createskills agent1_skills --skill-list pdf docx --agent-md-path /agent_workdir/AGENTS.md
magicskills syncskills agent1_skills

```

如果你希望更精细地控制暴露范围，可以先把所有 skill 装到统一目录，再通过多个命名集合分别为不同 agent 生成不同的 `AGENTS.md`。

## 🔌 不依赖 `AGENTS.md` 的接入方式

有些 agent 或框架不会主动读取 `AGENTS.md`。这种情况下，可以直接把 MagicSkills 的统一分发接口暴露给它，而不是依赖文档同步。

CLI 入口使用：

```bash
magicskills skill-tool <action> --arg "<arg>" --name <skills-name>
```

例如：

```bash
magicskills skill-tool listskill --name agent1_skills
magicskills skill-tool readskill --name agent1_skills --arg "<path>"
magicskills skill-tool execskill --name agent1_skills --arg "<command>"
```

Python API 入口使用：

```python
agent1_skills.skill_tool(action: str, arg: str = "")
```

例如：

```python
from magicskills import ALL_SKILLS, Skills

skill_a = ALL_SKILLS().get_skill("pdf")
skill_b = ALL_SKILLS().get_skill("docx")  # 改成你自己的第二个 skill 名称或路径

agent1_skills  = Skills(
    skill_list=[skill_a, skill_b],
    name="agent1_skills",
)

print(agent1_skills.skill_tool("listskill"))
print(agent1_skills.skill_tool("readskill", "<path>"))
print(agent1_skills.skill_tool("execskill", "<command>"))

@tool("_skill_tool", description=agent1_skills.tool_description)
def _skill_tool(action: str, arg: str = "") -> str:
    return json.dumps(agent1_skills.skill_tool(action, arg), ensure_ascii=False)

```

这种方式适合两类场景：

- agent 有 tool-call / function-call 机制，但没有读取 `AGENTS.md` 的能力
- 你希望由上层程序自己控制何时列出 skill、何时读取 skill、何时执行命令

简化理解就是：

- 读 `AGENTS.md` 的 agent，推荐走 `createskills + syncskills`
- 不读 `AGENTS.md` 的 agent，推荐走 `skill-tool` 或 `skills.skill_tool()`


## 🌱 共享与沉淀 Skill 生态

MagicSkills 不只是一个本地的 skill 管理工具，也希望形成一个可以持续沉淀、共享和复用的 Skill 生态。

如果你已经在本地实现了一个通用 skill，可以通过 `uploadskill` 把它上传到本项目的 `skills/` 目录，并自动走 fork、push、PR 流程。  
如果你想复用社区里已经沉淀好的 skill，可以通过 `install` 把别人上传的 skill 下载到本地，接入自己的 agent 或工作流。

推荐流程如下：

1. 在本地完成一个可复用的 skill，并确保目录内包含 `SKILL.md`
2. 使用 `uploadskill` 把这个 skill 提交到 MagicSkills 的开源 skill 库
3. 其他用户通过 `install` 下载这些 skill，并组合进自己的 `Skills` 集合或 `AGENTS.md`

示例：

```bash
magicskills uploadskill ./skills/my-skill
magicskills install my-skill
```

# ❓ 常见问题

### Skill 至少需要包含什么？

至少需要满足两点：

- 它是一个目录
- 目录内存在 `SKILL.md`

像 `references/`、`scripts/`、`assets/` 这类目录是常见约定，但不是强制要求。

### 我应该用 `syncskills` 还是 `skill-tool`？

可以直接按接入方式判断：

- 如果你的 agent 会读取 `AGENTS.md`，优先用 `createskills + syncskills`
- 如果你的 agent 不读取 `AGENTS.md`，而是通过 tool-call / function-call 接入，优先用 `skill-tool` 或 `skills.skill_tool()`

前者更适合文档驱动的 agent 接入，后者更适合程序直接调用。

### `install` 默认会把 skill 装到哪里？

默认情况下，skill 会安装到当前项目下的 `./.claude/skills/`。

如果你使用：

- `--global`，默认目录会变成 `~/.claude/skills`
- `--universal`，默认目录会变成当前项目下的 `./.agent/skills`
- `--global --universal`，默认目录会变成 `~/.agent/skills`
- `--target`，则以你显式指定的目录为准

### 同名 skill 冲突时怎么办？

很多命令既支持传 skill 名称，也支持传 skill 路径。  
如果同名 skill 有多个，不要再传名称，直接传显式路径，例如：

```bash
magicskills readskill ./skills/demo/SKILL.md
magicskills deleteskill ./skills/demo
```

简单理解就是：名称用于方便，路径用于消歧。

### `execskill` 会自动切到 skill 目录执行吗？

不会。`execskill()` 当前是在当前进程的工作目录里执行命令，不会自动切换到某个 skill 目录。

这意味着：

- MagicSkills 统一了执行入口
- 但不会偷偷改变你的运行上下文

如果你的命令依赖某个特定目录，请在命令里自行 `cd` 到目标目录，或先在正确的工作目录下调用。

### 我怎样把本地 skill 分享给别人使用？

如果你希望把本地 skill 沉淀到开源生态里，可以使用 `uploadskill` 把它上传到本项目的 `skills/` 目录；其他人之后就可以通过 `install` 下载和复用。

典型流程如下：

```bash
magicskills uploadskill ./skills/my-skill
magicskills install my-skill
```

前者负责共享，后者负责复用。

# 📋 环境要求

- **Python** 3.10 / 3.11 / 3.12 / 3.13
- **Git**（用于安装远程仓库中的 skill）

---

# 📜 许可证

[MIT](LICENSE)

---

<div align="center">

**由 [北京大学 Narwhal-Lab](https://github.com/Narwhal-Lab) 开源维护**

</div>
