import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello!!!"}


@app.get("/hello/{user}")
async def welcome_user(user: str) -> dict:
    return {"user": f"Hello, {user}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
