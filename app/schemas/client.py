import datetime
from pydantic import BaseModel


class Client(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_num: int
    date_of_birthday: datetime.datetime
    address: str
    city: str
    state: str
    zip: int
