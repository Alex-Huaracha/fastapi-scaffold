import uuid
from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.user import models, service


async def valid_user_id(user_id: uuid.UUID, session: SessionDep):
    return await service.get_by_id(session, user_id)


UserDep = Annotated[models.User, Depends(valid_user_id)]
