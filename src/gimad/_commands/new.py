import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from typer import Option

from gimad._constants import MIGRATION_DIR, ONEOFF_DIR, PERMANENT_DIR


def _migration_name(name: str) -> str:
    name = re.sub(r"[^\s\w]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.lower()


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

    script_dir = Path(MIGRATION_DIR).joinpath(
        PERMANENT_DIR if permanent else ONEOFF_DIR,
    )
    migration_name = _migration_name(name)
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
    script_name = f"{timestamp}_{migration_name}.py"
    # TODO: Render template
    script_dir.joinpath(script_name).write_text("")
