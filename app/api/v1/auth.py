from fastapi import APIRouter

from app.dependencies.notifications import NotificationServiceDep
from app.dependencies.users import UserServiceDep
from app.schemas.user import (LoginRequest, TokenResponse, UserCreate,
                              UserResponse)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
async def register(
    service: UserServiceDep,
    notification_service: NotificationServiceDep,
    user: UserCreate,
):
    created_user = service.register(user)
    notification_service.send_welcome_notification(created_user.email)
    return created_user


@router.post("/login", response_model=TokenResponse)
async def login(service: UserServiceDep, login: LoginRequest):
    return service.login(login)
