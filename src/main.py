import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from src.routers import users
from src.routers import categories
from src.routers import products
from src.routers import reviews
from src.routers import cart

sys.path.insert(1, str(Path(__file__).parent.parent))

# Создаём приложение FastAPI
app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)

# Подключаем маршруты категорий
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(cart.router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
