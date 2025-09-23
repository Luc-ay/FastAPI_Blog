from fastapi import APIRouter

router = APIRouter(
      prefix="/user",
      tags=["user"],
      responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]