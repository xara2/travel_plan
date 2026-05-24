import json, os, re
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.attraction import Attraction
from ..schemas.attraction import AttractionOut

router = APIRouter(prefix="/api/attractions", tags=["attractions"])
CITIES_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cities.json")

# Suffixes to strip from city names for fuzzy matching
CITY_SUFFIXES = re.compile(
    r'(市|区|县|自治州|自治县|地区|盟|林区|新区|街道|镇|乡)$'
)


def _normalize_city(name: str) -> str:
    return CITY_SUFFIXES.sub("", name.strip())


@router.get("", response_model=list[AttractionOut])
def search_attractions(
    city: str = Query(default=""),
    province: str = Query(default=""),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    q = db.query(Attraction)
    if province:
        norm_province = _normalize_city(province)
        q = q.filter(
            (Attraction.province == province) |
            (Attraction.province == norm_province) |
            Attraction.province.contains(norm_province)
        )
    if city:
        normalized = _normalize_city(city)
        q = q.filter(
            (Attraction.city == city) |
            (Attraction.city == normalized) |
            Attraction.city.contains(normalized) |
            Attraction.city.like(f"%{normalized}%")
        )
    if keyword:
        q = q.filter(
            (Attraction.name.contains(keyword)) |
            (Attraction.description.contains(keyword)) |
            (Attraction.category.contains(keyword))
        )
    return q.limit(50).all()


@router.get("/cities")
def list_cities(db: Session = Depends(get_db)):
    """Returns full province/city hierarchy from cities.json, falls back to DB."""
    if os.path.exists(CITIES_FILE):
        with open(CITIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    cities = db.query(Attraction.city).distinct().all()
    return [c[0] for c in cities]


@router.get("/{attraction_id}", response_model=AttractionOut)
def get_attraction(attraction_id: int, db: Session = Depends(get_db)):
    attr = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attr:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="景点不存在")
    return attr
