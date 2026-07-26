from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database.database import engine, Base
from app.models.user import User
from app.api.v1 import users, auth, products
from app.exceptions import EmailAlreadyExistsException

app = FastAPI()

@app.exception_handler(EmailAlreadyExistsException)
async def email_already_exists_exception_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)

Base.metadata.create_all(bind=engine)
