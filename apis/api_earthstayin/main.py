from fastapi import FastAPI

from api_earthstayin.v1 import properties, reservations

app = FastAPI()

app.include_router(properties.router)
app.include_router(reservations.router)