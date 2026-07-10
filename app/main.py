from app.schemas.user import UserResponse
from fastapi import FastAPI
from app.schemas.user import UserCreate

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello FastAPI"
    }


@app.get("/users")
async def get_users(page: int, limit: int):
    return [
        {
            "id": 1,
            "name": "Phan Anh",
        },
        {
            "id": 2,
            "name": "John",
        },
    ]


@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {
        "id": 1,
        **user.model_dump()
    }
