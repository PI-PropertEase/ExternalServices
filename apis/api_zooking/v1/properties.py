from fastapi import APIRouter, HTTPException
from typing import List
from base_schemas.property import PropertyBase, PropertyInDB, ClosedTimeFrame
from .zooking_schemas import (
    ZookingPropertyInDB,
    ZookingBedroom,
    ZookingBedType,
    ZookingBathroom,
    ZookingBathroomFixtures,
    ZookingAmenity,
    ZookingPropertyBase,
    ZookingPropertyBaseUpdate,
)
from threading import Lock
from collections import defaultdict

data = {
    1: ZookingPropertyInDB(
        id=1,
        user_email="joedoe@gmail.com",
        name="Girassol",
        address="Rua 1234",
        location="Aveiro",
        curr_price=140.00,
        description="Tem muito sol",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=2, bed_type=ZookingBedType.SINGLE_BED),
            ],
            "bedroom_2": [
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.QUEEN_BED),
            ],
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[ZookingBathroomFixtures.TOILET],
            ),
            ZookingBathroom(
                name="bathroom_topfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.SHOWER,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    2: ZookingPropertyInDB(
        id=2,
        user_email="alicez@gmail.com",
        name="Poente Azul",
        address="Rua 5678",
        location="Coimbra",
        curr_price=24.00,
        description="A casa mais azul desde 1999",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=2, bed_type=ZookingBedType.KING_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    3: ZookingPropertyInDB(
        id=3,
        user_email="alicez@gmail.com",
        name="Conforto e Bem Estar",
        address="Rua 91011",
        location="Coimbra",
        curr_price=36.00,
        description="A residencia mais confortável",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
            ],
            "bedroom_2": [
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
            ],
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    4: ZookingPropertyInDB(
        id=4,
        user_email="alicez@gmail.com",
        name="Flores e Amores",
        address="Rua 121314",
        location="Lisboa",
        curr_price=24.00,
        description="Tem um jardim fixe",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=2, bed_type=ZookingBedType.KING_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    5: ZookingPropertyInDB(
        id=5,
        user_email="alicez@gmail.com",
        name="São José Residences",
        address="Rua 151617",
        location="Albufeira",
        curr_price=54.00,
        description="Yes",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=4, bed_type=ZookingBedType.SINGLE_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    6: ZookingPropertyInDB(
        id=6,
        user_email="alicez@gmail.com",
        name="Residencial Aveiro",
        address="Rua 181920",
        location="Porto",
        curr_price=133.00,
        description="Nao é em braga",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
            ],
            "bedroom_2": [
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
                ZookingBedroom(number_beds=1, bed_type=ZookingBedType.SINGLE_BED),
            ],
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    7: ZookingPropertyInDB(
        id=7,
        user_email="joedoe@gmail.com",
        name="Ponto8",
        address="Rua 212223",
        location="Vila do Conde",
        curr_price=32.00,
        description=".8",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=2, bed_type=ZookingBedType.KING_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    8: ZookingPropertyInDB(
        id=8,
        user_email="joedoe@gmail.com",
        name="Bom Lugar",
        address="Rua 242526",
        location="Évora",
        curr_price=130.00,
        description="O nome desta casa nao é mentira",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=4, bed_type=ZookingBedType.SINGLE_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    9: ZookingPropertyInDB(
        id=9,
        user_email="joedoe@gmail.com",
        name="Hotel Miradouro",
        address="Rua 272829",
        location="Braga",
        curr_price=30.00,
        description="Tem uma boa view",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=4, bed_type=ZookingBedType.SINGLE_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
    10: ZookingPropertyInDB(
        id=10,
        user_email="joedoe@gmail.com",
        name="Spot Hostel",
        address="Rua 303132",
        location="Covilhã",
        curr_price=90.00,
        description="Sim, vais dormir num quarto com 10 pessoas",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                ZookingBedroom(number_beds=4, bed_type=ZookingBedType.SINGLE_BED)
            ]
        },
        bathrooms=[
            ZookingBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    ZookingBathroomFixtures.TOILET,
                    ZookingBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[ZookingAmenity.AC, ZookingAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
    ),
}

lock = Lock()
closed_time_frame_sequence_id_lock = Lock()
closed_time_frame_sequence_id = 1
router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", status_code=200)
def get_properties_by_user(email: str) -> List[ZookingPropertyInDB]:
    return [property for property in data.values() if property.user_email == email]


@router.get("/{property_id}", status_code=200)
def get_property_by_id(property_id: int) -> ZookingPropertyInDB:
    if not data.get(property_id):
        raise HTTPException(status_code=404, detail="Property doesn't exist")
    return data[property_id]


@router.post("", status_code=201)
def create_property(property_data: ZookingPropertyBase) -> ZookingPropertyInDB:
    with lock:
        last_id = list(data.keys())[-1]
        id = last_id + 1
        property_in_db = ZookingPropertyInDB(
            user_email=property_data.user_email,
            name=property_data.name,
            address=property_data.address,
            location=property_data.location,
            curr_price=property_data.curr_price,
            description=property_data.description,
            number_of_guests=property_data.number_of_guests,
            square_meters=property_data.square_meters,
            bedrooms=property_data.bedrooms,
            bathrooms=property_data.bathrooms,
            amenities=property_data.amenities,
            additional_info=property_data.additional_info,
            id=id,
        )
        data[id] = property_in_db
    saved_property = data[id]
    return saved_property


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property_data: ZookingPropertyBaseUpdate) -> ZookingPropertyInDB:
    if not (property_to_update := data.get(property_id)):
        raise HTTPException(status_code=404, detail="Property doesn't exist")
    update_parameters = {field_name: field_value for field_name, field_value in property_data if field_value is not None}
    if (request_closed_time_frames := update_parameters.get("closed_time_frames")) is not None:
        update_closed_time_frames = property_to_update.closed_time_frames
        print("BEFORE: update_parameters", update_parameters)
        print("BEFORE: request_closed_time_frames", request_closed_time_frames)
        print("BEFORE: update_closed_time_frames", update_closed_time_frames)

        for closed_time_frame in request_closed_time_frames:
            if closed_time_frame.id is None:
                # insert new event with a new id
                global closed_time_frame_sequence_id
                with closed_time_frame_sequence_id_lock:
                    update_closed_time_frames[closed_time_frame_sequence_id] = ClosedTimeFrame(**closed_time_frame.model_dump())
                    closed_time_frame_sequence_id += 1
            else:
                # update existing event if key is valid (already exists)
                if closed_time_frame.id not in update_closed_time_frames:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Closed time frame with id {closed_time_frame.id} for property id {property_id} doesn't exist"
                    )
                print("closed_time_frame", closed_time_frame)
                if closed_time_frame.begin_datetime is None and closed_time_frame.end_datetime is None:
                    update_closed_time_frames.pop(closed_time_frame.id)
                else:
                    update_closed_time_frames[closed_time_frame.id] = closed_time_frame

        update_parameters["closed_time_frames"] = update_closed_time_frames
        print("AFTER: update_closed_time_frames", update_closed_time_frames)

    updated_property = property_to_update.model_copy(update=update_parameters)
    data[property_id] = updated_property
    return updated_property


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int) -> List[ZookingPropertyInDB]:
    if not data.get(property_id):
        raise HTTPException(status_code=404, detail="Property doesn't exist")
    del data[property_id]
    return data.values()
