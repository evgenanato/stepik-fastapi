from fastapi import APIRouter, FastAPI

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.get("/")
async def get_notes():
    return "Notes API is working"
