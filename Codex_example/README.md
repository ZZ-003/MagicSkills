# Codex Examples

本目录汇总了 Codex 的两种 `syncskills` 集成方式。

## 推荐先看哪个

- 如果你想让 Codex 直接根据 `AGENTS.md` 里的 `<usage> + <available_skills>` 使用 skill，先看 [syncskills_agents_md_None](./syncskills_agents_md_None/README.md)。
- 如果你想显式要求 Codex 先走 `magicskills skill-tool listskill/readskill/execskill` 这套 CLI 流程，再看 [syncskills_agents_md_cli](./syncskills_agents_md_cli/README.md)。

## 两种方式的区别

- `syncskills_agents_md_None`：使用默认的 `syncskills` 输出，把选中的 skill 以标准 `Available Skills` 形式写入 `AGENTS.md`。
- `syncskills_agents_md_cli`：使用 `syncskills --mode cli_description`，把 `AGENTS.md` 改写成以 `magicskills skill-tool` 为核心的 CLI 指引。

## 入口

- [None 模式示例](./syncskills_agents_md_None/README.md)
- [CLI 模式示例](./syncskills_agents_md_cli/README.md)
