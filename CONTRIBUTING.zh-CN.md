# 参与贡献指南

英文版见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

感谢你关注 MagicSkills。我们欢迎 Bug 反馈、功能建议、文档改进、可复用 skill 贡献，以及聚焦明确的 Pull Request。

## 开始之前

- 提交前先搜索已有的 Discussions、Issue 和 Pull Request，避免重复。
- 如果是功能想法、工作流建议、较大的行为变更，或者会影响 API / CLI 的改动，请先在 GitHub Discussions 或 Issue 里讨论动机和方向。
- 如果只是错别字修复、文档澄清或范围很小的 Bug 修复，通常可以直接提 PR。

## 可以贡献什么

- 报告 Bug 和回归问题
- 提出新功能或工作流改进建议
- 改进文档、示例和上手材料
- 贡献可复用的 skill
- 修复实现问题或补充测试

## 推荐流程

1. 如果改动不算很小，先创建或认领一个 Discussion 或 Issue。
2. Fork 仓库，并创建一个聚焦的分支。
3. 用最小改动解决当前问题。
4. 如果用户可见行为发生变化，请同步更新文档、示例或 CLI 帮助信息。
5. 运行与你改动相关的测试或示例。
6. 提交 Pull Request，并附上足够的上下文。

## 分支命名

推荐使用下面这些前缀：

- `feat/...` 用于新功能
- `fix/...` 用于 Bug 修复
- `docs/...` 用于纯文档改动
- `chore/...` 用于维护性工作

示例：

```text
feat/add-github-templates
fix/addskill-name-resolution
docs/update-contributing-guide
```

## Commit Message

建议使用清晰、聚焦的提交信息。推荐采用 conventional 风格，但不是强制要求。

推荐格式：

```text
type(scope): short summary
```

示例：

```text
feat(cli): add addskill collection support
fix(syncskills): preserve description when rewriting agents file
docs(readme): add contribution guide link
```

## Pull Request 需要包含什么

请尽量包含以下内容：

- 这次改了什么
- 为什么需要这个改动
- 关联的 Issue，如果有
- 测试或验证说明
- 如果有帮助，可以附上截图或终端输出

也请尽量避免：

- 在同一个 PR 里混入无关重构
- 对未涉及文件做纯格式化噪音改动
- 修改了行为却没有同步更新文档

## skill 贡献说明

如果你要贡献一个可复用的 skill：

- 确保 skill 目录里包含 `SKILL.md`
- 只有在确实需要时再附带 `scripts`、`references` 或 `assets`
- 在 `SKILL.md` 中明确说明适用场景
- 尽量让 skill 自包含且便于审查

## Review 说明

- 对于较大的 PR，维护者可能会要求拆分成更小的改动。
- 对于功能建议，维护者可能会先要求在 GitHub Discussions 或 Issue 中讨论，再进入代码审查。
- Review 速度会受到改动范围和维护者时间安排影响。

## 许可证

当你向本仓库提交代码、文档或 skill 时，即表示你同意这些贡献将按照仓库的 [MIT License](./LICENSE) 发布。
