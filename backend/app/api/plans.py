import httpx, random
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import TravelPlan, PlanDay, PlanItem, Attraction
from ..utils.auth import get_current_user
from ..models.user import User
from ..config import AMAP_API_KEY
from ..schemas.plan import (
    GeneratePlanReq, TravelPlanOut, TravelPlanListOut
)

router = APIRouter(prefix="/api/plans", tags=["plans"])


def _build_plan_out(plan) -> dict:
    """Build response dict from a TravelPlan ORM object."""
    return {
        "id": plan.id,
        "title": plan.title,
        "destination": plan.destination,
        "start_date": plan.start_date,
        "end_date": plan.end_date,
        "duration": plan.duration,
        "created_at": plan.created_at.isoformat() if plan.created_at else "",
        "days": [
            {
                "id": day.id,
                "day_number": day.day_number,
                "date": day.date,
                "items": sorted(
                    [
                        {
                            "id": item.id,
                            "attraction_id": item.attraction_id,
                            "order": item.order,
                            "time_slot": item.time_slot,
                            "note": item.note or "",
                            "attraction": {
                                "id": item.attraction.id,
                                "name": item.attraction.name,
                                "city": item.attraction.city,
                                "province": item.attraction.province or "",
                                "description": item.attraction.description or "",
                                "image_url": item.attraction.image_url or "",
                                "lat": item.attraction.lat,
                                "lng": item.attraction.lng,
                                "category": item.attraction.category or "",
                                "rating": item.attraction.rating or 4.0,
                                "visit_duration": item.attraction.visit_duration or 120,
                                "ticket_price": item.attraction.ticket_price or 0,
                                "need_reservation": item.attraction.need_reservation or False,
                                "opening_hours": item.attraction.opening_hours or "08:00-17:00",
                            },
                        }
                        for item in day.items
                    ],
                    key=lambda x: x["order"],
                ),
            }
            for day in plan.days
        ],
    }


@router.post("/generate")
def generate_plan(
    req: GeneratePlanReq,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not req.attraction_ids:
        raise HTTPException(status_code=400, detail="请至少选择一个景点")
    if req.duration < 1:
        raise HTTPException(status_code=400, detail="旅行天数至少为1天")

    attractions = (
        db.query(Attraction)
        .filter(Attraction.id.in_(req.attraction_ids))
        .all()
    )
    if not attractions:
        raise HTTPException(status_code=400, detail="未找到有效景点")

    # Sort attractions by lat/lng proximity
    with_lat = [a for a in attractions if a.lat and a.lng]
    without_lat = [a for a in attractions if not a.lat or not a.lng]

    # Greedy clustering: group geographically nearby attractions per day
    if with_lat:
        center_lat = sum(a.lat for a in with_lat) / len(with_lat)
        sorted_by_lat = sorted(with_lat, key=lambda a: a.lat)
    else:
        sorted_by_lat = []
        center_lat = 0

    # Distribute across days
    per_day = max(1, len(attractions) // req.duration)
    days_data = []
    all_attrs = sorted_by_lat + without_lat
    for d in range(req.duration):
        day_attrs = all_attrs[d * per_day : (d + 1) * per_day]
        if d == req.duration - 1:
            day_attrs = all_attrs[d * per_day :]
        days_data.append(day_attrs)

    # Create plan
    plan = TravelPlan(
        user_id=user.id,
        title=req.title,
        destination=req.destination,
        start_date=req.start_date,
        end_date=req.end_date,
        duration=req.duration,
    )
    db.add(plan)
    db.flush()

    # Calculate time slots based on departure time
    try:
        base_hour = int(req.depart_time.split(":")[0])
    except (ValueError, AttributeError):
        base_hour = 9
    time_slots = []
    for i in range(len(attractions) + 2):
        h = base_hour + i * 3
        if h < 12:
            label = f"{h:02d}:00 上午"
        elif h < 18:
            label = f"{h:02d}:00 下午"
        else:
            label = f"{h:02d}:00 傍晚"
        time_slots.append(label)

    for day_idx, day_attrs in enumerate(days_data):
        plan_day = PlanDay(
            plan_id=plan.id,
            day_number=day_idx + 1,
            date=req.start_date + timedelta(days=day_idx),
        )
        db.add(plan_day)
        db.flush()

        for i, attr in enumerate(day_attrs):
            slot = time_slots[min(i, len(time_slots) - 1)]
            item = PlanItem(
                plan_day_id=plan_day.id,
                attraction_id=attr.id,
                order=i + 1,
                time_slot=slot,
                note=f"游览{attr.name}，建议游玩{attr.visit_duration}分钟",
            )
            db.add(item)

    db.commit()

    # Reload with eager loading
    plan = (
        db.query(TravelPlan)
        .options(
            joinedload(TravelPlan.days)
            .joinedload(PlanDay.items)
            .joinedload(PlanItem.attraction)
        )
        .filter(TravelPlan.id == plan.id)
        .first()
    )
    return _build_plan_out(plan)


@router.get("", response_model=list[TravelPlanListOut])
def list_plans(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plans = (
        db.query(TravelPlan)
        .filter(TravelPlan.user_id == user.id)
        .order_by(TravelPlan.created_at.desc())
        .all()
    )
    return [
        {
            "id": p.id,
            "title": p.title,
            "destination": p.destination,
            "start_date": p.start_date,
            "end_date": p.end_date,
            "duration": p.duration,
            "created_at": p.created_at.isoformat() if p.created_at else "",
        }
        for p in plans
    ]


@router.get("/{plan_id}")
def get_plan(
    plan_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = (
        db.query(TravelPlan)
        .options(
            joinedload(TravelPlan.days)
            .joinedload(PlanDay.items)
            .joinedload(PlanItem.attraction)
        )
        .filter(TravelPlan.id == plan_id, TravelPlan.user_id == user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="计划不存在")
    return _build_plan_out(plan)


@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = (
        db.query(TravelPlan)
        .filter(TravelPlan.id == plan_id, TravelPlan.user_id == user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="计划不存在")
    db.delete(plan)
    db.commit()
    return {"message": "删除成功"}


@router.get("/route/options")
async def get_route_options(
    origin_lng: float = Query(...),
    origin_lat: float = Query(...),
    dest_lng: float = Query(...),
    dest_lat: float = Query(...),
    user: User = Depends(get_current_user),
):
    """Get transportation options between two points via Amap Direction API."""
    origin = f"{origin_lng},{origin_lat}"
    destination = f"{dest_lng},{dest_lat}"
    options = {}

    async with httpx.AsyncClient(timeout=10) as client:
        # Driving
        try:
            dr = await client.get("https://restapi.amap.com/v3/direction/driving", params={
                "key": AMAP_API_KEY, "origin": origin, "destination": destination,
                "strategy": 0, "extensions": "base",
            })
            if dr.status_code == 200:
                data = dr.json()
                if data.get("status") == "1" and data["route"]["paths"]:
                    p = data["route"]["paths"][0]
                    options["driving"] = {
                        "type": "打车/自驾",
                        "duration": int(p["duration"]) // 60,
                        "distance": int(p["distance"]),
                        "cost": round(int(p["distance"]) * 0.0025 + 8, 0),
                        "desc": f"约{int(p['duration'])//60}分钟，{int(p['distance'])}米，约￥{round(int(p['distance'])*0.0025+8,0)}",
                    }
        except Exception:
            pass

        # Transit
        try:
            tr = await client.get("https://restapi.amap.com/v3/direction/transit/integrated", params={
                "key": AMAP_API_KEY, "origin": origin, "destination": destination,
                "city": "", "cityd": "", "strategy": 0, "extensions": "base",
            })
            if tr.status_code == 200:
                data = tr.json()
                if data.get("status") == "1" and data["route"]["transits"]:
                    t = data["route"]["transits"][0]
                    options["transit"] = {
                        "type": "公交/地铁",
                        "duration": int(t["duration"]) // 60,
                        "distance": int(t["distance"]),
                        "cost": int(t.get("cost", 2)),
                        "desc": f"约{int(t['duration'])//60}分钟，{int(t['distance'])}米，约￥{int(t.get('cost',2))}",
                    }
        except Exception:
            pass

        # Walking
        try:
            wk = await client.get("https://restapi.amap.com/v3/direction/walking", params={
                "key": AMAP_API_KEY, "origin": origin, "destination": destination,
            })
            if wk.status_code == 200:
                data = wk.json()
                if data.get("status") == "1" and data["route"]["paths"]:
                    p = data["route"]["paths"][0]
                    options["walking"] = {
                        "type": "步行",
                        "duration": int(p["duration"]) // 60,
                        "distance": int(p["distance"]),
                        "cost": 0,
                        "desc": f"约{int(p['duration'])//60}分钟，{int(p['distance'])}米",
                    }
        except Exception:
            pass

    if not options:
        # Fallback estimates if API fails
        from math import radians, cos, sin, asin, sqrt
        def haversine(lng1, lat1, lng2, lat2):
            lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
            dlon, dlat = lng2 - lng1, lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
            return 2 * asin(sqrt(a)) * 6371000
        dist = haversine(origin_lng, origin_lat, dest_lng, dest_lat)
        drv_time = max(5, int(dist / 500))
        options["driving"] = {
            "type": "打车/自驾", "duration": drv_time, "distance": int(dist),
            "cost": round(dist * 0.0025 + 8, 0),
            "desc": f"约{drv_time}分钟，{int(dist)}米，约￥{round(dist*0.0025+8,0)}"
        }
        options["transit"] = {
            "type": "公交/地铁", "duration": int(drv_time * 1.8), "distance": int(dist),
            "cost": 2,
            "desc": f"约{int(drv_time*1.8)}分钟，{int(dist)}米，约￥2"
        }
        options["walking"] = {
            "type": "步行", "duration": int(dist / 80), "distance": int(dist),
            "cost": 0,
            "desc": f"约{int(dist/80)}分钟，{int(dist)}米"
        }

    return {"routes": list(options.values())}
