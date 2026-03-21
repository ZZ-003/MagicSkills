# Claude Code

## Claude Code启动

## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令



### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills`

执行 `magicskills install https://github.com/anthropics/skills.git -t ~/allskills`


### 创建skills

执行 `magicskills createskills claudecode --skill-list c_2_ast brand-guidelines --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills claudecode --mode cli_description --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容

```markdown
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Whenever you receive a task, you must first run "magicskills skill-tool listskill --name claudecode" to view all available skills.
Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's SKILL.md file by path.
Based on that documentation, either continue reading more files with "magicskills skill-tool readskill --arg <file_path>" or run the needed command with "magicskills skill-tool execskill --arg <command>".
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

```

# claude注意

他只会读取CLAUDE.md
我们可以选择
```bash
magicskills syncskills claudecode --mode cli_description --output ./CLAUDE.md -y
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
