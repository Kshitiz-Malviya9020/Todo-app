from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Todo(Base):
    __tablename__ = "todos"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'ongoing', 'done')",
            name="check_todo_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="check_todo_priority",
        ),
        Index("ix_todos_user_status", "user_id", "status"),
    )

    todo_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        server_default="medium",
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.utc_timestamp(),
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Each todo belongs to one user.
    user: Mapped["User"] = relationship(
        back_populates="todos",
    )
