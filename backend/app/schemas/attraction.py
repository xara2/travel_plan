from pydantic import BaseModel


class AttractionOut(BaseModel):
    id: int
    name: str
    city: str
    province: str
    description: str
    image_url: str
    lat: float
    lng: float
    category: str
    rating: float
    visit_duration: int
    ticket_price: int = 0
    need_reservation: bool = False
    opening_hours: str = "08:00-17:00"

    model_config = {"from_attributes": True}


class AttractionSearchParams(BaseModel):
    city: str = ""
    keyword: str = ""
