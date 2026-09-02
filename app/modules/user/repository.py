from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user import models


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: models.User) -> models.User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_email(self, email: str) -> models.User | None:
        result = await self.db.execute(
            select(models.User).where(
                func.lower(models.User.email) == email.lower(),
            )
        )

        return result.scalars().first()
