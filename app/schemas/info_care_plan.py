from pydantic import BaseModel


class Info(BaseModel):
    class Config:
        orm_mode = True


class InfoCarePlan(Info):
    id: int
    care_plan: str
