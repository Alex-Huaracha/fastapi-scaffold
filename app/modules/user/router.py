from typing import Annotated

from fastapi import APIRouter, Query, status

from app.core.database import SessionDep
from app.core.schemas import Page
from app.modules.user import service
from app.modules.user.dependencies import ExistingUser
from app.modules.user.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter()


@router.get("", response_model=Page[UserPublic])
async def read_users(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    users, total = await service.get_users(session, offset, limit)
    return {"data": users, "total": total, "offset": offset, "limit": limit}


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, data: UserCreate):
    return await service.create(session, data)


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(user: ExistingUser):
    return user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    session: SessionDep,
    user: ExistingUser,
    data: UserUpdate,
):
    return await service.update(session, user, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, user: ExistingUser):
    await service.delete(session, user)
