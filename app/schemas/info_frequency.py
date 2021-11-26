from pydantic import BaseModel


class InfoBase(BaseModel):
    class Config:
        orm_mode = True


class InfoFrequency(InfoBase):
    id: int
    frequency: str
