from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.user import User
from app.api.v1 import users, auth, products

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)

Base.metadata.create_all(bind=engine)
