"""Command implementation for adding one skill into one collection."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..type.skill import Skill
from ..utils.utils import (
    detect_location,
    extract_yaml_field,
    is_directory_or_symlink_to_directory,
    read_text,
    skill_paths_from_skills,
)

if TYPE_CHECKING:
    from ..type.skills import Skills


def _looks_like_path_target(value: str | Path) -> bool:
    """Return True when target should be treated as filesystem path."""
    if isinstance(value, Path):
        return True
    raw = str(value).strip()
    if not raw:
        return False
    if "/" in raw or "\\" in raw or raw.startswith(".") or raw.startswith("~"):
        return True
    return Path(raw).expanduser().exists()


def addskill(
    skills: Skills,
    target: Path | str,
    source: str | Path | None = None,
) -> Path:
    """Register one skill by target(name or path) into this collection."""
    raw_target = str(target).strip()
    if not raw_target:
        raise ValueError("addskill requires target: <name-or-path>")

    created_source = str(source).strip() if source is not None else ""

    if _looks_like_path_target(target):
        skill_dir = Path(raw_target).expanduser().resolve()
    else:
        from ..type.skillsregistry import ALL_SKILLS

        try:
            resolved_skill = ALL_SKILLS().get_skill(raw_target)
        except KeyError as exc:
            message = str(exc)
            if "Multiple skills named" in message:
                raise ValueError(
                    f"addskill: skill name '{raw_target}' is duplicated; "
                    "pass <skill-directory-path> as target.\n"
                    f"{message}"
                ) from exc
            raise KeyError(f"addskill: skill target not found: {raw_target}") from exc

        skill_dir = resolved_skill.path.expanduser().resolve()
        if not created_source:
            created_source = resolved_skill.source

    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill directory not found: {skill_dir}")
    if not is_directory_or_symlink_to_directory(skill_dir):
        raise ValueError(f"Skill path exists and is not a directory: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Skill directory is invalid (missing SKILL.md): {skill_dir}")

    content = read_text(skill_md)
    description = extract_yaml_field(content, "description")
    is_global, universal = detect_location(skill_dir.parent)
    if not created_source:
        created_source = str(skill_dir.parent.expanduser().resolve())
    created_skill = Skill(
        name=skill_dir.name,
        description=description,
        path=skill_dir,
        base_dir=skill_dir.parent,
        source=created_source,
        is_global=is_global,
        universal=universal,
    )

    from ..type.skillsregistry import ALL_SKILLS, REGISTRY

    all_skills = ALL_SKILLS()
    created_skill_path = created_skill.path.expanduser().resolve()
    if all_skills is not skills:
        all_skills.skill_list = [
            item
            for item in all_skills.skill_list
            if item.path.expanduser().resolve() != created_skill_path
        ]
        all_skills.skill_list.append(created_skill)
        all_skills.paths = skill_paths_from_skills(all_skills.skill_list)

    skills.skill_list = [
        item
        for item in skills.skill_list
        if item.path.expanduser().resolve() != created_skill_path
    ]
    skills.skill_list.append(created_skill)
    skills.paths = skill_paths_from_skills(skills.skill_list)
    REGISTRY.saveskills()

    return skill_dir
