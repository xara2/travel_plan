from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from ..database import Base


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False, index=True)
    province = Column(String(50), default="")
    description = Column(Text, default="")
    image_url = Column(String(300), default="")
    lat = Column(Float, default=0.0)
    lng = Column(Float, default=0.0)
    category = Column(String(50), default="景点")
    rating = Column(Float, default=4.0)
    visit_duration = Column(Integer, default=120)
    ticket_price = Column(Integer, default=0)
    need_reservation = Column(Boolean, default=False)
    opening_hours = Column(String(50), default="08:00-17:00")
