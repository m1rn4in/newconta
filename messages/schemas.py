
from pydantic import BaseModel

class MessageCreate(BaseModel):
    name:str

class MessageRead(BaseModel):
    id:int
    name:str

    class Config:
        orm_mode = True

class MessageUpdate(BaseModel):
    name:str