from typing import Annotated

from rich import print
from typer import Option


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
