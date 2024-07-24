from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .import schemas
from .import Models
from .database import engine, SessionLocal
from typing import List

app = FastAPI()

# Used to create model at BE
Models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add a product
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
#List all products
# @app.get('/products',response_model=List[schemas.responseModel])
@app.get('/products')
def getAllProducts(db:Session = Depends(get_db)):
    all_products = db.query(Models.product).all()
    # return all_products # used for showing response model
    return{
          "message":"Listed Successfully",
          "data":all_products
    }

#Filter individual products
@app.get('/products/{id}')
def getIndividualProducts(id,db:Session = Depends(get_db)):
    products = db.query(Models.product).filter(Models.product.id == id).first()
    return{
          "message":"Listed Successfully",
          "data":products
    }

#Delet products

@app.delete('/products/{id}')
def deleteProducts(id,db:Session = Depends(get_db)):
    db.query(Models.product).filter(Models.product.id == id).delete(synchronize_session=False)
    db.commit()
    return{
          "message":"Deleted Successfully",
    }

@app.put('/products/{id}')
def editProduct(id,requestData:schemas.Product, db:Session = Depends(get_db)):
    products = db.query(Models.product).filter(Models.product.id == id)
    if not products.first():
        pass

    products.update(requestData.dict())
    db.commit()

    return{
        "message":"product added successFully",
        "data":requestData
    }