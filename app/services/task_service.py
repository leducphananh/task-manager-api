from typing import Optional

from app.core.cache_keys import CacheKeys
from app.core.config import settings
from app.core.logging import logger
from app.exceptions import TaskNotFoundException
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.common import PaginationResponse
from app.schemas.task import TaskCreate, TaskQuery, TaskResponse, TaskUpdate
from app.services.redis_service import RedisService, redis_service


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
        redis: Optional[RedisService] = redis_service,
    ):
        self.repository = repository
        self.redis = redis

    def _get_task_or_404(self, task_id: int, user_id: int) -> Task:
        task = self.repository.get_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundException()
        return task

    def _invalidate_task_cache(self, user_id: int, task_id: int):
        """Xóa cache của một task cụ thể."""
        if self.redis:
            self.redis.delete(CacheKeys.task(user_id, task_id))

    def _invalidate_task_list_cache(self, user_id: int):
        """Xóa toàn bộ cache danh sách task của user."""
        if self.redis:
            self.redis.delete_by_pattern(CacheKeys.task_list_pattern(user_id))

    def create_task(self, user_id: int, task: TaskCreate):
        new_task = Task(
            user_id=user_id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
        )
        created_task = self.repository.create(new_task)
        self._invalidate_task_list_cache(user_id)
        return created_task

    def get_tasks(self, user_id: int, query: TaskQuery):
        cache_key = CacheKeys.task_list(user_id, query.page)

        # 1. Thử lấy từ cache Redis (Cache-Aside pattern cho danh sách)
        if self.redis:
            cached_resp = self.redis.get_model(
                cache_key, PaginationResponse[TaskResponse]
            )
            if cached_resp:
                return cached_resp

        # 2. Nếu miss cache -> Lấy từ DB PostgreSQL
        items, total = self.repository.get_all_by_user_id(user_id, query)
        total_pages = (total + query.page_size -
                       1) // query.page_size if query.page_size > 0 else 0

        resp = PaginationResponse[TaskResponse](
            items=[TaskResponse.model_validate(t) for t in items],
            page=query.page,
            page_size=query.page_size,
            total=total,
            total_pages=total_pages,
        )

        # 3. Lưu vào cache Redis
        if self.redis:
            self.redis.set(cache_key, resp, ex=settings.redis_default_ttl)

        return resp

    def get_task_by_id(self, task_id: int, user_id: int):
        cache_key = CacheKeys.task(user_id, task_id)

        # 1. Thử lấy từ cache Redis (Cache-Aside pattern)
        if self.redis:
            cached_task = self.redis.get_model(cache_key, TaskResponse)
            if cached_task:
                return cached_task

        # 2. Nếu miss cache -> Lấy từ DB PostgreSQL
        task = self._get_task_or_404(task_id, user_id)
        task_resp = TaskResponse.model_validate(task)

        # 3. Lưu vào cache Redis sử dụng TTL cấu hình
        if self.redis:
            self.redis.set(cache_key, task_resp, ex=settings.redis_default_ttl)

        return task_resp

    def update_task(self, task_id: int, user_id: int, task_in: TaskUpdate):
        task = self._get_task_or_404(task_id, user_id)
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        updated_task = self.repository.update(task)
        self._invalidate_task_cache(user_id, task_id)
        self._invalidate_task_list_cache(user_id)
        return updated_task

    def delete_task(self, task_id: int, user_id: int):
        task = self._get_task_or_404(task_id, user_id)
        deleted_task = self.repository.delete(task)
        self._invalidate_task_cache(user_id, task_id)
        self._invalidate_task_list_cache(user_id)
        return deleted_task

    def update_status(self, task_id: int, user_id: int, status: TaskStatus):
        task = self._get_task_or_404(task_id, user_id)
        task.status = status
        updated_task = self.repository.update(task)
        self._invalidate_task_cache(user_id, task_id)
        self._invalidate_task_list_cache(user_id)
        return updated_task
