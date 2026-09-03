from fastapi import APIRouter, status

from app.core.database import SessionDep
from app.modules.user import service
from app.modules.user.dependencies import UserDep
from app.modules.user.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter()


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    session: SessionDep,
):
    return await service.create(session, data)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user: UserDep):
    return user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(user: UserDep, data: UserUpdate, session: SessionDep):
    return await service.update(session, user, data)
