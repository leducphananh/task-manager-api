from typing import List, Optional

from app.models.task import \
    Task  # Import Task để SQLAlchemy nhận diện relationship với User
from app.models.user import User


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
