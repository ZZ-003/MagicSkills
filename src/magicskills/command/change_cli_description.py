"""Command implementation for updating CLI description."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..type.skills import Skills


def change_cli_description(skills: Skills, description: str) -> None:
    """Update CLI description used in generated XML usage section."""
    skills.cli_description = description
    owner_registry = getattr(skills, "_registry", None)
    if owner_registry is not None:
        owner_registry.saveskills()
