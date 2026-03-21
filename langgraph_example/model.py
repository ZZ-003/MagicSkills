"""LangGraph ReAct agent example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install langchain-openai langgraph python-dotenv
    python langgraph_example/model.py --scenario all

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

# Windows 终端默认 GBK 编码，遇到 Unicode 特殊字符会崩溃
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills createskills langgraph_agent1_skills --skill-list c_2_ast --agent-md-path ./AGENTS.md
  magicskills createskills langgraph_agent2_skills --skill-list c_2_ast --agent-md-path ./AGENTS.md
"""


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("langgraph_agent1_skills")
    except KeyError:
        errors.append("langgraph_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("langgraph_agent2_skills")
    except KeyError:
        errors.append("langgraph_agent2_skills")

    if errors:
        print(f"Error: skills collection(s) not found: {errors}", file=sys.stderr)
        print(_SETUP_HINT, file=sys.stderr)
        sys.exit(1)

    return agent1_skills, agent2_skills  # type: ignore[return-value]


agent1_skills, agent2_skills = _load_agent_skills()


# ── 2. Build per-agent LangChain skill tools ───────────────────
def _make_skill_tool(skills: Skills):
    @tool("skill_tool", description=skills.tool_description)
    def _skill_tool(action: str, arg: str = "") -> str:
        return json.dumps(skills.skill_tool(action, arg), ensure_ascii=False)

    return _skill_tool


# ── 3. Build LLM and agents ─────────────────────────────────────
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.0,
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

agent1 = create_react_agent(llm, [_make_skill_tool(agent1_skills)])  # read scenario
agent2 = create_react_agent(llm, [_make_skill_tool(agent2_skills)])  # exec scenario


# ── 4. 场景配置：log1=不停读文档 / log2=有执行 ──────────────────
SCENARIOS: dict[str, tuple[str, str, object]] = {
    "read": (
        "log1.json",
        "我想了解更多 AST 知识。",
        agent1,
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
        agent2,
    ),
}


def run_once(prompt: str, log_name: str, agent) -> None:
    log_lines: list[str] = []
    log_file = Path(__file__).parent / log_name

    try:
        result = agent.invoke(
            {"messages": [("user", prompt)]},
            {"recursion_limit": 40},
        )

        # ── 5. 打印 & 保存日志 ────────────────────────────────────
        for i, m in enumerate(result["messages"]):
            msg_type = getattr(m, "type", m.__class__.__name__)
            header = f"\n--- {i} | {msg_type} ---"
            print(header)
            log_lines.append(header)

            if getattr(m, "content", None):
                print(m.content)
                log_lines.append(m.content)

            if isinstance(m, AIMessage) and getattr(m, "tool_calls", None):
                print("\n[tool_calls]")
                log_lines.append("\n[tool_calls]")
                for tc in m.tool_calls:
                    print(tc)
                    log_lines.append(str(tc))

            if isinstance(m, ToolMessage):
                print("\n[tool_result]")
                print(m.content)
                log_lines.append("\n[tool_result]")
                log_lines.append(m.content)

        print("\n=== final ===")
        print(result["messages"][-1].content)
        log_lines.extend(["\n=== final ===", str(result["messages"][-1].content)])
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
        log_name, prompt, agent = SCENARIOS[name]
        print(f"\n================ {name.upper()} ================\n")
        run_once(prompt, log_name, agent)


if __name__ == "__main__":
    main()
