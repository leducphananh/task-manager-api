from typing import List

from fastapi import APIRouter

from app.dependencies.auth import CurrentUserDep
from app.dependencies.tasks import TaskServiceDep
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TaskUpdateStatus,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(current_user: CurrentUserDep, task_service: TaskServiceDep):
    return task_service.get_tasks(current_user.id)


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate, current_user: CurrentUserDep, task_service: TaskServiceDep
):
    return task_service.create_task(current_user.id, task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int, current_user: CurrentUserDep, task_service: TaskServiceDep
):
    return task_service.get_task_by_id(task_id, current_user.id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: CurrentUserDep,
    task_service: TaskServiceDep,
):
    return task_service.update_task(task_id, current_user.id, task)


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_in: TaskUpdateStatus,
    current_user: CurrentUserDep,
    task_service: TaskServiceDep,
):
    return task_service.update_status(
        task_id, current_user.id, status_in.status
    )


@router.delete("/{task_id}")
async def delete_task(
    task_id: int, current_user: CurrentUserDep, task_service: TaskServiceDep
):
    task_service.delete_task(task_id, current_user.id)
    return {"message": "Task deleted successfully", "id": task_id}
