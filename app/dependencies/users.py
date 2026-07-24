from typing import Annotated

from fastapi import Depends

from app.dependencies.database import DBSession
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_service(db: DBSession) -> UserService:
    repository = UserRepository(db)

    return UserService(repository)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]
