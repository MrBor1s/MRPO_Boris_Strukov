from __future__ import annotations

import sqlite3
from pathlib import Path


def initialize_database(db_path: Path, sql_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        with open(sql_path, encoding='utf-8') as file:
            script = file.read()
        connection.executescript(script)
        connection.commit()
    finally:
        connection.close()
