"""LangChain tool-binding example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r langchain_example/requirements.txt
    python langchain_example/model.py --scenario all

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
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills createskills langchain_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills createskills langchain_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("langchain_agent1_skills")
    except KeyError:
        errors.append("langchain_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("langchain_agent2_skills")
    except KeyError:
        errors.append("langchain_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Per-agent skill tool factory ────────────────────────────
def _make_skill_tool(skills: Skills):
    @tool("skill_tool", description=skills.tool_description)
    def _skill_tool(action: str, arg: str = "") -> str:
        return json.dumps(skills.skill_tool(action, arg), ensure_ascii=False)

    return _skill_tool


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


# ── 4. 多轮 tool-calling loop ─────────────────────────────────
def run_once(prompt: str, log_name: str, skills: Skills) -> None:
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=120,
    )
    skill_tool = _make_skill_tool(skills)
    llm_with_tools = llm.bind_tools([skill_tool])

    messages: list = [("user", prompt)]
    log_lines: list[str] = []
    log_file = Path(__file__).parent / log_name
    max_rounds = 15

    try:
        for _round in range(max_rounds):
            msg = llm_with_tools.invoke(messages)
            messages.append(msg)

            header = f"[AI] content={msg.content[:200] if msg.content else ''}"
            print(header)
            log_lines.append(header)

            if not getattr(msg, "tool_calls", None):
                break

            for tc in msg.tool_calls:
                tc_info = f"  -> tool_call: {tc['name']}({tc['args']})"
                print(tc_info)
                log_lines.append(tc_info)

                tool_result = skill_tool.invoke(tc["args"])
                result_info = f"  <- result: {tool_result[:300]}"
                print(result_info)
                log_lines.append(result_info)

                messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))
        else:
            log_lines.append("\n[WARN] max rounds reached")

        print("\n=== final ===")
        print(msg.content)
        log_lines.append(f"\n=== final ===\n{msg.content}")
    finally:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))


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
