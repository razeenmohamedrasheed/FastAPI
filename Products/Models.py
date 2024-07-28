from sqlalchemy import Column,Integer,String,ForeignKey
from Products.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer,ForeignKey('sellers.id'))
    sellers = relationship('Sellers',back_populates='products')


class Sellers(Base):
    __tablename__ = 'sellers'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship('Product',back_populates='sellers')