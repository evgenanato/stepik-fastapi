import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class UserUpdate(BaseModel):
    name: str
    age: int = Field(gt=0)


class User(BaseModel):
    id: int
    name: str
    age: int


users = [
    User(id=1, name="Алексей", age=25),
    User(id=2, name="Мария", age=30),
    User(id=3, name="Иван", age=22),
    User(id=4, name="Елена", age=28),
    User(id=5, name="Дмитрий", age=35),
]


@app.post("/users", response_model=User)
async def add_user(user_create: UserUpdate) -> User:
    next_id = len(users) + 1
    new_user = User(id=next_id, name=user_create.name, age=user_create.age)
    users.append(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


@app.put("/users/{user_id}", response_model=User)
async def edit_user(user_id: int, user_update: UserUpdate) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            updated_user = User(id=user.id, name=user_update.name, age=user_update.age)
            users[i] = updated_user
            return updated_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


if __name__ == "__main__":
    uvicorn.run("lesson_3_3:app", reload=True)
