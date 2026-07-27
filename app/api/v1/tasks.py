from typing import List

from fastapi import APIRouter

from app.dependencies.auth import CurrentUserDep
from app.dependencies.tasks import TaskServiceDep
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(current_user: CurrentUserDep, task_service: TaskServiceDep):
    return task_service.get_tasks(current_user.id)


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: CurrentUserDep, task_service: TaskServiceDep):
    return task_service.create_task(current_user.id, task)
