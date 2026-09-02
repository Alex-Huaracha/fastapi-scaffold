from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate, UserPublic
from app.modules.user.service import EmailAlreadyRegistered, UserService


def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]) -> UserService:
    return UserService(UserRepository(db))


router = APIRouter()


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await service.create(data)
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
