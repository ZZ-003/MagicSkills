"""CrewAI agent example — progressive skill disclosure.

Usage:
    # First follow README.md setup steps, then:
    pip install -r crewai_example/requirements.txt
    python crewai_example/model.py --scenario all

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
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from crewai import Agent, Crew, LLM, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv

from magicskills import REGISTRY
from magicskills.type.skills import Skills

load_dotenv()

_SETUP_HINT = """\
Please follow the README.md setup steps to create skills collections first:
  magicskills addskills crewai_agent1_skills --skill-list c_2_ast pdf --agent-md-path ./AGENTS.md
  magicskills addskills crewai_agent2_skills --skill-list c_2_ast docx --agent-md-path ./AGENTS.md
"""

PYTHON_EXE = Path(sys.executable).resolve()


# ── 1. Load skill collections from registry ────────────────────
def _load_agent_skills() -> tuple[Skills, Skills]:
    errors: list[str] = []
    agent1_skills: Skills | None = None
    agent2_skills: Skills | None = None

    try:
        agent1_skills = REGISTRY.get_skills("crewai_agent1_skills")
    except KeyError:
        errors.append("crewai_agent1_skills")

    try:
        agent2_skills = REGISTRY.get_skills("crewai_agent2_skills")
    except KeyError:
        errors.append("crewai_agent2_skills")

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


def _normalize_model_for_litellm(model_name: str) -> str:
    raw = (model_name or "").strip()
    if not raw:
        return raw
    provider_prefixes = (
        "openai/", "azure/", "anthropic/", "gemini/",
        "huggingface/", "deepseek/", "ollama/",
    )
    if raw.startswith(provider_prefixes):
        return raw
    return f"openai/{raw}"


# ── 3. Per-agent skill tool factory ────────────────────────────
def _make_skill_tool(skills: Skills) -> BaseTool:
    class SkillTool(BaseTool):
        name: str = "skill_tool"
        description: str = skills.tool_description

        def _run(self, action: str, arg: str = "") -> str:
            fixed_arg = _normalize_exec_arg(arg, skills) if action == "execskill" else arg
            result = skills.skill_tool(action, fixed_arg)
            result = _truncate_readskill_result(result)
            return json.dumps(result, ensure_ascii=False)

    return SkillTool()


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


# ── 5. 构建 agent 并运行 ──────────────────────────────────────
def run_once(task_prompt: str, log_name: str, skills: Skills) -> None:
    model_name = _normalize_model_for_litellm(os.getenv("OPENAI_MODEL", ""))
    llm = LLM(
        model=model_name,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0.1,
    )

    researcher = Agent(
        role="technical researcher",
        goal="Use the available skills to solve the user's task with the minimum necessary steps",
        backstory=(
            "You are a technical expert. Start by discovering available skills, then "
            "read the most relevant skill instructions, and only then execute the "
            "necessary command."
        ),
        tools=[_make_skill_tool(skills)],
        verbose=True,
        llm=llm,
        function_calling_llm=llm,
        max_iter=10,
        respect_context_window=True,
    )

    task = Task(
        description=task_prompt,
        agent=researcher,
        expected_output="Agent output with complete tool usage trace.",
    )

    crew = Crew(agents=[researcher], tasks=[task])
    log_file = Path(__file__).parent / log_name
    log_buffer = io.StringIO()
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = TeeWriter(original_stdout, log_buffer)
    sys.stderr = TeeWriter(original_stderr, log_buffer)
    try:
        result = crew.kickoff()
        print("\n=== final ===")
        print(result)
        log_content = log_buffer.getvalue()
    except BaseException:
        log_content = (
            "[ERROR] Agent run interrupted or failed.\n\n"
            + traceback.format_exc()
        )
        print(log_content)
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
