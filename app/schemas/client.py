from pydantic import BaseModel


class Client(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_num: int
