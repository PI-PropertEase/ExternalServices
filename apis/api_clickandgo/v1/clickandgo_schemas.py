from enum import Enum
from typing import Optional

from base_schemas.property import PropertyBase, PropertyBaseUpdate, ClosedTimeFrame
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
    name: str
    bathroom_fixtures: list[CNGBathroomFixtures]


class CNGUser(BaseModel):
    name: str
    phone_number: str
    languages: list[str]


class CNGHouseRules(BaseModel):
    check_in: str  # string in format "00:00-10:00" (2 hours separated by hifen)
    check_out: str
    smoking_allowed: bool
    parties_allowed: bool
    rest_time: str
    pets_allowed: bool


class CNGPropertyBase(PropertyBase):
    town: str
    description: str
    guest_num: int
    house_area: int
    bedrooms: dict[str, list[CNGBedroom]]
    bathrooms: list[CNGBathroom]
    available_amenities: list[CNGAmenity]
    house_rules: CNGHouseRules
    additional_info: str
    cancellation_policy: str
    house_managers: list[CNGUser]


class CNGPropertyBaseUpdate(PropertyBaseUpdate):
    town: Optional[str] = None
    description: Optional[str] = None
    guest_num: Optional[int] = None
    house_area: Optional[int] = None
    bedrooms: Optional[dict[str, list[CNGBedroom]]] = None
    bathrooms: Optional[list[CNGBathroom]] = None
    available_amenities: Optional[list[CNGAmenity]] = None
    house_rules: Optional[CNGHouseRules] = None
    additional_info: Optional[str] = None
    cancellation_policy: Optional[str] = None
    house_managers: Optional[list[CNGUser]] = None


class CNGPropertyInDB(CNGPropertyBase):
    id: int
    closed_time_frames: dict[int, ClosedTimeFrame] = {}

