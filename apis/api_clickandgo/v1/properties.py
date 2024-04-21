from fastapi import APIRouter, HTTPException
from typing import List
from .clickandgo_schemas import (
    CNGPropertyBase,
    CNGPropertyInDB,
    CNGBedroom,
    CNGBedType,
    CNGBathroom,
    CNGBathroomFixtures,
    CNGAmenity,
    CNGUser,
    CNGHouseRules, CNGPropertyBaseUpdate,
)
from threading import Lock

data = {
    1: CNGPropertyInDB(
        id=1,
        user_email="joedoe@gmail.com",
        name="Girassol",
        address="Rua 1234",
        curr_price=143.00,
        description="Cool house",
        guest_num=3,
        house_area=500,
        bedrooms={
            "bedroom_1": [
                CNGBedroom(number_beds=2, bed_type=CNGBedType.SINGLE),
            ],
            "bedroom_2": [
                CNGBedroom(number_beds=1, bed_type=CNGBedType.QUEEN),
            ],
        },
        bathrooms=[
            CNGBathroom(
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.SHOWER,
                ],
            )
        ],
        available_amenities=[CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Joe Doe",
            phone_number="+351910910910",
            languages=["Portuguese", "English", "Spanish", "Italian"],
        ),
    ),
    2: CNGPropertyInDB(
        id=2,
        user_email="alicez@gmail.com",
        name="Poente Azul",
        address="Rua 5678",
        curr_price=22.00,
        description="Interesting house",
        guest_num=5,
        house_area=200,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=2, bed_type=CNGBedType.KING)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.AC, CNGAmenity.PATIO, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Alice Zqt",
            phone_number="+351920920920",
            languages=["Portuguese", "English"],
        ),
    ),
    3: CNGPropertyInDB(
        id=3,
        user_email="alicez@gmail.com",
        name="Conforto e Bem Estar",
        address="Rua 91011",
        curr_price=38.00,
        description="Don't visit at 3am",
        guest_num=4,
        house_area=350,
        bedrooms={
            "bedroom_1": [
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
            ],
            "bedroom_2": [
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
            ],
        },
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Alice Zqt",
            phone_number="+351920920920",
            languages=["Portuguese", "English"],
        ),
    ),
    4: CNGPropertyInDB(
        id=4,
        user_email="alicez@gmail.com",
        name="Flores e Amores",
        address="Rua 121314",
        curr_price=30.00,
        description="Amores e flores",
        guest_num=4,
        house_area=420,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=2, bed_type=CNGBedType.KING)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Alice Zqt",
            phone_number="+351920920920",
            languages=["Portuguese", "English"],
        ),
    ),
    5: CNGPropertyInDB(
        id=5,
        user_email="alicez@gmail.com",
        name="São José Residences",
        address="Rua 151617",
        curr_price=59.00,
        description="A lenda reza que o são josé abre as portas da casa de banho durante a noite",
        guest_num=4,
        house_area=212,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=4, bed_type=CNGBedType.SINGLE)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Alice Zqt",
            phone_number="+351920920920",
            languages=["Portuguese", "English"],
        ),
    ),
    6: CNGPropertyInDB(
        id=6,
        user_email="alicez@gmail.com",
        name="Residencial Aveiro",
        address="Rua 181920",
        curr_price=131.00,
        description="Espaçoso",
        guest_num=4,
        house_area=551,
        bedrooms={
            "bedroom_1": [
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
            ],
            "bedroom_2": [
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
                CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE),
            ],
        },
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Alice Zqt",
            phone_number="+351920920920",
            languages=["Portuguese", "English"],
        ),
    ),
    7: CNGPropertyInDB(
        id=7,
        user_email="joedoe@gmail.com",
        name="Ponto8",
        address="Rua 212223",
        curr_price=32.44,
        description="Baratíssimo e alta qualidade",
        guest_num=5,
        house_area=712,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=2, bed_type=CNGBedType.KING)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Joe Doe",
            phone_number="+351910910910",
            languages=["Portuguese", "English", "Spanish", "Italian"],
        ),
    ),
    8: CNGPropertyInDB(
        id=8,
        user_email="joedoe@gmail.com",
        name="Bom Lugar",
        address="Rua 242526",
        curr_price=137.00,
        description="Venham visitar, somos fixes",
        guest_num=4,
        house_area=123,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=4, bed_type=CNGBedType.SINGLE)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Joe Doe",
            phone_number="+351910910910",
            languages=["Portuguese", "English", "Spanish", "Italian"],
        ),
    ),
    9: CNGPropertyInDB(
        id=9,
        user_email="joedoe@gmail.com",
        name="Hotel Miradouro",
        address="Rua 272829",
        curr_price=33.00,
        description="Olá",
        guest_num=5,
        house_area=512,
        bedrooms={"bedroom_1": [CNGBedroom(number_beds=4, bed_type=CNGBedType.SINGLE)]},
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Joe Doe",
            phone_number="+351910910910",
            languages=["Portuguese", "English", "Spanish", "Italian"],
        ),
    ),
    10: CNGPropertyInDB(
        id=10,
        user_email="joedoe@gmail.com",
        name="Spot Hostel",
        address="Rua 303132",
        curr_price=91.00,
        description="Nao sei o que escrever aqui",
        guest_num=3,
        house_area=432,
        bedrooms={
            "bedroom_1": [CNGBedroom(number_beds=2, bed_type=CNGBedType.TWIN)],
            "bedroom_2": [CNGBedroom(number_beds=1, bed_type=CNGBedType.SINGLE)],
        },
        bathrooms=[
            CNGBathroom(
                name="bathroom_groundfloor",
                bathroom_fixtures=[
                    CNGBathroomFixtures.TOILET,
                    CNGBathroomFixtures.TUB,
                ],
            ),
        ],
        available_amenities=[CNGAmenity.PARKING, CNGAmenity.AC, CNGAmenity.WIFI_FREE],
        house_rules=CNGHouseRules(
            check_in="16:00-23:59",
            check_out="00:00-10:00",
            smoking_allowed=False,
            parties_allowed=True,
            rest_time="22:00-08:00",
            pets_allowed=True,
        ),
        additional_info="Somos fixes",
        cancellation_policy="Não há reembolsos",
        house_manager=CNGUser(
            name="Joe Doe",
            phone_number="+351910910910",
            languages=["Portuguese", "English", "Spanish", "Italian"],
        ),
    ),
}

lock = Lock()

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", status_code=200)
def get_properties_by_user(email: str) -> List[CNGPropertyInDB]:
    return [property for property in data.values() if property.user_email == email]


@router.get("/{property_id}", status_code=200)
def get_property_by_id(property_id: int) -> CNGPropertyInDB:
    return data[property_id]


@router.post("", status_code=201)
def create_property(property_data: CNGPropertyBase) -> CNGPropertyInDB:
    with lock:
        last_id = list(data.keys())[-1]
        id = last_id + 1
        property_in_db = CNGPropertyInDB(
            user_email=property_data.user_email,
            name=property_data.name,
            address=property_data.address,
            curr_price=property_data.curr_price,
            description=property_data.description,
            guest_num=property_data.guest_num,
            house_area=property_data.house_area,
            bedrooms=property_data.bedrooms,
            bathrooms=property_data.bathrooms,
            available_amenities=property_data.available_amenities,
            house_rules=property_data.house_rules,
            additional_info=property_data.additional_info,
            cancellation_policy=property_data.cancellation_policy,
            house_manager=property_data.house_manager,
            id=id,
        )
        data[id] = property_in_db
    saved_property = data[id]
    return saved_property


@router.put("/{property_id}", status_code=200)
def update_property(property_id: int, property_data: CNGPropertyBaseUpdate) -> CNGPropertyInDB:
    if not (property_to_update := data.get(property_id)):
        raise HTTPException(status_code=404, detail="Property doesn't exist")
    update_parameters = {field_name: field_value for field_name, field_value in property_data if field_value is not None}
    updated_property = property_to_update.model_copy(update=update_parameters)
    data[property_id] = updated_property
    return updated_property


@router.delete("/{property_id}", status_code=200)
def delete_property(property_id: int) -> List[CNGPropertyInDB]:
    del data[property_id]
    return data.values()
