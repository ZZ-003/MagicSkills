# Aider

## 使用Aider
python -m pip install aider-install
aider-install

cd /to/your/project

export OPENAI_API_BASE={}
export OPENAI_API_KEY={}

aider --model openai/qwen3-max --subtree-only --no-auto-commits



## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令
或者直接`pip install magicskills` 

本文的示例 skill 以 **`docx`** 为例
### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills` 选择从本地已经下载好的skill下载到目标路径里

执行 `magicskills install https://github.com/anthropics/skills.git -t ~/allskills`将github上的下载到目标路径

### 创建skills

执行 `magicskills createskills Aider_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills Aider_skills  --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
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
<path>/root/allskills/c_2_ast</path>
</skill>

<skill>
<name>docx</name>
<description>Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.</description>
<path>/root/allskills/docx</path>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>

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
