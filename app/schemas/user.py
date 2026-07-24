from pydantic import Field
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=20
    )
    age: int = 18


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
