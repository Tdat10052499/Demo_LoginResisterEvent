from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None

class EventRead(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    registered_at: datetime

    class Config:
        from_attributes = True
