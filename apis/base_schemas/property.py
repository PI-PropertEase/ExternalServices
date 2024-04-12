from pydantic import BaseModel

class PropertyBase(BaseModel):
    user_email: str
    name: str
    address: str
    curr_price: float

class PropertyInDB(PropertyBase):
    id: int