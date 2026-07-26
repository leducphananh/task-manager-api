from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, user: UserCreate):
        existing_user = self.repository.find_by_email(user.email)
        if existing_user:
            from app.exceptions import EmailAlreadyExistsException
            raise EmailAlreadyExistsException()

        hashed_password = hash_password(user.password)

        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=hashed_password
        )
        return self.repository.create(new_user)
