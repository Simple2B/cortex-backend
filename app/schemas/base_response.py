from pydantic import BaseModel


class BaseResponsePydantic(BaseModel):
    msg: str
