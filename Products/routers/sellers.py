from fastapi import APIRouter,Response,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import Models
from typing import List
from ..import schemas
from passlib.context import CryptContext


router = APIRouter(
    tags=['Sellers']
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post('/seller')
def addSeller(payload:schemas.Seller,db:Session = Depends(get_db),status_code=status.HTTP_201_CREATED):
    try:
        hashedPassword = pwd_context.hash(payload.password)
        newSeller = Models.Sellers(
            username = payload.userName,
            email = payload.email,
            password = hashedPassword
        )
        db.add(newSeller)
        db.commit()
        db.refresh(newSeller)
        return {
            "message":"Created User",
            "data":newSeller
        }
    except Exception as e:
        print(str(e))