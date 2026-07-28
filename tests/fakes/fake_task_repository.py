from typing import Any, List, Optional

from app.models.task import Task
from app.models.user import User  # Đảm bảo SQLAlchemy nhận diện relationship


class FakeTaskRepository:
    """Fake Task Repository để test unit mà không cần kết nối Database thật."""

    def __init__(self):
        self.tasks: List[Task] = []

    def create(self, task: Task) -> Task:
        if not task.id:
            task.id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def get_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id and t.user_id == user_id:
                return t
        return None

    def get_all_by_user_id(self, user_id: int, query: Optional[Any] = None) -> tuple[List[Task], int]:
        tasks = [t for t in self.tasks if t.user_id == user_id]
        if query and getattr(query, "status", None):
            tasks = [t for t in tasks if t.status == query.status]
        if query and getattr(query, "keyword", None):
            kw = query.keyword.lower()
            tasks = [t for t in tasks if kw in t.title.lower() or (
                t.description and kw in t.description.lower())]
        return tasks, len(tasks)

    def update(self, task: Task) -> Task:
        for i, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[i] = task
                return task
        return task

    def delete(self, task: Task) -> Task:
        if task in self.tasks:
            self.tasks.remove(task)
        return task
