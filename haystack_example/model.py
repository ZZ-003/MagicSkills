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
from typing import Any

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
from magicskills.utils.utils import extract_yaml_field

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


def _compact_text(text: str | None, limit: int = 220) -> str:
    """Collapse whitespace and trim long text for concise logs."""
    normalized = " ".join((text or "").split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _preview_lines(text: str | None, max_lines: int = 4, max_chars: int = 260) -> str:
    """Keep only the first few meaningful lines from long command output."""
    lines = [line.rstrip() for line in (text or "").splitlines() if line.strip()]
    if not lines:
        return ""
    preview = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        preview += "\n..."
    if len(preview) <= max_chars:
        return preview
    return preview[: max_chars - 3] + "..."


def _summarize_skill_tool_result(payload: dict[str, Any], origin_args: dict[str, Any]) -> dict[str, Any]:
    """Compress verbose MagicSkills tool payloads into high-signal summaries."""
    action = str(payload.get("action") or origin_args.get("action") or "")
    summary: dict[str, Any] = {"action": action, "ok": bool(payload.get("ok", False))}

    if not summary["ok"]:
        summary["error"] = _compact_text(str(payload.get("error", "")), limit=240)
        return summary

    result = payload.get("result")
    if action == "listskill" and isinstance(result, list):
        names = [str(item.get("name", "")) for item in result if isinstance(item, dict)]
        summary["count"] = len(names)
        summary["skills"] = names[:8]
        return summary

    if action == "readskill" and isinstance(result, str):
        target = str(origin_args.get("arg", ""))
        summary["target"] = target
        summary["name"] = extract_yaml_field(result, "name") or (Path(target).stem if target else "")
        summary["description"] = _compact_text(extract_yaml_field(result, "description"), limit=180)
        return summary

    if action == "execskill" and isinstance(result, dict):
        command = str(result.get("command", ""))
        stdout_preview = _preview_lines(str(result.get("stdout", "")))
        stderr_preview = _preview_lines(str(result.get("stderr", "")))
        summary["command"] = _compact_text(command, limit=180)
        summary["returncode"] = int(result.get("returncode", 0))
        if stdout_preview:
            summary["stdout_preview"] = stdout_preview
        if stderr_preview:
            summary["stderr_preview"] = stderr_preview
        return summary

    summary["preview"] = _compact_text(json.dumps(result, ensure_ascii=False, default=str), limit=240)
    return summary


def _summarize_message(message: ChatMessage) -> list[dict[str, Any]]:
    """Convert one Haystack ChatMessage into concise, structured log entries."""
    entries: list[dict[str, Any]] = []
    role = message.role.value

    if role == "system":
        return entries

    if role == "user" and message.text:
        return [{"type": "user", "text": _compact_text(message.text, limit=240)}]

    if message.tool_calls:
        for tool_call in message.tool_calls:
            entry: dict[str, Any] = {
                "type": "tool_call",
                "tool": tool_call.tool_name,
            }
            if tool_call.tool_name == "skill_tool":
                entry["action"] = tool_call.arguments.get("action", "")
                arg = str(tool_call.arguments.get("arg", "") or "")
                if arg:
                    entry["arg"] = _compact_text(arg, limit=180)
            else:
                entry["arguments"] = tool_call.arguments
            entries.append(entry)
        return entries

    if message.tool_call_results:
        for tool_result in message.tool_call_results:
            raw_result = tool_result.result
            if isinstance(raw_result, str):
                try:
                    payload = json.loads(raw_result)
                except json.JSONDecodeError:
                    payload = None
            else:
                payload = None

            if isinstance(payload, dict):
                entries.append(
                    {
                        "type": "tool_result",
                        **_summarize_skill_tool_result(payload, tool_result.origin.arguments),
                    }
                )
            else:
                entries.append(
                    {
                        "type": "tool_result",
                        "tool": tool_result.origin.tool_name,
                        "error": tool_result.error,
                        "preview": _compact_text(str(raw_result), limit=240),
                    }
                )
        return entries

    if message.text:
        entries.append({"type": "assistant", "text": _compact_text(message.text, limit=320)})
    return entries


def _summarize_run_result(prompt: str, result: dict[str, Any]) -> dict[str, Any]:
    """Build a concise log payload from the verbose Haystack run result."""
    raw_messages = result.get("messages", [])
    steps: list[dict[str, Any]] = []
    for message in raw_messages:
        if isinstance(message, ChatMessage):
            steps.extend(_summarize_message(message))

    final_message = result.get("last_message")
    final_answer = ""
    if isinstance(final_message, ChatMessage) and final_message.text:
        final_answer = _compact_text(final_message.text, limit=500)

    return {
        "prompt": _compact_text(prompt, limit=260),
        "steps": steps,
        "final_answer": final_answer,
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
        # system_prompt="Always call skill_tool in order: listskill, readskill, then execskill if needed.", # Haystack 框架限制，read 场景不加 system_prompt 就展示不了渐进式披露
        max_agent_steps=20,
    )

    log_file = Path(__file__).parent / log_name
    try:
        result = agent.run(messages=[ChatMessage.from_user(prompt)])
        summary = _summarize_run_result(prompt, result)
        log_content = json.dumps(summary, ensure_ascii=False, indent=2)
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
