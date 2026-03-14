[Back to README](../README.md) | [简体中文](./cli.zh-CN.md)

<a id="cli-en"></a>
# 🛠️ CLI

After installation, the `magicskills` command becomes available:

```bash
magicskills -h
magicskills <command> -h
```

The examples below assume `bash/zsh`; if you use PowerShell, adjust quoting and escaping rules accordingly.

## 📚 CLI Command Overview

| Command                   | Use case                                               | Main capability                                                 |
| ------------------------- | ------------------------------------------------------ | --------------------------------------------------------------- |
| `listskill`               | See which skills exist in the current built-in set     | List skill names, descriptions, and `SKILL.md` paths            |
| `readskill`               | Read a skill description or any local text file        | Output content by skill name or file path                       |
| `execskill`               | Run commands in the current working directory          | Supports streaming, JSON output, no-shell mode, custom paths    |
| `syncskills`              | Sync a named skills collection into `AGENTS.md`        | Generate or replace the `<skills_system>` block                 |
| `install`                 | Install skills from local paths, Git repos, or default | Copy skill files and register them into `Allskills`             |
| `createskill`             | Register an existing skill directory into `Allskills`  | Register metadata without copying files                         |
| `uploadskill`             | Submit a local skill to the default MagicSkills repo   | Automate fork, push, and PR flow                                |
| `deleteskill`             | Delete one skill                                       | Delete the skill directory and remove shared references         |
| `showskill`               | Review the full contents of a skill package            | Show metadata and all files inside the skill directory          |
| `createskills`            | Create a named skills collection                       | Build an isolated skill set for an agent or team               |
| `listskills`              | List all named skills collections                      | Human-readable output or JSON output                            |
| `deleteskills`            | Delete a named skills collection                       | Delete only the collection registration, not the skill files    |
| `changetooldescription`   | Modify the collection's `tool_description` metadata    | Update tool-oriented description for later querying and integration |
| `changeclidescription`    | Modify the collection's `cli_description` metadata     | Update CLI-oriented description for later querying and integration |
| `skill-tool`              | Invoke skill capabilities in a tool-function style     | Use unified JSON output to dispatch list/read/exec              |

## 📌 General Conventions

- `Allskills` is the built-in skills collection. `listskill`, `readskill`, `install`, `createskill`, `uploadskill`, `deleteskill`, and `showskill` all operate around it by default.
- Named skills collections are created through `createskills`, and their metadata is stored in `~/.magicskills/collections.json`.
- Many commands accept both a `skill name` and a `skill directory path`. If multiple skills share the same name, you must pass an explicit path.
- The default install directory for `install` depends on the scope.
- Current project default: `./.claude/skills`
- `--global` default: `~/.claude/skills`
- `--universal` current project directory: `./.agent/skills`
- `--global --universal` directory: `~/.agent/skills`
- When `readskill` receives a skill name, it actually reads the `SKILL.md` inside that skill directory.
- For `execskill`, it is recommended to separate CLI args from the command with `--`.

## 📋 `listskill`

**Use case**

You want a quick view of which skills are already registered in the current `Allskills`, along with each skill's basic description.

**Command format**

```bash
magicskills listskill
```

**Parameters**

None.

**Examples**

```bash
magicskills listskill
```

The output lists each skill in order with:

- `name`
- `description`
- `path` (pointing to that skill's `SKILL.md`)

## 📖 `readskill`

**Use case**

You already know a skill name and want to read its `SKILL.md` directly, or you want to use this command to read any local file.

**Command format**

```bash
magicskills readskill <path>
```

**Parameters**

- `<path>`: may be a file path or a skill name in `Allskills`.
- When a skill name is passed, the command reads the `SKILL.md` inside the corresponding skill directory.
- When an explicit path is passed, the target must be a file, not a directory.
- If multiple skills share the same name, you must pass a concrete file path, for example `./skills/demo/SKILL.md`.

**Examples**

Read by skill name:

```bash
magicskills readskill demo
```

Read by `SKILL.md` file path:

```bash
magicskills readskill ./skills/demo/SKILL.md
```

Read any local file:

```bash
magicskills readskill ./AGENTS.md
```

When there is a name collision, use an explicit path:

```bash
magicskills readskill ./vendor-skills/demo/SKILL.md
```

## ▶️ `execskill`

**Use case**

You want to execute a command in the current working directory while keeping the invocation style consistent with the MagicSkills ecosystem. It is also suitable as a unified execution entry point for agents or automation scripts.

**Command format**

```bash
magicskills execskill [--no-shell] [--json] [--paths [PATHS ...]] -- <command>
```

**Parameters**

- `<command>`: the command string to execute. It is recommended to place it after `--`.
- `--no-shell`: disable shell mode. Internally, the command is split with `shlex.split()`, which is better for directly invoking executables and their arguments.
- `--json`: instead of streaming terminal output directly, return JSON containing `command`, `returncode`, `stdout`, and `stderr`.
- `--paths [PATHS ...]`: specify custom skill lookup paths. A temporary `Skills` collection is constructed from those paths before executing the command.

**Examples**

Default streaming execution:

```bash
magicskills execskill -- pwd
```

Return JSON for script consumption:

```bash
magicskills execskill --json -- echo hello
```

Run Python in no-shell mode:

```bash
magicskills execskill --no-shell -- python -c 'print(123)'
```

Run a command in the context of custom skills paths:

```bash
magicskills execskill --paths ./.claude/skills ./vendor-skills -- ls -la
```

## 🔄 `syncskills`

**Use case**

You have already created a named skills collection and want to sync it into an `AGENTS.md` file so the agent can see those skills in its system context.

**Command format**

```bash
magicskills syncskills <name> [-o OUTPUT] [--mode {none,tool_description,cli_description}] [-y]
```

**Parameters**

- `<name>`: the name of the named skills collection
- `-o, --output`: output file path; if omitted, the collection's own `agent_md_path` is used
- `--mode`: sync rendering mode
- `none`: keep the original `<usage> + <available_skills>` layout
- `tool_description`: write only `<usage>` using the collection's `tool_description`
- `cli_description`: write only `<usage>` using the collection's `cli_description`
- `-y, --yes`: skip interactive confirmation and sync immediately

**Examples**

Sync to the collection's default `agent_md_path`:

```bash
magicskills syncskills coder
```

Sync to a specific file:

```bash
magicskills syncskills coder --output ./AGENTS.md
```

Sync using only `tool_description`:

```bash
magicskills syncskills coder --mode tool_description
```

Sync using only `cli_description`:

```bash
magicskills syncskills coder --mode cli_description
```

Skip confirmation in CI or scripts:

```bash
magicskills syncskills coder -o ./AGENTS.md -y
```

Notes:

- If the target file does not exist, the command creates it first and writes a base `# AGENTS` title.
- If the file already contains a `<skills_system>` block, the command replaces it; otherwise it appends a new block to the end of the file.
- `none` is the compatibility mode and keeps the previous XML structure unchanged.

## 📦 `install`

**Use case**

You want to install skills into the current project or a global directory. This command supports installing a specific skill from the default repository, or all skills from a local directory or remote Git repository.

**Command format**

```bash
magicskills install <source> [--global] [--universal] [-t TARGET] [-y]
```

**Parameters**

- `<source>`: supports four input forms.
- skill name: such as `demo`. The command clones the default repository `https://github.com/Narwhal-Lab/MagicSkills.git` and installs only the matching skill.
- GitHub short form: such as `owner/repo`. The command converts it to `https://github.com/owner/repo.git` and installs all skill directories in that repository that contain `SKILL.md`.
- Git URL: for example `https://github.com/owner/repo.git` or `git@github.com:owner/repo.git`.
- local path: may be a single skill directory or a root directory containing multiple skills; the command recursively finds all `SKILL.md` files.
- `--global`: switch the install root to the user's Home instead of the current project directory.
- `--universal`: switch the install root from `.claude/skills` to `.agent/skills`.
- `-t, --target`: custom install directory; cannot be used together with `--global` or `--universal`.
- `-y, --yes`: if a skill with the same name already exists in the target directory, overwrite it directly.

**Resolution order**

- If `<source>` exists locally, it is handled as a local path.
- If `<source>` looks like a plain skill name and does not contain `/`, `\\`, `.git`, or a URL prefix, it is handled as a skill name in the default repository.
- All other cases are handled as Git repositories.

**Examples**

Install one skill from the default MagicSkills repository:

```bash
magicskills install demo
```

Batch install from a local skills root:

```bash
magicskills install ./skills
```

Install from a single local skill directory:

```bash
magicskills install ./skills/demo
```

Install from a GitHub short form:

```bash
magicskills install Narwhal-Lab/MagicSkills
```

Install from a full Git URL:

```bash
magicskills install https://github.com/owner/repo.git
```

Install into global `.claude/skills`:

```bash
magicskills install demo --global
```

Install into the current project's `.agent/skills`:

```bash
magicskills install demo --universal
```

Install into a custom directory:

```bash
magicskills install demo --target ./custom-skills
```

Overwrite a skill with the same name:

```bash
magicskills install demo --target ./custom-skills -y
```

Notes:

- Remote installation depends on `git`.
- After installation, the CLI prints the actual directories written to disk.
- The install flow also registers installed skills into the current process `Allskills` collection.

## 🧰 `createskill`

**Use case**

You already wrote a skill directory by hand and only want to register it into `Allskills`, instead of copying it again.

**Command format**

```bash
magicskills createskill <path> [--source SOURCE]
```

**Parameters**

- `<path>`: the skill directory path; the directory must contain `SKILL.md`
- `--source`: optional source info to record for this skill; when omitted, the absolute path of the skill's parent directory is used

**Examples**

Register a local skill directory:

```bash
magicskills createskill ./skills/my-skill
```

Explicitly record the source repository or source directory:

```bash
magicskills createskill ./skills/my-skill --source https://github.com/owner/repo.git
```

Notes:

- The behavior of this command is "register an existing skill", not "generate a skill template".
- `description` is extracted from the `SKILL.md` frontmatter.

## 📤 `uploadskill`

**Use case**

You already prepared a local skill and want to automatically submit it to the default MagicSkills repository and create a Pull Request.

**Command format**

```bash
magicskills uploadskill <source>
```

**Parameters**

- `<source>`: may be a skill name in `Allskills` or a local skill directory path

**Default workflow**

- Validate that the directory resolved from `source` exists and contains `SKILL.md`
- Check whether `gh` is installed and logged in
- `gh repo fork Narwhal-Lab/MagicSkills --clone`
- Pull the upstream default branch and create a new branch such as `fix/upload-<skill>-<timestamp>`
- Copy the skill into `skills/<skill-name>` inside the repository
- Commit, push, and create a PR

**Examples**

Upload by skill name:

```bash
magicskills uploadskill demo
```

Upload by local path:

```bash
magicskills uploadskill ./skills/demo
```

Notes:

- If multiple skills with the same name exist in `Allskills`, you must pass the skill directory path instead.
- In an interactive terminal, if `gh` is missing, the CLI asks whether to try automatic installation; if `gh` is not logged in, it asks whether to run `gh auth login`.
- If `gh auth login` is inconvenient, the CLI will also ask whether to enter a temporary `GH_TOKEN`.
- On success, it outputs fields such as `Repo`, `Branch`, `Target`, `Committed`, `Pushed`, and `PR URL`.

## 🗑️ `deleteskill`

**Use case**

You want to delete a skill completely, not just hide it from a list.

**Command format**

```bash
magicskills deleteskill <target>
```

**Parameters**

- `<target>`: may be a skill name or a skill directory path

**Examples**

Delete by name:

```bash
magicskills deleteskill demo
```

When names collide, delete by path:

```bash
magicskills deleteskill ./skills/demo
```

Notes:

- This CLI command operates on the built-in `Allskills` by default.
- Deletion removes the actual skill directory immediately and does not ask for confirmation a second time.
- After a successful deletion, if other named collections also reference the same skill path, the corresponding entries in those collections are also removed.

## 🔍 `showskill`

**Use case**

You want to fully review a skill package rather than only reading `SKILL.md`. This is useful in code review, submission flows, checking binary files, or verifying script entry points.

**Command format**

```bash
magicskills showskill <target>
```

**Parameters**

- `<target>`: may be a skill name or a skill directory path

**Examples**

View by name:

```bash
magicskills showskill demo
```

View by path:

```bash
magicskills showskill ./skills/demo
```

Notes:

- The output first shows `Skill Overview`, including name, description, skill directory, `base_dir`, `SKILL.md` path, and installation source.
- Then it shows the contents of all files under the skill directory.
- When binary files are encountered, it prints `[binary file omitted: <size> bytes]` instead of raw unreadable data.

## 🧩 `createskills`

**Use case**

You need to create an independent named skills collection for an agent, team, or workflow, then use `syncskills` to generate the matching `AGENTS.md`.

**Command format**

```bash
magicskills createskills <name> [--skill-list [SKILLS ...]] [--paths [PATHS ...]] [--tool-description TEXT] [--cli-description TEXT] [--agent-md-path PATH]
```

**Parameters**

- `<name>`: the new collection name, which must be unique
- `--skill-list [SKILLS ...]`: explicitly list which skills should enter the collection. Each item may be a skill name or a skill directory path and is resolved from `Allskills`.
- `--paths [PATHS ...]`: include the skills resolved from these paths into the new collection. Common usage patterns:
- pass a specific skill directory, for example `./.claude/skills/demo`
- pass a skills root directory, for example `./.claude/skills`
- `--tool-description`: override the collection's `tool_description` metadata
- `--cli-description`: override the collection's `cli_description` metadata
- `--agent-md-path`: specify which `AGENTS.md` this collection should sync to by default

**Examples**

Create an empty collection:

```bash
magicskills createskills coder
```

Create from an explicit skill list:

```bash
magicskills createskills reviewer --skill-list demo code-review
```

Create from explicit skill paths:

```bash
magicskills createskills reviewer --skill-list ./.claude/skills/code-review
```

Construct a collection from a skills root:

```bash
magicskills createskills coder --paths ./.claude/skills
```

Include only one specific skill:

```bash
magicskills createskills reviewer --paths ./.claude/skills/code-review
```

Specify multiple paths at once:

```bash
magicskills createskills fullstack --paths ./.claude/skills ./vendor-skills
```

Set metadata while creating the collection:

```bash
magicskills createskills coder \
  --paths ./.claude/skills \
  --tool-description "Unified skill tool for coding tasks" \
  --cli-description "Use magicskills CLI commands only" \
  --agent-md-path ./agents/coder/AGENTS.md
```

Notes:

- If neither `--skill-list` nor `--paths` is passed, the current version creates an empty named collection.
- `--skill-list` and `--paths` cannot be used together.
- Every item in `--skill-list` must resolve to a unique skill in the current `Allskills`; if names collide, pass the skill directory path instead.
- Every path in `--paths` must resolve to existing skills in the current `Allskills`, or to a parent skills root directory that contains them.
- On success, the command prints the collection name and `Skills count`.

## 🗂️ `listskills`

**Use case**

You want to inspect which named skills collections are currently registered on the machine, or feed that information into scripts.

**Command format**

```bash
magicskills listskills [--json]
```

**Parameters**

- `--json`: output a JSON array; otherwise output a human-readable boxed format

**Examples**

View all collections:

```bash
magicskills listskills
```

Output in JSON:

```bash
magicskills listskills --json
```

Each collection object in JSON output includes:

- `name`
- `skills_count`
- `paths`
- `tool_description`
- `cli_description`
- `agent_md_path`

## 🧹 `deleteskills`

**Use case**

When a named skills collection is no longer needed, you want to delete only its registration and keep the original skill files.

**Command format**

```bash
magicskills deleteskills <name>
```

**Parameters**

- `<name>`: the name of the named skills collection to delete

**Examples**

Delete a named collection:

```bash
magicskills deleteskills coder
```

Notes:

- `deleteskills` only removes collection registration and does not delete skill directories.
- The built-in `Allskills` collection cannot be deleted.

## ✏️ `changetooldescription`

**Use case**

You want to modify the `tool_description` metadata on a named skills collection so it can later be read via `listskills --json`, the Python API, or external frameworks.

**Command format**

```bash
magicskills changetooldescription <name> <description>
```

**Parameters**

- `<name>`: the name of the named skills collection
- `<description>`: the new tool description text; if it contains spaces, remember to quote it

**Examples**

Update the description:

```bash
magicskills changetooldescription coder "Unified skill tool for coding and review tasks"
```

View it after updating:

```bash
magicskills listskills --json
```

Notes:

- This updates collection metadata.
- It affects `syncskills` output only when you use `--mode tool_description`.

## ✏️ `changeclidescription`

**Use case**

You want to modify the `cli_description` metadata on a named skills collection so it can later be read via `listskills --json`, the Python API, or `syncskills --mode cli_description`.

**Command format**

```bash
magicskills changeclidescription <name> <description>
```

**Parameters**

- `<name>`: the name of the named skills collection
- `<description>`: the new CLI description text; if it contains spaces, remember to quote it

**Examples**

Update the description:

```bash
magicskills changeclidescription coder "Use magicskills listskill, readskill, and execskill commands only"
```

View it after updating:

```bash
magicskills listskills --json
```

Notes:

- This updates collection metadata.
- It affects `syncskills` output only when you use `--mode cli_description`.

## 🤖 `skill-tool`

**Use case**

When you need a stable CLI wrapper oriented toward agent/tool-call usage, this command is the right fit. It wraps `listskill`, `readskill`, and `execskill` into a unified JSON return structure and uses the process exit code to indicate success or failure.

**Command format**

```bash
magicskills skill-tool <action> [--arg ARG] [--name NAME]
```

**Parameters**

- `<action>`: action name, supporting the following primary actions and aliases
- `listskill`, `list`, `list_metadata`
- `readskill`, `read`, `read_file`
- `execskill`, `exec`, `run_command`
- `--arg ARG`: action argument
- for `listskill`, this can usually be omitted
- for `readskill`, pass a skill name or file path
- for `execskill`, pass a plain command string, a JSON string, or the legacy `name::command` format
- `--name NAME`: specify which named skills collection to use; if omitted, `Allskills` is used by default

**Examples**

List skills in the default collection:

```bash
magicskills skill-tool listskill
```

Read a skill inside a named collection:

```bash
magicskills skill-tool readskill --name coder --arg demo
```

Read an explicit file path:

```bash
magicskills skill-tool readskill --arg ./skills/demo/SKILL.md
```

Execute a plain command string:

```bash
magicskills skill-tool execskill --arg "echo hello"
```

Execute a command via JSON input:

```bash
magicskills skill-tool execskill --arg '{"command":"echo hello"}'
```

Support the legacy `name::command` format:

```bash
magicskills skill-tool execskill --arg 'demo::echo hello'
```

Notes:

- Output is always JSON.
- When `ok` is `true`, the CLI exits with code `0`; otherwise it exits with code `1`.
- When an unknown action is passed, it returns `{"ok": false, "error": "Unknown action: ..."}`.
