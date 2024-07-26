from fastapi import APIRouter,HTTPException,status
from ..import schemas,Models
from ..database import get_db
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Login']
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post('/login')
def createUser(payload:schemas.Login,db: Session = Depends(get_db)):
    user = db.query(Models.Sellers).filter(Models.Sellers.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    if not pwd_context.verify(payload.password,user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")
    return payload
