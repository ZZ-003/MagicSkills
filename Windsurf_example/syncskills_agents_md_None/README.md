# windsurf


## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令



### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills`



### 创建skills

执行 `magicskills createskills Windsurf_skills --skill-list c_2_ast --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills Windsurf_skills --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容
'''md


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

# 设置windsurf添加对应的AGENTS.md到它的global rules里


# 了解更多AST知识

我想了解更多AST知识
见image1.png



# 转换一段代码为AST代码

请将下面这段 C 代码转换为 AST
```c
#include <stdio.h>

int main() {
    puts("Hello from agent");
    return 0;
}
```

见image2.png
