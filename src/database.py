from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Строка подключения для SQLite
BASE_DIR = Path(__file__).parent.parent
DATABASE_PATH = BASE_DIR / "ecommerce.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):  # New
    pass
