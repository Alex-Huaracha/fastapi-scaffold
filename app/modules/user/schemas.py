import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(max_length=100)
    name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=30)
    email: EmailStr | None = Field(default=None, max_length=100)
    name: str | None = Field(default=None, min_length=3, max_length=30)
    last_name: str | None = Field(default=None, min_length=3, max_length=30)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: EmailStr
    name: str
    last_name: str
