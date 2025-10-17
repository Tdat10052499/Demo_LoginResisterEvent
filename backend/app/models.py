from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from .database import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)  # Nullable cho SSO users
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=True)  # Cho local login
    hashed_password = Column(String(255), nullable=True)  # Cho local login
    provider = Column(String(50), nullable=True)  # "local" hoặc "microsoft"
    created_at = Column(DateTime, default=datetime.utcnow)
    registrations = relationship("EventRegistration", back_populates="user")

class EventRegistration(Base):
    __tablename__ = "event_registrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    note = Column(Text)
    registered_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="registrations")
