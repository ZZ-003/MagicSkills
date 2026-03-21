"""Hugging Face smolagents example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r smolagents_example/requirements.txt
    python smolagents_example/model.py --scenario all

Env vars (put in .env):
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel, Tool

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills createskills smolagents_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills createskills smolagents_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("smolagents_agent1_skills")
    except KeyError:
        errors.append("smolagents_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("smolagents_agent2_skills")
    except KeyError:
        errors.append("smolagents_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Per-agent skill tool factory ────────────────────────────
def _make_skill_tool(skills: Skills) -> Tool:
    class MagicSkillsTool(Tool):
        name = "skill_tool"
        description = skills.tool_description
        inputs = {
            "action": {
                "type": "string",
                "description": "The action to perform (listskill / readskill / execskill)",
            },
            "arg": {
                "type": "string",
                "description": "The argument for the action",
                "nullable": True,
            },
        }
        output_type = "string"

        def __init__(self) -> None:
            super().__init__()
            self._skills = skills

        def forward(self, action: str, arg: str = "") -> str:
            result = self._skills.skill_tool(action.strip(), arg.strip())
            return json.dumps(result, ensure_ascii=False)

    return MagicSkillsTool()


# ── 2b. 修补 DeepSeek 的 </code 截断问题 ──────────────────────
class PatchedOpenAIServerModel(OpenAIServerModel):
    """Fix DeepSeek V3.2 outputting '</code' without closing '>'."""

    def __call__(self, messages, **kwargs):
        result = super().__call__(messages, **kwargs)
        if hasattr(result, "content") and isinstance(result.content, str):
            result.content = re.sub(r"</code(?!>)", "</code>", result.content)
        return result


# ── 3. 场景配置 ─────────────────────────────────────────────────
SCENARIOS: dict[str, tuple[str, str, Skills]] = {
    "read": (
        "log1.json",
        "我想了解更多 AST 知识。",
        agent1_skills,
    ),
    "exec": (
        "log2.json",
        "请将下面这段 C 代码转换为 AST\n"
        "```c\n"
        "#include <stdio.h>\n\n"
        "int main() {\n"
        '    puts("Hello from agent");\n'
        "    return 0;\n"
        "}\n"
        "```",
        agent2_skills,
    ),
}


class TeeWriter(io.TextIOBase):
    def __init__(self, *writers: io.TextIOBase) -> None:
        self._writers = writers

    def write(self, s: str) -> int:
        for writer in self._writers:
            writer.write(s)
        return len(s)

    def flush(self) -> None:
        for writer in self._writers:
            writer.flush()


def run_once(prompt: str, log_name: str, skills: Skills) -> None:
    # ── 4. 构建 agent 并运行 ──────────────────────────────────
    model = PatchedOpenAIServerModel(
        model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_base=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    agent = CodeAgent(
        tools=[_make_skill_tool(skills)],
        model=model,
        additional_authorized_imports=["json", "sys", "os", "subprocess", "pathlib"],
        max_steps=50,
        instructions="On Windows, use 'python' instead of 'python3' when running scripts.",
    )

    log_file = Path(__file__).parent / log_name
    log_buffer = io.StringIO()
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = TeeWriter(original_stdout, log_buffer)
    sys.stderr = TeeWriter(original_stderr, log_buffer)
    try:
        result = agent.run(prompt)
        print("\n=== final ===")
        print(result)
        log_content = log_buffer.getvalue()
    except BaseException:
        log_content = "[ERROR] Agent run interrupted or failed."
        raise
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(log_content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=["read", "exec", "all"],
        default="all",
        help="Which scenario to run: read (log1), exec (log2), or all.",
    )
    args = parser.parse_args()

    targets = ["read", "exec"] if args.scenario == "all" else [args.scenario]
    for name in targets:
        log_name, prompt, skills = SCENARIOS[name]
        print(f"\n================ {name.upper()} ================\n")
        run_once(prompt, log_name, skills)


if __name__ == "__main__":
    main()
