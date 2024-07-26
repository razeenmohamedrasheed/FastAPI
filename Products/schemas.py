from pydantic import BaseModel

class Product(BaseModel):
    name:str
    description:str
    price:int

class DisplaySeller(BaseModel):
    username:str
    email:str
    class Config:
        orm_mode = True

# Response Model
class DisplayProduct(BaseModel):
    name:str
    description:str
    seller:DisplaySeller
    class Config:
        orm_mode = True


class Seller(BaseModel):
    userName:str
    email:str
    password:str

class Login(BaseModel):
    username:str
    password:str