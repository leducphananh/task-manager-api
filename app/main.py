from typing import Annotated
from fastapi import Depends
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


def get_current_user():
    return {
        "id": 1,
        "name": "Phan Anh",
        "age": 25,
    }


CurrentUser = Annotated[
    dict,
    Depends(get_current_user)
]


@app.get("/me")
async def get_me(user: CurrentUser):
    return {
        "user": user
    }
