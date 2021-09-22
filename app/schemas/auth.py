from pydantic import BaseModel


class Doctor(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class DoctorLogin(BaseModel):
    email: str
    password: str


class DoctorCreate(BaseModel):
    api_key: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
