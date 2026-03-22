# Codex

## codex启动

cd到Codex_example文件夹
/init 在当前启动codex的目录下初始化一个AGENTS.md文件

MagicSkills/Codex_example/image/image1.png

## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令



### 安装 skill(之前已经下载过的可以选择跳过)


执行 `magicskills install skill_template  -t ~/allskills` 选择从本地已经下载好的skill下载到目标路径里

执行 `magicskills install https://github.com/anthropics/skills.git -t ~/allskills`将github上的下载到目标路径

### 创建skills

执行 `magicskills createskills codex_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills codex_skills --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容
'''md
# Repository Guidelines


When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively.

How to use skills:
Unified skill cli. If you are not sure, you can first use "magicskills listskill" to search for available skills. Then, determine which skill might be the most useful. After that, try to use "magicskills readskill <path>" to read the SKILL.md file under this skill path to get more detailed information. Finally, based on the content of this file, decide whether to read the documentation in other paths or use "magicskills execskill <command>" to directly execute the relevant script.

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
<path>/root/allskills/c_2_ast</path>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>

'''


# 了解更多AST知识

我想了解更多AST知识
见log1.txt

# 转换一段代码为AST代码

请将下面这段 C 代码转换为 AST
```c
#include <stdio.h>

int main() {
    puts("Hello from agent");
    return 0;
}
```

见log2.txt
