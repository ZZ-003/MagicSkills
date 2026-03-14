from __future__ import annotations

from pathlib import Path

from magicskills.command.change_cli_description import change_cli_description
from magicskills.command.syncskills import syncskills
from magicskills.type.skills import Skills
from magicskills.type.skillsregistry import REGISTRY, SkillsRegistry
from magicskills.utils.utils import skill_paths_to_skills


def _write_skill(path: Path, description: str = "Demo skill") -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        f"---\nname: {path.name}\ndescription: {description}\n---\n\n# {path.name}\n",
        encoding="utf-8",
    )


def _build_skills(tmp_path: Path, *, cli_description: str | None = None) -> Skills:
    skill_root = tmp_path / "skills"
    _write_skill(skill_root / "demo")
    return Skills(
        name="demo_collection",
        skill_list=skill_paths_to_skills([skill_root]),
        tool_description="Use the tool channel only.",
        cli_description=cli_description,
        agent_md_path=tmp_path / "AGENTS.md",
    )


def _reset_registry(tmp_path: Path) -> Path:
    store_path = tmp_path / "collections.json"
    REGISTRY.loadskills(store_path)
    return store_path


def test_syncskills_none_mode_keeps_original_skills_block(tmp_path: Path) -> None:
    skills = _build_skills(tmp_path, cli_description="Use the CLI path only.")

    output = syncskills(skills, mode="none")

    content = output.read_text(encoding="utf-8")
    assert "<available_skills>" in content
    assert "<name>demo</name>" in content
    assert "Use the tool channel only." not in content
    assert "Use the CLI path only." not in content


def test_syncskills_tool_description_mode_omits_skills_block(tmp_path: Path) -> None:
    skills = _build_skills(tmp_path)

    output = syncskills(skills, mode="tool_description")

    content = output.read_text(encoding="utf-8")
    assert "<usage>\nUse the tool channel only.\n</usage>" in content
    assert "<available_skills>" not in content
    assert "<name>demo</name>" not in content


def test_syncskills_cli_description_mode_omits_skills_block(tmp_path: Path) -> None:
    skills = _build_skills(tmp_path, cli_description="Use the CLI path only.")

    output = syncskills(skills, mode="cli_description")

    content = output.read_text(encoding="utf-8")
    assert "<usage>\nUse the CLI path only.\n</usage>" in content
    assert "<available_skills>" not in content
    assert "<name>demo</name>" not in content


def test_syncskills_cli_description_mode_uses_default_description(tmp_path: Path) -> None:
    skills = _build_skills(tmp_path)

    output = syncskills(skills, mode="cli_description")

    content = output.read_text(encoding="utf-8")
    assert "Unified skill CLI." in content
    assert "<available_skills>" not in content


def test_registry_persists_cli_description(tmp_path: Path) -> None:
    store_path = _reset_registry(tmp_path)
    skill_root = tmp_path / "skills"
    _write_skill(skill_root / "demo")
    skill_list = skill_paths_to_skills([skill_root])

    REGISTRY.createskills(
        name="demo_collection",
        skill_list=skill_list,
        tool_description="Tool desc",
        cli_description="CLI desc",
        agent_md_path=str(tmp_path / "AGENTS.md"),
        save=True,
    )

    REGISTRY.loadskills(store_path)
    loaded = REGISTRY.get_skills("demo_collection")

    assert loaded.tool_description == "Tool desc"
    assert loaded.cli_description == "CLI desc"


def test_change_cli_description_persists_to_registry(tmp_path: Path) -> None:
    store_path = _reset_registry(tmp_path)
    skill_root = tmp_path / "skills"
    _write_skill(skill_root / "demo")
    skill_list = skill_paths_to_skills([skill_root])

    instance = REGISTRY.createskills(
        name="demo_collection",
        skill_list=skill_list,
        tool_description="Tool desc",
        cli_description="CLI desc",
        agent_md_path=str(tmp_path / "AGENTS.md"),
        save=True,
    )

    change_cli_description(instance, "Updated CLI desc")

    REGISTRY.loadskills(store_path)
    loaded = REGISTRY.get_skills("demo_collection")
    assert loaded.cli_description == "Updated CLI desc"


def test_skillsregistry_direct_instantiation_is_disabled() -> None:
    try:
        SkillsRegistry()
    except RuntimeError as exc:
        assert "Use the global REGISTRY singleton instead." in str(exc)
        return
    raise AssertionError("SkillsRegistry() should be disabled for external callers")
