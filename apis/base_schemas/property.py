from typing import Optional

from pydantic import BaseModel


class PropertyBase(BaseModel):
    user_email: str
    name: str
    address: str
    curr_price: float


class PropertyBaseUpdate(BaseModel):
    user_email: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    curr_price: Optional[float] = None


class PropertyInDB(PropertyBase):
    id: int
