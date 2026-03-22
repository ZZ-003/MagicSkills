# Cursor


## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令

本文的示例 skill 以 **`docx`** 为例


### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install skill_template  -t ~/allskills` 选择从本地已经下载好的skill下载到目标路径里

执行 `magicskills install https://github.com/anthropics/skills.git -t ~/allskills`将github上的下载到目标路径

### 创建skills

执行 `magicskills addskills cursor_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills cursor_skills --mode cli_description --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`addskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容
'''md
<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Whenever you receive a task, you must first run "magicskills skill-tool listskill --name cursor_skills" to view all available skills.
Then use "magicskills skill-tool readskill --arg <file_path>" to read the selected skill's SKILL.md file by path.
Based on that documentation, either continue reading more files with "magicskills skill-tool readskill --arg <file_path>" or run the needed command with "magicskills skill-tool execskill --arg <command>".
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

'''

# 设置cursor添加对应的AGENTS.md到它的rules里
cursor一般会在当前目录下的所有AGENTS.md都添加到当前rules


# 了解更多AST知识
我想了解更多AST知识
见image1.png



# 转换一段代码为AST代码

我想将下面这段 C 代码转换为 AST
```c
#include <stdio.h>

int main() {
    puts("Hello from agent");
    return 0;
}
```

见image2.png
