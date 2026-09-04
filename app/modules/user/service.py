import uuid
from collections.abc import Sequence

from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user import models
from app.modules.user.exceptions import (
    EmailAlreadyRegistered,
    UserAlreadyExists,
    UserInUse,
    UsernameAlreadyRegistered,
    UserNotFound,
)
from app.modules.user.schemas import UserCreate, UserUpdate


async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> models.User:
    user = await session.get(models.User, user_id)
    if user is None:
        raise UserNotFound

    return user


async def get_users(
    session: AsyncSession, offset: int = 0, limit: int = 100
) -> tuple[Sequence[models.User], int]:
    total = (await session.scalars(select(func.count()).select_from(models.User))).one()

    users = (
        await session.scalars(
            select(models.User)
            .order_by(models.User.name, models.User.id)
            .offset(offset)
            .limit(limit)
        )
    ).all()

    return users, total


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


async def update(
    session: AsyncSession, user: models.User, data: UserUpdate
) -> models.User:
    values = data.model_dump(exclude_unset=True)

    if "email" in values:
        values["email"] = values["email"].lower()

    for field, value in values.items():
        setattr(user, field, value)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise UserAlreadyExists from exc

    return user


async def delete(session: AsyncSession, user: models.User) -> None:
    await session.delete(user)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise UserInUse from exc
