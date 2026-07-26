from fastapi import APIRouter

from app.dependencies.users import UserServiceDep
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
