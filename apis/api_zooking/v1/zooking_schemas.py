from enum import Enum
from typing import Optional
from base_schemas.property import PropertyBase, PropertyBaseUpdate, ClosedTimeFrame
from pydantic import BaseModel


class ZookingAmenity(str, Enum):
    WIFI = "wifi"
    OPEN_PARKING = "open_parking"
    AC = "AC"


class ZookingBedType(str, Enum):
    QUEEN_BED = "queen_bed"
    KING_BED = "king_bed"
    SINGLE_BED = "single_bed"


class ZookingBedroom(BaseModel):
    number_beds: int
    bed_type: ZookingBedType


class ZookingBathroomFixtures(str, Enum):
    TUB = "tub"
    SHOWER = "shower"
    TOILET = "toilet"


class ZookingBathroom(BaseModel):
    name: str
    bathroom_fixtures: list[ZookingBathroomFixtures]


class ZookingPropertyBase(PropertyBase):
    description: str
    number_of_guests: int
    square_meters: int
    bedrooms: dict[str, list[ZookingBedroom]]
    bathrooms: list[ZookingBathroom]
    amenities: list[ZookingAmenity]
    additional_info: str


class ZookingPropertyBaseUpdate(PropertyBaseUpdate):
    description: Optional[str] = None
    number_of_guests: Optional[int] = None
    square_meters: Optional[int] = None
    bedrooms: Optional[dict[str, list[ZookingBedroom]]] = None
    bathrooms: Optional[list[ZookingBathroom]] = None
    amenities: Optional[list[ZookingAmenity]] = None
    additional_info: Optional[str] = None


class ZookingPropertyInDB(ZookingPropertyBase):
    id: int
    closed_time_frames: dict[int, ClosedTimeFrame] = {}
