import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# Определяем модель Pydantic для сообщения
class Message(BaseModel):
    id: int
    content: str


# Инициализируем messages_db как список объектов Message
messages_db: list[Message] = [Message(id=0, content="First post in FastAPI")]


@app.get("/messages", response_model=list[Message])
async def read_messages() -> list[Message]:
    return messages_db


@app.get("/messages/{message_id}", response_model=Message)
async def read_messages_by_id(message_id: int) -> Message:
    for message in messages_db:
        if message.id == message_id:
            return message
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
