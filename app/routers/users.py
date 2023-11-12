from fastapi import APIRouter

router = APIRouter(
    prefix="/users"
)


@router.get("/", tags=["users"])
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "currentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
