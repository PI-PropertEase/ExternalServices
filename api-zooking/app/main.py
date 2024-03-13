from fastapi import FastAPI

from .api.v1 import properties

app = FastAPI()

app.include_router(properties.router)
