from app.exceptions import TaskNotFoundException
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.common import PaginationResponse
from app.schemas.task import TaskCreate, TaskQuery, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def _get_task_or_404(self, task_id: int, user_id: int) -> Task:
        task = self.repository.get_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundException()
        return task

    def create_task(self, user_id: int, task: TaskCreate):
        new_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
        )
        return self.repository.create(new_task)

    def get_tasks(self, user_id: int, query: TaskQuery):
        items, total = self.repository.get_all_by_user_id(user_id, query)
        total_pages = (total + query.page_size -
                       1) // query.page_size if query.page_size > 0 else 0
        return PaginationResponse(
            items=items,
            page=query.page,
            page_size=query.page_size,
            total=total,
            total_pages=total_pages,
        )

    def get_task_by_id(self, task_id: int, user_id: int):
        return self._get_task_or_404(task_id, user_id)

    def update_task(self, task_id: int, user_id: int, task_in: TaskUpdate):
        task = self._get_task_or_404(task_id, user_id)
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        return self.repository.update(task)

    def delete_task(self, task_id: int, user_id: int):
        task = self._get_task_or_404(task_id, user_id)
        return self.repository.delete(task)

    def update_status(self, task_id: int, user_id: int, status: TaskStatus):
        task = self._get_task_or_404(task_id, user_id)
        task.status = status
        return self.repository.update(task)
