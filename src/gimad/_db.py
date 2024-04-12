import contextlib
from collections.abc import Sequence
from typing import Self

import psycopg
from psycopg.errors import DuplicateTable


class DatabaseClient:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url

    def __enter__(self) -> Self:
        self._connection = psycopg.connect(self.db_url, autocommit=True)
        self._cursor = self._connection.cursor()
        return self

    def __exit__(self, type: object, value: object, traceback: object) -> None:
        self._cursor.close()
        self._connection.close()

    def setup_history_table(self) -> None:
        with contextlib.suppress(DuplicateTable):
            self._cursor.execute(
                """
                create table data_migrations(
                    name varchar primary key,
                    type varchar not null,
                    created_at timestamptz not null default now()
                )
                """,
            )

    def exclude_executed_scripts(self, scripts: Sequence[str]) -> list:
        res = self._cursor.execute(
            """
            with all_scripts as (
                select unnest((%s)::varchar[]) name
                )
            select name
            from all_scripts
            where all_scripts.name not in (select name from data_migrations)
            """,
            (scripts,),
        )
        return [r[0] for r in res]
