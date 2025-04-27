###(модели пользователей, мастеров и заказов)

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import datetime

class UserRole(str, enum.Enum):
    client = "client"
    master = "master"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False)

    master_profile = relationship("MasterProfile", back_populates="user", uselist=False)

class MasterProfile(Base):
    __tablename__ = "masters_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialization = Column(String, index=True)
    description = Column(Text)

    user = relationship("User", back_populates="master_profile")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    master_id = Column(Integer, ForeignKey("masters_profiles.id"))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
