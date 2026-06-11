from typing import Annotated

import uvicorn

from fastapi import FastAPI, Path, Query

app = FastAPI()

country_dict = {
    "Russia": ["Moscow", "St. Petersburg", "Novosibirsk", "Ekaterinburg", "Kazan"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia"],
}


@app.get("/user/{username}")
async def login(
    username: Annotated[
        str,
        Path(
            min_length=3,
            max_length=15,
            description="Enter your username",
            examples=[
                "permin0ff",
            ],
        ),
    ],
    first_name: str | None = Query(
        default=None,
        max_length=10,
    ),
) -> dict:
    return {"user": username, "Name": first_name}


@app.get("/user")
async def search(people: Annotated[list[str], Query()]) -> dict:
    return {"user": people}


@app.get("/country/{country}")
async def list_cities(country: str, limit: int) -> dict:
    if country in country_dict:
        cities = country_dict[country]
    return {"country": country, "cities": cities[0:limit]}


@app.get("/users/{name}/{age}")
async def users(name: str, age: int) -> dict:
    return {"user_name": name, "user_age": age}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
