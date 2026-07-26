from fastapi import APIRouter
from app.dependencies.users import UserServiceDep
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
