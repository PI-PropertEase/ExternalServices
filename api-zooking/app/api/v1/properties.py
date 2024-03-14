from fastapi import APIRouter
from typing import Dict
from app.schemas.property import PropertyBase

data = {
    1: {"name": "AL1", "address": "Rua 1234", "status": "Free", "curr_price": 340.00},
    2: {"name": "AL2", "address": "Rua 5678", "status": "Free", "curr_price": 140.00},
    3: {"name": "AL3", "address": "Rua 91011", "status": "Free", "curr_price": 360.00},
    4: {"name": "AL4", "address": "Rua 121314", "status": "Occupied", "curr_price": 240.00},
    5: {"name": "AL5", "address": "Rua 151617", "status": "Free", "curr_price": 540.00},
    6: {"name": "AL6", "address": "Rua 181920", "status": "Maintenance", "curr_price": 330.00},
    7: {"name": "AL7", "address": "Rua 212223", "status": "Free", "curr_price": 320.00},
    8: {"name": "AL8", "address": "Rua 242526", "status": "Cleaning", "curr_price": 34.00},
    9: {"name": "AL9", "address": "Rua 272829", "status": "Occupied", "curr_price": 30.00},
    10: {"name": "AL10", "address": "Rua 303132", "status": "Occupied", "curr_price": 140.00}
}

router = APIRouter(
    prefix="/properties",
    tags=["properties"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200)
def get_properties_list() -> Dict[int, PropertyBase]:
    return data


@router.get("/{property_id}", status_code=200)
def get_propery_by_id(property_id: int) -> PropertyBase:
    return data[property_id]  


@router.post("/", status_code=201)
def create_property(property: PropertyBase) -> PropertyBase:
    data[len(data)+1] = property
    return property


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property: PropertyBase) -> PropertyBase:
    data[property_id] = property
    return property