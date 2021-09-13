from pydantic import BaseModel


class BaseDoctor(BaseModel):
    username: str


class DoctorCreate(BaseDoctor):
    password: str


class Doctor(BaseDoctor):
    id: int
    api_key: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
