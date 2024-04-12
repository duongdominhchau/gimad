import os
import sys

from rich import print
from typer import Typer

from gimad._commands.down import down
from gimad._commands.init import init
from gimad._commands.new import new
from gimad._commands.redo import redo
from gimad._commands.up import up

app = Typer(
    no_args_is_help=True,
    help="""
Non-schema migration runner for PostgreSQL

For debugging, set the environment variable DEBUG=1 to see the stack trace
    """,
)
app.command()(init)
app.command()(new)
app.command()(up)
app.command()(down)
app.command()(redo)


def main() -> None:
    try:
        app()
    except Exception as e:  # noqa: BLE001
        if not os.environ.get("DEBUG"):
            print(f"[red]{e}[/red]", file=sys.stderr)
        else:
            raise
