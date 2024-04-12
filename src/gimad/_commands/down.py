from typing import Annotated

from rich import print
from typer import Argument


def down(
    n: Annotated[
        int,
        Argument(help="Number of migrations to rollback"),
    ] = 1,
) -> None:
    """Run rollback scripts"""
    print("Rolling back", n, "migrations")
