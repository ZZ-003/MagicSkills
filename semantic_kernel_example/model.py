"""Semantic Kernel function-calling example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r semantic_kernel_example/requirements.txt
    python semantic_kernel_example/model.py --scenario all

Env vars (put in .env):
    OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
"""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import sys
from typing import Any
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from openai import AsyncOpenAI
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills addskills semantic_kernel_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills addskills semantic_kernel_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("semantic_kernel_agent1_skills")
    except KeyError:
        errors.append("semantic_kernel_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("semantic_kernel_agent2_skills")
    except KeyError:
        errors.append("semantic_kernel_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Per-agent skill plugin factory ──────────────────────────
def _make_skill_plugin(skills: Skills) -> object:
    class MagicSkillsPlugin:
        @kernel_function(
            name="skill_tool",
            description=skills.tool_description,
        )
        async def skill_tool(self, action: str, arg: str = "") -> str:
            result = skills.skill_tool(action, arg)
            return json.dumps(result, ensure_ascii=False)

    return MagicSkillsPlugin()


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


def _dump_payload(value: Any) -> str:
    if hasattr(value, "model_dump"):
        data = value.model_dump(mode="json")
    else:
        data = value
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def _record_message(log_lines: list[str], header: str, payload: Any) -> None:
    body = _dump_payload(payload)
    print(header)
    print(body)
    log_lines.extend([header, body])


# ── 4. 构建 agent 并运行 ──────────────────────────────────────
async def run_once(prompt: str, log_name: str, skills: Skills) -> None:
    chat_service = OpenAIChatCompletion(
        ai_model_id=os.getenv("OPENAI_MODEL"),
        async_client=AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        ),
    )

    agent = ChatCompletionAgent(
        service=chat_service,
        plugins=[_make_skill_plugin(skills)],
        instructions="On Windows, use 'python' instead of 'python3' when running scripts.",
    )

    log_lines: list[str] = []
    log_file = Path(__file__).parent / log_name
    response_count = 0
    final_text = "[EMPTY]"

    async def on_intermediate_message(message: Any) -> None:
        header = f"\n--- intermediate | {type(message).__name__} ---"
        _record_message(log_lines, header, message)

    try:
        async for response in agent.invoke(
            messages=prompt,
            on_intermediate_message=on_intermediate_message,
        ):
            response_count += 1
            header = f"\n--- final_response | {response_count} ---"
            _record_message(log_lines, header, response.message)
            final_text = str(response.content)

        footer = "\n=== final ==="
        print(footer)
        print(final_text)
        log_lines.extend([footer, final_text])
    finally:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))


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
