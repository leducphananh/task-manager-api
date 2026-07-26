from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import auth, products, users
from app.database.database import Base, engine
from app.exceptions import AppException

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)

Base.metadata.create_all(bind=engine)
