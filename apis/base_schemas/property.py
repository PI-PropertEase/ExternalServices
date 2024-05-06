from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator


class ClosedTimeFrame(BaseModel):
    begin_datetime: datetime
    end_datetime: datetime

    @model_validator(mode="after")
    def validate(self):
        if self.begin_datetime < datetime.now():
            raise ValueError("begin_datetime cannot be in the past")
        if self.begin_datetime >= self.end_datetime:
            raise ValueError("begin_datetime cannot be greater or equal to end_datetime")
        return self


class ClosedTimeFrameUpdate(ClosedTimeFrame):
    id: Optional[int] = None
    begin_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    @model_validator(mode="after")
    def validate(self):
        """
        Allow only these combinations:
          - id
          - id, begin_datetime, end_datetime
          - begin_datetime, end_datetime
        """

        print("running validator")
        if self.id is not None:
            datetime_nones_size = len([mydatetime for mydatetime in [self.begin_datetime, self.end_datetime] if mydatetime is None])

            if datetime_nones_size != 2:
                if datetime_nones_size != 0:
                    raise ValueError("When id is not none, begin_datetime and end_datetime must both be None "
                                     "or both not None")
            else:
                return self
        else:
            if self.begin_datetime is None or self.end_datetime is None:
                raise ValueError("begin_datetime and end_datetime have to both be specified when id is not None")

        if self.begin_datetime < datetime.now():
            raise ValueError("begin_datetime cannot be in the past")
        if self.begin_datetime >= self.end_datetime:
            raise ValueError("begin_datetime cannot be greater or equal to end_datetime")

        return self


class PropertyBase(BaseModel):
    user_email: str
    name: str
    address: str
    curr_price: float


class PropertyBaseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    curr_price: Optional[float] = None
    closed_time_frames: Optional[list[ClosedTimeFrameUpdate]] = None


class PropertyInDB(PropertyBase):
    id: int
