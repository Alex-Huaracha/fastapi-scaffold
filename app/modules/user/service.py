import uuid

from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user import models
from app.modules.user.exceptions import (
    EmailAlreadyRegistered,
    UserAlreadyExists,
    UsernameAlreadyRegistered,
    UserNotFound,
)
from app.modules.user.schemas import UserCreate


async def create(session: AsyncSession, data: UserCreate) -> models.User:
    if await session.scalar(
        select(exists().where(models.User.email == data.email.lower()))
    ):
        raise EmailAlreadyRegistered

    if await session.scalar(
        select(exists().where(models.User.username == data.username))
    ):
        raise UsernameAlreadyRegistered

    new_user = models.User(
        username=data.username,
        email=data.email.lower(),
        password=data.password,
        name=data.name,
        last_name=data.last_name,
    )

    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise UserAlreadyExists from exc

    return new_user


async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> models.User:
    user = await session.get(models.User, user_id)
    if user is None:
        raise UserNotFound

    return user

