from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from core.database import get_db

from auth.handler import sign_jwt
from .models import UserModel
from .schemas import (
    UserCreateSchema,
    UserLoginSchema,
)
from .enums import UserRegisterType

router = APIRouter(tags=["Users"], prefix="/users")



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreateSchema, db: Session = Depends(get_db)
) -> dict[str, str]:
    if not user_create.email:
        user_create.email = str(user_create.username) + "@localhost.com"
    stmt = select(UserModel).where(
        or_(
            UserModel.email == user_create.email,
            UserModel.username == user_create.username,
        )
    )
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already exists",
        )

    new_user = UserModel(
        **user_create.model_dump(exclude={"confirm_password", "password"}),
        user_register_type=UserRegisterType.USERNAME
    )

    new_user.set_password(user_create.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return sign_jwt(str(new_user.id))


@router.post("/login")
async def login_user(
    user_create: UserLoginSchema, db: Session = Depends(get_db)
) -> dict[str, str]:
    stmt = select(UserModel).where(
        or_(
            UserModel.email == user_create.email,
            UserModel.username == user_create.username,
        )
    )
    existing_user = db.execute(stmt).scalar_one_or_none()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email does not exist",
        )

    if not existing_user.verify_password(user_create.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    return sign_jwt(str(existing_user.id))

