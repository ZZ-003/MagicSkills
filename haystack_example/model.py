"""Haystack agent example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r haystack_example/requirements.txt
    python haystack_example/model.py --scenario all

Env vars (put in .env):
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.tools import create_tool_from_function
from haystack.utils import Secret

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills createskills haystack_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills createskills haystack_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("haystack_agent1_skills")
    except KeyError:
        errors.append("haystack_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("haystack_agent2_skills")
    except KeyError:
        errors.append("haystack_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Per-agent skill tool factory ────────────────────────────
def _make_skill_tool(skills: Skills):
    def skill_tool_fn(action: str, arg: str = "") -> str:
        """MagicSkills unified tool interface."""
        result = skills.skill_tool(action, arg)
        return json.dumps(result, ensure_ascii=False)

    return create_tool_from_function(
        function=skill_tool_fn,
        name="skill_tool",
        description=skills.tool_description,
    )


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


def run_once(prompt: str, log_name: str, skills: Skills) -> None:
    # ── 4. 构建 agent 并运行 ──────────────────────────────────
    generator = OpenAIChatGenerator(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        generation_kwargs={"temperature": 0.2},
        timeout=300.0,
    )

    agent = Agent(
        chat_generator=generator,
        tools=[_make_skill_tool(skills)],
        system_prompt="Always call skill_tool in order: listskill, readskill, then execskill if needed.", # Haystack 框架限制，read 场景不加 system_prompt 就展示不了渐进式披露
        max_agent_steps=20,
    )

    log_file = Path(__file__).parent / log_name
    try:
        result = agent.run(messages=[ChatMessage.from_user(prompt)])
        log_content = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        print(log_content)
    except BaseException:
        log_content = "[ERROR] Agent run interrupted or failed."
        raise
    finally:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(log_content or "[EMPTY]")


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
