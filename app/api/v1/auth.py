from fastapi import APIRouter

from app.dependencies.users import UserServiceDep
from app.schemas.user import LoginRequest, UserCreate, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
async def register(service: UserServiceDep, user: UserCreate):
    return service.register(user)


@router.post("/login", response_model=UserResponse)
async def login(service: UserServiceDep, login: LoginRequest):
    return service.login(login)
