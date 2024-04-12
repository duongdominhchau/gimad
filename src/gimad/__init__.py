import re
import sys
from pathlib import Path
from typing import Annotated

from rich import print
from typer import Argument, Option, Typer

app = Typer(
    no_args_is_help=True,
    short_help="Non-schema migration runner for PostgreSQL",
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
    try:
        migration_root.mkdir()
        for d in ("permanent", "oneoff"):
            migration_root.joinpath(d).mkdir()
    except FileExistsError:
        msg = f"[red]ERROR: Migration script dir '{migration_dir}' already exist[/red]"
        print(msg, file=sys.stderr)


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
    script_dir = Path()
    migration_name = _migration_name(name)
    print(migration_name)


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
    app()
