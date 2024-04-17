from enum import Enum
from base_schemas.property import PropertyBase
from pydantic import BaseModel


class CNGAmenity(str, Enum):
    WIFI_FREE = "wifi_free"
    PARKING = "parking"
    AC = "AC"
    PATIO = "patio"

class CNGBedType(str, Enum):
    QUEEN = "queen"
    KING = "king"
    SINGLE = "single"
    TWIN = "twin"

class CNGBedroom(BaseModel):
    number_beds: int
    bed_type: CNGBedType

class CNGBathroomFixtures(str, Enum):
    TUB = "tub"
    SHOWER = "shower"
    TOILET = "toilet"

class CNGBathroom(BaseModel):
    bathroom_fixtures: list[CNGBathroomFixtures]

class CNGUser(BaseModel):
    name: str
    phone_number: str
    languages: list[str]

class CNGPropertyBase(PropertyBase):
    description: str
    guest_num: int
    house_area: int
    bedrooms: list[CNGBedroom]
    bathrooms: list[CNGBathroom]
    available_amenities: list[CNGAmenity]
    additional_info: str
    cancellation_policy: str
    house_manager: CNGUser

class CNGPropertyInDB(CNGPropertyBase):
    id: int
