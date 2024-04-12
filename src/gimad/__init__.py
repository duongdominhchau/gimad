import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from rich import print
from typer import Argument, Option, Typer

PERMANENT_DIR = "permanent"
ONEOFF_DIR = "oneoff"


app = Typer(
    no_args_is_help=True,
    help="Non-schema migration runner for PostgreSQL",
)


@app.command()
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


@app.command()
def new(
    name: str,
    permanent: Annotated[
        bool,
        Option(
            help="""
Create a permanent data migration.

By default, the migration generated is one-off. A one-off migration is useful for
existing databases only. For example to remove an abnormal record from the database.

A permanent migration is different, it is useful for new database as well. For example,
adding records to a look-up table is useful to both existing databases as well as new
ones. This is essentially database seeding script.
            """,
        ),
    ] = False,
) -> None:
    """Create new data migration"""

    migration_dir = os.environ.get("GIMAD_MIGRATION_DIR", "data_migrations")
    script_dir = Path(migration_dir).joinpath(
        PERMANENT_DIR if permanent else ONEOFF_DIR,
    )
    migration_name = _migration_name(name)
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
    script_name = f"{timestamp}_{migration_name}.py"
    # TODO: Render template
    script_dir.joinpath(script_name).write_text("")


def _migration_name(name: str) -> str:
    name = re.sub(r"[^\s\w]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.lower()


@app.command()
def up(
    skip_oneoff: Annotated[
        bool,
        Option(
            help="""
Only run permanent migrations

This option is useful for initializing a new database.
            """,
        ),
    ] = False,
) -> None:
    """Run pending migrations"""
    print("Running pending migrations with skip_oneoff =", skip_oneoff)


@app.command()
def down(
    n: Annotated[int, Argument(help="Number of migrations to rollback")] = 1,
) -> None:
    """Run rollback scripts"""
    print("Rolling back", n, "migrations")


@app.command()
def redo() -> None:
    """Run an executed migration"""


def main() -> None:
    try:
        app()
    except Exception as e:  # noqa: BLE001
        if not os.environ.get("DEBUG"):
            print(f"[red]{e}[/red]", file=sys.stderr)
        else:
            raise
