import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # New

sys.path.insert(0, str(Path(__file__).parent.parent))
BASE_DIR = Path(__file__).parent.parent
DATABASE_PATH = BASE_DIR / "ecommerce.db"

# Строка подключения для SQLite
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)


# Определяем базовый класс для моделей
# class Base(DeclarativeBase):  # New
#     pass


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для PostgreSQl
DATABASE_URL = "postgresql+asyncpg://stepik_user:stepik@localhost:5432/stepik_db"

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
