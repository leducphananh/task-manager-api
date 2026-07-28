from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskQuery


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int, user_id: int):
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.user_id == user_id)
            .first()
        )

    def get_all_by_user_id(self, user_id: int, query: TaskQuery):
        db_query = self.db.query(Task).filter(Task.user_id == user_id)

        # Lọc theo trạng thái
        if query.status:
            db_query = db_query.filter(Task.status == query.status)

        # Lọc theo từ khóa (tìm trong title hoặc description)
        if query.keyword:
            search = f"%{query.keyword}%"
            db_query = db_query.filter(
                Task.title.ilike(search) | Task.description.ilike(search)
            )

        # Đếm tổng số lượng bản ghi thỏa mãn điều kiện lọc
        total = db_query.count()

        # Sắp xếp
        sort_column = getattr(Task, query.sort_by, Task.created_at)
        if query.order == "asc":
            db_query = db_query.order_by(sort_column.asc())
        else:
            db_query = db_query.order_by(sort_column.desc())

        # Phân trang
        offset = (query.page - 1) * query.page_size
        items = db_query.offset(offset).limit(query.page_size).all()

        return items, total

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()
        return task
