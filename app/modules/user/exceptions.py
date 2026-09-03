from fastapi import status

from app.core.exceptions import AppError


class EmailAlreadyRegistered(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Email already registered"


class UsernameAlreadyRegistered(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Username already registered"


class UserAlreadyExists(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Username or email already exists"


class UserNotFound(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"
