from fastapi import APIRouter , Depends ,Path , HTTPException,status,Query
from sqlalchemy import select , delete
from sqlalchemy.orm import Session 
from core.database import get_db
from core.base_schemas import Base404ErrorSchema
from .models import TaskModel
from .schemas import TaskSchema , TaskCreateSchema 

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get("")
async def get_tasks(db: Session = Depends(get_db),limit:int = Query(10, gt=0),offset:int = Query(0, ge=0))-> list[TaskSchema]:
    stmt = db.query(TaskModel).limit(limit).offset(offset)
    tasks = db.execute(stmt).scalars().all()
    return tasks


@router.post("",status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskModel(**task.model_dump())
    db.add(new_task)
    db.commit()
    return new_task

@router.delete("",status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_tasks(db: Session = Depends(get_db)) -> None:
    stmt = delete(TaskModel)
    db.execute(stmt)
    db.commit()
    return

@router.get("/{id}",responses={404:{"model":Base404ErrorSchema}})
async def get_task(id:int = Path(...),db:Session = Depends(get_db)) -> TaskSchema:
    stmt = select(TaskModel).where(TaskModel.id==id)
    task = db.execute(stmt).scalars().first()
    if task:
        return task
    raise HTTPException(status.HTTP_404_NOT_FOUND,Base404ErrorSchema().detail)

@router.put("/{id}",responses={404:{"model":Base404ErrorSchema}})
async def update_task(task_data:TaskCreateSchema,id:int = Path(...),db:Session = Depends(get_db)) -> TaskSchema:
    stmt = select(TaskModel).where(TaskModel.id==id)
    task = db.execute(stmt).scalars().first()
    if task:
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    raise HTTPException(status.HTTP_404_NOT_FOUND,Base404ErrorSchema().detail)

@router.delete("/{id}",responses={404:{"model":Base404ErrorSchema}},status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id:int = Path(...),db:Session = Depends(get_db)):
    stmt = select(TaskModel).where(TaskModel.id==id)
    task = db.execute(stmt).scalars().first()
    if task:
        db.delete(task)
        db.commit()
        return 
    raise HTTPException(status.HTTP_404_NOT_FOUND,Base404ErrorSchema().detail)