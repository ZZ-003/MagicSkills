# MagicSkills Python API Guide

这是一份面向用户场景的 Python API 实战指南，把公开 API 的主要调用形态放进真实上下文里跑一遍并展示。

## 0. 本文的真实测试上下文

以下内容在当前仓库内的真实工作区完成：

- 仓库根目录：`D:\pythonAPI\MagicSkills`
- Python 版本：`3.12.6`
- 实测工作区：`D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live`
- 进程工作目录：`D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project`
- 真实样本 skill：
  - 本地 bundle：`article-outline`、`meeting-summary`
  - 本地 Git 仓库样本：`incident-brief`
  - 模板新建 skill：`prompt-polish`
  - 删除测试专用 skill：`throwaway-cleanup`
  - 远程仓库样本：`c_2_ast`

本文里所有“通过 / 失败 / 抛异常”的描述都来自真实运行。

## 1. 什么时候应该直接用 Python API

如果你处在下面这些场景里，Python API 往往比 CLI 更自然：

- 你在写 agent runtime、工具包装层、服务端接口，已经在 Python 进程里了。
- 你想把 `Skills` 对象常驻内存，避免每一步都重新解析 CLI 参数。
- 你要把 `skill_tool()` 暴露成一个 tool / function-call 接口给上层框架。
- 你想在测试里直接断言 `ExecResult`、`UploadResult`、`Skills`、`Skill` 这些结构，而不是再解析命令行输出。

如果你只是手动试一下命令，CLI 更直接；如果你要把技能系统嵌进程序里，Python API 更合适。

## 2. 场景一：项目启动时先准备技能池

假设你在做一个文档生成服务。这个服务启动后，要先把本地技能池、远程仓库技能、团队共用技能都装好，再进入正式运行。

这时最常用的一组 API 是：

- `createskill_template()`
- `install()`
- `ALL_SKILLS()`
- `DEFAULT_SKILLS_ROOT`

### 2.1 先创建一个新的 skill 骨架

如果团队里还没有这个 skill，先用模板完成一个目录。

```python
from pathlib import Path
from magicskills import createskill_template

base_dir = Path(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills")
skill_dir = createskill_template("prompt-polish", base_dir)
print(skill_dir)
```

真实结果输出：

```text
D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish
```

这一步之后至少会生成这些内容：

```text
prompt-polish/
├── SKILL.md
├── assets/
├── references/
└── scripts/
```

之后可以继续把它补成一个真实可读的 skill：

- `SKILL.md`
- `references/checklist.md`
- `scripts/lint_prompt.py`

即，团队先起草一个 skill，再逐步填充资料。

### 2.2 `DEFAULT_SKILLS_ROOT` 到底指向哪里

```python
from magicskills import DEFAULT_SKILLS_ROOT
print(DEFAULT_SKILLS_ROOT)
```

真实结果：

```text
D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\.claude\skills
```

注意：它是在 import 时按当前工作目录计算出来的。

这意味着：

- 如果你的服务在不同工作目录启动，`DEFAULT_SKILLS_ROOT` 也会跟着变。
- 需要稳定路径时，不要只依赖常量，最好自己显式传 `target_root`。

### 2.3 `install()` 的所有常见形态

`install()` 实际上覆盖了多种用户来源：

- 我已经有本地技能目录
- 我本地已经有一个 Git 仓库
- 我要从 GitHub 仓库安装
- 我要从默认 MagicSkills 仓库按技能名抓一个 skill
- 我要安装到项目目录 / 全局目录 / universal 目录 / 自定义目录

各调用形态测试如下：

| 调用形态 | 真实调用 | 结果 |
| --- | --- | --- |
| 本地目录 + 自定义目标 | `install(str(local_bundle), target_root=local_target)` | 通过 |
| 同一 bundle 再装到另一个自定义目标 | `install(str(local_bundle), target_root=duplicate_target)` | 通过 |
| 本地 Git 仓库目录 | `install(str(git_source), target_root=git_fixture_target)` | 通过 |
| 远程 Git URL | `install("https://github.com/Narwhal-Lab/MagicSkills.git", target_root=git_url_target)` | 通过 |
| GitHub shorthand | `install("Narwhal-Lab/MagicSkills", target_root=shorthand_target)` | 通过 |
| 默认仓库技能名 | `install("c_2_ast", target_root=catalog_target)` | 通过 |
| 全局默认目录 | `install(str(local_bundle), global_=True)` | 通过 |
| 项目 universal 目录 | `install(str(local_bundle), universal=True)` | 通过 |
| 全局 universal 目录 | `install(str(local_bundle), global_=True, universal=True)` | 通过 |
| 已存在目录不加 `yes=True` | `install(str(local_bundle), target_root=local_target)` | 抛 `FileExistsError` |
| 已存在目录加 `yes=True` | `install(str(local_bundle), target_root=local_target, yes=True)` | 通过 |
| `file://...` 本地 Git URL | `install(file_uri, target_root=...)` | 抛 `ValueError` |

### 2.4 本地目录安装

```python
from pathlib import Path
from magicskills import install

local_target = Path(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\local-target")
paths = install(
    r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\sources\local_bundle",
    target_root=local_target,
)
print(paths)
```

真实结果：

```text
[
  D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\local-target\article-outline,
  D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\local-target\meeting-summary
]
```

这个形态最适合：

- 团队已经把 skills 仓库 clone 到本地
- 你要在测试里控制样本数据
- 你希望安装结果完全可复现

### 2.5 远程仓库安装：Git URL、GitHub shorthand、默认仓库技能名

#### Git URL

```python
from magicskills import install

paths = install(
    "https://github.com/Narwhal-Lab/MagicSkills.git",
    target_root=r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\git-url-target",
)
print(paths)
```

真实结果：

```text
[
  D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\git-url-target\c_2_ast
]
```

#### GitHub shorthand

```python
paths = install(
    "Narwhal-Lab/MagicSkills",
    target_root=r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\shorthand-target",
)
print(paths)
```

真实结果：

```text
[
  D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\shorthand-target\c_2_ast
]
```

#### 默认仓库技能名

```python
paths = install(
    "c_2_ast",
    target_root=r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\catalog-target",
)
print(paths)
```

真实结果：

```text
[
  D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\catalog-target\c_2_ast
]
```

这三种形态适合的用户场景不同：

- Git URL：你已经明确知道远程仓库地址
- GitHub shorthand：你在文档、issue、README 里看到的往往就是 `owner/repo`
- 默认仓库技能名：你只想装 MagicSkills 官方仓库里的某一个 skill

### 2.6 `file://...` 不是 `install()` 支持的 Git URL 形态

远程 Git 仓库可以了，但是对于本地 Git 仓库的 `file://...` URL：

```python
install(
    "file:///D:/pythonAPI/MagicSkills/tmp_pyapi_doc/workspace_live/sources/git_repo_source",
    target_root=git_url_target,
)
```

真实结果：

```text
ValueError: Unsupported source: file:///D:/pythonAPI/MagicSkills/tmp_pyapi_doc/workspace_live/sources/git_repo_source
```

- 如果你本地已经有仓库目录，直接把它当普通本地路径传给 `install()` 就可以
- `Git URL` 分支目前只接受 `https://...`、`git@...` 或以 `.git` 结尾的字符串

### 2.7 全局目录 / universal 目录 / 覆盖安装

测试源码：

```python
from magicskills import install

installed_global = install(str(local_bundle), global_=True)
installed_universal = install(str(local_bundle), universal=True)
installed_global_universal = install(str(local_bundle), global_=True, universal=True)

try:
    install(str(local_bundle), target_root=local_target)
except FileExistsError as exc:
    print(exc)

installed_overwrite = install(str(local_bundle), target_root=local_target, yes=True)

print(installed_global)
print(installed_universal)
print(installed_global_universal)
print(installed_overwrite)
```

实测结果：

```text
global_=True
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\home\.claude\skills\article-outline
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\home\.claude\skills\meeting-summary

universal=True
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\.agent\skills\article-outline
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\.agent\skills\meeting-summary

global_=True, universal=True
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\home\.agent\skills\article-outline
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\home\.agent\skills\meeting-summary
```

覆盖测试结果：

```text
install(..., target_root=local_target)
=> FileExistsError: Skill 'article-outline' already exists at ...\local-target\article-outline

install(..., target_root=local_target, yes=True)
=> 重新覆盖成功
```

如果你在 CI、初始化脚本、一次性同步任务里跑 `install()`，`yes=True` 经常是必要的。

### 2.8 `ALL_SKILLS()` 会把同名 skill 按不同路径都保留下来

把同一批 skills 装到了多个根目录后，`ALL_SKILLS()` 里的技能总数变成了 14，而且出现了多个同名项：

```text
article-outline x 5
meeting-summary x 5
c_2_ast x 3
incident-brief x 1
```

这对用户有两个直接影响：

1. MagicSkills 不会自动把“同名 skill”合并成一个逻辑实体。
2. 只要你把同名 skill 装在多个路径里，后续 `readskill()`、`addskill()`、`deleteskill()` 都可能要求你改传显式路径。

## 3. 场景二：给不同 agent / 服务构建不同的技能集合

现在假设你的技能池已经准备好了，下一步要给不同的 agent 构建不同的 `Skills` 视图。

这时最常用的是：

- `Skill`
- `Skills`
- `REGISTRY`
- `ALL_SKILLS()`
- `addskill()`
- `addskills()`
- `listskills()`

### 3.1 手动构造 `Skill`

如果你只是要把 skill 元数据传给别的系统，或者要做序列化，`Skill` 本身就够用。

```python
from pathlib import Path
from magicskills import Skill

skill = Skill(
    name="manual-skill-record",
    description="Manual Skill dataclass example for documentation.",
    path=Path(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish"),
    base_dir=Path(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills"),
    source="manual://docs",
)
print(skill.to_dict())
```

真实结果：

```python
{
    "name": "manual-skill-record",
    "description": "Manual Skill dataclass example for documentation.",
    "global": False,
    "universal": False,
    "path": "D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\project\\manual_skills\\prompt-polish",
    "baseDir": "D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\project\\manual_skills",
    "source": "manual://docs",
}
```

### 3.2 `Skills(...)` 构造函数的主要形态

本次实测了四种形态：

| 形态 | 真实调用 | 结果 |
| --- | --- | --- |
| 只给 `paths` | `Skills(paths=[local_target])` | 通过 |
| 只给 `skill_list` | `Skills(skill_list=[...])` | 通过 |
| `skill_list + paths` 完全匹配 | `Skills(skill_list=[...], paths=[...])` | 通过 |
| `skill_list + paths` 不匹配 | `Skills(skill_list=[...], paths=[...])` | `ValueError: skills and paths do not match` |

真实结果摘录：

```python
Skills(paths=[local_target]).skills
=> ["article-outline", "meeting-summary"]

Skills(skill_list=[...]).paths
=> [
  "...\\local-target\\article-outline",
  "...\\local-target\\meeting-summary",
]
```

这样理解：

- 你已经知道一组目录，就传 `paths`
- 你已经在别处拿到了 `Skill` 对象，就传 `skill_list`
- 两者一起传时，MagicSkills 会做一致性校验，不会默认“以其中一个为准”

### 3.3 `addskills()`：把运行时集合注册进全局 `REGISTRY`

在场景里创建了这些集合：

```python
empty_team = addskills("empty-team")
writer_team = addskills("writer-team", skill_list="incident-brief", agent_md_path=...)
reviewer_team = addskills(
    "reviewer-team",
    skill_list=[meeting_summary_skill, prompt_polish_skill],
    tool_description="Reviewer tool description v1",
    cli_description="Reviewer CLI description v1 for {skills_name}",
    agent_md_path=...,
)
path_team = addskills("path-team", paths=[str(local_target)])
duplicate_team = addskills("duplicate-team", paths=[str(local_target), str(duplicate_target)])
```

真实结果：

```text
listskills_after_creation
=> ['Allskills', 'cleanup-team', 'duplicate-team', 'empty-team', 'path-team', 'reviewer-team', 'writer-team']
```

`addskills()` 适合这些场景：

- 你要给不同 agent 准备不同 skill 子集
- 你要把 `agent_md_path`、`tool_description`、`cli_description` 一起保存进 registry
- 你希望后续 `syncskills()`、`loadskills()`、`saveskills()` 直接围绕集合名工作

### 3.4 `addskill()`：向现有集合里补一个 skill

测了两个分支：

```python
addskill(empty_team, str(local_target / "article-outline"), source="local-bundle-source")
addskill(empty_team, "incident-brief")
```

真实结果：

```python
empty_team.skills
=> ["article-outline", "incident-brief"]

empty_team skill_sources
=> {
  "article-outline": "local-bundle-source",
  "incident-brief": "D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\sources\\git_repo_source",
}
```

- 传路径时，适合你已经明确锁定了某个 skill 实例，并且想自定义 `source`
- 传名称时，适合目标 skill 在 `Allskills` 里唯一可解析

## 4. 场景三：在运行时让 agent 看 skill、读 skill、查 skill

当 agent 收到任务后，常见流程不是“立刻执行命令”，而是：

1. 看看集合里有哪些 skills
2. 读取某个 skill 的 `SKILL.md`
3. 如果不够，再查看整个 skill 目录

对应 API：

- `listskill()`
- `readskill()`
- `showskill()`

### 4.1 `listskill()`：适合给人类看，也适合做第一步检索

```python
from magicskills import listskill

print(listskill(reviewer_team))
```

真实结果：

```text
1. name: meeting-summary
   description: Turn raw meeting notes into concise summaries and action items.
   path: D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\installed\local-target\meeting-summary\SKILL.md
2. name: prompt-polish
   description: Refine prompts for clarity, constraints, and evaluation hooks.
   path: D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish\SKILL.md
```

### 4.2 `readskill()`：按名称读，或者按文件路径读

#### 按名称读

```python
print(readskill(reviewer_team, "meeting-summary"))
```

真实结果：

```text
---
name: meeting-summary
description: Turn raw meeting notes into concise summaries and action items.
---

# meeting-summary

Use this skill when the raw input is unstructured meeting notes.
```

#### 按路径读

```python
print(readskill(reviewer_team, article_outline_path))
```

真实结果：

```text
---
name: article-outline
description: Generate structured article outlines for user-facing technical docs.
---

# article-outline

Use this skill when a documentation task needs sectioning before drafting.
```

### 4.3 一旦有重名 skill，`readskill()` 必须改传路径

把同一个 `article-outline` 安装到了两个不同根目录，然后执行：

```python
readskill(duplicate_team, "article-outline")
```

真实结果：

```text
ValueError: readskill: skill name 'article-outline' is duplicated; please pass an explicit file path (for example: <skill-path>/SKILL.md).
"Multiple skills named 'article-outline' found. Provide path. Candidates: D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\installed\\local-target\\article-outline, D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\installed\\duplicate-target\\article-outline"
```

所以注意：

- 名称是“方便模式”
- 路径才是“唯一模式”

### 4.4 `showskill()`：当 `SKILL.md` 不够时再用

`showskill()` 适合这些场景：

- 你不只想读 `SKILL.md`
- 你还想把 `references/`、`scripts/`、`assets/` 一起交给 agent
- 你想在审查 skill 包结构时一眼看完整内容

按名称调用：

```python
print(showskill(reviewer_team, "prompt-polish"))
```

真实结果前几行：

```text
+----------------------------------------------------------------------------------------------+
| Skill Overview                                                                               |
+----------------------------------------------------------------------------------------------+
| Skill: prompt-polish                                                                         |
| Description: Refine prompts for clarity, constraints, and evaluation hooks.                  |
| Skill directory: D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish
| Skills root (base_dir): D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills
| SKILL.md path: D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish\SKILL.md
| Install source: D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills
+----------------------------------------------------------------------------------------------+
```

按路径调用：

```python
print(showskill(duplicate_team, local_target / "article-outline"))
```

这也真实通过了。

## 5. 场景四：在 Python 进程里统一执行命令

对上层调用方来说，`execskill()` 的意义不是“替代 shell”，而是给运行时提供一个统一的执行入口和结构化结果。

以下是把它放进了“agent 先读 skill，再执行项目脚本”的上下文里测试。

首先准备脚本：

```python
# hello.py
print("hello from python api")
```

### 5.1 `shell=True`、`shell=False`、实例方法

```python
execskill(ALL_SKILLS(), "python hello.py")
execskill(ALL_SKILLS(), "python hello.py", shell=False)
reviewer_team.execskill("python hello.py", shell=False)
```

真实结果全部成功，而且结果结构一致：

```python
{
    "command": "python hello.py",
    "returncode": 0,
    "stdout": "hello from python api\n",
    "stderr": "",
}
```

### 5.2 `stream=True`：终端会先看到输出，返回对象里的 `stdout/stderr` 为空

```python
execskill(ALL_SKILLS(), "python hello.py", stream=True)
```

真实结果摘录：

```text
hello from python api
{'command': 'python hello.py', 'returncode': 0, 'stdout': '', 'stderr': ''}
```

这决定了上层代码怎么处理结果：

- 如果你要把输出收集起来做后处理，用 `stream=False`
- 如果你要把输出直接打到当前终端，让用户实时看，用 `stream=True`

### 5.3 `timeout` 不是“返回超时状态”，而是直接抛异常

用一个会 sleep 的脚本测试了超时行为：

```python
execskill(ALL_SKILLS(), "python sleepy.py", timeout=0.1)
```

真实结果：

```text
TimeoutExpired: Command 'python sleepy.py' timed out after 0.1 seconds
```

所以如果你在服务里调用 `execskill()`，不要只看 `returncode`，还要准备好接 `TimeoutExpired`。

### 5.4 `execskill()` 的执行目录就是当前进程 cwd

测试里要能成功跑 `python hello.py`，前提就是当前进程 cwd 已经切到了：

```text
D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project
```

`execskill()` 不会自动切换到某个 skill 目录下执行。

## 6. 场景五：把 MagicSkills 暴露成上层统一工具

如果你要把 MagicSkills 暴露给 LangChain、LangGraph、AutoGen、CrewAI、Haystack、Semantic Kernel、LlamaIndex 等上层框架，真正最好用的入口通常不是你自己一层层分发，而是直接用 `skill_tool()`。

下文的测试的上下文：“上层只知道 action + arg，不知道底层函数名”。

### 6.1 `listskill` 的三个 action 形态

```python
skill_tool(reviewer_team, "listskill")
skill_tool(reviewer_team, "list")
skill_tool(reviewer_team, "list_metadata")
```

这三种都真实通过，返回结构一致：

```python
{
    "ok": True,
    "action": "list",
    "result": [
        {
            "name": "meeting-summary",
            "description": "Turn raw meeting notes into concise summaries and action items.",
            "path": "D:\\pythonAPI\\MagicSkills\\tmp_pyapi_doc\\workspace_live\\installed\\local-target\\meeting-summary\\SKILL.md",
        },
        ...
    ],
}
```

### 6.2 `readskill` 的三个 action 形态

```python
skill_tool(reviewer_team, "readskill", "prompt-polish")
skill_tool(reviewer_team, "read", str(article_outline_path))
skill_tool(reviewer_team, "read_file", str(article_outline_path))
```

第一个结果：

```python
{
    "ok": True,
    "action": "readskill",
    "result": "---\nname: prompt-polish\ndescription: Refine prompts for clarity, constraints, and evaluation hooks.\n---\n\n# Prompt Polish\n\nUse this skill when a prompt needs clearer instructions or testability.\n"
}
```

第二个结果：
```python
{
    "ok": True,
    "action": "read",
    "result": "---\nname: article-outline\ndescription: Generate structured article outlines for user-facing technical docs.\n---\n\n# article-outline\n\nUse this skill when a documentation task needs sectioning before drafting.\n"
}

```

第三个结果与 `read` 相同，只是 `action` 字段变成了 `read_file`。

### 6.3 `execskill` 的所有 arg 形态

不是只支持一种字符串格式。

#### 普通命令字符串

```python
skill_tool(reviewer_team, "execskill", "python hello.py")
skill_tool(reviewer_team, "exec", "python hello.py")
skill_tool(reviewer_team, "run_command", "python hello.py")
```

#### JSON 字符串

```python
skill_tool(reviewer_team, "execskill", '{"command":"python hello.py"}')
```

#### 旧格式 `name::command`

```python
skill_tool(reviewer_team, "execskill", "prompt-polish::python hello.py")
```

这三类测试得到同一个结果：

```python
{
    "ok": True,
    "action": "execskill",
    "result": {
        "command": "python hello.py",
        "returncode": 0,
        "stdout": "hello from python api\n",
        "stderr": "",
    },
}
```

### 6.4 未知 action 不抛异常，而是返回 `ok=False`

```python
skill_tool(reviewer_team, "unknown", "")
```

真实结果：

```python
{"ok": False, "error": "Unknown action: unknown"}
```

上层包装层可以统一按 `ok` 字段处理，不一定要靠异常分支。

## 7. 场景六：把集合同步到 `AGENTS.md`

当你已经有一个稳定的 `Skills` 集合，并且目标 runtime 能读取 `AGENTS.md` 时，下一步就是：

- `change_tool_description()`
- `changetooldescription()`
- `change_cli_description()`
- `changeclidescription()`
- `syncskills()`

### 7.1 `change_tool_description()` 和别名

调用了：

```python
change_tool_description(reviewer_team, "Reviewer tool description v2")
changetooldescription(reviewer_team, "Reviewer tool description v3 alias")
```

最终结果：

```text
reviewer_team.tool_description
=> Reviewer tool description v3 alias
```

### 7.2 `change_cli_description()` 和别名

```python
change_cli_description(reviewer_team, "Reviewer CLI description v2 for {skills_name}")
changeclidescription(reviewer_team, "Reviewer CLI description v3 alias for {skills_name}")
```

最终结果：

```text
reviewer_team.cli_description
=> Reviewer CLI description v3 alias for {skills_name}
```

### 7.3 `syncskills()` 的三种常见形态

本次实测：

| 形态 | 真实调用 | 结果 |
| --- | --- | --- |
| 用集合自己的 `agent_md_path` | `syncskills(reviewer_team)` | 通过 |
| 显式传输出文件 | `syncskills(reviewer_team, PROJECT_DIR / "AGENTS-existing.md")` | 通过 |
| `mode="cli_description"` | `syncskills(reviewer_team, PROJECT_DIR / "AGENTS-cli.md", mode="cli_description")` | 通过 |

#### 默认 `mode="none"`

真实输出摘录：

```text
# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively.
...
<available_skills>
<skill>
<name>meeting-summary</name>
...
```

#### `mode="cli_description"`

真实输出摘录：

```text
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Reviewer CLI description v3 alias for reviewer-team
</usage>
<!-- SKILLS_TABLE_END -->
```

说明：

- `tool_description` 不是 `syncskills(mode="none")` 的渲染来源
- `cli_description` 只会在 `mode="cli_description"` 下进入输出

## 8. 场景七：持久化集合、重新加载、再做清理

下文在工作流中测试了以下内容：

- `saveskills()`
- `loadskills()`
- `listskills()`
- `deleteskill()`
- `deleteskills()`

### 8.1 `saveskills()` / `loadskills()`

```python
saved_path = saveskills(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\saved-registry.json")
collections = loadskills(saved_path)
```

真实结果：

```text
saved_path
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\saved-registry.json

names_after_loadskills
=> ['Allskills', 'cleanup-team', 'duplicate-team', 'reviewer-team', 'writer-team']
```

### 8.2 `deleteskill()`：删集合内引用，还是删磁盘目录，本质上是两种不同场景

#### 从命名集合里删除

```python
deleted = deleteskill(reviewer_team, "prompt-polish")
```

真实结果：

```text
deleted
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\manual_skills\prompt-polish

prompt_polish_exists_after_named_delete
=> True
```

也就是说：

- `reviewer_team` 里不再引用它
- 但磁盘目录还在

这适合“某个 agent 不再需要某个 skill，但团队总技能池还保留它”的场景。

#### 从 `Allskills` 里删除

```python
deleted = deleteskill(ALL_SKILLS(), str(cleanup_skill_dir))
```

真实结果：

```text
deleted
=> D:\pythonAPI\MagicSkills\tmp_pyapi_doc\workspace_live\project\cleanup_skills\throwaway-cleanup

cleanup_exists_after_allskills_delete
=> False

cleanup_team_after_allskills_delete
=> []
```

这个结果非常关键：

- 从 `Allskills` 删除时，磁盘目录真的会被删掉
- 引用它的其他命名集合也会一起被清理

### 8.3 `deleteskills()`：一次删多个命名集合

```python
deleteskills("empty-team", "path-team")
```

真实结果：

```text
names_after_deleteskills
=> ['Allskills', 'cleanup-team', 'duplicate-team', 'reviewer-team', 'writer-team']
```

它只删除集合注册，不删除 skill 文件本身。

## 9. 场景八：`uploadskill()` 应该怎么安全地理解

`uploadskill()` 是公开 Python API，但它和其他函数不一样：成功路径会产生真实的外部副作用。

这次我先验证了前置条件和参数分支。

### 9.1 当前环境前置条件

首先要有 `gh auth`。运行 `gh auth status` 查看：

```text
github.com
  ✓ Logged in to github.com account xxx
  - Active account: true
```

### 9.2 两种调用形态

#### 形态一：传 `Skills` 对象 + `target`

形态一验证了参数校验与调用方式；真实成功上传跑通的见形态二。

```python
uploadskill(reviewer_team, "some-skill")
```

如果少传 `target`：

```python
uploadskill(ALL_SKILLS())
```

真实结果：

```text
ValueError: uploadskill requires target when called with a Skills instance
```

#### 形态二：直接传 skill 目录路径

```python
from pathlib import Path
from magicskills import uploadskill

result = uploadskill(
    Path(r"D:\pythonAPI\MagicSkills\tmp_pyapi_doc\upload_live_skill\pyapi-upload-probe-20260325-2")
)
print(result)
```

结果如下：

```python
UploadResult(
    skill_name='pyapi-upload-probe-20260325-2',
    repo='https://github.com/Narwhal-Lab/MagicSkills.git',
    branch='main',
    remote_subpath='skills/pyapi-upload-probe-20260325-2',
    committed=True,
    pushed=True,
    push_remote='origin',
    push_branch='fix/upload-pyapi-upload-probe-20260325-2-1774402355',
    pr_url='https://github.com/Narwhal-Lab/MagicSkills/pull/24',
    pr_created=True,
)
```

你可以打开上文中的 [URL](https://github.com/Narwhal-Lab/MagicSkills/pull/24) 查看这个 PR。

### 9.3 本次真实成功上传结果与注意事项

本次真实测试中，`uploadskill()` 已成功完成以下步骤：

- 确认 GitHub CLI 登录状态
- fork / clone 目标仓库
- 创建上传分支
- 提交 skill 文件
- push 到 fork
- 自动创建 PR

真实创建的 PR 为[URL](https://github.com/Narwhal-Lab/MagicSkills/pull/24)

`uploadskill()` 已可以完整走通默认的 fork -> push -> PR 工作流。

使用这个 API 时，仍需注意：

- 测试时最好使用唯一 skill 名称，避免和仓库里已有 skill 冲突
- 运行前应确保 `gh auth status` 正常
- 如果只是做验证，测试结束后应及时关闭临时 PR 并清理测试分支

## 10. 实操注意事项总结

1. `install()` 的远程三种形态都应该写，但要明确 `file://...` 不是受支持的 Git URL 形态。
2. 只要同名 skill 来自多个路径，`readskill()`、`addskill()`、`deleteskill()` 都应该优先教用户传显式路径。
3. `execskill(stream=True)` 会把输出直接打到终端，同时返回对象里的 `stdout/stderr` 为空。
4. `execskill(timeout=...)` 会直接抛 `TimeoutExpired`，不是返回一个超时状态码。
5. `syncskills(mode="none")` 用的是固定 usage 模板，不会把 `tool_description` 渲染进去。
6. `syncskills(mode="cli_description")` 才会使用 `cli_description`，而且会把 `{skills_name}` 格式化成真实集合名。
7. 从命名集合调用 `deleteskill()` 只删集合引用；从 `Allskills` 调用才会删磁盘目录并级联清理其他集合。

## 11. 附录：本文实际覆盖的公开 Python API

本次覆盖到的公开 API / 形态如下：

- `Skill`
- `Skill.to_dict()`
- `Skills(paths=...)`
- `Skills(skill_list=...)`
- `Skills(skill_list=..., paths=...)`
- `REGISTRY`
- `ALL_SKILLS()`
- `DEFAULT_SKILLS_ROOT`
- `createskill_template()`
- `install()` 的本地目录、自定义目标、全局目录、universal、远程 Git URL、GitHub shorthand、默认仓库技能名、覆盖安装、`file://...` 失败分支
- `addskill()` 的路径形态、名称形态、自定义 `source`
- `addskills()` 的空集合、字符串 `skill_list`、列表 `skill_list`、`paths`
- `listskill()`
- `readskill()` 的名称形态、文件路径形态、重名失败分支
- `showskill()` 的名称形态、路径形态
- `execskill()` 的 `shell=True`、`shell=False`、`stream=True`、`timeout=...`
- `skill_tool()` 的 `listskill/list/list_metadata`
- `skill_tool()` 的 `readskill/read/read_file`
- `skill_tool()` 的 `execskill/exec/run_command`
- `skill_tool()` 的普通字符串、JSON 字符串、旧格式 `name::command`
- `change_tool_description()` / `changetooldescription()`
- `change_cli_description()` / `changeclidescription()`
- `syncskills()` 的默认输出、显式输出、`mode="cli_description"`
- `listskills()`
- `saveskills()`
- `loadskills()`
- `deleteskill()` 的命名集合删除、`Allskills` 删除
- `deleteskills()` 的多名称删除
- `uploadskill()` 的两种调用入口 / 参数失败分支 / `gh` 前置条件检查 / 成功上传路径 / UploadResult / PR 创建结果