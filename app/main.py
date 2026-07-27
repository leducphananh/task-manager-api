from fastapi import APIRouter, FastAPI, Request
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

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
app.include_router(api_router)

Base.metadata.create_all(bind=engine)
