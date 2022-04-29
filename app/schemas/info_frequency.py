from pydantic import BaseModel
from typing import Optional


class InfoBase(BaseModel):
    class Config:
        orm_mode = True


class InfoFrequency(InfoBase):
    id: Optional[int]
    number: int
    frequency: str
