from pydantic import BaseModel


class Page[T](BaseModel):
    data: list[T]
    total: int
    offset: int
    limit: int
