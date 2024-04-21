from fastapi import APIRouter, HTTPException
from typing import List
from threading import Lock
from .earthstayin_schemas import (
    EarthStayinPropertyInDB,
    EarthStayinPropertyBase,
    EarthStayinBathroom,
    EarthStayinBathroomFixtures,
    EarthStayinBedroom,
    EarthStayinBedType,
    EarthStayinAmenity,
    EarthStayinHouseRules, EarthStayinPropertyBaseUpdate,
)

data = {
    1: EarthStayinPropertyInDB(
        id=1,
        user_email="joedoe@gmail.com",
        name="Girassol",
        address="Rua 1235",
        curr_price=149.00,
        description="Tem muita luz natural e é muito confortável",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=2, bed_type=EarthStayinBedType.SINGLE_BED
                )
            ],
            "bedroom_2": [
                EarthStayinBedroom(number_beds=1, bed_type=EarthStayinBedType.QUEEN_BED)
            ],
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                ],
            ),
            EarthStayinBathroom(
                name="bathroom_lastfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.SHOWER,
                ],
            ),
        ],
        amenities=[
            EarthStayinAmenity.WIFI,
            EarthStayinAmenity.AC,
        ],
        accessibilities=["elevator", "ramp"],
        additional_info="Rebuçados grátis.",
        house_rules=EarthStayinHouseRules(
            checkin_time="15:00-23:59",
            checkout_time="00:00-11:00",
            smoking_allowed=False,
            rest_time="23:00",
            pets_allowed=False,
        ),
    ),
    2: EarthStayinPropertyInDB(
        id=2,
        user_email="alicez@gmail.com",
        name="Poente Azul",
        address="Rua 5678",
        curr_price=21.50,
        description="A casa mais azul do bairro, desde 1999",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(number_beds=2, bed_type=EarthStayinBedType.KING_BED),
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[
            EarthStayinAmenity.WIFI,
            EarthStayinAmenity.AC,
        ],
        accessibilities=[],
        additional_info="Um rebuçado por cada hóspede.",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:00-23:59",
            checkout_time="00:00-10:30",
            smoking_allowed=True,
            rest_time="22:00",
            pets_allowed=False,
        ),
    ),
    3: EarthStayinPropertyInDB(
        id=3,
        user_email="alicez@gmail.com",
        name="Conforto e Bem Estar",
        address="Rua 91011",
        curr_price=33.00,
        accessibilities=["ramp"],
        description="A residência mais confortável",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
            ],
            "bedroom_2": [
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
            ],
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Recebem um rebuçado",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:30-23:59",
            checkout_time="00:00-11:30",
            smoking_allowed=True,
            rest_time="22:30",
            pets_allowed=True,
        ),
    ),
    4: EarthStayinPropertyInDB(
        id=4,
        user_email="alicez@gmail.com",
        name="Flores e Amores",
        address="Rua 121314",
        curr_price=29.00,
        accessibilities=[],
        description="Tem um jardim bonito",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(number_beds=2, bed_type=EarthStayinBedType.KING_BED)
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_firstfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[
            EarthStayinAmenity.AC,
            EarthStayinAmenity.WIFI,
            EarthStayinAmenity.OPEN_PARKING,
        ],
        additional_info="Se cá aparecerem, recebem um rebuçado",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:45-23:59",
            checkout_time="00:00-11:15",
            smoking_allowed=False,
            rest_time="23:00",
            pets_allowed=False,
        ),
    ),
    5: EarthStayinPropertyInDB(
        id=5,
        user_email="alicez@gmail.com",
        name="São José Residences",
        address="Rua 151617",
        curr_price=53.00,
        accessibilities=["elevator"],
        description="",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=4, bed_type=EarthStayinBedType.SINGLE_BED
                )
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:30-23:59",
            checkout_time="00:00-11:30",
            smoking_allowed=True,
            rest_time="22:00",
            pets_allowed=False,
        ),
    ),
    6: EarthStayinPropertyInDB(
        id=6,
        user_email="alicez@gmail.com",
        name="Residencial Aveiro",
        address="Rua 181920",
        curr_price=132.00,
        accessibilities=["elevator", "ramp", "braille"],
        description="Nao é em Braga",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
            ],
            "bedroom_2": [
                EarthStayinBedroom(
                    number_beds=1, bed_type=EarthStayinBedType.SINGLE_BED
                ),
                EarthStayinBedroom(number_beds=1, bed_type=EarthStayinBedType.TWIN_BED),
            ],
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                    EarthStayinBathroomFixtures.BIDET,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Rebuçados.",
        house_rules=EarthStayinHouseRules(
            checkin_time="13:30-23:59",
            checkout_time="00:00-10:30",
            smoking_allowed=True,
            rest_time="22:00",
            pets_allowed=True,
        ),
    ),
    7: EarthStayinPropertyInDB(
        id=7,
        user_email="joedoe@gmail.com",
        name="Ponto8",
        address="Rua 212223",
        curr_price=38.00,
        accessibilities=[],
        description=".8",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(number_beds=2, bed_type=EarthStayinBedType.KING_BED)
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:30-23:59",
            checkout_time="00:00-11:00",
            smoking_allowed=True,
            rest_time="23:00",
            pets_allowed=True,
        ),
    ),
    8: EarthStayinPropertyInDB(
        id=8,
        user_email="joedoe@gmail.com",
        name="Bom Lugar",
        address="Rua 242526",
        curr_price=131.00,
        accessibilities=["elevator", "ramp"],
        description="O nome desta casa nao é nenhuma mentira",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=4, bed_type=EarthStayinBedType.SINGLE_BED
                )
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Se cá aparecerem, recebem um rebuçado",
        house_rules=EarthStayinHouseRules(
            checkin_time="15:00-23:59",
            checkout_time="00:00-11:30",
            smoking_allowed=False,
            rest_time="22:30",
            pets_allowed=False,
        ),
    ),
    9: EarthStayinPropertyInDB(
        id=9,
        user_email="joedoe@gmail.com",
        name="Hotel Miradouro",
        address="Rua 272829",
        curr_price=34.00,
        accessibilities=[],
        description="Tem uma excelente vista",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=4, bed_type=EarthStayinBedType.SINGLE_BED
                )
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Pode levar rebuçados para casa",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:30-23:59",
            checkout_time="00:00-11:00",
            smoking_allowed=False,
            rest_time="22:30",
            pets_allowed=False,
        ),
    ),
    10: EarthStayinPropertyInDB(
        id=10,
        user_email="joedoe@gmail.com",
        name="Spot Hostel",
        address="Rua 303132",
        curr_price=85.00,
        accessibilities=["elevator", "braille"],
        description="Provavelmente vais dormir num quarto com 10 pessoas",
        number_of_guests=4,
        square_meters=2000,
        bedrooms={
            "bedroom_1": [
                EarthStayinBedroom(
                    number_beds=4, bed_type=EarthStayinBedType.SINGLE_BED
                )
            ]
        },
        bathrooms=[
            EarthStayinBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    EarthStayinBathroomFixtures.TOILET,
                    EarthStayinBathroomFixtures.TUB,
                ],
            ),
        ],
        amenities=[EarthStayinAmenity.AC, EarthStayinAmenity.WIFI],
        additional_info="Olha os rebuçados!",
        house_rules=EarthStayinHouseRules(
            checkin_time="14:30-23:59",
            checkout_time="00:00-11:00",
            smoking_allowed=True,
            rest_time="23:30",
            pets_allowed=False,
        ),
    ),
}

lock = Lock()

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", status_code=200)
def get_properties_by_user(email: str) -> List[EarthStayinPropertyInDB]:
    return [property for property in data.values() if property.user_email == email]


@router.get("/{property_id}", status_code=200)
def get_property_by_id(property_id: int) -> EarthStayinPropertyInDB:
    return data[property_id]


@router.post("", status_code=201)
def create_property(property_data: EarthStayinPropertyBase) -> EarthStayinPropertyInDB:
    with lock:
        last_id = list(data.keys())[-1]
        id = last_id + 1
        property_in_db = EarthStayinPropertyInDB(
            user_email=property_data.user_email,
            name=property_data.name,
            address=property_data.address,
            curr_price=property_data.curr_price,
            description=property_data.description,
            number_of_guests=property_data.number_of_guests,
            square_meters=property_data.square_meters,
            bedrooms=property_data.bedrooms,
            bathrooms=property_data.bathrooms,
            amenities=property_data.amenities,
            accessibilities=property_data.accessibilities,
            additional_info=property_data.additional_info,
            house_rules=property_data.house_rules,
            id=id,
        )
        data[id] = property_in_db
    saved_property = data[id]
    return saved_property


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property_data: EarthStayinPropertyBaseUpdate) -> EarthStayinPropertyInDB:
    if not (property_to_update := data.get(property_id)):
        raise HTTPException(status_code=404, detail="Property doesn't exist")
    update_parameters = {field_name: field_value for field_name, field_value in property_data if field_value is not None}
    updated_property = property_to_update.model_copy(update=update_parameters)
    data[property_id] = updated_property
    return updated_property


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int) -> List[EarthStayinPropertyInDB]:
    del data[property_id]
    return data.values()
