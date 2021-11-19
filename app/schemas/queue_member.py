from typing import Optional

from pydantic import BaseModel


class QueueMember(BaseModel):
    place_in_queue: int
    canceled: Optional[bool]
    client_id: int
    visit_id: int
    reception_id: int


class Queue(BaseModel):
    place_in_queue: Optional[int]
    client_id: int
    visit_id: int
    reception_id: int

    class Config:
        orm_mode = True
