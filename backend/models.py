from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """Task model representing a todo item belonging to a user."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
