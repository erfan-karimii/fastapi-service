from core.base_model import BaseModel 
from sqlalchemy import  String, Boolean , Text 
from sqlalchemy.orm import Mapped , mapped_column


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    title:Mapped[str] = mapped_column(String(256), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    is_completed:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, is_completed={self.is_completed})"
