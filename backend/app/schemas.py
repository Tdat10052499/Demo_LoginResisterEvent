from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

# Schema cho đăng ký user mới
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

# Schema cho đăng nhập
class UserLogin(BaseModel):
    username: str
    password: str

# Schema cho tạo user (legacy)
class UserCreate(BaseModel):
    username: str | None = None
    email: str
    password: str | None = None
    name: str | None = None
    provider: str | None = None

# Schema để trả về user info
class UserRead(BaseModel):
    id: UUID
    username: str | None = None
    email: str
    name: str | None = None
    provider: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

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
