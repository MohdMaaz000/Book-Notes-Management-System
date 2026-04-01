from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginationParams, TimestampedSchema


class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class CommentQueryParams(PaginationParams):
    sort_by: str = Field(default="created_at", pattern="^(created_at|updated_at)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    author_id: UUID | None = None


class CommentResponse(TimestampedSchema):
    model_config = ConfigDict(from_attributes=True)

    content: str
    user_id: UUID
    note_id: UUID
