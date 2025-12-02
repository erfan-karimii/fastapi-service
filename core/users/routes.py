from fastapi import APIRouter , Depends ,Path , HTTPException,status,Query
from sqlalchemy import select , delete
from sqlalchemy.orm import Session 

from core.database import get_db
from core.base_schemas import Base404ErrorSchema

from .models import UserModel
from .schemas import UserResponseSchema , UserCreateSchema , UserUpdateSchema
from .enums import UserRegisterType

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("")
async def list_users(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> list[UserResponseSchema]:
    stmt = select(UserModel).offset(offset).limit(limit)
    result = db.execute(stmt).scalars().all()
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreateSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    if user_create.password != user_create.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    
    new_user = UserModel(
        **user_create.model_dump(exclude={"confirm_password"}),
        user_register_type=UserRegisterType.USERNAME
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponseSchema.model_validate(new_user,from_attributes=True)


@router.get("/{user_id}", responses={404: {"model": Base404ErrorSchema}})
async def get_user(user_id: int = Path(...,gt=0 ,description="ID of the user to retrieve"), db: Session = Depends(get_db)) -> UserResponseSchema:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result