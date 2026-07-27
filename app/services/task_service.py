from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, user_id: int, task: TaskCreate):
        new_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
        )
        return self.repository.create(new_task)

    def get_tasks(self, user_id: int):
        return self.repository.get_all_by_user_id(user_id)

    def get_task_by_id(self, task_id: int, user_id: int):
        return self.repository.get_by_id(task_id, user_id)

    def update_task(self, task_id: int, user_id: int, task_in: TaskCreate):
        task = self.repository.get_by_id(task_id, user_id)
        task.title = task_in.title
        task.description = task_in.description
        task.status = task_in.status
        task.due_date = task_in.due_date
        return self.repository.update(task)

    def delete_task(self, task_id: int, user_id: int):
        task = self.repository.get_by_id(task_id, user_id)
        return self.repository.delete(task)

    def update_status(self, task_id: int, user_id: int, status: str):
        task = self.repository.get_by_id(task_id, user_id)
        task.status = status
        return self.repository.update(task)
