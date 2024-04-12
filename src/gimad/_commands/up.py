from typing import Annotated

from rich import print
from typer import Option

from gimad._config import load_config
from gimad._db import DatabaseClient
from gimad._migration import MigrationScript, collect_migrations


def _collect_pending_migrations(
    client: DatabaseClient,
    all_scripts: list[MigrationScript],
) -> list[MigrationScript]:
    pending_names = set(client.exclude_executed_scripts([s.name for s in all_scripts]))
    return [s for s in all_scripts if s.name in pending_names]


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
    scripts = collect_migrations(skip_oneoff)
    config = load_config()
    with DatabaseClient(config.db_url) as client:
        client.setup_history_table()
        pending_scripts = _collect_pending_migrations(client, scripts)
        print(pending_scripts)
