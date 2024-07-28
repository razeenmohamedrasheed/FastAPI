from fastapi import APIRouter,HTTPException,status
from Products import schemas,Models
from Products.database import get_db
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Login']
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "fJ5z1iUGQCi2gL0tSQhCwBwlC0uOJBN023Bwy8Z6Y79fkFSGoEveCsXP3UNJP0yXjsWmxNGwy42mzKAU8Anidz6ZfLpPBwn0o6WK"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

# TOKEN GENERATION LOGIC
def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_JWT = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_JWT

@router.post('/login')
def userLogin(payload:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    user = db.query(Models.Sellers).filter(Models.Sellers.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    if not pwd_context.verify(payload.password,user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")
    access_token = generate_token(data={"sub":user.username})
    return{
        "accesstoken":access_token,
        "tokentype":"bearer"
    }
    
def getCurrentUser(token:str = Depends(OAuth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={'WWW-Authenticate':'Bearer'}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
