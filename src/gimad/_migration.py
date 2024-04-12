from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Self

from gimad._constants import MIGRATION_DIR, ONEOFF_DIR, PERMANENT_DIR


class MigrationType(StrEnum):
    PERMANENT = auto()
    ONEOFF = auto()


@dataclass
class MigrationScript:
    name: str
    kind: MigrationType

    @classmethod
    def from_path(cls, p: Path) -> Self:
        return cls(name=p.name, kind=MigrationType(p.parent.name))


def collect_migrations(skip_oneoff: bool = False) -> list:
    """Collect all migration scripts from migration script directory"""
    permanent_scripts = MIGRATION_DIR.joinpath(PERMANENT_DIR).glob("*.py")
    migrations = [MigrationScript.from_path(p) for p in permanent_scripts]
    if not skip_oneoff:
        oneoff_scripts = MIGRATION_DIR.joinpath(ONEOFF_DIR).glob("*.py")
        migrations.extend(MigrationScript.from_path(p) for p in oneoff_scripts)
    return migrations
