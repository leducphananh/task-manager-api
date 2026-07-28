from datetime import datetime
from typing import Callable

import pytest

from app.core.security import hash_password
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.services.task_service import TaskService
from app.services.user_service import UserService
from tests.fakes.fake_task_repository import FakeTaskRepository
from tests.fakes.fake_user_repository import FakeUserRepository


# ==========================================
# 1. REPOSITORY FIXTURES
# ==========================================
@pytest.fixture
def user_repo() -> FakeUserRepository:
    """Tạo FakeUserRepository độc lập cho mỗi test case."""
    return FakeUserRepository()


@pytest.fixture
def task_repo() -> FakeTaskRepository:
    """Tạo FakeTaskRepository độc lập cho mỗi test case."""
    return FakeTaskRepository()


# ==========================================
# 2. SERVICE FIXTURES (Dependency Injection)
# ==========================================
@pytest.fixture
def user_service(user_repo: FakeUserRepository) -> UserService:
    """Bơm user_repo vào UserService."""
    return UserService(repository=user_repo)


@pytest.fixture
def task_service(task_repo: FakeTaskRepository) -> TaskService:
    """Bơm task_repo vào TaskService (với redis=None trong các test mặc định để cô lập hạ tầng)."""
    return TaskService(repository=task_repo, redis=None)


# ==========================================
# 3. FACTORY FIXTURES (Xưởng tạo dữ liệu mẫu)
# ==========================================
@pytest.fixture
def user_factory() -> Callable[..., User]:
    """Hàm hỗ trợ tạo nhanh object User mẫu trong test."""
    def _create_user(
        id: int = 1,
        name: str = "Test User",
        email: str = "test@test.com",
        password: str = "12345678",
    ) -> User:
        return User(
            id=id,
            name=name,
            email=email,
            password_hash=hash_password(
                password) if password != "fake_hashed_string" else "fake_hashed_string",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    return _create_user


@pytest.fixture
def task_factory() -> Callable[..., Task]:
    """Hàm hỗ trợ tạo nhanh object Task mẫu trong test."""
    def _create_task(
        id: int = 1,
        user_id: int = 1,
        title: str = "Test Task",
        description: str = "Test Description",
        status: TaskStatus = TaskStatus.TODO,
    ) -> Task:
        return Task(
            id=id,
            user_id=user_id,
            title=title,
            description=description,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    return _create_task
