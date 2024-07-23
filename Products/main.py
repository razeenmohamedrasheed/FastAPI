from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .import schemas
from .import Models
from .database import engine, SessionLocal

app = FastAPI()

# Used to create model at BE
Models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/products')
def addProduct(requestData:schemas.Product, db:Session = Depends(get_db)):
    new_product = Models.product(
        name= requestData.name,
        description= requestData.description,
        price= requestData.price,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return{
        "message":"product added successFully",
        "data":requestData
    }

@app.get('/products')
def getAllProducts(db:Session = Depends(get_db)):
    all_products = db.query(Models.product).all()
    return{
          "message":"Listed Successfully",
          "data":all_products
    }

@app.get('/products/{id}')
def getAllProducts(id,db:Session = Depends(get_db)):
    products = db.query(Models.product).filter(Models.product.id == id).first()
    return{
          "message":"Listed Successfully",
          "data":products
    }