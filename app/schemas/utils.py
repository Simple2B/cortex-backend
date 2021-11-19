from pydantic import BaseModel


class OrmModeModel(BaseModel):
    class Config:
        orm_mode = True
