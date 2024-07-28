from fastapi import APIRouter,Response,HTTPException,status
from Products.routers.login import getCurrentUser
from sqlalchemy.orm import Session
from fastapi.params import Depends
from Products.database import get_db
from Products import Models
from typing import List
from Products import schemas

router = APIRouter(
    tags=['Products']
)

# Add a product
@router.post('/products',status_code=status.HTTP_201_CREATED)
def addProduct(requestData:schemas.Product, db:Session = Depends(get_db)):
    new_product = Models.Product(
        name= requestData.name,
        description= requestData.description,
        price= requestData.price,
        seller_id = 1
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    # return requestData
    return{
        "message":"product added successFully",
        "data":requestData
    }

#List all products
# @app.get('/products',response_model=List[schemas.responseModel]) ==> Response model importing from schemas Page
@router.get('/products')
def getAllProducts(db:Session = Depends(get_db),current_user:schemas.Seller = Depends(getCurrentUser)):
    all_products = db.query(Models.Product).all()
    # return all_products # used for showing response model
    return{
          "message":"Listed Successfully",
          "data":all_products
    }

#Filter individual products
@router.get('/products/{id}')
def getIndividualProducts(id,response:Response, db:Session = Depends(get_db)):
    products = db.query(Models.Product).filter(Models.Product.id == id).first()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return{
          "message":"Listed Successfully",
          "data":products
    }

#Delet products

@router.delete('/products/{id}')
def deleteProducts(id,db:Session = Depends(get_db)):
    db.query(Models.Product).filter(Models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return{
          "message":"Deleted Successfully",
    }

@router.put('/products/{id}')
def editProduct(id,requestData:schemas.Product, db:Session = Depends(get_db)):
    products = db.query(Models.Product).filter(Models.Product.id == id)
    if not products.first():
        pass

    products.update(requestData.dict())
    db.commit()

    return{
        "message":"product added successFully",
        "data":requestData
    }