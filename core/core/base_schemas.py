from pydantic import BaseModel


class Base404ErrorSchema(BaseModel):
    detail: str = "Item not found"