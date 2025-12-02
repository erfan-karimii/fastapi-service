from random import randint
from contextlib import asynccontextmanager
from fastapi import FastAPI , Query , HTTPException , status , Path , Depends , APIRouter
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy import select ,delete
from sqlalchemy.orm import Session 
from schemas import PersonResponseSchema , PersonCreateSchema ,PersonUpdateSchema
from database import Base , engine , get_db , User


VERSION =  '0.0.1'

# logfire.configure(environment="test fasapi",service_name="fastapi service",service_version=VERSION)  
# logfire.instrument_system_metrics()


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine)
    yield
    

app = FastAPI(
    version=VERSION,
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan
)

    
@app.get("/names")
def read_names(q: str | None = Query(None,max_length=50), db:Session = Depends(get_db)) -> list[PersonResponseSchema]:
    stmt = select(User)
    if q:
        stmt = stmt.where(User.name.ilike(q))
    results = db.execute(stmt).scalars().all()
    return results

@app.post("/names")
def create_name(person: PersonCreateSchema,db:Session = Depends(get_db)):
    user = User(name=person.name,age=randint(10,50))
    db.add(user)
    db.commit()

    return JSONResponse(content={"detail": "data created successfully"},status_code=status.HTTP_201_CREATED)


@app.delete("/names")
def delete_names(db:Session = Depends(get_db)):
    stmt = delete(User)
    db.execute(stmt)
    db.commit() 
    return JSONResponse(content={"detail": "All names deleted successfully"},status_code=status.HTTP_202_ACCEPTED)


@app.get("/names/{id}")
def read_name(id:int = Path,db:Session = Depends(get_db)) -> PersonResponseSchema:
    stmt = select(User).where(User.id == id)
    user = db.execute(stmt).scalars().first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="not found")


@app.put("/names/{id}")
def replace_name(id: int,data:PersonUpdateSchema,db:Session = Depends(get_db)) -> PersonResponseSchema:
    stmt = select(User).where(User.id == id)
    user = db.execute(stmt).scalars().first()
    if user:
        user.name = data.name
        db.commit()
        return JSONResponse(content={"detail":"obj replaces succesfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=404, detail="not found")
    


@app.delete("/names/{id}")
def delete_name(id:int,db:Session = Depends(get_db)):
    stmt = select(User).where(User.id == id)
    user = db.execute(stmt).scalars().first()
    if user:
        db.delete(user)
        db.commit()
        return JSONResponse(content={"detail": "obj deleted succesfully"},status_code=status.HTTP_202_ACCEPTED)
    raise HTTPException(status_code=404, detail="not found")




if __name__ == "__main__":
    uvicorn.run(
        "main:app",       
        host="0.0.0.0",    
        port=8000,         
        reload=True,       
    )