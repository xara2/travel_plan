from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    nickname = Column(String(50), default="")
    avatar = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
