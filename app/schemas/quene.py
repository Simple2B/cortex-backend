from pydantic import BaseModel


class Queue(BaseModel):
    client_id: int
    reception_id: int
    place_in_queue: int
    visit_id: int
