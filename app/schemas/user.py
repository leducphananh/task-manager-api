from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=20
    )
    age: int = 18
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
