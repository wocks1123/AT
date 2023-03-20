from datetime import datetime

from pydantic import BaseModel


class ATBase(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
        }
