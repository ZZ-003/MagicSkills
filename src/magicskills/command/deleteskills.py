"""Command implementation for deleting named skills collections."""

from __future__ import annotations

from ..type.skillsregistry import REGISTRY


def deleteskills(name: str, *more_names: str) -> None:
    """Delete one or more registered Skills collections by name."""
    REGISTRY.deleteskills(name, *more_names)
