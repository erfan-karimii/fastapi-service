from core.base_model import BaseModel 
from sqlalchemy import  String, Boolean , Text , ForeignKey 
from sqlalchemy.orm import Mapped , mapped_column


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title:Mapped[str] = mapped_column(String(256), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    is_completed:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, description={self.description[:10]}, is_completed={self.is_completed})"
    

    def __str__(self):
        return self.title
