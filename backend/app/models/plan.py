from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base
import datetime


class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), default="我的旅行计划")
    destination = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    duration = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    days = relationship("PlanDay", back_populates="plan", cascade="all, delete-orphan")


class PlanDay(Base):
    __tablename__ = "plan_days"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("travel_plans.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    plan = relationship("TravelPlan", back_populates="days")
    items = relationship("PlanItem", back_populates="plan_day", cascade="all, delete-orphan")


class PlanItem(Base):
    __tablename__ = "plan_items"

    id = Column(Integer, primary_key=True, index=True)
    plan_day_id = Column(Integer, ForeignKey("plan_days.id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=False)
    order = Column(Integer, default=1)
    time_slot = Column(String(20), default="上午")
    note = Column(String(200), default="")

    plan_day = relationship("PlanDay", back_populates="items")
    attraction = relationship("Attraction")
