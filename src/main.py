import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# Определяем модель Pydantic для сообщения
class Message(BaseModel):
    id: int
    content: str


class MessageCreate(BaseModel):
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


# POST /messages: Создание нового сообщения
@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message_create: MessageCreate) -> Message:
    # Генерируем новый ID на основе максимального существующего
    next_id = max((msg.id for msg in messages_db), default=-1) + 1
    new_message = Message(id=next_id, content=message_create.content)
    messages_db.append(new_message)
    return new_message


@app.put("/messages/{message_id}")
async def update_message(message_id: int, updated_message: Message) -> Message:
    if updated_message.id != message_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The ID in the request body must match the ID in the path",
        )
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            messages_db[i] = updated_message
            return updated_message
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
    )


@app.delete("/messages/{message_id}")
async def delete_message(message_id: int):
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            messages_db.pop(i)
            return {"status": f"Message ID = {message_id} deleted!"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )


@app.delete("/messages", status_code=status.HTTP_200_OK)
async def delete_messages() -> dict:
    messages_db.clear()
    return {"detail": "All messages deleted!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
