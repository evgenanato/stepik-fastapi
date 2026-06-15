import uvicorn
from fastapi import FastAPI, HTTPException, status, Body

app = FastAPI()


comments_db = {0: "First comment in FastAPI"}


@app.get("/comments")
async def read_comments() -> dict:
    return comments_db


@app.get("/comments/{comment_id}")
async def read_comment(comment_id: int) -> str:
    try:
        return comments_db[comment_id]
    except:
        raise HTTPException(status_code=404, detail="Comment not found")


@app.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(comment: str = Body()) -> str:
    current_index = max(comments_db) + 1 if comments_db else 0
    comments_db[current_index] = comment
    return "Comment created!"


@app.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment: str = Body()) -> str:
    if comment_id in comments_db:
        comments_db[comment_id] = comment
        return "Comment updated!"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )


@app.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> str:
    if comment_id not in comments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    comments_db.pop(comment_id)
    return "Comment deleted!"


@app.delete("/comments", status_code=status.HTTP_200_OK)
async def delete_comments() -> str:
    comments_db.clear()
    return "Clear comment_db"


if __name__ == "__main__":
    uvicorn.run("crud:app", reload=True)
