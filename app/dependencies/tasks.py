from fastapi import Depends
from sqlalchemy.util.typing import Annotated

from app.dependencies.database import DBSession
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_service(db: DBSession) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)


TaskServiceDep = Annotated[
    TaskService,
    Depends(get_task_service)
]
