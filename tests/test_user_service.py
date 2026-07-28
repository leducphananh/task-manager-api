from datetime import datetime
from typing import List, Optional
from unittest.mock import patch

import pytest

from app.core.security import hash_password
from app.exceptions import InvalidCredentialsException
from app.models.task import \
    Task  # Import Task để SQLAlchemy nhận diện relationship với User
from app.models.user import User
from app.repositories import task_repository
from app.schemas.user import LoginRequest
from app.services.user_service import UserService


class FakeUserRepository:
    """Fake Repository để test unit mà không cần kết nối Database thật."""

    def __init__(self):
        self.users: List[User] = []

    def create(self, user: User) -> User:
        if not user.id:
            user.id = len(self.users) + 1
        self.users.append(user)
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        for u in self.users:
            if u.email == email:
                return u
        return None

    def find_by_id(self, id: int) -> Optional[User]:
        for u in self.users:
            if u.id == id:
                return u
        return None


def test_login_success():
    # 1. Khởi tạo Fake Repository
    repo = FakeUserRepository()

    # 2. Tạo một user giả lập với mật khẩu đã được băm (hash)
    user = User(
        id=1,
        name="Test",
        email="test@test.com",
        password_hash=hash_password("12345678"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repo.users.append(user)

    # 3. Khởi tạo UserService và truyền Fake Repository vào (Dependency Injection)
    service = UserService(repository=repo)

    # 4. Thực hiện gọi hàm login với thông tin hợp lệ
    login_req = LoginRequest(email="test@test.com", password="12345678")
    result = service.login(login_req)

    # 5. Kiểm tra kết quả trả về (Assertion)
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert len(result["access_token"]) > 0


def test_login_invalid_email():
    repo = FakeUserRepository()
    service = UserService(repository=repo)
    # email không tồn tại trong danh sách của repo
    login_req = LoginRequest(email="nonexistent@test.com", password="12345678")

    # Kiểm tra service phải ném ra ngoại lệ InvalidCredentialsException
    with pytest.raises(InvalidCredentialsException):
        service.login(login_req)


def test_login_invalid_password():
    repo = FakeUserRepository()
    user = User(
        id=1,
        name="Test",
        email="test@test.com",
        password_hash=hash_password("12345678"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repo.users.append(user)

    service = UserService(repository=repo)
    # Nhập sai mật khẩu
    login_req = LoginRequest(email="test@test.com", password="wrongpassword")

    # Kiểm tra service phải ném ra ngoại lệ InvalidCredentialsException
    with pytest.raises(InvalidCredentialsException):
        service.login(login_req)


def test_login_success_with_monkeypatch(monkeypatch):
    """Minh họa cách Mock verify_password bằng công cụ monkeypatch của pytest."""
    repo = FakeUserRepository()

    # Lưu ý: Không cần hash mật khẩu thật tốn thời gian, chỉ cần một chuỗi giả
    user = User(
        id=1,
        name="Test",
        email="test@test.com",
        password_hash="fake_hashed_string",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repo.users.append(user)

    service = UserService(repository=repo)

    # Dùng monkeypatch để thay thế hàm verify_password tại nơi nó được sử dụng (user_service)
    # bằng một hàm lambda luôn trả về True
    monkeypatch.setattr(
        "app.services.user_service.verify_password", lambda plain, hashed: True)

    login_req = LoginRequest(email="test@test.com", password="any_password")
    result = service.login(login_req)

    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_success_with_unittest_mock():
    """Minh họa cách Mock verify_password bằng thư viện chuẩn unittest.mock."""
    repo = FakeUserRepository()

    user = User(
        id=1,
        name="Test",
        email="test@test.com",
        password_hash="fake_hashed_string",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repo.users.append(user)

    service = UserService(repository=repo)

    # Dùng context manager patch() của unittest.mock
    with patch("app.services.user_service.verify_password") as mock_verify:
        mock_verify.return_value = True  # Thiết lập khi gọi hàm thì trả về True

        login_req = LoginRequest(
            email="test@test.com", password="any_password")
        result = service.login(login_req)

        # Kiểm tra token
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        # Quyền năng của unittest.mock: Kiểm tra hàm verify_password có thực sự được gọi đúng 1 lần
        # và đúng với tham số truyền vào hay không!
        mock_verify.assert_called_once_with(
            "any_password", "fake_hashed_string")
