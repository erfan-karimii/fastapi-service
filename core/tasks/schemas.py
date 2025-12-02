from datetime import datetime
from pydantic import BaseModel , Field , field_serializer


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, description="Title of the task")
    description: str | None = Field(
            None,
            max_length=500,
            description="Description of the task"
        )    
    is_completed: bool = Field(..., description="Completion status of the task")


    @field_serializer("description",mode="plain")
    def serialize_description(self,v) -> str:
        return v[:15]


class TaskSchema(TaskBaseSchema):
    id: int = Field(..., description="ID of the task")
    created_date:datetime = Field(..., description="Creation date of the task")
    updated_date:datetime = Field(..., description="Last updated date of the task")
    

    

class TaskCreateSchema(TaskBaseSchema):
    pass