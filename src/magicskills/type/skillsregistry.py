"""Persistent registry for named Skills collections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .skill import Skill
from .skills import Skills
from ..utils.utils import skill_paths_from_skills, skill_paths_to_skills


REGISTRY_DIRNAME = ".magicskills"
REGISTRY_FILENAME = "collections.json"
ALL_SKILLS_NAME = "Allskills"
_REGISTRY_INIT_TOKEN = object()


def _default_store_path() -> Path:
    """Default per-project path for collection registry storage."""
    return Path.home() / REGISTRY_DIRNAME / REGISTRY_FILENAME


class SkillsRegistry:
    """Named Skills collection registry with JSON persistence."""

    def __init__(self, store_path: Path | None = None, *, _init_token: object | None = None) -> None:
        if _init_token is not _REGISTRY_INIT_TOKEN:
            raise RuntimeError("SkillsRegistry is internal. Use the global REGISTRY singleton instead.")
        self._instances: dict[str, Skills] = {}
        self._store_path = (store_path or _default_store_path()).expanduser()
        self.loadskills()
        self._ensure_default_instance()

    def _ensure_default_instance(self) -> None:
        """Ensure built-in `Allskills` collection always exists in registry."""
        if ALL_SKILLS_NAME not in self._instances:
            instance = Skills(name=ALL_SKILLS_NAME)
            instance._registry = self
            self._instances[ALL_SKILLS_NAME] = instance

    def _allskills_instance(self) -> Skills:
        """Return the built-in `Allskills` collection, creating it when missing."""
        self._ensure_default_instance()
        return self._instances[ALL_SKILLS_NAME]

    def _normalize_provided_skills(self, skill_list: Iterable[Skill]) -> list[Skill]:
        """Ensure provided skills exist in `Allskills` and return canonical instances."""
        allskills = self._allskills_instance()
        canonical_by_path = {
            skill.path.expanduser().resolve(): skill
            for skill in allskills.skill_list
        }

        normalized: list[Skill] = []
        seen_paths: set[Path] = set()
        for skill in skill_list:
            resolved_path = skill.path.expanduser().resolve()
            if resolved_path in seen_paths:
                continue
            seen_paths.add(resolved_path)

            canonical = canonical_by_path.get(resolved_path)
            if canonical is None:
                allskills.skill_list.append(skill)
                canonical_by_path[resolved_path] = skill
                canonical = skill
            normalized.append(canonical)

        allskills.paths = skill_paths_from_skills(allskills.skill_list)
        return normalized

    def _serialize(self) -> dict[str, object]:
        """Serialize registry state into JSON-friendly payload."""
        collections: dict[str, dict[str, object]] = {}
        for name in sorted(self._instances.keys()):
            instance = self._instances[name]
            instance.paths = skill_paths_from_skills(instance.skill_list)
            collections[name] = {
                "paths": [str(path) for path in instance.paths],
                "tool_description": instance.tool_description,
                "cli_description": instance.cli_description,
                "agent_md_path": str(instance.agent_md_path),
            }
        return {"collections": collections}

    def loadskills(self, path: Path | str | None = None) -> list[Skills]:
        """Load collections from disk and rebuild the same Skills instances."""
        if path is not None:
            self._store_path = Path(path).expanduser()
        self._instances = {}
        if not self._store_path.exists():
            self._ensure_default_instance()
            return self.listskills()

        try:
            content = self._store_path.read_text(encoding="utf-8")
            payload: dict[str, Any] = json.loads(content)
        except (OSError, json.JSONDecodeError):
            self._ensure_default_instance()
            return self.listskills()

        collections = payload.get("collections", {})
        if isinstance(collections, dict):
            ordered_items: list[tuple[str, dict[str, Any]]] = []
            for name, spec in collections.items():
                if not isinstance(name, str) or not isinstance(spec, dict):
                    continue
                ordered_items.append((name, spec))

            ordered_items.sort(key=lambda item: (item[0] != ALL_SKILLS_NAME, item[0]))

            for name, spec in ordered_items:
                path_values = spec.get("paths", [])
                tool_description = spec.get("tool_description")
                cli_description = spec.get("cli_description")
                agent_md_path = spec.get("agent_md_path")
                paths = path_values if isinstance(path_values, list) else None
                self.addskills(
                    name=name,
                    paths=paths,
                    tool_description=tool_description if isinstance(tool_description, str) else None,
                    cli_description=cli_description if isinstance(cli_description, str) else None,
                    agent_md_path=agent_md_path if isinstance(agent_md_path, str) else None,
                    save=False,
                )

        self._ensure_default_instance()
        return self.listskills()

    def saveskills(self, path: Path | str | None = None) -> Path:
        """Persist registry so `loadskills` can restore the same Skills list."""
        if path is not None:
            self._store_path = Path(path).expanduser()
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        self._store_path.write_text(
            json.dumps(self._serialize(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return self._store_path

    def addskills(
        self,
        name: str,
        skill_list: Iterable[Skill] | str | None = None,
        paths: Iterable[str] | None = None,
        tool_description: str | None = None,
        cli_description: str | None = None,
        agent_md_path: str | None = None,
        save: bool = True,
    ) -> Skills:
        """Create and register one named Skills collection."""
        if name in self._instances:
            raise ValueError(f"Skills instance '{name}' already exists")

        if skill_list is None:
            if paths is None:
                instance = Skills(
                    name=name,
                    tool_description=tool_description,
                    cli_description=cli_description,
                    agent_md_path=agent_md_path,
                )
            else:
                allskills = self._instances.get(ALL_SKILLS_NAME)
                if allskills is None or name == ALL_SKILLS_NAME:
                    discovered = skill_paths_to_skills(paths)
                else:
                    discovered = []
                    seen_paths: set[Path] = set()
                    for value in paths:
                        try:
                            matched_skills = [allskills.get_skill(value)]
                        except KeyError:
                            target_base_dir = Path(value).expanduser().resolve()
                            matched_skills = [
                                item
                                for item in allskills.skill_list
                                if item.base_dir.expanduser().resolve() == target_base_dir
                            ]
                            if not matched_skills:
                                raise KeyError(f"Skill target '{value}' not found in Allskills")
                        for item in matched_skills:
                            resolved_path = item.path.expanduser().resolve()
                            if resolved_path in seen_paths:
                                continue
                            seen_paths.add(resolved_path)
                            discovered.append(item)
                instance = Skills(
                    name=name,
                    skill_list=discovered,
                    paths=skill_paths_from_skills(discovered),
                    tool_description=tool_description,
                    cli_description=cli_description,
                    agent_md_path=agent_md_path,
                )
        else:
            if isinstance(skill_list, str):
                allskills = self._allskills_instance()
                provided_skills = [allskills.get_skill(skill_list)]
            else:
                provided_skills = self._normalize_provided_skills(skill_list)
            instance = Skills(
                name=name,
                skill_list=provided_skills,
                paths=skill_paths_from_skills(provided_skills),
                tool_description=tool_description,
                cli_description=cli_description,
                agent_md_path=agent_md_path,
            )

        instance._registry = self
        self._instances[name] = instance
        if save:
            self.saveskills()
        return instance

    def listskills(self) -> list[Skills]:
        """List all registered Skills collections."""
        return [self._instances[name] for name in sorted(self._instances.keys())]

    def get_skills(self, name: str) -> Skills:
        """Get one named collection."""
        if name not in self._instances:
            raise KeyError(f"Skills instance '{name}' not found")
        return self._instances[name]

    def deleteskills(self, name: str, *more_names: str) -> None:
        """Delete one or more named collections and persist change once."""
        names: list[str] = []
        for value in (name, *more_names):
            if value not in names:
                names.append(value)

        for value in names:
            if value == ALL_SKILLS_NAME:
                raise ValueError(f"Skills instance '{ALL_SKILLS_NAME}' is built-in and cannot be deleted")
            if value not in self._instances:
                raise KeyError(f"Skills instance '{value}' not found")

        for value in names:
            del self._instances[value]
        self.saveskills()

REGISTRY = SkillsRegistry(_init_token=_REGISTRY_INIT_TOKEN)


def ALL_SKILLS() -> Skills:
    """Return the current built-in `Allskills` collection from the active registry."""
    return REGISTRY.get_skills(ALL_SKILLS_NAME)


__all__ = [
    "REGISTRY_DIRNAME",
    "REGISTRY_FILENAME",
    "ALL_SKILLS_NAME",
    "SkillsRegistry",
    "REGISTRY",
    "ALL_SKILLS",
]
