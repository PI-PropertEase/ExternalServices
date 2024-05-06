from enum import Enum
from typing import Optional

from base_schemas.property import PropertyBase, PropertyBaseUpdate, ClosedTimeFrame
from pydantic import BaseModel


class EarthStayinAmenity(str, Enum):
    WIFI = "free_wifi"
    OPEN_PARKING = "car_parking"
    AC = "AC"


class EarthStayinBedType(str, Enum):
    QUEEN_BED = "queen_bed"
    KING_BED = "king_bed"
    SINGLE_BED = "single_bed"
    TWIN_BED = "twin_bed"


class EarthStayinBedroom(BaseModel):
    number_beds: int
    bed_type: EarthStayinBedType


class EarthStayinBathroomFixtures(str, Enum):
    TUB = "tub"
    SHOWER = "shower"
    TOILET = "toilet"
    BIDET = "bidet"


class EarthStayinBathroom(BaseModel):
    name: str
    bathroom_fixtures: list[EarthStayinBathroomFixtures]


class EarthStayinHouseRules(BaseModel):
    checkin_time: str
    checkout_time: str
    smoking_allowed: bool
    rest_time: str
    pets_allowed: bool


class EarthStayinPropertyBase(PropertyBase):
    description: str
    number_of_guests: int
    square_meters: int
    bedrooms: dict[str, list[EarthStayinBedroom]]
    bathrooms: list[EarthStayinBathroom]
    amenities: list[EarthStayinAmenity]
    accessibilities: list[str]
    additional_info: str
    house_rules: EarthStayinHouseRules


class EarthStayinPropertyBaseUpdate(PropertyBaseUpdate):
    description: Optional[str] = None
    number_of_guests: Optional[int] = None
    square_meters: Optional[int] = None
    bedrooms: Optional[dict[str, list[EarthStayinBedroom]]] = None
    bathrooms: Optional[list[EarthStayinBathroom]] = None
    amenities: Optional[list[EarthStayinAmenity]] = None
    accessibilities: Optional[list[str]] = None
    additional_info: Optional[str] = None
    house_rules: Optional[EarthStayinHouseRules] = None


class EarthStayinPropertyInDB(EarthStayinPropertyBase):
    id: int


class ClosedTimeFrameWithPropertyId(ClosedTimeFrame):
    property_id: int


class ClosedTimeFrameWithIdAndPropertyId(ClosedTimeFrame):
    id: int
    property_id: int


def convert_to_closedtimeframe_with_id_and_property_id(
        closed_time_frame_id: int,
        closed_time_frame_with_property_id: ClosedTimeFrameWithPropertyId,
) -> ClosedTimeFrameWithIdAndPropertyId:
    return ClosedTimeFrameWithIdAndPropertyId(
        id=closed_time_frame_id,
        property_id=closed_time_frame_with_property_id.property_id,
        begin_datetime=closed_time_frame_with_property_id.begin_datetime,
        end_datetime=closed_time_frame_with_property_id.end_datetime,
    )
