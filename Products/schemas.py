from pydantic import BaseModel

class Product(BaseModel):
    name:str
    description:str
    price:int

# Response Model
class responseModel(BaseModel):
    name:str
    description:str
    class Config:
        orm_mode = True