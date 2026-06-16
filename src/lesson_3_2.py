from datetime import datetime

from pydantic import BaseModel, Field, SecretStr, EmailStr


class User(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=20,
        description="Пользовательское имя, от 5 до 20 символов",
    )
    password: SecretStr = Field(
        min_length=8,
        max_length=50,
        description="Пароль, от 8 до 50 символов",
    )
    email: EmailStr = Field(
        description="Электронная почта",
    )
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
        description="Имя, от 2 до 30 символов",
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
        description="Фамилия, от 2 до 30 символов",
    )
    is_active: bool = Field(
        default=True,
        description="Учётная запись активна",
    )
    is_staff: bool = Field(
        default=False,
        description="Является служебным пользователем",
    )
    is_superuser: bool = Field(
        default=False,
        description="Является суперпользователем",
    )
    date_joined: datetime = Field(
        default_factory=datetime.now,
        description="Зарегистрирован",
    )
    last_login: datetime | None = Field(
        default=None,
        description="Последнее посещение",
    )
