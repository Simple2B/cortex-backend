from pydantic import BaseModel


class Info(BaseModel):
    class Config:
        orm_mode = True


class InfoFrequency(Info):
    frequency: str
