from pydantic import BaseModel


class BaseDoctor(BaseModel):
    # first_name: str
    # last_name: str
    email: str


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
