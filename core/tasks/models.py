from datetime import datetime
from core.database import Base 
from sqlalchemy import  Integer, String, Boolean , Text , DateTime, func
from sqlalchemy.orm import Mapped , mapped_column


class TaskModel(Base):
    __tablename__ = "tasks"

    id:Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True, index=True)
    title:Mapped[str] = mapped_column(String(256), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    is_completed:Mapped[bool] = mapped_column(Boolean, default=False)

    created_date:Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_date:Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, is_completed={self.is_completed})"
