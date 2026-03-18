from __future__ import annotations

from pathlib import Path

from magicskills import cli as cli_module
from magicskills.type.skills import Skills
from magicskills.utils.utils import skill_paths_to_skills


def _write_skill(path: Path, *, description: str = "Demo skill") -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        f"---\ndescription: {description}\n---\n\n# {path.name}\n",
        encoding="utf-8",
    )


def _build_skills(tmp_path: Path) -> Skills:
    primary_root = tmp_path / "skills_primary"
    secondary_root = tmp_path / "skills_secondary"
    _write_skill(primary_root / "docx", description="Primary DOCX skill")
    _write_skill(secondary_root / "docx", description="Secondary DOCX skill")
    _write_skill(primary_root / "pdf", description="PDF skill")
    return Skills(skill_list=skill_paths_to_skills([primary_root, secondary_root]))


def test_listskill_without_name_lists_allskills_instance(tmp_path: Path, monkeypatch, capsys) -> None:
    allskills = _build_skills(tmp_path)
    monkeypatch.setattr(cli_module, "ALL_SKILLS", lambda: allskills)

    parser = cli_module.build_parser()
    args = parser.parse_args(["listskill"])

    result = args.func(args)

    captured = capsys.readouterr().out
    assert result == 0
    assert captured.count("name: docx") == 2
    assert "name: pdf" in captured


def test_listskill_with_name_lists_named_skills_collection(tmp_path: Path, monkeypatch, capsys) -> None:
    allskills = _build_skills(tmp_path)
    docx_only = Skills(
        name="docx_only",
        skill_list=[skill for skill in allskills.skill_list if skill.name == "docx"],
    )
    monkeypatch.setattr(cli_module, "_registered_skills_or_exit", lambda name: docx_only)

    parser = cli_module.build_parser()
    args = parser.parse_args(["listskill", "--name", "docx_only"])

    result = args.func(args)

    captured = capsys.readouterr().out
    assert result == 0
    assert captured.count("name: docx") == 2
    assert "name: pdf" not in captured
    assert "skills_primary/docx/SKILL.md" in captured
    assert "skills_secondary/docx/SKILL.md" in captured


def test_listskill_with_name_uses_registry_lookup_errors(monkeypatch) -> None:
    monkeypatch.setattr(
        cli_module,
        "_registered_skills_or_exit",
        lambda name: (_ for _ in ()).throw(SystemExit(f"Skills instance '{name}' not found")),
    )
    parser = cli_module.build_parser()
    args = parser.parse_args(["listskill", "--name", "missing"])

    try:
        args.func(args)
    except SystemExit as exc:
        assert str(exc) == "Skills instance 'missing' not found"
    else:
        raise AssertionError("Expected SystemExit for missing skills collection")
