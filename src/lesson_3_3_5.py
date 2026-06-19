from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Note(BaseModel):
    id: int
    text: str


notes = [
    Note(id=1, text="Купить хлеб"),
    Note(id=2, text="Написать отчет"),
    Note(id=3, text="Позвонить маме"),
    Note(id=4, text="Сходить в спортзал"),
    Note(id=5, text="Прочитать книгу"),
]


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note.id == note_id:
            deleted_note = notes.pop(i)
            return deleted_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
