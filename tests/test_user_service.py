from unittest.mock import patch

import pytest

from app.exceptions import InvalidCredentialsException
from app.schemas.user import LoginRequest


def test_login_success(user_repo, user_service, user_factory):
    # Dùng user_factory đẻ ra 1 user mẫu nhanh chóng rồi thêm vào user_repo
    user = user_factory(id=1, email="test@test.com", password="12345678")
    user_repo.users.append(user)

    login_req = LoginRequest(email="test@test.com", password="12345678")
    result = user_service.login(login_req)

    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert len(result["access_token"]) > 0


def test_login_invalid_email(user_service):
    # Không cần tạo user, danh sách repo mặc định là rỗng -> email không tồn tại
    login_req = LoginRequest(email="nonexistent@test.com", password="12345678")

    with pytest.raises(InvalidCredentialsException):
        user_service.login(login_req)


def test_login_invalid_password(user_repo, user_service, user_factory):
    user = user_factory(id=1, email="test@test.com", password="12345678")
    user_repo.users.append(user)

    # Nhập sai mật khẩu
    login_req = LoginRequest(email="test@test.com", password="wrongpassword")

    with pytest.raises(InvalidCredentialsException):
        user_service.login(login_req)


def test_login_success_with_monkeypatch(monkeypatch, user_repo, user_service, user_factory):
    """Minh họa cách Mock verify_password bằng công cụ monkeypatch của pytest."""
    user = user_factory(id=1, email="test@test.com",
                        password="fake_hashed_string")
    user_repo.users.append(user)

    # Dùng monkeypatch để thay thế hàm verify_password tại nơi nó được sử dụng (user_service)
    monkeypatch.setattr(
        "app.services.user_service.verify_password", lambda plain, hashed: True)

    login_req = LoginRequest(email="test@test.com", password="any_password")
    result = user_service.login(login_req)

    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_success_with_unittest_mock(user_repo, user_service, user_factory):
    """Minh họa cách Mock verify_password bằng thư viện chuẩn unittest.mock."""
    user = user_factory(id=1, email="test@test.com",
                        password="fake_hashed_string")
    user_repo.users.append(user)

    # Dùng context manager patch() của unittest.mock
    with patch("app.services.user_service.verify_password") as mock_verify:
        mock_verify.return_value = True

        login_req = LoginRequest(
            email="test@test.com", password="any_password")
        result = user_service.login(login_req)

        assert "access_token" in result
        assert result["token_type"] == "bearer"
        mock_verify.assert_called_once_with(
            "any_password", "fake_hashed_string")
