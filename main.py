from __future__ import annotations

from pathlib import Path

from app.db_init import initialize_database
from app.repository import Repository
from app.services import ImageService
from app.ui import ShoeStoreApp

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'database' / 'shoe_store.db'
SQL_PATH = BASE_DIR / 'database' / 'init.sql'
RESOURCES_DIR = BASE_DIR / 'resources'


def main() -> None:
    if not DB_PATH.exists():
        initialize_database(DB_PATH, SQL_PATH)
    repository = Repository(DB_PATH)
    image_service = ImageService(RESOURCES_DIR)
    application = ShoeStoreApp(repository, image_service)
    application.mainloop()


if __name__ == '__main__':
    main()
