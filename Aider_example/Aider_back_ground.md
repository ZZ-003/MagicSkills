# Aider 背景说明

## 1. Aider 是什么

`aider` 本质上是一个“面向代码仓库的 LLM 聊天编辑器”。

它最擅长的事情是：

- 读取当前 git 仓库里的文件
- 把文件内容和仓库结构整理后发给大模型
- 根据模型输出修改文件
- 结合 git 做差异查看、提交、撤销

所以它更像“会改代码的对话式编辑器”，而不是“会自己循环调用工具的通用 Agent”。

---

## 2. Aider 的基本原理

可以把一轮 `aider` 会话理解成下面这个流程：

1. 读取当前仓库信息
   - 找到 `git working dir`
   - 收集仓库里的文件列表
   - 生成 `repo-map`，也就是给模型看的仓库结构摘要

2. 收集上下文
   - 你当前加入 chat 的文件
   - `--read` / `read-only` 文件
   - 历史对话
   - 系统提示和编辑格式说明

3. 把这些内容发给模型

4. 解析模型输出
   - 如果输出像普通回答，就显示在终端里
   - 如果输出像代码修改格式，就尝试应用到文件

5. 等你进行下一轮输入

关键点：

- `aider` 有“对话循环”
- 但默认没有“自主工具循环”

也就是说，它不会天然进入这种流程：

1. 模型决定调用工具
2. 系统自动执行工具
3. 把执行结果回填给模型
4. 模型继续下一步
5. 直到任务完成

这也是它和 ReAct / tool-calling agent 的根本区别。

---

## 3. 为什么它经常“不按 AGENTS.md 做”

在 `aider` 里，`AGENTS.md` 更接近“参考提示词”，不是“强制执行协议”。

这意味着：

- 它会读取 `AGENTS.md`
- 会把里面的内容作为上下文提示给模型
- 但不会把 `AGENTS.md` 里的命令自动注册成真实工具

所以如果 `AGENTS.md` 里写的是：

- 先 `listskill`
- 再 `readskill`
- 最后 `execskill`

`aider` 最多只是“看到这些规则”，并不等于它真的获得了这些工具能力。

它仍然可能：

- 只输出一行建议命令
- 误改文件
- 幻觉出一个不存在的命令

因此在 MagicSkills 场景下，要特别注意：

- `AGENTS.md` 对 `aider` 是弱约束
- 不是强约束

---

## 4. Aider 最核心的能力是什么

最核心的是两件事：

### 4.1 聊天回答

例如：

```text
magicskills listskill
```

如果模型只输出这类文本，`aider` 会把它当普通回答显示出来。
它不会自动执行。

### 4.2 应用文件修改

如果模型输出的是可识别的编辑格式，`aider` 会把它当成“要修改文件”，然后真正写入磁盘。

所以 `aider` 的强项不是“自动跑命令”，而是“把模型输出变成文件改动”。

---

## 5. 常见命令和它们的作用

### 5.1 进入不同聊天模式

- `/ask`
  - 只问问题，不主动改文件
- `/code`
  - 进入代码修改模式
- `/architect`
  - 更偏向先规划再改动

### 5.2 文件上下文管理

- `/add <file>`
  - 把文件加入 chat，并允许编辑
- `/read-only <file>`
  - 把文件作为参考加入 chat，但不希望它被修改
- `/drop <file>`
  - 从 chat 中移除文件
- `/ls`
  - 查看当前 chat 里有哪些文件

### 5.3 执行命令

- `/run <command>`
  - 运行 shell 命令
- `! <command>`
  - 与 `/run` 类似

注意：

- `/ask` 不会执行命令
- 真正执行命令要用 `/run` 或 `!`

---

## 6. 推荐的启动方式

在这个仓库里，比较稳的启动方式通常是：

```bash
cd /root/LLK/MagicSkills/Aider_example
aider --model openai/qwen3-max --subtree-only --no-auto-commits
```

这样做的目的：

- `--subtree-only`
  - 只关注当前示例目录，减少大仓库噪音
- `--no-auto-commits`
  - 避免模型误操作后直接自动提交

如果你想让它读当前 `AGENTS.md`，可以配合：

```bash
aider --model openai/qwen3-max --subtree-only --no-auto-commits --read ./AGENTS.md
```

---

## 7. 在 MagicSkills 场景下该怎么用

### 7.1 适合的用法

`aider` 适合做这些事情：

- 帮你改 `AGENTS.md`
- 帮你改 README、文档、脚本
- 帮你分析当前仓库里的代码结构
- 帮你生成或修改与 skill 相关的本地代码

也就是：

- 文件编辑类任务
- 代码理解类任务
- 文档整理类任务

### 7.2 不适合的用法

`aider` 不适合直接承担下面这种角色：

- 读取 `AGENTS.md`
- 自动选择 skill
- 自动执行 `listskill -> readskill -> execskill`
- 自动把结果喂回模型
- 一直循环直到完成任务

这是标准的工具型 agent / orchestration runner 的工作，不是 `aider` 的强项。

---

## 8. 在本项目里最实用的工作方式

如果你的目标是“让 `aider` 参考 MagicSkills 规则”，建议采用半自动方式：

1. 用 `syncskills --mode cli_description` 生成 `AGENTS.md`
2. 启动 `aider`
3. 让它先给出下一条命令
4. 你手动 `/run` 执行
5. 再把结果给它做下一步判断

例如：

```text
/ask
只输出下一条命令，不要解释。
```

得到：

```text
magicskills skill-tool listskill --name Aider_skills
```

然后手动执行：

```text
/run magicskills skill-tool listskill --name Aider_skills
```

这种方式的优点是：

- `aider` 负责理解上下文
- 你负责真正执行命令
- 可以减少 hallucination

---

## 9. 什么时候应该不用 Aider

如果你要的是下面这种能力：

- 一次输入
- 模型自己决定下一步
- 自动调用工具
- 自动回填结果
- 反复循环直到完成

那就不应该继续硬用 `aider`。

更合适的是：

- 自己写一个 runner
- 或使用真正支持 tool-calling / agent loop 的框架

例如：

- LangGraph
- AutoGen
- Semantic Kernel
- 自定义 Python orchestrator

---

## 10. 一句话总结

`aider` 适合“读仓库 + 聊天 + 改文件”，不适合“自动执行一整套 skill 工作流直到完成任务”。

在本项目里，把它当成“会看 `AGENTS.md` 的代码编辑助手”是对的；把它当成“原生支持技能循环调用的 Agent”通常会失望。
