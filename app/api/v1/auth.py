from fastapi import APIRouter

from app.dependencies.users import UserServiceDep
from app.schemas.user import (LoginRequest, TokenResponse, UserCreate,
                              UserResponse)
from app.tasks.email_tasks import send_welcome_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
async def register(
    service: UserServiceDep,
    user: UserCreate,
):
    created_user = service.register(user)
    send_welcome_email.delay(created_user.email)
    return created_user


@router.post("/login", response_model=TokenResponse)
async def login(service: UserServiceDep, login: LoginRequest):
    return service.login(login)
