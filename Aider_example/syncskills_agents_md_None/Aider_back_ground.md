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
- 但不会把 `AGENTS.md` 里的 skill 自动注册成真实工具

当前这个 `None` 版 `AGENTS.md` 写的是：

- 只使用 `Available Skills` 里列出的 skill
- 先读取对应 skill 的 `SKILL.md`
- 再根据 `SKILL.md` 决定是否继续读文档或执行脚本

实际日志说明了一件更细的事：

- 它有时能大致遵守这个方向
- 但不会稳定地一次就给出正确命令

`log1.txt` 里，它先推荐：

```text
cat /root/allskills/c_2_ast/SKILL.md
```

然后在看到输出后，又继续推荐：

```text
ls -la /root/allskills/c_2_ast/
cat /root/allskills/c_2_ast/reference.md
```

这说明它确实会沿着“先读 `SKILL.md`，再读补充文档”的思路走。

但 `log2.txt` 里，它第一步又会直接幻觉出一个并不存在的脚本：

```text
/root/allskills/c_2_ast/parse_c_to_ast.sh
```

报错以后，它才逐步回到正确路径：

- 先读 `SKILL.md`
- 再看目录
- 再看 `scripts/`
- 最后收敛到 `c_2_ast.py --input ...`

因此在 MagicSkills 场景下，要特别注意：

- `AGENTS.md` 对 `aider` 是弱约束
- 它能参考规则，但不能保证严格执行
- 真正有效的是你把每一步 `/run` 结果继续喂回去

---

## 4. Aider 最核心的能力是什么

最核心的是两件事：

### 4.1 聊天回答

例如：

```text
cat /root/allskills/c_2_ast/SKILL.md
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
cd /root/LLK/MagicSkills/Aider_example/syncskills_agents_md_None
aider --model openai/qwen3-max --subtree-only --no-auto-commits
```

从实际日志看，这样启动后，`aider` 会自动把当前目录下的 `AGENTS.md` 加入只读上下文。

这样做的目的：

- `--subtree-only`
  - 只关注当前示例目录，减少大仓库噪音
- `--no-auto-commits`
  - 避免模型误操作后直接自动提交

如果你想显式指定，也可以写成：

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
- 帮你根据已有 skill 文档整理下一步命令

也就是：

- 文件编辑类任务
- 代码理解类任务
- 文档整理类任务
- 半自动命令规划任务

### 7.2 不适合的用法

`aider` 不适合直接承担下面这种角色：

- 读取 `AGENTS.md`
- 自动选择 skill
- 自动读取对应 `SKILL.md`
- 自动执行脚本
- 自动把结果喂回模型
- 一直循环直到完成任务

这是标准的工具型 agent / orchestration runner 的工作，不是 `aider` 的强项。

---

## 8. 在本项目里最实用的工作方式

如果你的目标是“让 `aider` 参考当前 `AGENTS.md` 里的 skill 列表”，最实用的办法不是指望它一步答对，而是采用下面这种半自动流程：

1. 用 `/ask` 让它只给出下一条命令
2. 你手动用 `/run` 执行
3. 把实际输出继续喂回去
4. 让它基于新输出给出下一条命令

这正是 `log1.txt` 和 `log2.txt` 里真正有效的部分。

### 8.1 场景一：我想了解更多 AST 知识

`log1.txt` 里的原始提问是：

```text
/ask 我想了解更多AST知识。请给出下一步命令
```

在这个场景里，日志里实际跑通的链路是：

1. 先让它给出第一条命令

```text
cat /root/allskills/c_2_ast/SKILL.md
```

2. 你手动执行

```text
/run cat /root/allskills/c_2_ast/SKILL.md
```

3. 再继续问下一条命令

```text
/ask 我想了解更多AST知识。请给出下一步命令
```

4. 它会进一步推荐

```text
ls -la /root/allskills/c_2_ast/
```

5. 你执行后，再继续问

```text
cat /root/allskills/c_2_ast/reference.md
```

所以在这个 `None` 版场景里，更符合真实日志的理解是：

- 先选中 `c_2_ast`
- 先读 `SKILL.md`
- 再看技能目录结构
- 再读 `reference.md`

这里不是先跑 `listskill`，也不是先做 `/read-only`，而是直接用最普通的 shell 命令逐步探索。

### 8.2 场景二：我想把一段 C 代码转换为 AST

`log2.txt` 里的原始提问是：

```text
/ask 给出下一条命令，我想将下面这段 C 代码转换为 AST
```

对应的 C 代码是：

```c
#include <stdio.h>

int main() {
    puts("Hello from agent");
    return 0;
}
```

这个日志最值得保留的不是第一条答案，而是它暴露出的两个典型错误。

第一个错误：Aider 一开始幻觉出了一个不存在的脚本：

```text
/root/allskills/c_2_ast/parse_c_to_ast.sh
```

第二个错误：后面它虽然找到了真正的脚本 `c_2_ast.py`，但第一次调用时漏掉了必需参数：

```text
python3 /root/allskills/c_2_ast/scripts/c_2_ast.py /root/allskills/c_2_ast/scripts/input.c
```

执行后真实报错是：

```text
usage: c_2_ast.py [-h] --input INPUT
c_2_ast.py: error: the following arguments are required: --input
```

报错再喂回去以后，它才修正为：

```text
python3 /root/allskills/c_2_ast/scripts/c_2_ast.py --input /root/allskills/c_2_ast/scripts/input.c
```

因此，这个场景里日志实际证明的稳妥流程是：

1. 如果第一条命令明显可疑，先执行一下，用真实错误把它纠正回来
2. 然后回到 `SKILL.md`
3. 再看技能目录
4. 再看 `scripts/`
5. 再生成输入文件
6. 最后调用真正脚本

也就是这条链路：

```text
cat /root/allskills/c_2_ast/SKILL.md
ls -l /root/allskills/c_2_ast/
ls -l /root/allskills/c_2_ast/scripts/
echo '...C code...' > /root/allskills/c_2_ast/scripts/input.c
python3 /root/allskills/c_2_ast/scripts/c_2_ast.py --input /root/allskills/c_2_ast/scripts/input.c
```

如果只看这两个日志，那么对 `None` 模式最准确的总结就是：

- 它可能先说错
- 但你把真实命令输出持续回填后，它能逐步收敛

### 8.3 一个典型误区

在这个场景里，最常见的问题通常有三件事。

第一件，以为 `AGENTS.md` 里已经写了 skill 规则，`aider` 就会自动执行完整流程。

实际日志证明不是这样。
它最多只是“参考这些规则”，不会自动读取 `SKILL.md`、自动运行脚本、自动重试直到成功。

第二件，以为它第一次给出的命令就一定可靠。

`log2.txt` 里第一条就是错的：

```text
/root/allskills/c_2_ast/parse_c_to_ast.sh
```

所以这里真正靠谱的不是“相信第一条答案”，而是：

- 执行
- 看报错
- 把结果喂回去
- 让它继续收敛

第三件，把“最终成功”误解成“它一开始就懂了”。

实际上，日志里真正有效的是你后面手动做的这些事：

- `/run cat /root/allskills/c_2_ast/SKILL.md`
- `/run ls -l /root/allskills/c_2_ast/`
- `/run ls -l /root/allskills/c_2_ast/scripts/`
- `/run python3 ... --input ...`

所以整件事可以压缩成一句话：

- `aider` 在 `None` 模式下可以帮你规划下一步
- 但正确结果通常来自“逐步执行并回填输出”，不是一次性自动完成

在 `aider` 里，最核心的区分就是：

- 问问题，不想改文件，用 `/ask`
- 真要执行命令，用 `/run`
- 真要改代码，用普通输入或者 `/code`

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

在本项目里，把它当成“会参考 `AGENTS.md` 的代码编辑助手”是对的；把它当成“原生支持技能循环调用的 Agent”通常会失望。

而对当前这个 `None` 版示例来说，更准确的理解是：

- `AGENTS.md` 已经列出可用 skill
- `aider` 有时会先读对 `SKILL.md`，有时也会先答错
- 真正稳定的方法是 `/ask` 规划一步、`/run` 执行一步、再把结果继续喂回去
