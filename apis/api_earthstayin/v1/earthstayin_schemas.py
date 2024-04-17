from enum import Enum
from base_schemas.property import PropertyBase
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

class EarthStayinPropertyBase(PropertyBase):
    description: str
    number_of_guests: int
    square_meters: int
    bedrooms: list[EarthStayinBedroom]
    bathrooms: list[EarthStayinBathroom]
    amenities: list[EarthStayinAmenity]
    accessibilities: list[str]
    additional_info: str

class EarthStayinPropertyInDB(EarthStayinPropertyBase):
    id: int
