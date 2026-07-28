import pytest

from app.exceptions import TaskNotFoundException
from app.models.task import TaskStatus
from app.schemas.task import TaskCreate, TaskQuery, TaskUpdate


def test_create_task(task_service):
    task_create = TaskCreate(
        title="Học Pytest Fixtures",
        description="Thực hành xây dựng kiến trúc test chuyên nghiệp",
        status=TaskStatus.TODO,
    )
    created = task_service.create_task(user_id=1, task=task_create)

    assert created.id == 1
    assert created.user_id == 1
    assert created.title == "Học Pytest Fixtures"
    assert created.status == TaskStatus.TODO


def test_get_tasks(task_repo, task_service, task_factory):
    # Tạo 2 task cho user 1 và 1 task cho user 2
    task_repo.tasks.append(task_factory(id=1, user_id=1, title="Task 1"))
    task_repo.tasks.append(task_factory(id=2, user_id=1, title="Task 2"))
    task_repo.tasks.append(task_factory(
        id=3, user_id=2, title="Other User Task"))

    query = TaskQuery(page=1, page_size=10)
    result = task_service.get_tasks(user_id=1, query=query)
    assert result.total == 2
    assert len(result.items) == 2
    assert all(t.user_id == 1 for t in result.items)


def test_get_task_by_id_success(task_repo, task_service, task_factory):
    task_repo.tasks.append(task_factory(id=10, user_id=5, title="Target Task"))

    found = task_service.get_task_by_id(task_id=10, user_id=5)
    assert found.title == "Target Task"


def test_get_task_by_id_not_found(task_service):
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task_id=999, user_id=1)


def test_get_task_by_id_unauthorized_user(task_repo, task_service, task_factory):
    """Test khi task_id tồn tại nhưng thuộc sở hữu của user khác -> Phải ném ngoại lệ TaskNotFoundException."""
    # Tạo task số 100 thuộc sở hữu của User 2
    task_repo.tasks.append(task_factory(
        id=100, user_id=2, title="Private Task of User 2"))

    # User 1 cố gắng lấy thông tin Task 100
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task_id=100, user_id=1)


def test_update_task(task_repo, task_service, task_factory):
    task = task_factory(id=1, user_id=1, title="Old Title",
                        status=TaskStatus.TODO)
    task_repo.tasks.append(task)

    update_req = TaskUpdate(title="New Title", status=TaskStatus.DONE)
    updated = task_service.update_task(
        task_id=1, user_id=1, task_in=update_req)

    assert updated.title == "New Title"
    assert updated.status == TaskStatus.DONE


def test_delete_task(task_repo, task_service, task_factory):
    task = task_factory(id=1, user_id=1)
    task_repo.tasks.append(task)

    deleted = task_service.delete_task(task_id=1, user_id=1)
    assert deleted.id == 1
    assert len(task_repo.tasks) == 0


def test_get_task_by_id_with_redis_cache(task_repo, task_factory):
    """Test cơ chế Cache-Aside với Redis: Lưu cache khi miss và trả về từ cache khi hit."""
    from unittest.mock import MagicMock
    from app.schemas.task import TaskResponse
    from app.services.task_service import TaskService

    mock_redis = MagicMock()
    # Lần 1: giả lập miss cache (get_model trả về None)
    mock_redis.get_model.return_value = None

    service_with_cache = TaskService(repository=task_repo, redis=mock_redis)
    task_repo.tasks.append(task_factory(id=50, user_id=1, title="Super Cached Task"))

    # Lần 1 gọi: sẽ lấy từ repository và lưu vào cache
    res1 = service_with_cache.get_task_by_id(task_id=50, user_id=1)
    assert res1.title == "Super Cached Task"
    mock_redis.get_model.assert_called_once_with("task:1:50", TaskResponse)
    mock_redis.set.assert_called_once()

    # Lần 2 giả lập hit cache: get_model trả về chính object vừa cache
    mock_redis.get_model.return_value = res1
    res2 = service_with_cache.get_task_by_id(task_id=50, user_id=1)
    assert res2.title == "Super Cached Task"
    assert mock_redis.get_model.call_count == 2


def test_get_tasks_with_redis_cache(task_repo, task_factory):
    """Test cơ chế Cache-Aside cho danh sách task (get_tasks)."""
    from unittest.mock import MagicMock
    from app.schemas.task import TaskQuery
    from app.services.task_service import TaskService

    mock_redis = MagicMock()
    mock_redis.get_model.return_value = None  # Lần 1: miss cache

    service_with_cache = TaskService(repository=task_repo, redis=mock_redis)
    task_repo.tasks.append(task_factory(id=101, user_id=1, title="List Cached Task"))

    query = TaskQuery(page=1, page_size=10)
    res1 = service_with_cache.get_tasks(user_id=1, query=query)
    assert len(res1.items) == 1
    assert res1.items[0].title == "List Cached Task"
    mock_redis.get_model.assert_called_once()
    mock_redis.set.assert_called_once()

    # Lần 2 hit cache
    mock_redis.get_model.return_value = res1
    res2 = service_with_cache.get_tasks(user_id=1, query=query)
    assert len(res2.items) == 1
    assert mock_redis.get_model.call_count == 2


