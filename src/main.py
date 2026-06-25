import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Messages CRUD")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageCreate(BaseModel):
    content: str


class MessageUpdate(BaseModel):
    content: str | None = None


class Message(BaseModel):
    id: int
    content: str


messages_db: list[Message] = [Message(id=0, content="First post in FastAPI")]


def next_id() -> int:
    return max((m.id for m in messages_db), default=-1) + 1


def get_index(message_id: int) -> int:
    for i, m in enumerate(messages_db):
        if m.id == message_id:
            return i
    return -1


@app.get("/messages", response_model=list[Message])
async def list_messages() -> list[Message]:
    return messages_db


# Эндпоинт для создания сообщения
@app.post("/messages", response_model=Message, status_code=201)
async def create_message(payload: MessageCreate) -> Message:
    message = Message(id=next_id(), content=payload.content)
    messages_db.append(message)
    return message


@app.get("/messages/{message_id}", response_model=Message)
async def get_message(message_id: int) -> Message:
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    return messages_db[idx]


@app.patch("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, payload: MessageUpdate) -> Message:
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    if payload.content is not None:
        messages_db[idx].content = payload.content

    return messages_db[idx]


@app.put("/messages/{message_id}", response_model=Message)
async def edit_message(message_id: int, payload: MessageCreate) -> Message:
    idx = get_index(message_id)
    if idx < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    updated_message = Message(id=message_id, content=payload.content)
    messages_db[idx] = updated_message
    return updated_message


@app.delete("/messages/{message_id}", status_code=204)
async def delete_message(message_id: int):

    idx = get_index(message_id)

    if idx < 0:
        raise HTTPException(status_code=404, detail="Message not found")

    messages_db.pop(idx)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
