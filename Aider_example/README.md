# Aider

## 使用Aider
python -m pip install aider-install
aider-install

cd /to/your/project

export OPENAI_API_BASE={}
export OPENAI_API_KEY={}

aider --model openai/{}



## 安装magicskills

首先 `git clone https://github.com/Narwhal-Lab/MagicSkills.git`

并执行  `pip install -e .` 指令
或者直接`pip install magicskills` 

本文的示例 skill 以 **`docx`** 为例
### 安装 skill(之前已经下载过的可以选择跳过)

执行 `magicskills install anthropics/skills -t ~/allskills`


### 创建skills

执行 `magicskills createskills Aider_skills --skill-list docx --agent-md-path ./AGENTS.md`

### 生成 AGETNS.md

执行 `magicskills syncskills Aider_skills --mode cli_description --output ./AGENTS.md -y` 指定输出AGENTS.md路径，不指定时候就默认用`createskills`指定的`--agent-md-path ./AGENTS.md`
此时AGENTS.md会出现如下内容

```markdown
# AGENTS

<skills_system priority="1">

<!-- SKILLS_TABLE_START -->
<usage>
Unified skill CLI tool. Use "magicskills skill-tool listskill --name Aider_skills" to find relevant skills.
Then use "magicskills skill-tool readskill --arg <path>" to read the selected skill's SKILL.md or related docs.
If needed, use "magicskills skill-tool execskill --arg <command>" to run the command.
</usage>
<!-- SKILLS_TABLE_END -->

</skills_system>

```


