# Contributing to MagicSkills

For Chinese readers, see [CONTRIBUTING.zh-CN.md](./CONTRIBUTING.zh-CN.md).

Thanks for your interest in improving MagicSkills. We welcome bug reports, feature proposals, documentation improvements, reusable skill contributions, and focused pull requests.

## Before You Start

- Search existing discussions, issues, and pull requests before opening a new one.
- For feature ideas, workflow proposals, larger behavior changes, or API / CLI changes, start with a GitHub Discussion or open an issue first to discuss the motivation and direction.
- Small fixes such as typos, documentation clarifications, or narrowly scoped bug fixes can usually go directly to a pull request.

## Ways to Contribute

- Report bugs and regressions
- Propose new features or workflow improvements
- Improve documentation, examples, and onboarding materials
- Contribute reusable skills
- Fix implementation bugs or improve tests

## Contribution Workflow

1. Open or find a discussion or issue if the change is not trivial.
2. Fork the repository and create a focused branch.
3. Make the smallest change that solves the problem.
4. Update docs, examples, or CLI help text if user-facing behavior changes.
5. Run relevant tests or examples for the area you changed.
6. Open a pull request with enough context for review.

## Branch Naming

Recommended branch prefixes:

- `feat/...` for new features
- `fix/...` for bug fixes
- `docs/...` for documentation-only changes
- `chore/...` for maintenance work

Examples:

```text
feat/add-github-templates
fix/addskill-name-resolution
docs/update-contributing-guide
```

## Commit Messages

Clear, focused commit messages are preferred. A conventional style is recommended but not strictly required.

Recommended format:

```text
type(scope): short summary
```

Examples:

```text
feat(cli): add addskill collection support
fix(syncskills): preserve description when rewriting agents file
docs(readme): add contribution guide link
```

## Pull Request Expectations

Please include:

- a short summary of what changed
- why the change is needed
- the linked issue, if there is one
- testing or validation notes
- screenshots or terminal output when they help explain the change

Please avoid:

- unrelated refactors in the same pull request
- formatting-only churn in untouched files
- silent behavior changes without documentation updates

## Skill Contributions

If you are contributing a reusable skill:

- make sure the skill directory contains `SKILL.md`
- include scripts, references, or assets only when they are actually needed
- describe the intended use case clearly in `SKILL.md`
- keep the skill self-contained and easy to inspect

## Review Notes

- Maintainers may ask you to split large pull requests into smaller pieces.
- Feature ideas may be redirected to GitHub Discussions or issue discussion before code review starts.
- Review latency can vary depending on scope and maintainer availability.

## Licensing

By submitting code, documentation, or skills to this repository, you agree that your contribution will be distributed under the repository's [MIT License](./LICENSE).
