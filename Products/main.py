from fastapi import FastAPI,status,Response,HTTPException
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
@app.post('/products',status_code=status.HTTP_201_CREATED)
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
# @app.get('/products',response_model=List[schemas.responseModel]) ==> Response model importing from schemas Page
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
def getIndividualProducts(id,response:Response, db:Session = Depends(get_db)):
    products = db.query(Models.product).filter(Models.product.id == id).first()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
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