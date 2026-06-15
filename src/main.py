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
            examples=["permin0ff"],
        ),
    ],
    first_name: Annotated[str | None, Query(max_length=10, pattern="^J|s$")] = None,
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


@app.get("/users/{name}")
async def get_user(
    name: Annotated[
        str,
        Path(
            min_length=4,
            max_length=20,
            description="Enter your name",
        ),
    ],
) -> dict:
    return {"user_name": name}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
