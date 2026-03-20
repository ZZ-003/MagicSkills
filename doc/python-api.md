[Back to README](../README.md) | [简体中文](./python-api.zh-CN.md)

<a id="python-api-en"></a>
# 🐍 Python API

If you want to call MagicSkills directly from scripts, tests, agent runtimes, or higher-level frameworks instead of going through the CLI, use the Python API. The content below follows the current `__all__` in `/root/LLK/MagicSkills/src/magicskills/__init__.py`.

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

**Exports**

- types: `Skill`, `Skills`
- accessors and constants: `REGISTRY`, `ALL_SKILLS()`, `DEFAULT_SKILLS_ROOT`
- single-skill and execution functions: `listskill`, `readskill`, `showskill`, `execskill`, `createskill`, `createskill_template`, `install`, `uploadskill`, `deleteskill`
- skills collection and registry functions: `createskills`, `listskills`, `deleteskills`, `syncskills`, `loadskills`, `saveskills`
- description and dispatch functions: `change_tool_description`, `changetooldescription`, `change_cli_description`, `changeclidescription`, `skill_tool`

**Usage advice**

- If you already have a `Skills` object, prefer instance methods such as `skills.readskill()`, `skills.execskill()`, and `skills.syncskills()`.
- If you want to directly reuse CLI-equivalent capabilities, top-level functions are more direct.
- `changetooldescription` is a compatibility alias of `change_tool_description`; they are equivalent.
- `changeclidescription` is a compatibility alias of `change_cli_description`; they are equivalent.

## 🧱 `Skill`

**Use case**

Use this when you need to manually construct a skill metadata object, or serialize skill metadata into another system.

**Constructor signature**

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

**Parameters**

- `name`: the skill name, usually equal to the skill directory name
- `description`: a short description of the skill, usually coming from the `description` field in `SKILL.md` frontmatter
- `path`: the skill directory path
- `base_dir`: the skills root directory that contains the skill
- `source`: source information, such as a local path, Git URL, or repository address
- `is_global`: whether it comes from a global directory
- `universal`: whether it comes from the `.agent/skills` layout

**Available capabilities**

- direct access to dataclass fields
- call `to_dict()` to get a JSON-friendly dictionary

**Examples**

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

**Use case**

Use this when you want to maintain a group of skills in memory and manage listing, reading, execution, syncing, deletion, and related operations in an object-oriented style.

**Constructor signature**

```python
Skills(
    skill_list: Iterable[Skill] | None = None,
    paths: Iterable[Path | str] | None = None,
    tool_description: str | None = None,
    cli_description: str | None = None,
    agent_md_path: Path | str | None = None,
    name: str = "all",
)
```

**Parameters**

- `skill_list`: an explicit list of `Skill` objects
- `paths`: a list of skills root directories, or a list of individual skill directories; skills are discovered automatically during construction
- `tool_description`: the tool description text of this collection
- `cli_description`: an alternate CLI-oriented description text for `syncskills(mode="cli_description")`
- `agent_md_path`: which `AGENTS.md` file this collection should sync to by default
- `name`: the collection name, defaulting to `"all"`

**Notes**

- If `skill_list` and `paths` are both provided, they must resolve to exactly the same skills, otherwise a `ValueError` is raised.
- When only `paths` is provided, directories are scanned automatically for `SKILL.md`.
- When only `skill_list` is provided, `paths` are inferred automatically.
- `agent_md_path` defaults to `AGENTS.md` in the current working directory.

**Common instance methods**

- `get_skill(target)`: retrieve one `Skill` by name or directory path
- `createskill(skill_path, source=None)`
- `deleteskill(target)`
- `listskill()`
- `readskill(target)`
- `uploadskill(target)`
- `showskill(target)`
- `execskill(command, shell=True, timeout=None, stream=False)`
- `change_tool_description(description)`
- `change_cli_description(description)`
- `syncskills(output_path=None, mode="none")`
- `skill_tool(action, arg="")`

These instance methods map one-to-one to the top-level functions described below. If you prefer a functional style, you can use the top-level functions directly.

**Examples**

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

## 🗃️ `SkillsRegistry` (Internal)

`SkillsRegistry` is the internal registry type behind `REGISTRY`. Direct instantiation is disabled. Use the global `REGISTRY` singleton for named collection management.

## 🏷️ `REGISTRY`

**Use case**

This is the process-level global `SkillsRegistry` singleton. Most named collection operations can be done directly around it.

**Parameters**

None. It is a ready-made object and does not need to be instantiated.

**Examples**

```python
from magicskills import REGISTRY

print([item.name for item in REGISTRY.listskills()])
```

Create and persist a collection through the global registry:

```python
from magicskills import REGISTRY

REGISTRY.createskills(name="coder")
coder = REGISTRY.get_skills("coder")
print(coder.agent_md_path)

REGISTRY.saveskills()
REGISTRY.loadskills()
```

## 🌐 `ALL_SKILLS()`

**Use case**

This is an accessor function that returns the built-in `Allskills` view from the current registry. Many top-level functions work naturally with the result of `ALL_SKILLS()` as their first argument.

**Parameters**

No parameters.

**Notes**

- `ALL_SKILLS()` always resolves the current value from `REGISTRY`.
- If you call `loadskills()` in the same process, calling `ALL_SKILLS()` again returns the refreshed `Allskills` view.

**Examples**

```python
from magicskills import ALL_SKILLS, listskill, readskill

print(listskill(ALL_SKILLS()))
print(readskill(ALL_SKILLS(), "demo"))
```

## 🏠 `DEFAULT_SKILLS_ROOT`

**Use case**

You want the default `.claude/skills` path for the current working directory, so you can reuse it in your own initialization or installation logic.

**Parameters**

None. It is a constant whose value is `Path.cwd() / ".claude" / "skills"`.

**Examples**

```python
from magicskills import DEFAULT_SKILLS_ROOT

print(DEFAULT_SKILLS_ROOT)
```

## 📋 `listskill()`

**Use case**

You want to format the skill list of a `Skills` collection into plain text output.

**Signature**

```python
listskill(skills: Skills) -> str
```

**Parameters**

- `skills`: the `Skills` collection to list

**Return value**

- returns a formatted multi-line string

**Examples**

```python
from magicskills import ALL_SKILLS, listskill

print(listskill(ALL_SKILLS()))
```

## 📖 `readskill()`

**Use case**

Read `SKILL.md` by skill name, or read any text file by file path.

**Signature**

```python
readskill(skills: Skills, target: str | Path) -> str
```

**Parameters**

- `skills`: the target `Skills` collection
- `target`: a skill name, or an explicit file path

**Return value**

- returns the text content of the file

**Examples**

Read by skill name:

```python
from magicskills import ALL_SKILLS, readskill

content = readskill(ALL_SKILLS(), "demo")
print(content)
```

Read by path:

```python
from pathlib import Path
from magicskills import ALL_SKILLS, readskill

content = readskill(ALL_SKILLS(), Path("./skills/demo/SKILL.md"))
print(content)
```

## 🔍 `showskill()`

**Use case**

You want more than `SKILL.md`; you want the metadata and full file contents of the entire skill directory.

**Signature**

```python
showskill(skills: Skills, target: str | Path) -> str
```

**Parameters**

- `skills`: the target `Skills` collection
- `target`: a skill name or a skill directory path

**Return value**

- returns a formatted full display string

**Examples**

```python
from magicskills import ALL_SKILLS, showskill

print(showskill(ALL_SKILLS(), "demo"))
```

## ▶️ `execskill()`

**Use case**

Use this when you want to execute commands via the Python API and receive structured execution results.

**Signature**

```python
execskill(
    skills: Skills,
    command: str,
    shell: bool = True,
    timeout: float | None = None,
    stream: bool = False,
) -> ExecResult
```

**Parameters**

- `skills`: the `Skills` collection required by the current API shape
- `command`: the command string to execute
- `shell`: whether to execute through a shell; default `True`
- `timeout`: timeout in seconds; omit to disable
- `stream`: whether to stream output directly to the current terminal; default `False`

**Return value**

- returns `ExecResult` with fields `command`, `returncode`, `stdout`, and `stderr`
- when `stream=True`, `stdout` and `stderr` are empty strings because the output is already written directly to the terminal

**Examples**

Get a structured result:

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "echo hello", stream=False)
print(result.returncode, result.stdout, result.stderr)
```

Execute in no-shell mode:

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "python -c 'print(123)'", shell=False)
print(result.stdout)
```

Stream execution:

```python
from magicskills import ALL_SKILLS, execskill

execskill(ALL_SKILLS(), "pytest -q", stream=True)
```

With timeout:

```python
from magicskills import ALL_SKILLS, execskill

result = execskill(ALL_SKILLS(), "sleep 1", timeout=2)
print(result.returncode)
```

## 🧱 `createskill_template()`

**Use case**

You need to generate a minimal usable skill skeleton first, and then fill in `SKILL.md`, scripts, and reference files.

**Signature**

```python
createskill_template(name: str, base_dir: Path | str) -> Path
```

**Parameters**

- `name`: the skill name, also used as the directory name
- `base_dir`: the skills root under which the skill should be created

**Return value**

- returns the `Path` of the new skill directory

**Examples**

```python
from magicskills import createskill_template

skill_dir = createskill_template("my-skill", "./skills")
print(skill_dir)
```

This API ensures the following exist:

- `<base_dir>/<name>/`
- `references/`
- `scripts/`
- `assets/`
- a default `SKILL.md`

## 🧰 `createskill()`

**Use case**

You already have an existing skill directory and only want to register it into a `Skills` collection.

**Signature**

```python
createskill(
    skills: Skills,
    skill_path: Path | str,
    source: str | Path | None = None,
) -> Path
```

**Parameters**

- `skills`: the target `Skills` collection
- `skill_path`: the skill directory path, which must contain `SKILL.md`
- `source`: optional source information; if omitted, the absolute path of the parent directory is recorded by default

**Return value**

- returns the registered skill directory `Path`

**Examples**

Register into the built-in `Allskills` view:

```python
from magicskills import ALL_SKILLS, createskill

path = createskill(ALL_SKILLS(), "./skills/demo")
print(path)
```

Explicitly record the source:

```python
from magicskills import ALL_SKILLS, createskill

path = createskill(
    ALL_SKILLS(),
    "./skills/demo",
    source="https://github.com/example/repo.git",
)
print(path)
```

Notes:

- This API registers an existing directory and does not copy files.
- If you register a skill into a non-`Allskills` collection, the same skill is also added to the built-in `Allskills` view.
- If the target collection belongs to the current `REGISTRY`, the registry is saved automatically.

## 📦 `install()`

**Use case**

You want to install skills through the Python API instead of calling the CLI.

**Signature**

```python
install(
    source: str | None = None,
    global_: bool = False,
    universal: bool = False,
    yes: bool = False,
    target_root: Path | str | None = None,
) -> list[Path]
```

**Parameters**

- `source`: a local path, GitHub short form, Git URL, or a skill name in the default repository
- `global_`: whether to use Home as the install base directory
- `universal`: whether to switch the install root to `.agent/skills`
- `yes`: whether to overwrite directly if the target already exists
- `target_root`: custom install directory; cannot be used together with `global_` or `universal`

**Return value**

- returns the list of directories actually written to disk

**Examples**

Install one skill from the default repository:

```python
from magicskills import install

paths = install("demo")
print(paths)
```

Batch install from a local directory:

```python
from magicskills import install

paths = install("./skills", target_root="./custom-skills", yes=True)
print(paths)
```

Install using a GitHub short form:

```python
from magicskills import install

paths = install("owner/repo", global_=True)
print(paths)
```

Notes:

- The resolution order is the same as the CLI: local path first, then default repository skill name, then Git repository.
- After installation, skills are registered into the built-in `Allskills` view and persisted into the current `REGISTRY`.

## 📤 `uploadskill()`

**Use case**

You want to trigger the skill upload, fork, push, and PR workflow directly from Python code.

**Signature**

```python
uploadskill(
    skills: Skills | Path | str,
    target: str | Path | None = None,
) -> UploadResult
```

**Parameters**

- `skills`: two valid forms are supported
- pass a `Skills` object: in this case you must also pass `target`, which identifies a skill by name or path in that collection
- pass a `Path` or `str` path: in this case `target` stays `None`, and the first argument itself is the skill directory
- `target`: used when the first argument is `Skills`, representing a skill name or skill directory path

**Return value**

- returns `UploadResult` with fields `skill_name`, `repo`, `branch`, `remote_subpath`, `committed`, `pushed`, `push_remote`, `push_branch`, `pr_url`, and `pr_created`

**Examples**

Upload by name from the built-in `Allskills` view:

```python
from magicskills import ALL_SKILLS, uploadskill

result = uploadskill(ALL_SKILLS(), "demo")
print(result.pr_url)
```

Upload directly by local path:

```python
from magicskills import uploadskill

result = uploadskill("./skills/demo")
print(result.repo, result.push_branch)
```

**Notes**

- Before running, the same prerequisites as the CLI must be satisfied: `gh` must be installed and authenticated locally, and the target skill directory must contain `SKILL.md`.
- If you pass a `Skills` object and multiple skills have the same name, pass an explicit directory path instead.

## 🗑️ `deleteskill()`

**Use case**

You want to delete a skill from the Python API; when applied to the built-in `Allskills` view, it also deletes the directory on disk.

**Signature**

```python
deleteskill(skills: Skills, target: str) -> str
```

**Parameters**

- `skills`: the target `Skills` collection
- `target`: a skill name or a skill directory path

**Return value**

- returns the resolved path string of the deleted skill

**Examples**

Remove only from a named collection:

```python
from magicskills import REGISTRY, deleteskill

team = REGISTRY.get_skills("coder")
deleted = deleteskill(team, "./skills/demo")
print(deleted)
```

Delete completely from the built-in `Allskills` view:

```python
from magicskills import ALL_SKILLS, deleteskill

deleted = deleteskill(ALL_SKILLS(), "demo")
print(deleted)
```

Notes:

- When you pass a non-`Allskills` collection, the skill is only removed from that collection and not deleted from disk.
- When you pass the built-in `Allskills` view, the actual skill directory is deleted, and matching path references are removed from other named collections as well.

## 🧩 `createskills()`

**Use case**

You want to create a named `Skills` collection and register it into the global `REGISTRY` immediately.

**Signature**

```python
createskills(
    name: str,
    skill_list: list[Skill] | str | None = None,
    paths: list[str] | None = None,
    tool_description: str | None = None,
    cli_description: str | None = None,
    agent_md_path: str | None = None,
) -> Skills
```

**Parameters**

- `name`: the collection name
- `skill_list`: may be a list of `Skill` objects, or a single skill name string
- `paths`: a list of skills root paths or individual skill directory paths
- `tool_description`: the tool description text of the collection
- `cli_description`: the CLI description text of the collection
- `agent_md_path`: which `AGENTS.md` this collection should sync to by default

**Return value**

- returns the created `Skills` object and persists it into the registry by default

**Examples**

Create an empty collection:

```python
from magicskills import createskills

skills = createskills("coder")
print(skills.name, len(skills.skills))
```

Create by paths:

```python
from magicskills import createskills

# Prerequisite: these skills have already entered the built-in Allskills view via install/createskill
skills = createskills(
    "coder",
    paths=["./.claude/skills"],
    tool_description="Unified skill tool for coding tasks",
    cli_description="Use magicskills CLI commands only",
    agent_md_path="./agents/coder/AGENTS.md",
)
print(skills.agent_md_path)
```

Create from a single skill name:

```python
from magicskills import createskills

# Prerequisite: the built-in Allskills view can already resolve a skill named demo
skills = createskills("reviewer", skill_list="demo")
print([item.name for item in skills.skills])
```

**Notes**

- If both `paths` and `skill_list` are omitted, an empty collection is created.
- `paths` and string-form `skill_list` both depend on the current built-in `Allskills` view being able to resolve the target skill or its parent skills root.

## 🗂️ `listskills()`

**Use case**

List all named collections currently managed by the global `REGISTRY`.

**Signature**

```python
listskills() -> list[Skills]
```

**Parameters**

None.

**Return value**

- returns a list of `Skills` objects

**Examples**

```python
from magicskills import listskills

for item in listskills():
    print(item.name, len(item.skills))
```

## 🧹 `deleteskills()`

**Use case**

Delete the registration of a named `Skills` collection.

**Signature**

```python
deleteskills(name: str, *more_names: str) -> None
```

**Parameters**

- `name`: the first named collection to delete
- `more_names`: optional additional named collections to delete in the same call

**Examples**

```python
from magicskills import deleteskills

deleteskills("coder")
```

Delete multiple named collections:

```python
from magicskills import deleteskills

deleteskills("coder", "reviewer", "release_skills")
```

**Notes**

- Only the collection registration is deleted; skill files remain intact.
- `Allskills` cannot be deleted.

## 🔄 `syncskills()`

**Use case**

Sync a `Skills` collection into an `AGENTS.md` file.

**Signature**

```python
syncskills(
    skills: Skills,
    output_path: Path | str | None = None,
    mode: str = "none",
) -> Path
```

**Parameters**

- `skills`: the `Skills` collection to sync
- `output_path`: the target file path; if omitted, `skills.agent_md_path` is used
- `mode`: one of `none` or `cli_description`

**How to choose the mode**

- `none`: use this for agents that can directly discover and use skills from the skill information list in `AGENTS.md`
- `cli_description`: use this for agents that cannot directly use skills from the skill information list in `AGENTS.md` and instead need CLI guidance through `magicskills skill-tool`

**Return value**

- returns the final written file path as a `Path`

**Examples**

Sync to the collection's default file:

```python
from magicskills import REGISTRY, syncskills

coder = REGISTRY.get_skills("coder")
path = syncskills(coder)
print(path)
```

Sync to a specified file:

```python
from magicskills import REGISTRY, syncskills

coder = REGISTRY.get_skills("coder")
path = syncskills(coder, "./AGENTS.md")
print(path)
```

Sync using only `cli_description`:

```python
from magicskills import REGISTRY, syncskills

coder = REGISTRY.get_skills("coder")
path = syncskills(coder, mode="cli_description")
print(path)
```

## 📥 `loadskills()`

**Use case**

Reload the persisted state of the global `REGISTRY` from disk.

**Signature**

```python
loadskills(path: str | None = None) -> list[Skills]
```

**Parameters**

- `path`: optional registry JSON path; if omitted, the current `REGISTRY` store path is used

**Return value**

- returns the list of loaded `Skills`

**Examples**

```python
from magicskills import loadskills

collections = loadskills("./collections.json")
print([item.name for item in collections])
```

## 💾 `saveskills()`

**Use case**

Write the current global `REGISTRY` state back to disk.

**Signature**

```python
saveskills(path: str | None = None) -> str
```

**Parameters**

- `path`: optional output path; if omitted, save to the current `REGISTRY` store path

**Return value**

- returns the written file path as a string

**Examples**

```python
from magicskills import saveskills

saved_path = saveskills("./collections.json")
print(saved_path)
```

## ✏️ `change_tool_description()` / `changetooldescription()`

**Use case**

Modify the `tool_description` metadata on a `Skills` collection.

**Signature**

```python
change_tool_description(skills: Skills, description: str) -> None
changetooldescription(skills: Skills, description: str) -> None
```

**Parameters**

- `skills`: the target `Skills` collection
- `description`: the new description text

**Examples**

```python
from magicskills import REGISTRY, change_tool_description

coder = REGISTRY.get_skills("coder")
change_tool_description(coder, "Unified skill tool for coding and review tasks")
```

Call through the compatibility alias:

```python
from magicskills import REGISTRY, changetooldescription

coder = REGISTRY.get_skills("coder")
changetooldescription(coder, "Unified skill tool")
```

**Notes**

- If the target collection belongs to the current `REGISTRY`, this API automatically persists the modification into the registry.
- This metadata is suitable for external frameworks or your own wrapper layer to read.
- It no longer affects `syncskills()` output.

## ✏️ `change_cli_description()` / `changeclidescription()`

**Use case**

Modify the `cli_description` metadata on a `Skills` collection.

**Signature**

```python
change_cli_description(skills: Skills, description: str) -> None
changeclidescription(skills: Skills, description: str) -> None
```

**Parameters**

- `skills`: the target `Skills` collection
- `description`: the new description text

**Examples**

```python
from magicskills import REGISTRY, change_cli_description

coder = REGISTRY.get_skills("coder")
change_cli_description(
    coder,
    'Whenever you receive a task, you must first run "magicskills skill-tool listskill --name {skills_name}", then use readskill to inspect relevant docs, and finally decide whether to keep reading or run execskill.',
)
```

Call through the compatibility alias:

```python
from magicskills import REGISTRY, changeclidescription

coder = REGISTRY.get_skills("coder")
changeclidescription(coder, 'Whenever you receive a task, you must first run "magicskills skill-tool listskill --name {skills_name}", then use readskill to inspect relevant docs, and finally decide whether to keep reading or run execskill.')
```

**Notes**

- If the target collection belongs to the current `REGISTRY`, this API automatically persists the modification into the registry.
- This metadata is suitable for CLI-oriented wrappers or your own runtime layer to read.
- It affects `syncskills()` output only when you use `mode="cli_description"`.

## 🤖 `skill_tool()`

**Use case**

You want to reuse a unified agent/tool-call style entry point in Python, rather than dispatching `listskill`, `readskill`, and `execskill` yourself.

**Signature**

```python
skill_tool(skills: Skills, action: str, arg: str = "") -> dict[str, object]
```

**Parameters**

- `skills`: the target `Skills` collection
- `action`: action name, supporting:
- `listskill`, `list`, `list_metadata`
- `readskill`, `read`, `read_file`
- `execskill`, `exec`, `run_command`
- `arg`: action argument
- for `listskill`, it may be empty
- for `readskill`, pass a skill name or file path
- for `execskill`, pass a plain command string, JSON string, or the legacy `name::command` format

**Return value**

- returns a dictionary, typically shaped like `{"ok": True, "action": "...", "result": ...}`
- when the action is unknown or execution fails, returns `{"ok": False, "error": "..."}`

**Examples**

List skills:

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "listskill"))
```

Read a skill:

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "readskill", "demo"))
```

Execute a plain command:

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", "echo hello"))
```

Execute a JSON-form command:

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", '{"command":"echo hello"}'))
```

Execute the legacy command format:

```python
from magicskills import ALL_SKILLS, skill_tool

print(skill_tool(ALL_SKILLS(), "execskill", "demo::echo hello"))
```
