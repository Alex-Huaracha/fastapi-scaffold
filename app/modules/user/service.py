from app.modules.user import models
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate


class EmailAlreadyRegistered(Exception):
    pass


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, data: UserCreate) -> models.User:
        if await self.repository.get_by_email(data.email):
            raise EmailAlreadyRegistered()

        new_user = models.User(
            email=data.email.lower(),
            password=data.password,
            name=data.name,
            last_name=data.last_name,
        )

        await self.repository.create(new_user)
        await self.db.commit()

        return new_user
