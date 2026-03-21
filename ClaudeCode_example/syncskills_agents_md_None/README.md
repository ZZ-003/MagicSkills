# Claude Code

## Claude Code启动

## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令



### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills`

执行 `magicskills install https://github.com/langchain-ai/deepagentsjs.git -t ~/allskills`

### 创建skills

执行 `magicskills createskills claudecode --skill-list c_2_ast arxiv-search --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills claudecode   --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容

```markdown
# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively.

How to use skills:
First, read the SKILL.md file in the corresponding path of the skill. Then, based on its content, decide whether to read more related docs or execute the relevant command or script.

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
</usage>

<available_skills>

<skill>
<name>c_2_ast</name>
<description>Parse C source code into an Abstract Syntax Tree (AST). Use when analyzing C programs, understanding code structure, performing static analysis, or preparing code for further program analysis (e.g., CFG, DFG, vulnerability detection).</description>
<path>C:\Users\13978\allskills\c_2_ast</path>
</skill>

<skill>
<name>arxiv-search</name>
<description>Search arXiv preprint repository for papers in physics, mathematics, computer science, quantitative biology, and related fields</description>
<path>C:\Users\13978\allskills\arxiv-search</path>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>


```

# claude注意

他只会读取CLAUDE.md
我们可以选择
```bash
magicskills syncskills claudecode  --output ./CLAUDE.md -y
```
或者生成AGENTS.md后
```bash
cp AGENTS.md CLAUDE.md
```

# 了解更多AST知识

我想了解更多AST知识
见log1.txt

# 转换一段代码为AST代码

我想将下面这段 C 代码转换为 AST
```c
#include <stdio.h>

int main() {
    puts("Hello from agent");
    return 0;
}
```

见log2.txt

# 询问最近的计算机视觉相关论文

见log3.txt