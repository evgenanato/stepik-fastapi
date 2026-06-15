from typing import Annotated

import uvicorn

from fastapi import FastAPI, Path, Query

app = FastAPI(
    title="Stepik Project",
    summary="Third episode",
    description="The CRUD application supports **writing**, *reading*, updating, and deleting posts.",
)

country_dict = {
    "Russia": ["Moscow", "St. Petersburg", "Novosibirsk", "Ekaterinburg", "Kazan"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia"],
}

profiles_dict = {
    "alex": {
        "name": "Александр",
        "age": 33,
        "phone": "+79463456789",
        "email": "alex@my-site.com",
    },
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


@app.get("/users")
async def retrieve_user_profile(
    username: Annotated[
        str, Query(min_length=2, max_length=50, description="Имя пользователя")
    ],
):
    if username in profiles_dict:
        return profiles_dict[username]
    else:
        return {"message": f"Пользователь {username} не найден"}


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


@app.get("/category/{category_id}/products")
async def category(
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Category ID",
        ),
    ],
    page: int,
):
    return {"category_id": category_id, "page": page}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
