from pydantic import BaseModel


class Quene(BaseModel):
    client_id: int
    reseption_id: int
    place_in_quene: int
    visit_id: int
