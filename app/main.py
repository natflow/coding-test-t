import logging

from fastapi import FastAPI
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from starlette.exceptions import HTTPException

from .api import router


app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return "it works"

handler = Mangum(app)

logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_exception_logger(request, exc):
    logger.warning(f"http error: {exc} ", exc_info=exc)
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_logger(request, exc):
    logger.info("request validation error", exc_info=exc)
    return await request_validation_exception_handler(request, exc)
