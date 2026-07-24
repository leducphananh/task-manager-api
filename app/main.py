from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.user import User
from app.api.v1 import user

app = FastAPI()

app.include_router(user.router)

Base.metadata.create_all(bind=engine)
