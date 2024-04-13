from fastapi import APIRouter
from typing import List
from base_schemas.property import PropertyBase, PropertyInDB
from threading import Lock

data = {
    1: PropertyInDB(id=1, user_email="joedoe@gmail.com", name="Girassol", address="Rua 1234", curr_price=140.00),
    2: PropertyInDB(id=2, user_email="alicez@gmail.com", name="Poente Azul", address="Rua 5678", curr_price=24.00),
    3: PropertyInDB(id=3, user_email="alicez@gmail.com", name="Conforto e Bem Estar", address="Rua 91011", curr_price=36.00),
    4: PropertyInDB(id=4, user_email="alicez@gmail.com", name="Flores e Amores", address="Rua 121314", curr_price=24.00),
    5: PropertyInDB(id=5, user_email="alicez@gmail.com",name="São José Residences", address="Rua 151617", curr_price=54.00),
    6: PropertyInDB(id=6, user_email="alicez@gmail.com", name="Residencial Aveiro", address="Rua 181920", curr_price=133.00),
    7: PropertyInDB(id=7, user_email="joedoe@gmail.com", name="Ponto8", address="Rua 212223", curr_price=32.00),
    8: PropertyInDB(id=8, user_email="joedoe@gmail.com", name="Bom Lugar", address="Rua 242526", curr_price=130.00),
    9: PropertyInDB(id=9, user_email="joedoe@gmail.com", name="Hotel Miradouro", address="Rua 272829", curr_price=30.00),
    10: PropertyInDB(id=10, user_email="joedoe@gmail.com", name="Spot Hostel", address="Rua 303132", curr_price=90.00)
}

lock = Lock()

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)


@router.get("", status_code=200)
def get_properties_by_user(email: str) -> List[PropertyInDB]:
    return [property for property in data.values() if property.user_email == email]


@router.get("/{property_id}", status_code=200)
def get_property_by_id(property_id: int) -> PropertyInDB:
    return data[property_id]  


@router.post("", status_code=201)
def create_property(property_data: PropertyBase) -> PropertyInDB:
    with lock:
        last_id = list(data.keys())[-1]
        id = last_id + 1
        property_in_db = PropertyInDB(
            user_email=property_data.user_email,
            name=property_data.name,
            address=property_data.address,
            curr_price=property_data.curr_price,
            id=id
        )
        data[id] = property_in_db
    saved_property = data[id]
    return saved_property


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property_data: PropertyBase) -> PropertyInDB:
    updated_property = PropertyInDB(
        user_email=property_data.user_email,
        name=property_data.name,
        address=property_data.address,
        curr_price=property_data.curr_price,
        id=property_id
    )
    data[property_id] = updated_property
    saved_property = data[property_id]
    return saved_property


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int) -> List[PropertyInDB]:
    del data[property_id]
    return data.values()