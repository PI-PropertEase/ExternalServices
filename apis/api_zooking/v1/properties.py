from fastapi import APIRouter
from typing import Dict
from base_schemas.property import PropertyBase, PropertyInDB
from threading import Lock

data = {
    1: PropertyBase(name="Girassol", address="Rua 1234", status="Free", curr_price=140.00),
    2: PropertyBase(name="Poente Azul", address="Rua 5678", status="Free", curr_price=24.00),
    3: PropertyBase(name="Conforto e Bem Estar", address="Rua 91011", status="Free", curr_price=36.00),
    4: PropertyBase(name="Flores e Amores", address="Rua 121314", status="Occupied", curr_price=24.00),
    5: PropertyBase(name="São José Residences", address="Rua 151617", status="Free", curr_price=54.00),
    6: PropertyBase(name="Residencial Aveiro", address="Rua 181920", status="Maintenance", curr_price=133.00),
    7: PropertyBase(name="Ponto8", address="Rua 212223", status="Free", curr_price=32.00),
    8: PropertyBase(name="Bom Lugar", address="Rua 242526", status="Cleaning", curr_price=130.00),
    9: PropertyBase(name="Hotel Miradouro", address="Rua 272829", status="Occupied", curr_price=30.00),
    10: PropertyBase(name="Spot Hostel", address="Rua 303132", status="Occupied", curr_price=90.00)
}

lock = Lock()

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)


@router.get("/", status_code=200)
def get_properties_list() -> Dict[int, PropertyBase]:
    return data


@router.get("/{property_id}", status_code=200)
def get_property_by_id(property_id: int) -> PropertyBase:
    return data[property_id]  


@router.post("/", status_code=201)
def create_property(property: PropertyBase) -> PropertyInDB:
    with lock:
        id = len(data)+1
        data[id] = property
    property_data = data[id]
    property_in_db = PropertyInDB(
        name=property_data.name,
        address=property_data.address,
        status=property_data.status,
        curr_price=property_data.curr_price,
        id=id
    )
    return property_in_db


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property: PropertyBase) -> PropertyInDB:
    data[property_id] = property
    property_data = data[property_id]
    property_in_db = PropertyInDB(
        name=property_data.name,
        address=property_data.address,
        status=property_data.status,
        curr_price=property_data.curr_price,
        id=property_id
    )
    return property_in_db


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int) -> Dict[int, PropertyBase]:
    del data[property_id]
    return data