from fastapi import APIRouter
from app.dependencies.users import UserServiceDep
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
async def get_users(service: UserServiceDep):
    return service.get_users()


@router.post("/", response_model=UserResponse)
async def create_user(service: UserServiceDep, user: UserCreate):
    new_user = User(name=user.name, age=user.age)
    return service.create_user(new_user)
