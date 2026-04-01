from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginationParams, TimestampedSchema


class NoteBase(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    content: str = Field(default="", max_length=20000)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    content: str | None = Field(default=None, max_length=20000)


class NoteQueryParams(PaginationParams):
    sort_by: str = Field(default="updated_at", pattern="^(title|created_at|updated_at)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    updated_from: datetime | None = None
    updated_to: datetime | None = None


class NoteResponse(TimestampedSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
