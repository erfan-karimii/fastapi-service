from sqlalchemy import  String, Boolean , Enum 
from sqlalchemy.orm import Mapped , mapped_column , relationship
from passlib.context import CryptContext

from core.base_model import BaseModel 
from tasks.models import TaskModel
from .enums import UserRegisterType 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    __tablename__ = "users"
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email:Mapped[str] = mapped_column(String(100), unique=True, nullable=True, index=True)
    password:Mapped[str] = mapped_column(String(255), nullable=True)
    user_register_type:Mapped[UserRegisterType] = mapped_column(Enum(UserRegisterType), nullable=False,default=UserRegisterType.USERNAME)
    first_name:Mapped[str] = mapped_column(String(50), nullable=True)
    last_name:Mapped[str] = mapped_column(String(50), nullable=True)
    tasks:Mapped[list[TaskModel]] = relationship("TaskModel",backref="user")

    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email}, user_register_type={self.user_register_type})"
    
    def __str__(self):
        return self.username
    
    def set_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)
    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password,self.password)
