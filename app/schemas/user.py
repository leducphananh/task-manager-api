from pydantic import Field, BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
