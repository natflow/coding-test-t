import os

from fastapi import FastAPI
from mangum import Mangum

from .api import router


app = FastAPI(root_path=os.environ.get("FASTAPI_ROOT_PATH"))
app.include_router(router)

handler = Mangum(app, api_gateway_base_path=os.environ.get("MANGUM_BASE_PATH"))
