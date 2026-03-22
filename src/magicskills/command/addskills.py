"""Command implementation for adding named skills collections."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..type.skill import Skill
from ..type.skillsregistry import REGISTRY

if TYPE_CHECKING:
    from ..type.skills import Skills


def addskills(
    name: str,
    skill_list: list[Skill] | str | None = None,
    paths: list[str] | None = None,
    tool_description: str | None = None,
    cli_description: str | None = None,
    agent_md_path: str | None = None,
) -> Skills:
    """Create and register one named Skills collection."""
    return REGISTRY.addskills(
        name=name,
        skill_list=skill_list,
        paths=paths,
        tool_description=tool_description,
        cli_description=cli_description,
        agent_md_path=str(Path(agent_md_path).expanduser().resolve()) if agent_md_path else None,
    )
