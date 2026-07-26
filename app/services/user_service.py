from app.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self):
        return self.repository.get_all()

    def create_user(self, user):
        return self.repository.create(user)
