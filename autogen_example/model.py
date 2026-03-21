"""AutoGen agent example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r autogen_example/requirements.txt
    python autogen_example/model.py --scenario all

Env vars (put in .env):
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
"""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import re
import sys
import traceback
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelFamily
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills createskills autogen_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills createskills autogen_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""

PYTHON_EXE = Path(sys.executable).resolve()


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("autogen_agent1_skills")
    except KeyError:
        errors.append("autogen_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("autogen_agent2_skills")
    except KeyError:
        errors.append("autogen_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Path normalizer (fixes LLM-hallucinated script paths) ───
def _get_c2ast_scripts(skills: Skills) -> Path:
    try:
        skill = skills.get_skill("c_2_ast")
        return (skill.path.parent / "scripts").resolve()
    except KeyError:
        return (ROOT / "skill_template" / "c_2_ast" / "scripts").resolve()


def _normalize_exec_arg(arg: str, skills: Skills) -> str:
    c2ast_scripts = _get_c2ast_scripts(skills)
    normalized = (arg or "").strip()
    if not normalized:
        return normalized

    for pattern in (
        r"skills_for_all_agent/skill/c_2_ast/scripts",
        r"/root/\.agent/skills/c_2_ast/scripts",
        r"/root/[^\s]*/c_2_ast/scripts",
    ):
        normalized = re.sub(pattern, lambda _m: str(c2ast_scripts), normalized)

    normalized = re.sub(
        r"(^|&&\s*)(python3|python)(\s+)",
        lambda m: f'{m.group(1)}"{PYTHON_EXE}"{m.group(3)}',
        normalized,
    )
    normalized = normalized.replace("ls -la", "dir")
    return normalized


def _truncate_readskill_result(payload: dict[str, object], limit: int = 6000) -> dict[str, object]:
    if payload.get("action") != "readskill" or not payload.get("ok"):
        return payload
    content = payload.get("result")
    if isinstance(content, str) and len(content) > limit:
        payload["result"] = content[:limit] + "\n...[TRUNCATED]..."
    return payload


# ── 3. Per-agent skill tool factory ────────────────────────────
def _make_skill_tool(skills: Skills) -> FunctionTool:
    async def skill_tool_fn(action: str, arg: str = "") -> str:
        """Unified skill tool interface for MagicSkills."""
        fixed_arg = _normalize_exec_arg(arg, skills) if action == "execskill" else arg
        result = skills.skill_tool(action, fixed_arg)
        result = _truncate_readskill_result(result)
        return json.dumps(result, ensure_ascii=False)

    return FunctionTool(skill_tool_fn, description=skills.tool_description)


# ── 4. 场景配置 ─────────────────────────────────────────────────
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


# ── 5. 构建 agent 并运行 ──────────────────────────────────────
async def run_once(task: str, log_name: str, skills: Skills) -> None:
    model_family = getattr(ModelFamily, "UNKNOWN", ModelFamily.GPT_4O)
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": False,
            "family": model_family,
            "structured_output": False,
        },
    )

    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[_make_skill_tool(skills)],
        system_message=(
            "You are a helpful assistant. You MUST always start every task by calling "
            "skill_tool with action='listskill' to discover available skills. "
            "Then use action='readskill' to read the relevant SKILL.md file before answering. "
            "Only use action='execskill' when the task requires running a command or script. "
            "Never answer from memory alone — always check skills first. "
            "When all steps are done and you have the final output, end your response with the word TERMINATE."
        ),
        reflect_on_tool_use=False,
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        termination_condition=MaxMessageTermination(30) | TextMentionTermination("TERMINATE"),
    )

    log_file = Path(__file__).parent / log_name
    try:
        result = await Console(team.run_stream(task=task), output_stats=True)
        lines: list[str] = []
        for i, message in enumerate(result.messages):
            header = f"\n--- {i} | {type(message).__name__} ---"
            lines.append(header)
            print(header)
            payload = json.dumps(message.model_dump(), ensure_ascii=False, indent=2, default=str)
            lines.append(payload)
            print(payload)
        log_content = "\n".join(lines)
    except BaseException:
        log_content = (
            "[ERROR] Agent run interrupted or failed.\n\n"
            + traceback.format_exc()
        )
        print(log_content)
    finally:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(log_content)


async def main() -> None:
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
        await run_once(prompt, log_name, skills)


if __name__ == "__main__":
    asyncio.run(main())
