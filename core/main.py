# from contextlib import asynccontextmanager
from fastapi import FastAPI 
import uvicorn
# from database import Base , engine 
from tasks.routes import router as tasks_router

VERSION =  '0.0.1'

tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operations with tasks.",
        "externalDocs": {
            "description": "Tasks external docs",
            "url": "https://example.com/tasks-docs"
        }
    }
]

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     Base.metadata.create_all(engine)
#     yield
    

app = FastAPI(
    title="TODO App",
    description="Todo application built with FastAPI",
    version=VERSION,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "erfan karimi",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={"displayRequestDuration": True},
    openapi_tags=tags_metadata,
    # lifespan=lifespan
)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",       
        host="0.0.0.0",    
        port=8000,         
        reload=True,       
    )