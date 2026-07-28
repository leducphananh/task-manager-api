import pytest

from app.exceptions import TaskNotFoundException
from app.models.task import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


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

    user_1_tasks = task_service.get_tasks(user_id=1)
    assert len(user_1_tasks) == 2
    assert all(t.user_id == 1 for t in user_1_tasks)


def test_get_task_by_id_success(task_repo, task_service, task_factory):
    task_repo.tasks.append(task_factory(id=10, user_id=5, title="Target Task"))

    found = task_service.get_task_by_id(task_id=10, user_id=5)
    assert found.title == "Target Task"


def test_get_task_by_id_not_found(task_service):
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task_id=999, user_id=1)


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
