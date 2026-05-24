import json, os
from .database import SessionLocal
from .models.attraction import Attraction

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_attractions():
    """Load attractions from JSON file if exists, otherwise return built-in data."""
    json_path = os.path.join(DATA_DIR, "attractions.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Fallback built-in data
    return [
        # 北京
        {"name": "故宫博物院", "city": "北京", "province": "北京市", "description": "中国古代宫廷建筑之精华，世界五大宫之首。", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600", "lat": 39.9163, "lng": 116.3972, "category": "历史文化", "rating": 4.9, "visit_duration": 240},
        {"name": "天安门广场", "city": "北京", "province": "北京市", "description": "世界上最大的城市广场。", "image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600", "lat": 39.9087, "lng": 116.3975, "category": "地标建筑", "rating": 4.8, "visit_duration": 60},
        {"name": "颐和园", "city": "北京", "province": "北京市", "description": "中国现存最大的皇家园林。", "image_url": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=600", "lat": 39.9999, "lng": 116.2755, "category": "园林古迹", "rating": 4.7, "visit_duration": 180},
        {"name": "八达岭长城", "city": "北京", "province": "北京市", "description": "明长城中保存最好的一段。", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600", "lat": 40.3597, "lng": 116.0200, "category": "历史文化", "rating": 4.8, "visit_duration": 240},
        {"name": "天坛公园", "city": "北京", "province": "北京市", "description": "明清皇帝祭天之所。", "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600", "lat": 39.8822, "lng": 116.4066, "category": "历史文化", "rating": 4.7, "visit_duration": 120},
        {"name": "鸟巢", "city": "北京", "province": "北京市", "description": "2008年奥运会主体育场。", "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600", "lat": 39.9928, "lng": 116.3884, "category": "现代建筑", "rating": 4.5, "visit_duration": 90},
        # 上海
        {"name": "外滩", "city": "上海", "province": "上海市", "description": "黄浦江畔的万国建筑博览群。", "image_url": "https://images.unsplash.com/photo-1537531383496-f4749b88b535?w=600", "lat": 31.2400, "lng": 121.4900, "category": "地标建筑", "rating": 4.8, "visit_duration": 120},
        {"name": "东方明珠塔", "city": "上海", "province": "上海市", "description": "上海标志性景观，高467.9米。", "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600", "lat": 31.2397, "lng": 121.4998, "category": "现代建筑", "rating": 4.5, "visit_duration": 120},
        {"name": "豫园", "city": "上海", "province": "上海市", "description": "江南古典园林代表作。", "image_url": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=600", "lat": 31.2277, "lng": 121.4924, "category": "园林古迹", "rating": 4.6, "visit_duration": 120},
        {"name": "上海迪士尼乐园", "city": "上海", "province": "上海市", "description": "中国大陆第一座迪士尼乐园。", "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600", "lat": 31.1433, "lng": 121.6620, "category": "主题乐园", "rating": 4.7, "visit_duration": 480},
        {"name": "南京路步行街", "city": "上海", "province": "上海市", "description": "中国最著名的商业街之一。", "image_url": "https://images.unsplash.com/photo-1537531383496-f4749b88b535?w=600", "lat": 31.2345, "lng": 121.4740, "category": "购物美食", "rating": 4.4, "visit_duration": 120},
        # 杭州
        {"name": "西湖", "city": "杭州", "province": "浙江省", "description": "中国最著名的湖泊景观，被誉为'人间天堂'。", "image_url": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=600", "lat": 30.2420, "lng": 120.1460, "category": "自然风光", "rating": 4.9, "visit_duration": 240},
        {"name": "灵隐寺", "city": "杭州", "province": "浙江省", "description": "中国佛教禅宗十大古刹之一。", "image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600", "lat": 30.2427, "lng": 120.1005, "category": "宗教文化", "rating": 4.7, "visit_duration": 120},
        # 成都
        {"name": "宽窄巷子", "city": "成都", "province": "四川省", "description": "成都现存较成规模的清朝古街道。", "image_url": "https://images.unsplash.com/photo-1537531383496-f4749b88b535?w=600", "lat": 30.6667, "lng": 104.0527, "category": "历史文化", "rating": 4.5, "visit_duration": 90},
        {"name": "大熊猫繁育研究基地", "city": "成都", "province": "四川省", "description": "世界上最大的大熊猫人工繁育机构。", "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600", "lat": 30.7322, "lng": 104.1445, "category": "自然风光", "rating": 4.8, "visit_duration": 180},
        # 西安
        {"name": "秦始皇兵马俑", "city": "西安", "province": "陕西省", "description": "世界第八大奇迹。", "image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600", "lat": 34.3849, "lng": 109.2730, "category": "历史文化", "rating": 4.9, "visit_duration": 180},
        {"name": "大雁塔", "city": "西安", "province": "陕西省", "description": "西安标志性建筑，始建于唐代。", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600", "lat": 34.2196, "lng": 108.9630, "category": "宗教文化", "rating": 4.6, "visit_duration": 90},
        {"name": "西安城墙", "city": "西安", "province": "陕西省", "description": "中国现存规模最大、保存最完整的古代城垣。", "image_url": "https://images.unsplash.com/photo-1537531383496-f4749b88b535?w=600", "lat": 34.2600, "lng": 108.9420, "category": "历史文化", "rating": 4.7, "visit_duration": 120},
        # 三亚
        {"name": "亚龙湾", "city": "三亚", "province": "海南省", "description": "被誉为'天下第一湾'。", "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600", "lat": 18.2250, "lng": 109.6250, "category": "自然风光", "rating": 4.7, "visit_duration": 240},
        {"name": "蜈支洲岛", "city": "三亚", "province": "海南省", "description": "中国顶级的潜水胜地。", "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600", "lat": 18.3140, "lng": 109.7630, "category": "自然风光", "rating": 4.7, "visit_duration": 300},
        # 昆明
        {"name": "石林", "city": "昆明", "province": "云南省", "description": "世界自然遗产，典型的喀斯特地貌。", "image_url": "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=600", "lat": 24.8220, "lng": 103.3250, "category": "自然风光", "rating": 4.6, "visit_duration": 240},
        {"name": "滇池", "city": "昆明", "province": "云南省", "description": "云南省最大的淡水湖。", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600", "lat": 24.9700, "lng": 102.6580, "category": "自然风光", "rating": 4.4, "visit_duration": 120},
        # 广州
        {"name": "广州塔", "city": "广州", "province": "广东省", "description": "又称小蛮腰，高600米。", "image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=600", "lat": 23.1060, "lng": 113.3240, "category": "现代建筑", "rating": 4.5, "visit_duration": 120},
        {"name": "长隆野生动物世界", "city": "广州", "province": "广东省", "description": "亚洲最大的野生动物园。", "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600", "lat": 22.9960, "lng": 113.3180, "category": "主题乐园", "rating": 4.7, "visit_duration": 360},
    ]


def seed_attractions():
    db = SessionLocal()
    try:
        if db.query(Attraction).count() > 0:
            return
        for attr in _load_attractions():
            db.add(Attraction(**attr))
        db.commit()
    finally:
        db.close()
