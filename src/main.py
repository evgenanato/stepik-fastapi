import uvicorn
from fastapi import FastAPI

from src.routers import categories
from src.routers import products

# Создаём приложение FastAPI
app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)

# Подключаем маршруты категорий
app.include_router(categories.router)
app.include_router(categories.router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
