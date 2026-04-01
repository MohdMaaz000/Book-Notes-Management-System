from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginationParams, TimestampedSchema


class BookBase(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=2000)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=2000)


class BookQueryParams(PaginationParams):
    sort_by: str = Field(default="created_at", pattern="^(title|created_at|updated_at)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    created_from: datetime | None = None
    created_to: datetime | None = None


class BookResponse(TimestampedSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None = None
