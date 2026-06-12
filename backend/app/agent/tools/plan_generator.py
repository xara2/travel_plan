"""AI-enhanced plan generation tool."""
import json


async def generate_plan_tool(
    attraction_ids: str = "",
    destination: str = "",
    duration: int = 3,
    preferences: str = "",
) -> str:
    """Generate a day-by-day travel plan from selected attractions.

    Args:
        attraction_ids: JSON array of attraction IDs, e.g. "[1, 5, 12]"
        destination: Destination city name
        duration: Number of days for the trip
        preferences: User preferences (e.g. "喜欢自然风光，不喜欢人多的景点")
    """
    from ...database import SessionLocal
    from ...models.attraction import Attraction
    from datetime import date

    try:
        ids = json.loads(attraction_ids) if isinstance(attraction_ids, str) else attraction_ids
    except (json.JSONDecodeError, TypeError):
        return "错误: attraction_ids 必须是 JSON 数组格式，例如 '[1, 5, 12]'"

    if not ids or duration < 1:
        return "错误: 请提供有效的景点ID列表和旅行天数"

    db = SessionLocal()
    try:
        attractions = db.query(Attraction).filter(Attraction.id.in_(ids)).all()
        if not attractions:
            return "未找到所选景点，请重新搜索并选择。"
    finally:
        db.close()

    # Group by geographic proximity (lat-sorted)
    with_lat = sorted(
        [a for a in attractions if a.lat and a.lng],
        key=lambda a: a.lat,
    )
    without_lat = [a for a in attractions if not a.lat or not a.lng]
    all_attrs = with_lat + without_lat

    # Distribute across days
    per_day = max(1, len(all_attrs) // duration)
    days = []

    time_labels = ["上午", "上午", "下午", "下午", "傍晚"]
    for d in range(duration):
        start = d * per_day
        end = start + per_day if d < duration - 1 else len(all_attrs)
        day_attrs = all_attrs[start:end]
        items = []
        for i, a in enumerate(day_attrs):
            slot = time_labels[min(i, len(time_labels) - 1)]
            items.append({
                "order": i + 1,
                "time_slot": f"{8 + i * 3:02d}:00 {slot}",
                "attraction": {
                    "id": a.id,
                    "name": a.name,
                    "category": a.category,
                    "rating": a.rating,
                    "duration_min": a.visit_duration,
                    "ticket_yuan": a.ticket_price,
                    "description": (a.description or "")[:100],
                },
            })
        days.append({
            "day": d + 1,
            "attractions_count": len(items),
            "items": items,
        })

    result = {
        "destination": destination,
        "duration_days": duration,
        "total_attractions": len(all_attrs),
        "plan": days,
        "tips": _generate_tips(all_attrs, duration),
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


def _generate_tips(attractions: list, duration: int) -> list[str]:
    tips = []
    total_tickets = sum(a.ticket_price or 0 for a in attractions)
    if total_tickets > 0:
        tips.append(f"门票总费用约 ¥{total_tickets}")
    if duration > 2:
        tips.append("建议提前预订住宿，旅游旺季房源紧张")
    if any(a.need_reservation for a in attractions):
        tips.append("部分景点需要提前预约，请查看官网并提前购票")
    tips.append("出行前请查看天气预报，合理安排户外活动")
    return tips
