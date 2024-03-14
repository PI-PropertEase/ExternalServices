from pydantic import BaseModel
from typing import List, Union

class PropertyBase(BaseModel):
    name: str
    address: str
    status: str
    curr_price: float