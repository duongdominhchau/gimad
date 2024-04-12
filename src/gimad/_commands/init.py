from pathlib import Path
from typing import Annotated

from typer import Argument

from gimad._constants import ONEOFF_DIR, PERMANENT_DIR


def init(
    migration_dir: Annotated[
        str,
        Argument(help="Name of the directory to store migration scripts"),
    ] = "data_migrations",
) -> None:
    """Initialize current directory with data migration directory structure"""
    migration_root = Path(migration_dir)
    migration_root.mkdir()
    for d in (PERMANENT_DIR, ONEOFF_DIR):
        migration_root.joinpath(d).mkdir()
