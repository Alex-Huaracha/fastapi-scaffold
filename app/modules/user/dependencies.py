import uuid
from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.user import models, service


async def resolve_user(user_id: uuid.UUID, session: SessionDep) -> models.User:
    return await service.get_by_id(session, user_id)


ExistingUser = Annotated[models.User, Depends(resolve_user)]
