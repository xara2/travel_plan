"""One-shot script to add ticket_price, need_reservation, opening_hours to attractions.json."""
import json
import os
import random

random.seed(42)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "attractions.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    attractions = json.load(f)

# Category-based defaults: (min_price, max_price, typical_hours, reservation_probability)
CATEGORY_DEFAULTS = {
    "历史文化": (30, 120, "08:30-17:00", 0.7),
    "博物馆": (0, 80, "09:00-17:00", 0.6),
    "地标建筑": (0, 100, "08:00-18:00", 0.3),
    "自然风光": (0, 120, "08:00-17:30", 0.2),
    "公园": (0, 30, "06:00-21:00", 0.05),
    "寺庙": (0, 50, "08:00-17:00", 0.1),
    "宗教": (0, 50, "08:00-17:00", 0.1),
    "主题乐园": (100, 400, "09:00-21:00", 0.5),
    "古镇": (0, 100, "全天", 0.1),
    "古村": (0, 80, "全天", 0.1),
    "街区": (0, 0, "全天", 0.0),
    "美食": (0, 0, "全天", 0.0),
    "购物": (0, 0, "10:00-22:00", 0.0),
    "演出": (100, 500, "19:00-21:30", 0.8),
    "温泉": (80, 300, "10:00-22:00", 0.3),
    "滑雪": (100, 400, "08:30-17:00", 0.2),
    "动物园": (20, 150, "08:30-17:30", 0.1),
    "植物园": (10, 60, "08:00-17:30", 0.05),
    "海洋馆": (100, 250, "09:00-17:30", 0.2),
    "游乐园": (50, 300, "09:00-21:00", 0.3),
    "名胜古迹": (20, 100, "08:00-17:30", 0.4),
}

# Specific famous attractions that need reservations
NEED_RESERVATION = {
    "故宫博物院", "布达拉宫", "莫高窟", "兵马俑", "秦始皇兵马俑博物馆",
    "九寨沟", "张家界国家森林公园", "黄山风景区", "泰山", "华山",
    "庐山", "峨眉山", "武夷山", "普陀山", "九华山",
    "东方明珠广播电视塔", "上海迪士尼乐园", "北京环球影城",
    "中国国家博物馆", "陕西历史博物馆", "南京博物院",
    "八达岭长城", "慕田峪长城", "天坛公园",
}

# Famous attractions with specific ticket prices
SPECIFIC_PRICES = {
    "故宫博物院": 60,
    "八达岭长城": 40,
    "慕田峪长城": 45,
    "天坛公园": 15,
    "颐和园": 30,
    "圆明园": 10,
    "布达拉宫": 200,
    "莫高窟": 238,
    "兵马俑": 120,
    "秦始皇兵马俑博物馆": 120,
    "九寨沟": 169,
    "张家界国家森林公园": 228,
    "黄山风景区": 190,
    "泰山": 115,
    "华山": 160,
    "庐山": 180,
    "峨眉山": 160,
    "武夷山": 140,
    "普陀山": 160,
    "东方明珠广播电视塔": 199,
    "上海迪士尼乐园": 399,
    "北京环球影城": 418,
    "中国国家博物馆": 0,
    "陕西历史博物馆": 0,
    "南京博物院": 0,
    "杭州西湖": 0,
    "上海外滩": 0,
    "天安门广场": 0,
    "夫子庙": 0,
}

SPECIFIC_HOURS = {
    "故宫博物院": "08:30-17:00（周一闭馆）",
    "中国国家博物馆": "09:00-17:00（周一闭馆）",
    "陕西历史博物馆": "08:30-18:00（周一闭馆）",
    "南京博物院": "09:00-17:00（周一闭馆）",
    "上海迪士尼乐园": "08:30-21:30",
    "北京环球影城": "09:00-21:00",
    "东方明珠广播电视塔": "08:00-21:30",
}

for a in attractions:
    name = a.get("name", "")
    category = a.get("category", "景点")
    defaults = CATEGORY_DEFAULTS.get(category, (0, 50, "08:00-17:00", 0.1))

    # ticket_price
    if name in SPECIFIC_PRICES:
        a["ticket_price"] = SPECIFIC_PRICES[name]
    elif "ticket_price" not in a:
        a["ticket_price"] = random.randint(defaults[0], defaults[1])

    # need_reservation
    if name in NEED_RESERVATION:
        a["need_reservation"] = True
    elif "need_reservation" not in a:
        a["need_reservation"] = random.random() < defaults[3]

    # opening_hours
    if name in SPECIFIC_HOURS:
        a["opening_hours"] = SPECIFIC_HOURS[name]
    elif "opening_hours" not in a:
        a["opening_hours"] = defaults[2]

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(attractions, f, ensure_ascii=False, indent=2)

print(f"Enriched {len(attractions)} attractions.")
