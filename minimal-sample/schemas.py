from pydantic import BaseModel , field_validator , Field , field_serializer


class BasePersonSchema(BaseModel):
    name : str = Field(..., max_length=50,description='test description' ,min_length=2,examples=["Alice","Bob","Charlie"])

    @field_validator('name')
    def name_validator(cls, name:str):
        if len(name) < 2 or len(name) > 50:
            raise ValueError('Name must be between 2 and 50 characters long')
        if not name.isalpha():
            raise ValueError('Name must contain only alphabetic characters')
        return name
    
    @field_serializer('name')
    def name_serializer(self, name:str):
        return name.title()




class PersonResponseSchema(BasePersonSchema):
    id : int

class PersonCreateSchema(BasePersonSchema):
    pass

class PersonUpdateSchema(BasePersonSchema):
    pass
