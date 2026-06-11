import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello!!!"}


@app.get("/user/profile")
async def profile() -> dict:
    return {"profile": "View profile user"}


@app.get("/products/{product_id}")
async def detail_view(product_id: int) -> dict:
    return {"product": f"Stock number {product_id}"}

@app.get("/hello/{user}")
async def welcome_user(user: str) -> dict:
    return {"user": f"Hello, {user}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
