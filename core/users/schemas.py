from datetime import datetime
from pydantic import BaseModel , Field , field_validator , EmailStr
from .enums import UserRegisterType


class UserBaseSchema(BaseModel):
    email: EmailStr | None = Field(None, max_length=100, description="Email of the user")


class UserResponseSchema(UserBaseSchema):
    username: str = Field(..., max_length=50, description="Username of the user")
    user_register_type: UserRegisterType = Field(..., description="Type of user registration")
    id: int = Field(..., description="ID of the user")
    is_active: bool = Field(..., description="Indicates if the user is active")
    is_verified: bool = Field(..., description="Indicates if the user is verified")
    created_date: datetime = Field(..., description="Timestamp when the user was created")
    updated_date: datetime = Field(..., description="Timestamp when the user was last updated")
    
    
class UserCreateSchema(UserBaseSchema):
    username: str = Field(..., max_length=50, description="Username of the user")
    password: str = Field(..., min_length=8, max_length=255, description="Password of the user")
    confirm_password: str = Field(..., min_length=8, max_length=255, description="Password confirmation")

    @field_validator("password", mode='after')
    def validate_password(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Password must not contain spaces")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")

        return value


class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(None, max_length=50, description="First name of the user")
    last_name: str | None = Field(None, max_length=50, description="Last name of the user")
