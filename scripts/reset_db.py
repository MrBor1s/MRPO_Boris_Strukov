from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.db_init import initialize_database  # noqa: E402

DB_PATH = BASE_DIR / 'database' / 'shoe_store.db'
SQL_PATH = BASE_DIR / 'database' / 'init.sql'

if DB_PATH.exists():
    DB_PATH.unlink()

initialize_database(DB_PATH, SQL_PATH)
print('База данных успешно пересоздана.')
