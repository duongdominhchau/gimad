from typing import Annotated

from rich import print
from typer import Option

from gimad._config import load_config
from gimad._migration import collect_migrations


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
    print(scripts)
    config = load_config()
    print(config)
