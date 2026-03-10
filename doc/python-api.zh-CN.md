[返回 README](../README.zh-CN.md) | [English](./python-api.md)

<a id="python-api-cn"></a>

# 🐍 Python API

如果你希望在脚本、测试、Agent runtime 或上层框架中直接调用 MagicSkills，而不是走 CLI，那么就使用 Python API。下面的内容以 `/root/LLK/MagicSkills/src/magicskills/__init__.py` 当前 `__all__` 为准。

```python
from pathlib import Path

from magicskills import (
    ALL_SKILLS,
    REGISTRY,
    Skills,
    listskill,
    readskill,
    execskill,
)
```

**导出分组**

- 类型：`Skill`、`Skills`、`SkillsRegistry`
- 访问器与常量：`REGISTRY`、`ALL_SKILLS()`、`DEFAULT_SKILLS_ROOT`
- 单 skill / 执行类函数：`listskill`、`readskill`、`showskill`、`execskill`、`createskill`、`createskill_template`、`install`、`uploadskill`、`deleteskill`
- skills 集合 / 注册表函数：`createskills`、`listskills`、`deleteskills`、`syncskills`、`loadskills`、`saveskills`
- 描述与分发函数：`change_tool_description`、`changetooldescription`、`skill_tool`

**使用建议**

- 如果你已经有 `Skills` 对象，优先调用实例方法，例如 `skills.readskill()`、`skills.execskill()`、`skills.syncskills()`。
- 如果你想直接复用 CLI 同名能力，使用顶层函数更直接。
- `changetooldescription` 是 `change_tool_description` 的兼容别名，两者等价。

## 🧱 `Skill`

**使用场景**

当你需要手动构造一个 skill 元数据对象，或者想把 skill 元信息序列化给其他系统时使用。

**构造签名**

```python
Skill(
    name: str,
    description: str,
    path: Path,
    base_dir: Path,
    source: str,
    is_global: bool = False,
    universal: bool = False,
)
```

**参数说明**

- `name`：skill 名称，通常等于 skill 目录名。
- `description`：skill 简述，通常来自 `SKILL.md` frontmatter 的 `description`。
- `path`：skill 目录路径。
- `base_dir`：skill 所在的 skills 根目录。
- `source`：来源信息，例如本地路径、Git URL、仓库地址。
- `is_global`：是否来自全局目录。
- `universal`：是否来自 `.agent/skills` 体系。

**可用能力**

- 直接访问 dataclass 字段。
- 调用 `to_dict()` 获得 JSON 友好的字典。

**功能示例**

```python
from pathlib import Path
from magicskills import Skill

skill = Skill(
    name="demo",
    description="Demo skill",
    path=Path("./skills/demo").resolve(),
    base_dir=Path("./skills").resolve(),
    source="https://github.com/example/repo.git",
)

print(skill.name)
print(skill.to_dict())
```

## 🧩 `Skills`

**使用场景**

当你希望在内存里维护一组 skills，并以面向对象的方式完成列表、读取、执行、同步、删除等操作时使用。

**构造签名**

```python
Skills(
    skill_list: Iterable[Skill] | None = None,
    paths: Iterable[Path | str] | None = None,
    tool_description: str | None = None,
    agent_md_path: Path | str | None = None,
    name: str = "all",
)
```

**参数说明**

- `skill_list`：显式传入的 `Skill` 对象列表。
- `paths`：skills 根目录列表，或单个 skill 目录列表；构造时会自动发现其中的 skill。
- `tool_description`：该集合的 tool 描述文本。
- `agent_md_path`：该集合默认同步到哪个 `AGENTS.md`。
- `name`：集合名称，默认是 `"all"`。

**补充说明**

- 如果同时传 `skill_list` 和 `paths`，两者必须能解析出完全一致的 skills，否则会抛出 `ValueError`。
- 只传 `paths` 时，会自动扫描目录下的 `SKILL.md`。
- 只传 `skill_list` 时，会自动反推出 `paths`。
- `agent_md_path` 默认为当前工作目录下的 `AGENTS.md`。

**常用实例方法**

- `get_skill(target)`：按名称或目录路径拿到单个 `Skill`
- `createskill(skill_path, source=None)`
- `deleteskill(target)`
- `listskill()`
- `readskill(target)`
- `uploadskill(target)`
- `showskill(target)`
- `execskill(command, shell=True, timeout=None, stream=False)`
- `change_tool_description(description)`
- `syncskills(output_path=None)`
- `skill_tool(action, arg="")`

这些实例方法和下面的同名顶层函数一一对应；如果你更偏好函数式风格，可以直接用顶层函数。

**功能示例**

```python
from magicskills import Skills

skills = Skills(
    paths=["./.claude/skills"],
    name="coder",
    agent_md_path="./agents/coder/AGENTS.md",
)

print(skills.listskill())
print(skills.readskill("demo"))

result = skills.execskill("echo hello", stream=False)
print(result.returncode, result.stdout)

skills.syncskills()
```

## 🗃️ `SkillsRegistry`

**使用场景**

当你需要维护多个命名 skills 集合，并把这些集合持久化到某个 JSON 文件时使用。

**构造签名**

```python
SkillsRegistry(store_path: Path | None = None)
```

**参数说明**

- `store_path`：注册表文件路径；不传时默认使用 `~/.magicskills/collections.json`。

**核心方法**

- `createskills(name, skill_list=None, paths=None, tool_description=None, agent_md_path=None, save=True)`
- `listskills()`
- `get_skills(name)`
- `deleteskills(name)`
- `loadskills(path=None)`
- `saveskills(path=None)`

如果你给 `createskills()` 传 `paths`，这些路径需要先能在当前 `Allskills` 中解析成具体 skill 或 skills 根目录。

**功能示例**

```python
from pathlib import Path
from magicskills import SkillsRegistry

registry = SkillsRegistry(store_path=Path("./collections.json"))
registry.createskills(name="coder")
print([item.name for item in registry.listskills()])

coder = registry.get_skills("coder")
print(coder.agent_md_path)

registry.saveskills()
registry.loadskills()
```

## 🏷️ `REGISTRY`

**使用场景**

这是进程级的全局 `SkillsRegistry` 单例。大多数命名集合操作都可以直接围绕它完成。

**参数说明**

无。它是现成对象，不需要实例化。

**功能示例**

```python
from magicskills import REGISTRY

print([item.name for item in REGISTRY.listskills()])
```

## 🌐 `ALL_SKILLS()`

**使用场景**

这是一个访问器函数，用来返回当前注册表中的内置 `Allskills` 视图。很多顶层函数都适合直接把 `ALL_SKILLS()` 的返回值作为第一个参数。

**参数说明**

无参数。

**补充说明**

- `ALL_SKILLS()` 每次都会从当前 `REGISTRY` 取值。
- 如果你在同一进程里调用了 `loadskills()`，再次调用 `ALL_SKILLS()` 会拿到刷新后的 `Allskills` 视图。

**功能示例**

```python
from magicskills import ALL_SKILLS, listskill, readskill

print(listskill(ALL_SKILLS()))
print(readskill(ALL_SKILLS(), "demo"))
```

## 🏠 `DEFAULT_SKILLS_ROOT`

**使用场景**

你想拿到当前工作目录默认的 `.claude/skills` 路径，给自己的初始化逻辑或安装逻辑复用。

**参数说明**

无。它是常量，值等于 `Path.cwd() / ".claude" / "skills"`。

**功能示例**

```python
from magicskills import DEFAULT_SKILLS_ROOT

print(DEFAULT_SKILLS_ROOT)
```

## 📋 `listskill()`

**使用场景**

想把某个 `Skills` 集合里的技能列表格式化成纯文本输出。

**签名**

```python
listskill(skills: Skills) -> str
```

**参数说明**

- `skills`：要列出的 `Skills` 集合。

**返回值**

- 返回格式化后的多行字符串。

**功能示例**

```python
from magicskills import ALL_SKILLS, listskill

print(listskill(ALL_SKILLS()))
```

## 📖 `readskill()`

**使用场景**

按 skill 名称读取 `SKILL.md`，或按文件路径读取任意文本文件。

**签名**

```python
readskill(skills: Skills, target: str | Path) -> str
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `target`：skill 名称，或显式文件路径。

**返回值**

- 返回文件文本内容。

**功能示例**

按 skill 名称读取：

```python
from magicskills import ALL_SKILLS, readskill

content = readskill(ALL_SKILLS(), "demo")
print(content)
```

按路径读取：

```python
from pathlib import Path
from magicskills import ALL_SKILLS, readskill

content = readskill(ALL_SKILLS(), Path("./skills/demo/SKILL.md"))
print(content)
```

## 🔍 `showskill()`

**使用场景**

你不只想看 `SKILL.md`，而是想看整个 skill 目录的元信息和所有文件内容。

**签名**

```python
showskill(skills: Skills, target: str | Path) -> str
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `target`：skill 名称，或 skill 目录路径。

**返回值**

- 返回带格式的完整展示文本。

**功能示例**

```python
from magicskills import ALL_SKILLS, showskill

print(showskill(ALL_SKILLS(), "demo"))
```

## ▶️ `execskill()`

**使用场景**

当你想用 Python API 执行命令，并拿到结构化执行结果时使用。

**签名**

```python
execskill(
    skills: Skills,
    command: str,
    shell: bool = True,
    timeout: float | None = None,
    stream: bool = False,
) -> ExecResult
```

**参数说明**

- `skills`：当前 API 形态要求传入的 `Skills` 集合。
- `command`：要执行的命令字符串。
- `shell`：是否通过 shell 执行；默认 `True`。
- `timeout`：超时时间，单位秒；不传表示不限制。
- `stream`：是否直接把输出流式打印到当前终端；默认 `False`。

**返回值**

- 返回 `ExecResult`，字段有 `command`、`returncode`、`stdout`、`stderr`。
- 当 `stream=True` 时，`stdout` 和 `stderr` 会是空字符串，因为输出已经直接写到终端。

**功能示例**

拿结构化结果：

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "echo hello", stream=False)
print(result.returncode, result.stdout, result.stderr)
```

无 shell 模式执行：

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "python -c 'print(123)'", shell=False)
print(result.stdout)
```

流式执行：

```python
from magicskills import ALL_SKILLS, execskill

execskill(ALL_SKILLS(), "pytest -q", stream=True)
```

带超时：

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "sleep 1", timeout=2)
print(result.returncode)
```

## 🧱 `createskill_template()`

**使用场景**

你需要先生成一个最小可用的 skill 目录骨架，再去补写 `SKILL.md`、脚本和资料文件。

**签名**

```python
createskill_template(name: str, base_dir: Path | str) -> Path
```

**参数说明**

- `name`：skill 名称，也会作为目录名。
- `base_dir`：要在哪个 skills 根目录下创建该 skill。

**返回值**

- 返回新建 skill 目录的 `Path`。

**功能示例**

```python
from magicskills import createskill_template

skill_dir = createskill_template("my-skill", "./skills")
print(skill_dir)
```

这个 API 会确保以下内容存在：

- `<base_dir>/<name>/`
- `references/`
- `scripts/`
- `assets/`
- 默认 `SKILL.md`

## 🧰 `createskill()`

**使用场景**

你已经有一个现成 skill 目录，只想把它注册到某个 `Skills` 集合里。

**签名**

```python
createskill(
    skills: Skills,
    skill_path: Path | str,
    source: str | Path | None = None,
) -> Path
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `skill_path`：skill 目录路径，目录内必须包含 `SKILL.md`。
- `source`：可选来源信息；不传时默认记录父目录的绝对路径。

**返回值**

- 返回注册的 skill 目录 `Path`。

**功能示例**

注册到内置 `Allskills` 视图：

```python
from magicskills import ALL_SKILLS, createskill

path = createskill(ALL_SKILLS(), "./skills/demo")
print(path)
```

显式记录来源：

```python
from magicskills import ALL_SKILLS, createskill

path = createskill(
    ALL_SKILLS(),
    "./skills/demo",
    source="https://github.com/example/repo.git",
)
print(path)
```

补充说明：

- 这个 API 注册的是“已有目录”，不会复制文件。
- 如果你把 skill 注册到某个非 `Allskills` 集合，同一 skill 也会同步加入内置 `Allskills` 视图。
- 如果目标集合属于当前 `REGISTRY`，注册表会自动保存。

## 📦 `install()`

**使用场景**

你想通过 Python API 直接安装 skill，而不是调用 CLI。

**签名**

```python
install(
    source: str | None = None,
    global_: bool = False,
    universal: bool = False,
    yes: bool = False,
    target_root: Path | str | None = None,
) -> list[Path]
```

**参数说明**

- `source`：本地路径、GitHub 仓库短写、Git URL 或默认仓库中的 skill 名称。
- `global_`：是否使用 Home 作为安装基准目录。
- `universal`：是否把安装根目录切到 `.agent/skills`。
- `yes`：目标已存在时是否直接覆盖。
- `target_root`：自定义安装目录；不能和 `global_`、`universal` 同时使用。

**返回值**

- 返回实际安装落盘的目录列表。

**功能示例**

从默认仓库安装单个 skill：

```python
from magicskills import install

paths = install("demo")
print(paths)
```

从本地目录批量安装：

```python
from magicskills import install

paths = install("./skills", target_root="./custom-skills", yes=True)
print(paths)
```

从 GitHub 仓库短写安装：

```python
from magicskills import install

paths = install("owner/repo", global_=True)
print(paths)
```

补充说明：

- 解析顺序与 CLI 一致：本地路径优先，其次是默认仓库 skill 名称，最后是 Git 仓库。
- 安装完成后会把 skill 注册到内置 `Allskills` 视图，并持久化到当前 `REGISTRY`。

## 📤 `uploadskill()`

**使用场景**

你想在 Python 代码里直接触发 skill 上传、fork、push、PR 流程。

**签名**

```python
uploadskill(
    skills: Skills | Path | str,
    target: str | Path | None = None,
) -> UploadResult
```

**参数说明**

- `skills`：有两种合法传法。
- 传 `Skills` 对象：此时必须再传 `target`，表示从该集合中按名称或路径定位 skill。
- 传 `Path` 或 `str` 路径：此时 `target` 保持 `None`，第一参数本身就是 skill 目录。
- `target`：当第一参数是 `Skills` 时使用，表示 skill 名称或 skill 目录路径。

**返回值**

- 返回 `UploadResult`，字段有 `skill_name`、`repo`、`branch`、`remote_subpath`、`committed`、`pushed`、`push_remote`、`push_branch`、`pr_url`、`pr_created`。

**功能示例**

从内置 `Allskills` 视图按名称上传：

```python
from magicskills import ALL_SKILLS, uploadskill

result = uploadskill(ALL_SKILLS(), "demo")
print(result.pr_url)
```

按本地路径直接上传：

```python
from magicskills import uploadskill

result = uploadskill("./skills/demo")
print(result.repo, result.push_branch)
```

**补充说明**

- 运行前需要满足和 CLI 相同的前置条件：本地已安装并认证 `gh`，并且目标 skill 目录存在 `SKILL.md`。
- 如果你传的是 `Skills` 对象且同名 skill 有多个，请改传显式目录路径。

## 🗑️ `deleteskill()`

**使用场景**

你想从 Python API 删除一个 skill；如果作用在内置 `Allskills` 视图上，会同时删除磁盘目录。

**签名**

```python
deleteskill(skills: Skills, target: str) -> str
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `target`：skill 名称或 skill 目录路径。

**返回值**

- 返回被删除 skill 的解析后路径字符串。

**功能示例**

只从命名集合里移除：

```python
from magicskills import REGISTRY, deleteskill

team = REGISTRY.get_skills("coder")
deleted = deleteskill(team, "./skills/demo")
print(deleted)
```

从内置 `Allskills` 视图彻底删除：

```python
from magicskills import ALL_SKILLS, deleteskill

deleted = deleteskill(ALL_SKILLS(), "demo")
print(deleted)
```

补充说明：

- 传非 `Allskills` 集合时，只从该集合移除，不删磁盘。
- 传内置 `Allskills` 视图时，会删除实际 skill 目录，并同步从其他命名集合中剔除同路径 skill。

## 🧩 `createskills()`

**使用场景**

你想创建一个命名 `Skills` 集合，并立即注册到全局 `REGISTRY` 中。

**签名**

```python
createskills(
    name: str,
    skill_list: list[Skill] | str | None = None,
    paths: list[str] | None = None,
    tool_description: str | None = None,
    agent_md_path: str | None = None,
) -> Skills
```

**参数说明**

- `name`：集合名称。
- `skill_list`：可直接传 `Skill` 列表；也可以传单个 skill 名称字符串。
- `paths`：skills 根目录或 skill 目录路径字符串列表。
- `tool_description`：集合的 tool 描述文本。
- `agent_md_path`：该集合默认同步到哪个 `AGENTS.md`。

**返回值**

- 返回创建后的 `Skills` 对象，并会默认持久化到注册表。

**功能示例**

创建空集合：

```python
from magicskills import createskills

skills = createskills("coder")
print(skills.name, len(skills.skills))
```

按路径创建：

```python
from magicskills import createskills

# 📝 前提：这些 skills 已经通过 install/createskill 进入内置 Allskills 视图
skills = createskills(
    "coder",
    paths=["./.claude/skills"],
    tool_description="Unified skill tool for coding tasks",
    agent_md_path="./agents/coder/AGENTS.md",
)
print(skills.agent_md_path)
```

按单个 skill 名称创建：

```python
from magicskills import createskills

# 📝 前提：内置 Allskills 视图中已经能解析到名为 demo 的 skill
skills = createskills("reviewer", skill_list="demo")
print([item.name for item in skills.skills])
```

**补充说明**

- 不传 `paths` 和 `skill_list` 时，会创建空集合。
- `paths` 和字符串形式的 `skill_list` 都依赖当前内置 `Allskills` 视图能先解析到对应 skill 或其上层 skills 根目录。

## 🗂️ `listskills()`

**使用场景**

列出全局 `REGISTRY` 当前管理的所有命名集合。

**签名**

```python
listskills() -> list[Skills]
```

**参数说明**

无。

**返回值**

- 返回 `Skills` 对象列表。

**功能示例**

```python
from magicskills import listskills

for item in listskills():
    print(item.name, len(item.skills))
```

## 🧹 `deleteskills()`

**使用场景**

删除一个命名 `Skills` 集合的注册信息。

**签名**

```python
deleteskills(name: str) -> None
```

**参数说明**

- `name`：要删除的命名集合名称。

**功能示例**

```python
from magicskills import deleteskills

deleteskills("coder")
```

**补充说明**

- 只删除集合注册，不删除 skill 文件。
- `Allskills` 不能被删除。

## 🔄 `syncskills()`

**使用场景**

把一个 `Skills` 集合同步进 `AGENTS.md` 文件。

**签名**

```python
syncskills(skills: Skills, output_path: Path | str | None = None) -> Path
```

**参数说明**

- `skills`：要同步的 `Skills` 集合。
- `output_path`：目标文件路径；不传时使用 `skills.agent_md_path`。

**返回值**

- 返回最终写入的文件路径 `Path`。

**功能示例**

同步到集合默认文件：

```python
from magicskills import REGISTRY, syncskills

coder = REGISTRY.get_skills("coder")
path = syncskills(coder)
print(path)
```

同步到指定文件：

```python
from magicskills import REGISTRY, syncskills

coder = REGISTRY.get_skills("coder")
path = syncskills(coder, "./AGENTS.md")
print(path)
```

## 📥 `loadskills()`

**使用场景**

从磁盘重新加载全局 `REGISTRY` 的持久化状态。

**签名**

```python
loadskills(path: str | None = None) -> list[Skills]
```

**参数说明**

- `path`：可选注册表 JSON 路径；不传则使用当前 `REGISTRY` 的存储路径。

**返回值**

- 返回加载后的 `Skills` 列表。

**功能示例**

```python
from magicskills import loadskills

collections = loadskills("./collections.json")
print([item.name for item in collections])
```

## 💾 `saveskills()`

**使用场景**

把当前全局 `REGISTRY` 的状态写回磁盘。

**签名**

```python
saveskills(path: str | None = None) -> str
```

**参数说明**

- `path`：可选输出路径；不传则保存到当前 `REGISTRY` 的存储路径。

**返回值**

- 返回写入文件路径字符串。

**功能示例**

```python
from magicskills import saveskills

saved_path = saveskills("./collections.json")
print(saved_path)
```

## ✏️ `change_tool_description()` / `changetooldescription()`

**使用场景**

修改某个 `Skills` 集合上的 `tool_description` 元数据。

**签名**

```python
change_tool_description(skills: Skills, description: str) -> None
changetooldescription(skills: Skills, description: str) -> None
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `description`：新的描述文本。

**功能示例**

```python
from magicskills import REGISTRY, change_tool_description

coder = REGISTRY.get_skills("coder")
change_tool_description(coder, "Unified skill tool for coding and review tasks")
```

用兼容别名调用：

```python
from magicskills import REGISTRY, changetooldescription

coder = REGISTRY.get_skills("coder")
changetooldescription(coder, "Unified skill tool")
```

**补充说明**

- 如果目标集合属于当前 `REGISTRY`，这个 API 会自动把修改持久化到注册表。
- 这个元数据适合给外部框架或你自己的工具包装层读取。
- 它不会改变 `syncskills()` 输出的固定 `AGENTS.md` usage 模板。

## 🤖 `skill_tool()`

**使用场景**

你想在 Python 里复用 agent/tool-call 风格的统一入口，而不自己手动分发 `listskill`、`readskill`、`execskill`。

**签名**

```python
skill_tool(skills: Skills, action: str, arg: str = "") -> dict[str, object]
```

**参数说明**

- `skills`：目标 `Skills` 集合。
- `action`：动作名，支持：
- `listskill`、`list`、`list_metadata`
- `readskill`、`read`、`read_file`
- `execskill`、`exec`、`run_command`
- `arg`：动作参数。
- 对 `listskill` 可以留空。
- 对 `readskill` 传 skill 名称或文件路径。
- 对 `execskill` 可传普通命令字符串、JSON 字符串，或旧格式 `name::command`。

**返回值**

- 返回字典，典型结构为 `{"ok": True, "action": "...", "result": ...}`。
- 未知 action 或运行失败时，返回 `{"ok": False, "error": "..."}`。

**功能示例**

列出 skills：

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "listskill"))
```

读取 skill：

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "readskill", "demo"))
```

执行普通命令：

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", "echo hello"))
```

执行 JSON 形式命令：

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", '{"command":"echo hello"}'))
```

执行旧格式命令：

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", "demo::echo hello"))
```

<a id="tips-cn"></a>
