from pydantic import BaseModel

class PropertyBase(BaseModel):
    name: str
    address: str
    status: str
    curr_price: float

class PropertyInDB(PropertyBase):
    id: int