from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "task_manager",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    include=["app.tasks.email_tasks"],
)
