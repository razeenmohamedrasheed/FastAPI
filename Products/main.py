from fastapi import FastAPI
from .database import engine
from .import Models
from .routers import product,sellers

# import bcrypt

app = FastAPI(
    title="Products API",
    description="API Notes",
    terms_of_service="https://docs.google.com/",
    contact={
        "devolped by":"Razeen Mohamed Rasheed",
        "Websit":"test",
        "email":"razeenrasheed83@gmail.com"
    }
)

app.include_router(product.router)
app.include_router(sellers.router)

# Used to create model at BE
Models.Base.metadata.create_all(engine)

