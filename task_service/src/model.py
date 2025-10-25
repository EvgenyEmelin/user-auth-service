from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class TaskModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow,nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow,nullable=False, onupdate=datetime.utcnow)
