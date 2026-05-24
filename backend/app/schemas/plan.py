from pydantic import BaseModel
from datetime import date
from .attraction import AttractionOut


class PlanItemOut(BaseModel):
    id: int
    attraction_id: int
    order: int
    time_slot: str
    note: str
    attraction: AttractionOut | None = None

    model_config = {"from_attributes": True}


class PlanDayOut(BaseModel):
    id: int
    day_number: int
    date: date
    items: list[PlanItemOut] = []

    model_config = {"from_attributes": True}


class TravelPlanOut(BaseModel):
    id: int
    title: str
    destination: str
    start_date: date
    end_date: date
    duration: int
    created_at: str
    days: list[PlanDayOut] = []

    model_config = {"from_attributes": True}


class TravelPlanListOut(BaseModel):
    id: int
    title: str
    destination: str
    start_date: date
    end_date: date
    duration: int
    created_at: str

    model_config = {"from_attributes": True}


class GeneratePlanReq(BaseModel):
    destination: str
    start_date: date
    end_date: date
    duration: int
    attraction_ids: list[int]
    title: str = "我的旅行计划"
    depart_time: str = "09:00"


class PlanBriefOut(BaseModel):
    id: int
    title: str
    destination: str
    start_date: date
    end_date: date
    duration: int

    model_config = {"from_attributes": True}
