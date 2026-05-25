"""Add missing major Chinese attractions to attractions.json."""
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "attractions.json")

NEW_ATTRACTIONS = [
    # === 北京 - Museums & Parks ===
    {"name": "中国国家博物馆", "city": "北京", "province": "北京市", "description": "世界上建筑面积最大的博物馆，收藏中华五千年珍贵文物140余万件，是了解中国历史文化的最佳场所。", "lat": 39.9053, "lng": 116.3977, "category": "博物馆", "rating": 4.8, "visit_duration": 180, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "首都博物馆", "city": "北京", "province": "北京市", "description": "展示北京历史文化与城市发展的大型综合性博物馆，建筑本身即为现代艺术佳作。", "lat": 39.9057, "lng": 116.3438, "category": "博物馆", "rating": 4.6, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "圆明园遗址公园", "city": "北京", "province": "北京市", "description": "清代皇家园林遗址，被誉为'万园之园'。虽历经劫难，残存的大水法石柱与湖光山色仍令人震撼。", "lat": 40.0087, "lng": 116.2985, "category": "园林古迹", "rating": 4.7, "visit_duration": 180, "ticket_price": 25, "need_reservation": False, "opening_hours": "07:00-19:00"},
    {"name": "北海公园", "city": "北京", "province": "北京市", "description": "中国现存最古老、最完整的皇家园林之一，白塔矗立琼华岛，'让我们荡起双桨'的经典场景。", "lat": 39.9244, "lng": 116.3893, "category": "园林古迹", "rating": 4.6, "visit_duration": 120, "ticket_price": 10, "need_reservation": False, "opening_hours": "06:00-21:00"},
    {"name": "恭王府", "city": "北京", "province": "北京市", "description": "清代规模最大的王府建筑群，曾是权臣和珅的府邸，后为恭亲王奕訢的王府，堪称半部清朝史。", "lat": 39.9366, "lng": 116.3838, "category": "历史文化", "rating": 4.7, "visit_duration": 120, "ticket_price": 40, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "雍和宫", "city": "北京", "province": "北京市", "description": "北京最大的藏传佛教寺院，原为雍正皇帝潜邸。万福阁内26米高的白檀木弥勒大佛令人叹为观止。", "lat": 39.9475, "lng": 116.4175, "category": "宗教文化", "rating": 4.7, "visit_duration": 90, "ticket_price": 25, "need_reservation": False, "opening_hours": "09:00-17:00"},
    {"name": "国家体育场（鸟巢）", "city": "北京", "province": "北京市", "description": "2008年北京奥运会主体育场，独特的钢结构编织外观成为现代北京的地标性建筑。", "lat": 39.9928, "lng": 116.3884, "category": "现代建筑", "rating": 4.5, "visit_duration": 90, "ticket_price": 50, "need_reservation": False, "opening_hours": "09:00-18:00"},
    {"name": "北京798艺术区", "city": "北京", "province": "北京市", "description": "由老工厂改造而成的当代艺术区，聚集众多画廊、设计工作室和时尚餐厅，是文艺青年的打卡胜地。", "lat": 39.9836, "lng": 116.4957, "category": "文化艺术", "rating": 4.5, "visit_duration": 150, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 上海 ===
    {"name": "上海科技馆", "city": "上海", "province": "上海市", "description": "国家5A级旅游景区，以'自然·人·科技'为主题，拥有11个常设展厅和4大高科技影院。", "lat": 31.2204, "lng": 121.5420, "category": "博物馆", "rating": 4.6, "visit_duration": 180, "ticket_price": 45, "need_reservation": False, "opening_hours": "09:00-17:15"},
    {"name": "上海自然博物馆", "city": "上海", "province": "上海市", "description": "集古生物学、植物学、动物学、人类学于一体的综合性博物馆，恐龙化石标本极为丰富。", "lat": 31.2370, "lng": 121.4670, "category": "博物馆", "rating": 4.7, "visit_duration": 150, "ticket_price": 30, "need_reservation": False, "opening_hours": "09:00-17:00"},
    {"name": "上海野生动物园", "city": "上海", "province": "上海市", "description": "国家5A级旅游景区，汇集世界各地珍稀动物200余种。可乘车穿越猛兽区近距离观察动物。", "lat": 31.0270, "lng": 121.7120, "category": "主题乐园", "rating": 4.6, "visit_duration": 240, "ticket_price": 130, "need_reservation": False, "opening_hours": "09:00-17:00"},
    {"name": "田子坊", "city": "上海", "province": "上海市", "description": "上海最具特色的石库门里弄改造而成的创意街区，弄堂里遍布艺术工作室、特色小店和咖啡馆。", "lat": 31.2120, "lng": 121.4690, "category": "购物美食", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 南京 ===
    {"name": "中山陵", "city": "南京", "province": "江苏省", "description": "中国近代伟人孙中山先生的陵墓，依山而建气势恢宏。392级台阶象征当时3亿9千2百万同胞。", "lat": 32.0610, "lng": 118.8483, "category": "历史文化", "rating": 4.8, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "08:30-17:00"},
    {"name": "夫子庙-秦淮风光带", "city": "南京", "province": "江苏省", "description": "南京最繁华的历史文化街区，以夫子庙为中心，秦淮河畔灯火璀璨，美食小吃应有尽有。", "lat": 32.0200, "lng": 118.7890, "category": "历史文化", "rating": 4.6, "visit_duration": 150, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "南京博物院", "city": "南京", "province": "江苏省", "description": "中国三大博物馆之一，前身为国立中央博物院。馆藏丰富以六朝文物和明代陶瓷著称。", "lat": 32.0420, "lng": 118.8200, "category": "博物馆", "rating": 4.7, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "明孝陵", "city": "南京", "province": "江苏省", "description": "明太祖朱元璋与马皇后的合葬陵墓，世界文化遗产。神道石刻气势非凡，秋日银杏尤为美丽。", "lat": 32.0580, "lng": 118.8573, "category": "历史文化", "rating": 4.7, "visit_duration": 120, "ticket_price": 70, "need_reservation": False, "opening_hours": "06:30-18:00"},
    {"name": "总统府", "city": "南京", "province": "江苏省", "description": "中国近代历史的见证地，清代为两江总督署，太平天国为天王府，民国时期为国民政府总统府。", "lat": 32.0460, "lng": 118.7977, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 40, "need_reservation": False, "opening_hours": "08:30-17:00"},

    # === 苏州 ===
    {"name": "拙政园", "city": "苏州", "province": "江苏省", "description": "中国四大名园之首，世界文化遗产。以水为中心，山水萦绕，厅榭精美，花木繁茂。", "lat": 31.3230, "lng": 120.6290, "category": "园林古迹", "rating": 4.8, "visit_duration": 150, "ticket_price": 80, "need_reservation": True, "opening_hours": "07:30-17:30"},
    {"name": "留园", "city": "苏州", "province": "江苏省", "description": "中国四大名园之一，世界文化遗产。以建筑空间处理精湛著称，移步换景令人叫绝。", "lat": 31.3162, "lng": 120.5862, "category": "园林古迹", "rating": 4.7, "visit_duration": 120, "ticket_price": 55, "need_reservation": False, "opening_hours": "07:30-17:30"},
    {"name": "虎丘", "city": "苏州", "province": "江苏省", "description": "有'吴中第一名胜'之称，千年虎丘塔斜而不倒是中国比萨斜塔。剑池藏有吴王阖闾墓葬之谜。", "lat": 31.3400, "lng": 120.5773, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 80, "need_reservation": False, "opening_hours": "07:30-17:30"},
    {"name": "周庄古镇", "city": "苏州", "province": "江苏省", "description": "中国第一水乡，江南六大古镇之首。小桥流水人家，沈厅张厅见证明清富商繁华。", "lat": 31.1313, "lng": 120.8432, "category": "历史文化", "rating": 4.5, "visit_duration": 240, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "苏州博物馆", "city": "苏州", "province": "江苏省", "description": "贝聿铭大师的封刀之作，建筑本身就是艺术品。粉墙黛瓦融入江南园林元素，馆藏吴地文物精品。", "lat": 31.3234, "lng": 120.6268, "category": "博物馆", "rating": 4.8, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},

    # === 杭州 ===
    {"name": "千岛湖", "city": "杭州", "province": "浙江省", "description": "国家5A级景区，1078座岛屿星罗棋布。水质清澈为国家一级水体，是农夫山泉水源地之一。", "lat": 29.6040, "lng": 119.0420, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 130, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "西溪国家湿地公园", "city": "杭州", "province": "浙江省", "description": "中国第一个国家湿地公园，城市中罕见的次生湿地。秋季芦花飞扬，乘摇橹船穿行水巷别有情趣。", "lat": 30.2690, "lng": 120.0693, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "浙江省博物馆", "city": "杭州", "province": "浙江省", "description": "浙江省最大的综合性人文科学博物馆，收藏河姆渡文化、良渚文化等珍贵文物十余万件。", "lat": 30.2535, "lng": 120.1560, "category": "博物馆", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "宋城", "city": "杭州", "province": "浙江省", "description": "大型宋代文化主题公园，'宋城千古情'演出被誉为世界三大名秀之一。", "lat": 30.1704, "lng": 120.0950, "category": "主题乐园", "rating": 4.5, "visit_duration": 240, "ticket_price": 320, "need_reservation": False, "opening_hours": "09:00-21:00"},

    # === 黄山 ===
    {"name": "黄山风景区", "city": "黄山", "province": "安徽省", "description": "世界文化与自然双重遗产，以'奇松、怪石、云海、温泉、冬雪'五绝闻名。徐霞客赞曰：'五岳归来不看山，黄山归来不看岳'。", "lat": 30.1320, "lng": 118.1670, "category": "自然风光", "rating": 4.9, "visit_duration": 480, "ticket_price": 230, "need_reservation": True, "opening_hours": "06:30-16:30"},
    {"name": "宏村", "city": "黄山", "province": "安徽省", "description": "世界文化遗产，徽派古村落的杰出代表。月沼和南湖倒映粉墙黛瓦，《卧虎藏龙》曾在此取景。", "lat": 29.9927, "lng": 117.9890, "category": "历史文化", "rating": 4.7, "visit_duration": 180, "ticket_price": 104, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "西递", "city": "黄山", "province": "安徽省", "description": "世界文化遗产，与宏村齐名的徽派古村落。以精美的石雕、砖雕和木雕'三绝'著称。", "lat": 29.9050, "lng": 117.9951, "category": "历史文化", "rating": 4.6, "visit_duration": 150, "ticket_price": 104, "need_reservation": False, "opening_hours": "08:00-17:00"},

    # === 西安 ===
    {"name": "陕西历史博物馆", "city": "西安", "province": "陕西省", "description": "中国第一座大型现代化国家级博物馆，馆藏文物170余万件，特别是周、秦、汉、唐文物珍品举世无双。", "lat": 34.2179, "lng": 108.9500, "category": "博物馆", "rating": 4.8, "visit_duration": 180, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:30"},
    {"name": "华清宫", "city": "西安", "province": "陕西省", "description": "唐代皇家温泉行宫，杨贵妃曾在此沐浴。骊山脚下的唐代建筑群与温泉汤池遗址见证了盛世爱情故事。", "lat": 34.3630, "lng": 109.2150, "category": "历史文化", "rating": 4.6, "visit_duration": 150, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "钟鼓楼", "city": "西安", "province": "陕西省", "description": "西安市中心标志性建筑，钟楼与鼓楼遥相呼应。登楼可俯瞰古城四条大街，晨钟暮鼓延续千年。", "lat": 34.2608, "lng": 108.9423, "category": "历史文化", "rating": 4.6, "visit_duration": 90, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:30-18:00"},

    # === 桂林 ===
    {"name": "漓江风景区", "city": "桂林", "province": "广西壮族自治区", "description": "世界自然遗产，国家5A级景区。百里漓江百里画廊，桂林山水甲天下，阳朔山水甲桂林。", "lat": 25.0250, "lng": 110.4380, "category": "自然风光", "rating": 4.9, "visit_duration": 480, "ticket_price": 215, "need_reservation": True, "opening_hours": "08:00-18:00"},
    {"name": "阳朔西街", "city": "桂林", "province": "广西壮族自治区", "description": "阳朔最古老最繁华的街道，中西文化交融的特色街区。夜晚尤为热闹，啤酒鱼是必尝美食。", "lat": 24.7778, "lng": 110.4910, "category": "购物美食", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "象鼻山", "city": "桂林", "province": "广西壮族自治区", "description": "桂林城徽标志，山形酷似一头巨象伸长鼻子汲取漓江水。'象山水月'是桂林最具代表性的景观。", "lat": 25.2710, "lng": 110.2920, "category": "自然风光", "rating": 4.5, "visit_duration": 60, "ticket_price": 55, "need_reservation": False, "opening_hours": "07:30-17:30"},
    {"name": "龙脊梯田", "city": "桂林", "province": "广西壮族自治区", "description": "世界人工奇观,壮族瑶族先民在崇山峻岭中开垦出壮观的梯田。四季景色各异，清晨云雾缭绕如仙境。", "lat": 25.7950, "lng": 110.1300, "category": "自然风光", "rating": 4.7, "visit_duration": 240, "ticket_price": 80, "need_reservation": False, "opening_hours": "07:00-18:00"},

    # === 广州 ===
    {"name": "广东省博物馆", "city": "广州", "province": "广东省", "description": "外形如'月光宝盒'的现代建筑，馆藏以广东历史文化和端砚、潮州木雕等岭南特色文物著称。", "lat": 23.1150, "lng": 113.3230, "category": "博物馆", "rating": 4.5, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "白云山", "city": "广州", "province": "广东省", "description": "南粤名山，国家5A级景区。由30多座山峰组成，登摩星岭可俯瞰广州市全景，自古有'羊城第一秀'美誉。", "lat": 23.1780, "lng": 113.2970, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 5, "need_reservation": False, "opening_hours": "06:00-21:00"},
    {"name": "沙面", "city": "广州", "province": "广东省", "description": "珠江冲积而成的沙洲，曾有十多个国家在此设立领事馆。欧陆风情建筑林立，是广州最具异国情调的地方。", "lat": 23.1110, "lng": 113.2400, "category": "历史文化", "rating": 4.5, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 深圳 ===
    {"name": "世界之窗", "city": "深圳", "province": "广东省", "description": "大型文化旅游景区，汇集世界奇观、历史遗迹、古今名胜的微缩景观。埃菲尔铁塔、金字塔等尽收眼底。", "lat": 22.5370, "lng": 113.9730, "category": "主题乐园", "rating": 4.4, "visit_duration": 300, "ticket_price": 220, "need_reservation": False, "opening_hours": "09:00-22:00"},
    {"name": "欢乐谷", "city": "深圳", "province": "广东省", "description": "大型现代主题乐园，拥有100多个游乐项目。雪域雄鹰过山车和玛雅水公园是热门体验。", "lat": 22.5460, "lng": 113.9780, "category": "主题乐园", "rating": 4.5, "visit_duration": 360, "ticket_price": 230, "need_reservation": False, "opening_hours": "09:30-21:00"},
    {"name": "大鹏所城", "city": "深圳", "province": "广东省", "description": "明清两代抗击倭寇的海防要塞，深圳别称'鹏城'的由来。古城的青石板路和斑驳城墙诉说着600年海防史。", "lat": 22.5940, "lng": 114.4860, "category": "历史文化", "rating": 4.3, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 成都 ===
    {"name": "都江堰", "city": "成都", "province": "四川省", "description": "世界文化遗产，两千多年前李冰父子修建的水利工程至今仍灌溉成都平原，堪称世界水利史上奇迹。", "lat": 31.0010, "lng": 103.6130, "category": "历史文化", "rating": 4.7, "visit_duration": 180, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "青城山", "city": "成都", "province": "四川省", "description": "道教发源地之一，世界文化遗产。群峰环绕状若城郭，林木青翠终年常绿，素有'青城天下幽'美誉。", "lat": 30.8990, "lng": 103.5730, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "武侯祠", "city": "成都", "province": "四川省", "description": "纪念三国时期蜀汉丞相诸葛亮的祠堂，也是中国唯一君臣合祀的祠庙。锦里古街就在旁边。", "lat": 30.6450, "lng": 104.0474, "category": "历史文化", "rating": 4.6, "visit_duration": 90, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "杜甫草堂", "city": "成都", "province": "四川省", "description": "唐代诗圣杜甫流寓成都时的故居，在此创作了240余首诗篇。茅屋、花径、竹林充满诗情画意。", "lat": 30.6620, "lng": 104.0260, "category": "历史文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:00-18:00"},

    # === 重庆 ===
    {"name": "洪崖洞", "city": "重庆", "province": "重庆市", "description": "依山就势建造的吊脚楼群，夜晚灯火辉煌犹如宫崎骏《千与千寻》中的奇幻世界。", "lat": 29.5630, "lng": 106.5800, "category": "地标建筑", "rating": 4.7, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "全天开放"},
    {"name": "磁器口古镇", "city": "重庆", "province": "重庆市", "description": "千年古镇，重庆码头文化的缩影。青石板路上陈麻花飘香，茶馆里川剧变脸精彩纷呈。", "lat": 29.5820, "lng": 106.4500, "category": "历史文化", "rating": 4.5, "visit_duration": 150, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "大足石刻", "city": "重庆", "province": "重庆市", "description": "世界文化遗产，中国晚期石窟艺术的杰出代表。五万余尊造像雕刻精美，宝顶山千手观音令人震撼。", "lat": 29.7170, "lng": 105.7150, "category": "历史文化", "rating": 4.7, "visit_duration": 180, "ticket_price": 140, "need_reservation": False, "opening_hours": "08:30-17:30"},
    {"name": "武隆天生三桥", "city": "重庆", "province": "重庆市", "description": "世界自然遗产，三座天然石拱桥气势磅礴。《满城尽带黄金甲》和《变形金刚4》均在此取景。", "lat": 29.4290, "lng": 107.7930, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 125, "need_reservation": False, "opening_hours": "08:00-17:00"},

    # === 武汉 ===
    {"name": "黄鹤楼", "city": "武汉", "province": "湖北省", "description": "江南三大名楼之首，历代文人墨客登临题咏。崔颢的'昔人已乘黄鹤去'让黄鹤楼名垂千古。", "lat": 30.5447, "lng": 114.3027, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 70, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "湖北省博物馆", "city": "武汉", "province": "湖北省", "description": "拥有曾侯乙编钟、越王勾践剑等国宝级文物。编钟演奏厅每天有仿古乐舞表演。", "lat": 30.5621, "lng": 114.3655, "category": "博物馆", "rating": 4.7, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "东湖", "city": "武汉", "province": "湖北省", "description": "中国最大的城中湖，水域面积33平方公里。听涛、磨山、落雁、吹笛四大景区各具特色。", "lat": 30.5570, "lng": 114.3947, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 长沙 ===
    {"name": "岳麓山", "city": "长沙", "province": "湖南省", "description": "南岳衡山72峰之尾，千年学府岳麓书院坐落山脚。'停车坐爱枫林晚，霜叶红于二月花'说的就是这里。", "lat": 28.1850, "lng": 112.9350, "category": "自然风光", "rating": 4.6, "visit_duration": 180, "ticket_price": 0, "need_reservation": False, "opening_hours": "06:00-23:00"},
    {"name": "湖南省博物馆", "city": "长沙", "province": "湖南省", "description": "以马王堆汉墓出土文物闻名世界，千年女尸辛追夫人和素纱襌衣是镇馆之宝。", "lat": 28.2115, "lng": 112.9915, "category": "博物馆", "rating": 4.8, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "橘子洲", "city": "长沙", "province": "湖南省", "description": "湘江中的长条形沙洲，毛主席青年时代常在此游泳。洲头有巨大的毛泽东青年雕像，烟花表演震撼壮观。", "lat": 28.1830, "lng": 112.9648, "category": "自然风光", "rating": 4.6, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "07:00-22:00"},

    # === 张家界 ===
    {"name": "天门山", "city": "张家界", "province": "湖南省", "description": "张家界之魂，以世界最长高山客运索道和惊险的玻璃栈道著称。天门洞是世界最高海拔的天然穿山溶洞。", "lat": 29.1253, "lng": 110.4820, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 278, "need_reservation": True, "opening_hours": "08:00-17:00"},
    {"name": "张家界大峡谷", "city": "张家界", "province": "湖南省", "description": "拥有世界最高最长的玻璃桥，横跨峡谷两侧绝壁。峡谷内溪流潺潺、瀑布飞泻、植被茂密。", "lat": 29.3860, "lng": 110.6050, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 128, "need_reservation": False, "opening_hours": "08:30-17:00"},

    # === 郑州/洛阳/开封 ===
    {"name": "河南博物院", "city": "郑州", "province": "河南省", "description": "国家级重点博物馆，馆藏文物14万余件。以史前文物、商周青铜器、历代陶瓷器最具特色。", "lat": 34.7890, "lng": 113.6620, "category": "博物馆", "rating": 4.7, "visit_duration": 150, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "嵩山少林寺", "city": "郑州", "province": "河南省", "description": "禅宗祖庭、武术圣地。少林武术名扬天下，塔林、初祖庵和常住院展现悠久的佛教文化。", "lat": 34.5070, "lng": 112.9340, "category": "宗教文化", "rating": 4.6, "visit_duration": 240, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "清明上河园", "city": "开封", "province": "河南省", "description": "以张择端《清明上河图》为蓝本建造的大型宋代历史文化主题公园，再现北宋东京繁华盛景。", "lat": 34.7980, "lng": 114.3410, "category": "主题乐园", "rating": 4.5, "visit_duration": 240, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:30-18:00"},

    # === 济南 ===
    {"name": "趵突泉", "city": "济南", "province": "山东省", "description": "天下第一泉，济南七十二名泉之冠。泉水三股并发声如隐雷，乾隆皇帝御赐'天下第一泉'称号。", "lat": 36.6610, "lng": 117.0124, "category": "自然风光", "rating": 4.6, "visit_duration": 120, "ticket_price": 40, "need_reservation": False, "opening_hours": "07:00-19:00"},
    {"name": "大明湖", "city": "济南", "province": "山东省", "description": "济南三大名胜之一，'四面荷花三面柳，一城山色半城湖'描绘的就是大明湖的美景。", "lat": 36.6720, "lng": 117.0170, "category": "自然风光", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "06:00-21:00"},
    {"name": "泰山", "city": "泰安", "province": "山东省", "description": "五岳之首，世界文化与自然双重遗产。历代帝王封禅之地，'会当凌绝顶，一览众山小'即此。日出奇观令人终生难忘。", "lat": 36.2560, "lng": 117.1100, "category": "自然风光", "rating": 4.8, "visit_duration": 480, "ticket_price": 125, "need_reservation": True, "opening_hours": "全天开放"},

    # === 青岛 ===
    {"name": "栈桥", "city": "青岛", "province": "山东省", "description": "青岛的标志性建筑，440米的海上长廊尽头矗立着回澜阁。海鸥翔集，碧波拍岸，是感受青岛魅力的最佳地点。", "lat": 36.0605, "lng": 120.3190, "category": "地标建筑", "rating": 4.5, "visit_duration": 60, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "八大关", "city": "青岛", "province": "山东省", "description": "以长城的八个关隘命名的八条街道，汇集俄式、英式、法式等20多个国家的建筑风格，被誉为'万国建筑博览会'。", "lat": 36.0535, "lng": 120.3530, "category": "历史文化", "rating": 4.6, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "崂山", "city": "青岛", "province": "山东省", "description": "海上第一名山，道教名山。山海相连，道教宫观众多。崂山矿泉水闻名全国。", "lat": 36.1448, "lng": 120.6441, "category": "自然风光", "rating": 4.6, "visit_duration": 360, "ticket_price": 130, "need_reservation": False, "opening_hours": "06:00-19:00"},

    # === 厦门 ===
    {"name": "鼓浪屿", "city": "厦门", "province": "福建省", "description": "世界文化遗产，'海上花园'美誉。岛上钢琴声悠扬，万国建筑风格各异，日光岩上俯瞰鹭江美景。", "lat": 24.4470, "lng": 118.0690, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 50, "need_reservation": True, "opening_hours": "全天开放"},
    {"name": "南普陀寺", "city": "厦门", "province": "福建省", "description": "闽南佛教圣地，始建于唐代。背靠五老峰，面临鹭江，素斋远近闻名。毗邻厦门大学。", "lat": 24.4430, "lng": 118.0930, "category": "宗教文化", "rating": 4.5, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "曾厝垵", "city": "厦门", "province": "福建省", "description": "被誉为'中国最文艺渔村'，各色文创小店、特色民宿和美食摊位遍布小巷。", "lat": 24.4320, "lng": 118.1080, "category": "购物美食", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 昆明 ===
    {"name": "云南省博物馆", "city": "昆明", "province": "云南省", "description": "展示云南多民族文化和历史的大型博物馆。古滇国青铜器和少数民族服饰展最具特色。", "lat": 24.9520, "lng": 102.7310, "category": "博物馆", "rating": 4.4, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "翠湖公园", "city": "昆明", "province": "云南省", "description": "昆明的'城中碧玉'，冬季成千上万的红嘴鸥从西伯利亚飞来越冬，人鸥同乐的景象温暖人心。", "lat": 25.0440, "lng": 102.7060, "category": "自然风光", "rating": 4.5, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 大理 ===
    {"name": "崇圣寺三塔", "city": "大理", "province": "云南省", "description": "大理的标志性建筑，三座千年古塔矗立在苍山洱海之间。主塔千寻塔高69.13米，历经千年风雨地震仍巍然屹立。", "lat": 25.7040, "lng": 100.1420, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 75, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "苍山", "city": "大理", "province": "云南省", "description": "横亘大理西侧的雄伟山脉，十九峰十八溪。登苍山可俯瞰洱海全景，洗马潭和玉带路是经典游览路线。", "lat": 25.6540, "lng": 100.1070, "category": "自然风光", "rating": 4.6, "visit_duration": 360, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:30-17:00"},

    # === 丽江 ===
    {"name": "玉龙雪山", "city": "丽江", "province": "云南省", "description": "北半球最南端的雪山，13座雪峰连绵不绝宛若巨龙。冰川公园海拔4680米，蓝月谷湖水湛蓝如宝石。", "lat": 27.1045, "lng": 100.1970, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 130, "need_reservation": True, "opening_hours": "07:00-16:30"},
    {"name": "束河古镇", "city": "丽江", "province": "云南省", "description": "茶马古道上的重要驿站，比大研古城更加宁静质朴。九鼎龙潭清澈见底，纳西族传统建筑保存完好。", "lat": 26.9140, "lng": 100.2070, "category": "历史文化", "rating": 4.5, "visit_duration": 180, "ticket_price": 40, "need_reservation": False, "opening_hours": "全天开放"},

    # === 拉萨 ===
    {"name": "大昭寺", "city": "拉萨", "province": "西藏自治区", "description": "藏传佛教最神圣的寺庙，供奉释迦牟尼12岁等身像。寺前磕长头的虔诚朝圣者令人动容。", "lat": 29.6530, "lng": 91.1310, "category": "宗教文化", "rating": 4.8, "visit_duration": 120, "ticket_price": 85, "need_reservation": True, "opening_hours": "09:00-18:00"},
    {"name": "八廓街", "city": "拉萨", "province": "西藏自治区", "description": "围绕大昭寺的古老转经道，拉萨最繁华的商业街。转经的人流与特色店铺交织成独特的文化景观。", "lat": 29.6540, "lng": 91.1324, "category": "购物美食", "rating": 4.7, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "纳木错", "city": "拉萨", "province": "西藏自治区", "description": "西藏三大圣湖之一，世界上海拔最高的大型湖泊。湛蓝湖水与念青唐古拉雪山交相辉映，天地壮美。", "lat": 30.7100, "lng": 90.9000, "category": "自然风光", "rating": 4.8, "visit_duration": 300, "ticket_price": 120, "need_reservation": False, "opening_hours": "全天开放"},

    # === 贵阳 ===
    {"name": "黔灵山公园", "city": "贵阳", "province": "贵州省", "description": "贵阳的城市绿肺，以猕猴众多著称。山上弘福寺香火旺盛，山顶瞰筑亭可俯瞰贵阳全景。", "lat": 26.5990, "lng": 106.6960, "category": "自然风光", "rating": 4.4, "visit_duration": 150, "ticket_price": 5, "need_reservation": False, "opening_hours": "06:30-22:00"},
    {"name": "甲秀楼", "city": "贵阳", "province": "贵州省", "description": "贵阳标志性古建筑，建于南明河上。取'科甲挺秀'之意，夜景灯光璀璨最是迷人。", "lat": 26.5750, "lng": 106.7140, "category": "历史文化", "rating": 4.4, "visit_duration": 60, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 南昌 ===
    {"name": "滕王阁", "city": "南昌", "province": "江西省", "description": "江南三大名楼之一，因王勃《滕王阁序》'落霞与孤鹜齐飞，秋水共长天一色'而名垂千古。", "lat": 28.6850, "lng": 115.8760, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "江西省博物馆", "city": "南昌", "province": "江西省", "description": "收藏海昏侯墓出土金器万余件令人震撼，另有景德镇瓷器精品和客家文化展品。", "lat": 28.6810, "lng": 115.8770, "category": "博物馆", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},

    # === 合肥 ===
    {"name": "安徽省博物馆", "city": "合肥", "province": "安徽省", "description": "毛泽东唯一视察过的省级博物馆，收藏徽州文化、文房四宝和潘玉良画作等精品。", "lat": 31.8620, "lng": 117.2680, "category": "博物馆", "rating": 4.4, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "三河古镇", "city": "合肥", "province": "安徽省", "description": "国家5A级景区，典型的皖中水乡古镇。青石板街、古桥与小船组成了恬静的水墨画卷。", "lat": 31.4950, "lng": 117.2200, "category": "历史文化", "rating": 4.3, "visit_duration": 180, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 福州 ===
    {"name": "三坊七巷", "city": "福州", "province": "福建省", "description": "中国城市里坊制度的活化石，明清建筑博物馆。林则徐、冰心等名人故居坐落其中。", "lat": 26.0796, "lng": 119.2965, "category": "历史文化", "rating": 4.5, "visit_duration": 150, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "福建博物院", "city": "福州", "province": "福建省", "description": "收藏闽越国、海上丝绸之路和德化白瓷等文物精品，展示福建千年历史文化和海洋文明。", "lat": 26.0930, "lng": 119.2790, "category": "博物馆", "rating": 4.4, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},

    # === 兰州 ===
    {"name": "甘肃省博物馆", "city": "兰州", "province": "甘肃省", "description": "以'马踏飞燕'铜奔马闻名世界，丝绸之路文明展是了解丝路文化的最佳窗口。", "lat": 36.0600, "lng": 103.8243, "category": "博物馆", "rating": 4.6, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "白塔山公园", "city": "兰州", "province": "甘肃省", "description": "兰州城市地标，山顶白塔与黄河铁桥遥相呼应。登高远眺黄河穿城而过的壮美景色。", "lat": 36.0640, "lng": 103.8200, "category": "自然风光", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "06:00-20:00"},

    # === 敦煌 ===
    {"name": "鸣沙山月牙泉", "city": "敦煌", "province": "甘肃省", "description": "沙漠奇观，鸣沙山沙动成响，月牙泉千年不涸。骑骆驼穿越沙丘，大漠落日美不胜收。", "lat": 40.0860, "lng": 94.6720, "category": "自然风光", "rating": 4.7, "visit_duration": 240, "ticket_price": 120, "need_reservation": False, "opening_hours": "06:00-19:00"},
    {"name": "雅丹国家地质公园", "city": "敦煌", "province": "甘肃省", "description": "世界地质奇观，风蚀形成的雅丹地貌千姿百态。'魔鬼城'的怪石在大漠中矗立宛如外星世界。", "lat": 40.5180, "lng": 93.2030, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 80, "need_reservation": False, "opening_hours": "06:00-19:00"},

    # === 乌鲁木齐 ===
    {"name": "新疆维吾尔自治区博物馆", "city": "乌鲁木齐", "province": "新疆维吾尔自治区", "description": "收藏丝路文物和古代干尸闻名。'楼兰美女'干尸和唐代绢画是镇馆之宝。", "lat": 43.8200, "lng": 87.5840, "category": "博物馆", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "10:00-18:00"},
    {"name": "天山天池", "city": "乌鲁木齐", "province": "新疆维吾尔自治区", "description": "世界自然遗产，高山冰碛湖。雪山环抱中一池碧水，古称'瑶池'，传说是西王母的沐浴之地。", "lat": 43.8970, "lng": 88.1310, "category": "自然风光", "rating": 4.7, "visit_duration": 300, "ticket_price": 155, "need_reservation": False, "opening_hours": "08:30-19:00"},

    # === 喀纳斯 ===
    {"name": "喀纳斯湖", "city": "阿勒泰", "province": "新疆维吾尔自治区", "description": "中国最美湖泊之一，湖水随季节变化呈现不同色彩。神秘的'湖怪'传说和金秋白桦林吸引了无数旅行者。", "lat": 48.8120, "lng": 87.0420, "category": "自然风光", "rating": 4.8, "visit_duration": 360, "ticket_price": 230, "need_reservation": True, "opening_hours": "08:00-19:00"},

    # === 西宁 ===
    {"name": "塔尔寺", "city": "西宁", "province": "青海省", "description": "藏传佛教格鲁派六大寺院之一，宗喀巴大师诞生地。酥油花、壁画和堆绣被称为'塔尔寺三绝'。", "lat": 36.4930, "lng": 101.5900, "category": "宗教文化", "rating": 4.6, "visit_duration": 150, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "青海省博物馆", "city": "西宁", "province": "青海省", "description": "展示青海高原历史文化和多民族风情，彩陶和唐卡收藏极为丰富。", "lat": 36.6270, "lng": 101.7750, "category": "博物馆", "rating": 4.4, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-17:00"},

    # === 银川 ===
    {"name": "西夏王陵", "city": "银川", "province": "宁夏回族自治区", "description": "西夏历代帝王陵墓群，有'东方金字塔'之称。巨大的夯土陵台在贺兰山脚下绵延分布，神秘壮观。", "lat": 38.4350, "lng": 105.9900, "category": "历史文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 75, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "宁夏博物馆", "city": "银川", "province": "宁夏回族自治区", "description": "展示西夏文明和回族文化的大型博物馆，西夏鎏金铜牛是国家一级文物。", "lat": 38.4830, "lng": 106.2390, "category": "博物馆", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-17:00"},

    # === 呼和浩特 ===
    {"name": "内蒙古博物院", "city": "呼和浩特", "province": "内蒙古自治区", "description": "了解蒙古族历史文化和草原文明的最佳场所。巨大的恐龙化石和匈奴王金冠最为著名。", "lat": 40.8270, "lng": 111.7490, "category": "博物馆", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-17:00"},
    {"name": "昭君墓", "city": "呼和浩特", "province": "内蒙古自治区", "description": "汉代王昭君的青冢，'一去紫台连朔漠，独留青冢向黄昏'。景区展现匈奴与汉朝和亲的历史。", "lat": 40.7060, "lng": 111.6770, "category": "历史文化", "rating": 4.3, "visit_duration": 90, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:30-17:30"},

    # === 哈尔滨 ===
    {"name": "冰雪大世界", "city": "哈尔滨", "province": "黑龙江省", "description": "世界最大的冰雪主题乐园，每年冬季用冰雪打造梦幻城堡和巨型雕塑。冰灯光影流转宛如仙境。", "lat": 45.7790, "lng": 126.6070, "category": "主题乐园", "rating": 4.8, "visit_duration": 240, "ticket_price": 330, "need_reservation": False, "opening_hours": "11:00-21:30"},
    {"name": "黑龙江省博物馆", "city": "哈尔滨", "province": "黑龙江省", "description": "收藏黑龙江流域历史文物和自然标本，展示东北古代民族文化和俄罗斯风情。", "lat": 45.7560, "lng": 126.6410, "category": "博物馆", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-16:30"},

    # === 长春 ===
    {"name": "伪满皇宫博物院", "city": "长春", "province": "吉林省", "description": "清末代皇帝溥仪充当伪满洲国傀儡皇帝时的宫廷遗址。中西合璧的建筑风格记录了那段特殊历史。", "lat": 43.9040, "lng": 125.3500, "category": "博物馆", "rating": 4.5, "visit_duration": 150, "ticket_price": 70, "need_reservation": False, "opening_hours": "08:30-16:30"},
    {"name": "净月潭", "city": "长春", "province": "吉林省", "description": "国家5A级景区，亚洲最大的人工林海。森林覆盖率达96%，是长春的天然氧吧和滑雪胜地。", "lat": 43.7870, "lng": 125.4530, "category": "自然风光", "rating": 4.4, "visit_duration": 180, "ticket_price": 30, "need_reservation": False, "opening_hours": "06:00-19:00"},

    # === 沈阳 ===
    {"name": "沈阳故宫", "city": "沈阳", "province": "辽宁省", "description": "中国仅存的两座完整皇家宫殿建筑群之一，清入关前的皇宫。融合满、汉、蒙古族建筑风格。", "lat": 41.7960, "lng": 123.4510, "category": "历史文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:30-17:00"},
    {"name": "辽宁省博物馆", "city": "沈阳", "province": "辽宁省", "description": "新中国第一座博物馆，馆藏晋唐宋元书画名迹和辽瓷精品。", "lat": 41.8040, "lng": 123.4220, "category": "博物馆", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "张氏帅府", "city": "沈阳", "province": "辽宁省", "description": "张作霖、张学良父子的官邸和私宅，见证了许多近代重大历史事件。大青楼和小青楼建筑别具一格。", "lat": 41.7910, "lng": 123.4550, "category": "历史文化", "rating": 4.4, "visit_duration": 90, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:30-17:00"},

    # === 大连 ===
    {"name": "老虎滩海洋公园", "city": "大连", "province": "辽宁省", "description": "国家5A级景区，中国最大的海洋主题公园之一。极地馆的企鹅和白鲸表演最受欢迎。", "lat": 38.8720, "lng": 121.6750, "category": "主题乐园", "rating": 4.5, "visit_duration": 300, "ticket_price": 220, "need_reservation": False, "opening_hours": "08:30-17:00"},
    {"name": "金石滩", "city": "大连", "province": "辽宁省", "description": "国家5A级景区，拥有独特的海滨喀斯特地貌。金色沙滩延绵数公里，是北方最佳海滨度假地之一。", "lat": 39.0800, "lng": 121.9900, "category": "自然风光", "rating": 4.4, "visit_duration": 300, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:00"},

    # === 南宁 ===
    {"name": "青秀山", "city": "南宁", "province": "广西壮族自治区", "description": "南宁的城市绿肺，国家5A级景区。热带植物茂密，龙象塔矗立山顶可俯瞰邕江和市区风光。", "lat": 22.7880, "lng": 108.3870, "category": "自然风光", "rating": 4.4, "visit_duration": 180, "ticket_price": 20, "need_reservation": False, "opening_hours": "07:00-18:00"},
    {"name": "广西壮族自治区博物馆", "city": "南宁", "province": "广西壮族自治区", "description": "展示广西历史文化与民族风情的综合性博物馆。铜鼓和壮族文化陈列最具特色。", "lat": 22.8150, "lng": 108.3700, "category": "博物馆", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-17:00"},

    # === 海口 ===
    {"name": "海南省博物馆", "city": "海口", "province": "海南省", "description": "展示海南岛历史文化和海洋文明的博物馆。南海水下考古和黎族文化是特色展览。", "lat": 20.0130, "lng": 110.3650, "category": "博物馆", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "09:00-17:00"},
    {"name": "骑楼老街", "city": "海口", "province": "海南省", "description": "中国保存最完整的南洋风格骑楼建筑群。百年骑楼下茶香与咖啡香交织，充满南洋风情。", "lat": 20.0380, "lng": 110.3390, "category": "历史文化", "rating": 4.3, "visit_duration": 90, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 太原 ===
    {"name": "山西博物院", "city": "太原", "province": "山西省", "description": "以'晋魂'为主题，收藏晋国青铜器、北朝壁画和佛教造像极其丰富。鸟尊是镇馆之宝。", "lat": 37.8620, "lng": 112.5290, "category": "博物馆", "rating": 4.6, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-17:00"},
    {"name": "晋祠", "city": "太原", "province": "山西省", "description": "中国现存最早的皇家祭祀园林，圣母殿内的宋代彩塑侍女像栩栩如生，难老泉千年不竭。", "lat": 37.7100, "lng": 112.4310, "category": "历史文化", "rating": 4.6, "visit_duration": 150, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},

    # === 平遥 ===
    {"name": "平遥古城", "city": "晋中", "province": "山西省", "description": "世界文化遗产，中国保存最完整的四大古城之一。城墙、票号和明清街市完整展现了明清县城风貌。", "lat": 37.2010, "lng": 112.1770, "category": "历史文化", "rating": 4.7, "visit_duration": 360, "ticket_price": 125, "need_reservation": False, "opening_hours": "08:00-17:30"},

    # === 大同 ===
    {"name": "华严寺", "city": "大同", "province": "山西省", "description": "辽代皇家寺院，大雄宝殿为现存最大的辽金佛殿。薄伽教藏殿内的'天宫楼阁'和合掌露齿菩萨为艺术精品。", "lat": 40.0910, "lng": 113.2990, "category": "宗教文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 50, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "悬空寺", "city": "大同", "province": "山西省", "description": "世界十大奇险建筑之一，寺庙悬于恒山峭壁之上已1500余年。三教合一的独特宗教文化令人称奇。", "lat": 39.6660, "lng": 113.7130, "category": "宗教文化", "rating": 4.7, "visit_duration": 120, "ticket_price": 130, "need_reservation": False, "opening_hours": "08:00-17:00"},

    # === 无锡 ===
    {"name": "灵山大佛", "city": "无锡", "province": "江苏省", "description": "世界最高的青铜立佛，高88米。九龙灌浴动态音乐群雕壮观无比，梵宫内部金碧辉煌。", "lat": 31.4320, "lng": 120.1080, "category": "宗教文化", "rating": 4.6, "visit_duration": 240, "ticket_price": 210, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "鼋头渚", "city": "无锡", "province": "江苏省", "description": "太湖第一名胜，郭沫若赞曰'太湖佳绝处，毕竟在鼋头'。春季樱花如云，秋季渔帆点点。", "lat": 31.5280, "lng": 120.2340, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 105, "need_reservation": False, "opening_hours": "08:00-16:30"},

    # === 扬州 ===
    {"name": "瘦西湖", "city": "扬州", "province": "江苏省", "description": "国家5A级景区，'烟花三月下扬州'的最佳诠释。长堤春柳、五亭桥和二十四桥构成经典江南画卷。", "lat": 32.4090, "lng": 119.4200, "category": "自然风光", "rating": 4.6, "visit_duration": 180, "ticket_price": 100, "need_reservation": False, "opening_hours": "07:00-17:30"},

    # === 宁波 ===
    {"name": "天一阁", "city": "宁波", "province": "浙江省", "description": "中国现存最早的私家藏书楼，距今450余年。藏书文化深厚，园林建筑古朴雅致。", "lat": 29.8720, "lng": 121.5390, "category": "博物馆", "rating": 4.5, "visit_duration": 90, "ticket_price": 30, "need_reservation": False, "opening_hours": "08:30-17:00"},
    {"name": "溪口雪窦山", "city": "宁波", "province": "浙江省", "description": "国家5A级景区，蒋介石故里。雪窦寺是中国佛教五大名山之一，千丈岩瀑布飞流直下。", "lat": 29.6800, "lng": 121.2000, "category": "自然风光", "rating": 4.4, "visit_duration": 240, "ticket_price": 150, "need_reservation": False, "opening_hours": "08:00-16:30"},

    # === 温州 ===
    {"name": "雁荡山", "city": "温州", "province": "浙江省", "description": "世界地质公园，以奇峰怪石、飞瀑流泉著称。灵峰夜景堪称一绝，大龙湫瀑布高197米气势磅礴。", "lat": 28.3670, "lng": 121.0730, "category": "自然风光", "rating": 4.5, "visit_duration": 300, "ticket_price": 160, "need_reservation": False, "opening_hours": "08:00-17:00"},

    # === 天津 ===
    {"name": "天津之眼", "city": "天津", "province": "天津市", "description": "世界上唯一建在桥上的摩天轮，高达120米。乘坐可俯瞰海河两岸风光和天津城市全景。", "lat": 39.1530, "lng": 117.1850, "category": "现代建筑", "rating": 4.4, "visit_duration": 60, "ticket_price": 70, "need_reservation": False, "opening_hours": "09:30-21:30"},
    {"name": "天津博物馆", "city": "天津", "province": "天津市", "description": "展示天津历史文化和艺术的大型博物馆。馆藏雪景寒林图和太保鼎等珍贵文物。", "lat": 39.0840, "lng": 117.2030, "category": "博物馆", "rating": 4.4, "visit_duration": 120, "ticket_price": 0, "need_reservation": True, "opening_hours": "09:00-16:30"},
    {"name": "五大道", "city": "天津", "province": "天津市", "description": "中国保留最完整的洋楼建筑群，汇集英、法、意、德、西班牙等国风格建筑2000余栋。", "lat": 39.1100, "lng": 117.2010, "category": "历史文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},

    # === 更多5A/4A景区 ===
    {"name": "九华山", "city": "池州", "province": "安徽省", "description": "中国佛教四大名山之一，地藏菩萨道场。99座山峰形似莲花，古刹林立香火鼎盛。", "lat": 30.4900, "lng": 117.8250, "category": "宗教文化", "rating": 4.6, "visit_duration": 360, "ticket_price": 190, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "三清山", "city": "上饶", "province": "江西省", "description": "世界自然遗产，道教名山。奇特的峰林地貌和花岗岩造型石令人叹为观止，云海日出堪称一绝。", "lat": 28.9200, "lng": 118.0730, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 150, "need_reservation": False, "opening_hours": "07:00-17:00"},
    {"name": "婺源", "city": "上饶", "province": "江西省", "description": "中国最美乡村，春季油菜花海漫山遍野。篁岭的晒秋和徽派古村落是摄影师的最爱。", "lat": 29.2540, "lng": 117.8650, "category": "自然风光", "rating": 4.6, "visit_duration": 360, "ticket_price": 150, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "井冈山", "city": "吉安", "province": "江西省", "description": "中国革命摇篮，国家5A级景区。红色历史与绿色生态交相辉映，黄洋界和茨坪最具代表性。", "lat": 26.5700, "lng": 114.1670, "category": "历史文化", "rating": 4.5, "visit_duration": 360, "ticket_price": 190, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "岳阳楼", "city": "岳阳", "province": "湖南省", "description": "江南三大名楼之一，范仲淹《岳阳楼记》'先天下之忧而忧，后天下之乐而乐'让此楼名垂千古。", "lat": 29.3830, "lng": 113.0880, "category": "历史文化", "rating": 4.5, "visit_duration": 90, "ticket_price": 70, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "衡山", "city": "衡阳", "province": "湖南省", "description": "五岳之南岳，以'独秀'闻名。祝融峰高耸入云，南岳大庙千年香火不断。雾凇雪景堪称一绝。", "lat": 27.2530, "lng": 112.7170, "category": "自然风光", "rating": 4.5, "visit_duration": 360, "ticket_price": 120, "need_reservation": False, "opening_hours": "07:00-17:30"},
    {"name": "丹霞山", "city": "韶关", "province": "广东省", "description": "世界自然遗产，丹霞地貌的命名地。红色砂岩经亿万年风化形成奇特造型，阳元石和阴元石最为著名。", "lat": 25.0330, "lng": 113.7420, "category": "自然风光", "rating": 4.5, "visit_duration": 240, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "七星岩", "city": "肇庆", "province": "广东省", "description": "国家5A级景区，七座石灰岩山峰如北斗七星排列在星湖之上。被誉为'岭南第一奇观'。", "lat": 23.0730, "lng": 112.4650, "category": "自然风光", "rating": 4.4, "visit_duration": 180, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "黄果树瀑布", "city": "安顺", "province": "贵州省", "description": "亚洲最大的瀑布群，主瀑高77.8米宽101米。水帘洞从瀑布背后穿行可触及飞瀑激流。", "lat": 25.9917, "lng": 105.6670, "category": "自然风光", "rating": 4.7, "visit_duration": 240, "ticket_price": 180, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "梵净山", "city": "铜仁", "province": "贵州省", "description": "世界自然遗产，佛教名山。蘑菇石和红云金顶是标志景观，云海日出佛光令人心醉。", "lat": 27.9320, "lng": 108.7180, "category": "自然风光", "rating": 4.6, "visit_duration": 360, "ticket_price": 120, "need_reservation": True, "opening_hours": "08:00-17:00"},
    {"name": "小七孔", "city": "黔南", "province": "贵州省", "description": "世界自然遗产荔波喀斯特的核心景区。碧水、瀑布、水上森林组成了一幅幅绝美的自然画卷。", "lat": 25.3520, "lng": 107.8220, "category": "自然风光", "rating": 4.7, "visit_duration": 300, "ticket_price": 130, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "西江千户苗寨", "city": "黔东南", "province": "贵州省", "description": "世界最大的苗族聚居村寨，千余户吊脚楼依山而建。苗年节、长桌宴和银饰服饰文化魅力无穷。", "lat": 26.4980, "lng": 108.1750, "category": "历史文化", "rating": 4.6, "visit_duration": 300, "ticket_price": 90, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "峨眉山", "city": "乐山", "province": "四川省", "description": "中国佛教四大名山之一，普贤菩萨道场。金顶十方普贤金像壮观，云海日出佛光令人神往。", "lat": 29.5240, "lng": 103.3370, "category": "自然风光", "rating": 4.7, "visit_duration": 480, "ticket_price": 160, "need_reservation": True, "opening_hours": "07:00-16:00"},
    {"name": "乐山大佛", "city": "乐山", "province": "四川省", "description": "世界最大的石刻弥勒佛坐像，高71米。开凿于唐代历时90年完工，'山是一尊佛，佛是一座山'。", "lat": 29.5460, "lng": 103.7750, "category": "历史文化", "rating": 4.7, "visit_duration": 120, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "九寨沟", "city": "阿坝", "province": "四川省", "description": "世界自然遗产，童话世界般的绝美风光。五花海、诺日朗瀑布和五彩池以其斑斓色彩惊艳世人。", "lat": 33.2630, "lng": 103.9000, "category": "自然风光", "rating": 4.9, "visit_duration": 480, "ticket_price": 169, "need_reservation": True, "opening_hours": "08:00-17:00"},
    {"name": "黄龙", "city": "阿坝", "province": "四川省", "description": "世界自然遗产，以钙华彩池闻名。五彩池层层叠叠如梯田般分布，雪山、森林、彩池构成绝美画卷。", "lat": 32.7300, "lng": 103.8300, "category": "自然风光", "rating": 4.7, "visit_duration": 300, "ticket_price": 170, "need_reservation": True, "opening_hours": "08:00-17:00"},
    {"name": "稻城亚丁", "city": "甘孜", "province": "四川省", "description": "被誉为'蓝色星球上最后一片净土'。三座神山仙乃日、央迈勇、夏诺多吉守护着这片世外桃源。", "lat": 28.4840, "lng": 100.3480, "category": "自然风光", "rating": 4.8, "visit_duration": 480, "ticket_price": 146, "need_reservation": True, "opening_hours": "07:00-17:00"},
    {"name": "香格里拉普达措", "city": "迪庆", "province": "云南省", "description": "国家5A级景区，拥有高原湖泊、牧场、雪山和湿地。属都湖和碧塔海是《消失的地平线》中的仙境。", "lat": 27.8210, "lng": 99.9990, "category": "自然风光", "rating": 4.6, "visit_duration": 300, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "梅里雪山", "city": "迪庆", "province": "云南省", "description": "藏区八大神山之首，主峰卡瓦格博海拔6740米至今无人登顶。'日照金山'是世人向往的绝景。", "lat": 28.4390, "lng": 98.6840, "category": "自然风光", "rating": 4.8, "visit_duration": 300, "ticket_price": 150, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "西双版纳热带植物园", "city": "西双版纳", "province": "云南省", "description": "国家5A级景区，中国面积最大、植物种类最多的植物园。收集热带植物13000余种。", "lat": 21.9350, "lng": 101.2520, "category": "自然风光", "rating": 4.6, "visit_duration": 240, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "野象谷", "city": "西双版纳", "province": "云南省", "description": "亚洲野象频繁出没的热带雨林。高空观象栈道可安全观察野象，蝴蝶园和百鸟园乐趣无穷。", "lat": 22.1040, "lng": 100.8670, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "元阳梯田", "city": "红河", "province": "云南省", "description": "世界文化遗产，哈尼族人千百年来在哀牢山上开垦的农耕奇迹。日出日落时分水面如镜金光璀璨。", "lat": 23.1470, "lng": 102.7460, "category": "自然风光", "rating": 4.7, "visit_duration": 300, "ticket_price": 100, "need_reservation": False, "opening_hours": "06:00-19:00"},
    {"name": "土楼", "city": "龙岩", "province": "福建省", "description": "世界文化遗产，客家民居的杰出代表。永定土楼群以承启楼最为壮观，'四菜一汤'布局别具匠心。", "lat": 24.6020, "lng": 117.0200, "category": "历史文化", "rating": 4.6, "visit_duration": 180, "ticket_price": 90, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "武夷山", "city": "南平", "province": "福建省", "description": "世界文化与自然双重遗产。九曲溪竹筏漂流和天游峰是最经典的体验，大红袍母树举世闻名。", "lat": 27.6700, "lng": 117.9700, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 140, "need_reservation": True, "opening_hours": "07:00-17:00"},
    {"name": "泰山", "city": "泰安", "province": "山东省", "description": "五岳之首，世界文化与自然双重遗产。历代帝王封禅之地，日出奇观令人终生难忘。", "lat": 36.2560, "lng": 117.1100, "category": "自然风光", "rating": 4.8, "visit_duration": 480, "ticket_price": 125, "need_reservation": True, "opening_hours": "全天开放"},
    {"name": "曲阜三孔", "city": "济宁", "province": "山东省", "description": "世界文化遗产，包括孔庙、孔府和孔林。儒家文化的圣地，祭祀孔子的至圣庙气势恢宏。", "lat": 35.5970, "lng": 116.9880, "category": "历史文化", "rating": 4.6, "visit_duration": 240, "ticket_price": 140, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "蓬莱阁", "city": "烟台", "province": "山东省", "description": "中国古代四大名楼之一，八仙过海传说发源地。海市蜃楼奇观和海滨风光令人流连忘返。", "lat": 37.8180, "lng": 120.7530, "category": "历史文化", "rating": 4.5, "visit_duration": 150, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "承德避暑山庄", "city": "承德", "province": "河北省", "description": "世界文化遗产，清代皇帝的夏宫。中国现存最大的皇家园林，融合南北园林艺术精华。", "lat": 40.9870, "lng": 117.9380, "category": "园林古迹", "rating": 4.6, "visit_duration": 240, "ticket_price": 130, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "山海关", "city": "秦皇岛", "province": "河北省", "description": "明长城东端起点，有'天下第一关'之称。老龙头长城入海处尤为壮观。", "lat": 40.0090, "lng": 119.7570, "category": "历史文化", "rating": 4.5, "visit_duration": 150, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "北戴河", "city": "秦皇岛", "province": "河北省", "description": "中国四大避暑胜地之一，拥有金色沙滩和碧蓝海水。鸽子窝公园日出是经典景观。", "lat": 39.8220, "lng": 119.5060, "category": "自然风光", "rating": 4.4, "visit_duration": 180, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "华山", "city": "渭南", "province": "陕西省", "description": "五岳之西岳，以'险'闻名天下。长空栈道和鹞子翻身是勇敢者的挑战，论剑处留下金庸武侠的印记。", "lat": 34.4800, "lng": 110.0820, "category": "自然风光", "rating": 4.7, "visit_duration": 480, "ticket_price": 160, "need_reservation": True, "opening_hours": "07:00-19:00"},
    {"name": "壶口瀑布", "city": "延安", "province": "陕西省", "description": "世界最大的黄色瀑布，黄河水从300米宽的河面骤然收束倾泻而下。气势磅礴如万马奔腾。", "lat": 36.1480, "lng": 110.4420, "category": "自然风光", "rating": 4.6, "visit_duration": 120, "ticket_price": 90, "need_reservation": False, "opening_hours": "07:00-18:00"},
    {"name": "莫高窟", "city": "敦煌", "province": "甘肃省", "description": "世界文化遗产，世界上现存规模最大的佛教艺术宝库。735个洞窟中保存着精美壁画和彩塑，飞天壁画惊艳千年。", "lat": 40.0420, "lng": 94.8060, "category": "历史文化", "rating": 4.9, "visit_duration": 240, "ticket_price": 238, "need_reservation": True, "opening_hours": "08:00-18:00"},
    {"name": "张掖丹霞", "city": "张掖", "province": "甘肃省", "description": "世界地质公园，中国最美丹霞地貌之一。彩色丘陵如画家打翻的调色盘，日落时色如渥丹灿若明霞。", "lat": 38.9380, "lng": 100.0320, "category": "自然风光", "rating": 4.6, "visit_duration": 180, "ticket_price": 75, "need_reservation": False, "opening_hours": "07:00-19:00"},
    {"name": "嘉峪关", "city": "嘉峪关", "province": "甘肃省", "description": "明长城西端起点，有'天下第一雄关'之称。关城建筑保存完整，大漠雄关令人追忆丝路辉煌。", "lat": 39.8010, "lng": 98.2180, "category": "历史文化", "rating": 4.5, "visit_duration": 120, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:30-18:00"},
    {"name": "沙坡头", "city": "中卫", "province": "宁夏回族自治区", "description": "国家5A级景区，集大漠、黄河、高山、绿洲于一体。骑骆驼穿越腾格里沙漠，滑沙体验惊险刺激。", "lat": 37.4600, "lng": 105.0130, "category": "自然风光", "rating": 4.5, "visit_duration": 240, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "华山长空栈道", "city": "渭南", "province": "陕西省", "description": "华山南峰东侧山腰的险道，以悬崖上的木栈道闻名，'华山第一险'之称。", "lat": 34.4630, "lng": 110.0750, "category": "自然风光", "rating": 4.8, "visit_duration": 30, "ticket_price": 0, "need_reservation": False, "opening_hours": "07:00-19:00"},
    {"name": "宏村西递", "city": "黄山", "province": "安徽省", "description": "世界文化遗产徽州古村落。宏村月沼和南湖倒影，西递精美砖雕石雕，共同构成徽派建筑精华。", "lat": 29.9927, "lng": 117.9890, "category": "历史文化", "rating": 4.7, "visit_duration": 240, "ticket_price": 104, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "镜泊湖", "city": "牡丹江", "province": "黑龙江省", "description": "中国最大的高山堰塞湖，世界地质公园。吊水楼瀑布是中国最宽的火山瀑布，冬季冰瀑奇观震撼。", "lat": 43.8350, "lng": 128.8730, "category": "自然风光", "rating": 4.5, "visit_duration": 240, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "五大连池", "city": "黑河", "province": "黑龙江省", "description": "世界地质公园，中国最年轻的火山群。五个相连的火山堰塞湖如明珠镶嵌在火山地貌中。", "lat": 48.6560, "lng": 126.1160, "category": "自然风光", "rating": 4.4, "visit_duration": 300, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "长白山天池", "city": "延边", "province": "吉林省", "description": "中国最深的湖泊，中朝界湖。16座山峰环抱一池碧水，天池水怪传说增添神秘色彩。", "lat": 42.0070, "lng": 128.0570, "category": "自然风光", "rating": 4.7, "visit_duration": 240, "ticket_price": 125, "need_reservation": True, "opening_hours": "07:00-16:00"},
    {"name": "本溪水洞", "city": "本溪", "province": "辽宁省", "description": "世界最长可乘船游览的地下暗河，国家5A级景区。洞内钟乳石千姿百态，灯光下宛如地下仙宫。", "lat": 41.2980, "lng": 124.0900, "category": "自然风光", "rating": 4.4, "visit_duration": 150, "ticket_price": 130, "need_reservation": False, "opening_hours": "08:30-16:30"},
    {"name": "凤凰古城", "city": "湘西", "province": "湖南省", "description": "中国最美小城之一，沈从文笔下的边城。沱江两岸吊脚楼和虹桥风雨楼构成了一幅绝美的湘西风情画。", "lat": 27.9480, "lng": 109.5990, "category": "历史文化", "rating": 4.5, "visit_duration": 240, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "武当山", "city": "十堰", "province": "湖北省", "description": "世界文化遗产，道教圣地。张三丰创立武当派之地，古建筑群规模宏大，紫霄宫和金顶最为壮观。", "lat": 32.4000, "lng": 111.0040, "category": "宗教文化", "rating": 4.6, "visit_duration": 360, "ticket_price": 140, "need_reservation": False, "opening_hours": "07:30-17:30"},
    {"name": "三峡大坝", "city": "宜昌", "province": "湖北省", "description": "世界最大的水利枢纽工程，国家5A级景区。坛子岭可俯瞰五级船闸和三峡大坝全貌。", "lat": 30.8076, "lng": 111.0040, "category": "现代建筑", "rating": 4.4, "visit_duration": 180, "ticket_price": 0, "need_reservation": True, "opening_hours": "08:00-17:00"},
    {"name": "恩施大峡谷", "city": "恩施", "province": "湖北省", "description": "媲美美国科罗拉多大峡谷的自然奇观。一炷香石柱和云龙地缝是核心景观，绝壁栈道令人心惊。", "lat": 30.2980, "lng": 109.5030, "category": "自然风光", "rating": 4.6, "visit_duration": 300, "ticket_price": 170, "need_reservation": False, "opening_hours": "08:00-16:00"},
    {"name": "庐山", "city": "九江", "province": "江西省", "description": "世界文化景观遗产，以雄、奇、险、秀闻名。历代文人留下四千余首诗词，三叠泉瀑布最为壮观。", "lat": 29.5670, "lng": 115.9810, "category": "自然风光", "rating": 4.6, "visit_duration": 360, "ticket_price": 180, "need_reservation": False, "opening_hours": "06:00-18:00"},
    {"name": "龙门石窟", "city": "洛阳", "province": "河南省", "description": "世界文化遗产，中国石刻艺术最高峰。伊河两岸2300余个窟龛10万余尊造像，卢舍那大佛最令人震撼。", "lat": 34.5600, "lng": 112.4740, "category": "历史文化", "rating": 4.7, "visit_duration": 180, "ticket_price": 90, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "云台山", "city": "焦作", "province": "河南省", "description": "世界地质公园，国家5A级景区。红石峡丹崖碧水令人惊艳，茱萸峰是王维'遍插茱萸少一人'的灵感来源。", "lat": 35.4520, "lng": 113.3770, "category": "自然风光", "rating": 4.6, "visit_duration": 300, "ticket_price": 180, "need_reservation": False, "opening_hours": "07:00-17:00"},
    {"name": "老君山", "city": "洛阳", "province": "河南省", "description": "道教圣地，老子归隐修炼处。金顶道观群在云雾中若隐若现，十里画屏栈道步步是景。", "lat": 33.7290, "lng": 111.6180, "category": "自然风光", "rating": 4.7, "visit_duration": 300, "ticket_price": 100, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "黄鹤楼", "city": "武汉", "province": "湖北省", "description": "江南三大名楼之首，'昔人已乘黄鹤去，此地空余黄鹤楼'。登楼远眺长江大桥和龟山电视塔尽收眼底。", "lat": 30.5447, "lng": 114.3027, "category": "历史文化", "rating": 4.6, "visit_duration": 120, "ticket_price": 70, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "兵马俑", "city": "西安", "province": "陕西省", "description": "世界第八大奇迹，秦始皇陵的陪葬坑。数千件与真人等大的陶俑陶马排列成阵，气势磅礴令人震撼。", "lat": 34.3849, "lng": 109.2730, "category": "历史文化", "rating": 4.9, "visit_duration": 180, "ticket_price": 120, "need_reservation": True, "opening_hours": "08:30-17:00"},
    {"name": "莫高窟藏经洞", "city": "敦煌", "province": "甘肃省", "description": "1900年王道士发现的藏经洞，出土5万余件珍贵文书和绢画，催生了敦煌学的诞生。", "lat": 40.0420, "lng": 94.8060, "category": "历史文化", "rating": 4.9, "visit_duration": 30, "ticket_price": 0, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "珠穆朗玛峰大本营", "city": "日喀则", "province": "西藏自治区", "description": "世界之巅的朝圣之地，海拔5200米的营地可近距离仰望珠峰雄伟身姿。", "lat": 28.1360, "lng": 86.8600, "category": "自然风光", "rating": 4.9, "visit_duration": 120, "ticket_price": 180, "need_reservation": True, "opening_hours": "全天开放"},
    {"name": "冈仁波齐", "city": "阿里", "province": "西藏自治区", "description": "藏传佛教、印度教和苯教公认的世界中心。金字塔状的山峰终年积雪，转山朝圣者络绎不绝。", "lat": 31.0680, "lng": 81.3130, "category": "宗教文化", "rating": 4.9, "visit_duration": 360, "ticket_price": 150, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "雅鲁藏布大峡谷", "city": "林芝", "province": "西藏自治区", "description": "世界第一大峡谷，最深达6009米。南迦巴瓦峰和雅鲁藏布江大拐弯构成令人震撼的自然奇观。", "lat": 29.6000, "lng": 94.9000, "category": "自然风光", "rating": 4.7, "visit_duration": 480, "ticket_price": 150, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "可可西里", "city": "玉树", "province": "青海省", "description": "世界自然遗产，中国最大的无人区。藏羚羊、藏野驴等珍稀动物在广袤高原上自由奔跑。", "lat": 35.3000, "lng": 93.3000, "category": "自然风光", "rating": 4.7, "visit_duration": 480, "ticket_price": 0, "need_reservation": True, "opening_hours": "全天开放"},
    {"name": "茶卡盐湖", "city": "海西", "province": "青海省", "description": "中国的'天空之镜'，湖面如镜倒映天空云彩和远山。小火车穿行盐湖的画面是青藏高原最经典的风景。", "lat": 36.7900, "lng": 99.0800, "category": "自然风光", "rating": 4.6, "visit_duration": 180, "ticket_price": 70, "need_reservation": False, "opening_hours": "07:00-18:30"},
    {"name": "那拉提草原", "city": "伊犁", "province": "新疆维吾尔自治区", "description": "世界四大草原之一，'空中草原'美誉。夏季野花遍地，雪山森林草甸构成了东方瑞士般的绝美风光。", "lat": 43.3230, "lng": 84.0980, "category": "自然风光", "rating": 4.7, "visit_duration": 360, "ticket_price": 95, "need_reservation": False, "opening_hours": "08:00-20:00"},
    {"name": "赛里木湖", "city": "博尔塔拉", "province": "新疆维吾尔自治区", "description": "新疆海拔最高面积最大的高山冷水湖，被称为'大西洋最后一滴眼泪'。湖水在阳光下呈现梦幻的蓝色。", "lat": 44.6020, "lng": 81.1660, "category": "自然风光", "rating": 4.7, "visit_duration": 240, "ticket_price": 70, "need_reservation": False, "opening_hours": "08:00-20:00"},
    {"name": "火焰山", "city": "吐鲁番", "province": "新疆维吾尔自治区", "description": "《西游记》中唐僧师徒经过的火焰山，中国最热的地方。红色砂岩在烈日下如火焰燃烧壮观无比。", "lat": 42.9120, "lng": 89.5830, "category": "自然风光", "rating": 4.3, "visit_duration": 90, "ticket_price": 40, "need_reservation": False, "opening_hours": "08:00-20:00"},
    {"name": "葡萄沟", "city": "吐鲁番", "province": "新疆维吾尔自治区", "description": "国家5A级景区，吐鲁番的清凉世界。葡萄架下品尝无核白葡萄，欣赏维吾尔族歌舞表演。", "lat": 42.9680, "lng": 89.5980, "category": "自然风光", "rating": 4.3, "visit_duration": 120, "ticket_price": 60, "need_reservation": False, "opening_hours": "08:00-20:00"},
    {"name": "喀什古城", "city": "喀什", "province": "新疆维吾尔自治区", "description": "中国唯一的以伊斯兰文化为特色的迷宫式城市街区。高台民居和艾提尕尔清真寺展现浓郁的西域风情。", "lat": 39.4660, "lng": 75.9900, "category": "历史文化", "rating": 4.7, "visit_duration": 240, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "成吉思汗陵", "city": "鄂尔多斯", "province": "内蒙古自治区", "description": "蒙古族人心中的圣地，供奉成吉思汗灵柩。气势恢宏的陵园展现了一代天骄的雄才大略。", "lat": 39.3740, "lng": 109.7740, "category": "历史文化", "rating": 4.4, "visit_duration": 150, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "响沙湾", "city": "鄂尔多斯", "province": "内蒙古自治区", "description": "国家5A级景区，因沙子会唱歌而得名。乘沙漠冲浪车驰骋金色沙海，骑骆驼感受丝路风情。", "lat": 40.2360, "lng": 109.9780, "category": "自然风光", "rating": 4.4, "visit_duration": 240, "ticket_price": 120, "need_reservation": False, "opening_hours": "08:00-18:00"},
    {"name": "额济纳胡杨林", "city": "阿拉善", "province": "内蒙古自治区", "description": "世界仅存的三片胡杨林之一，金秋十月满树金黄。胡杨'生而千年不死，死而千年不倒，倒而千年不朽'。", "lat": 41.9680, "lng": 101.0720, "category": "自然风光", "rating": 4.8, "visit_duration": 300, "ticket_price": 150, "need_reservation": False, "opening_hours": "06:00-19:00"},
    {"name": "呼伦贝尔大草原", "city": "呼伦贝尔", "province": "内蒙古自治区", "description": "中国最美的草原，世界三大草原之一。夏季绿草如茵牛羊成群，莫尔格勒河如九曲回肠蜿蜒其上。", "lat": 49.1660, "lng": 119.7230, "category": "自然风光", "rating": 4.8, "visit_duration": 480, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "哈尔滨中央大街", "city": "哈尔滨", "province": "黑龙江省", "description": "亚洲最长最繁华的步行街，铺满面包石的百年老街。汇集71座欧式建筑，马迭尔冰棍是必尝美食。", "lat": 45.7693, "lng": 126.6266, "category": "购物美食", "rating": 4.6, "visit_duration": 120, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "韶山", "city": "湘潭", "province": "湖南省", "description": "毛泽东同志故乡，国家5A级景区。毛泽东故居、铜像广场和滴水洞是红色旅游必到之处。", "lat": 27.9130, "lng": 112.4880, "category": "历史文化", "rating": 4.4, "visit_duration": 180, "ticket_price": 0, "need_reservation": False, "opening_hours": "08:00-17:00"},
    {"name": "花山岩画", "city": "崇左", "province": "广西壮族自治区", "description": "世界文化遗产，壮族先民骆越人在悬崖上留下的千年岩画。红色人物图像神秘壮观。", "lat": 22.3930, "lng": 107.1030, "category": "历史文化", "rating": 4.3, "visit_duration": 120, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "德天跨国瀑布", "city": "崇左", "province": "广西壮族自治区", "description": "亚洲最大的跨国瀑布，横跨中越两国。三级跌落宽阔壮观，乘竹筏可近距离感受水雾扑面。", "lat": 22.8450, "lng": 106.7250, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 80, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "北海银滩", "city": "北海", "province": "广西壮族自治区", "description": "中国第一滩，沙质细白如银。24公里长的海岸线平缓宽阔，是中国南方最佳的海滨浴场。", "lat": 21.4150, "lng": 109.1510, "category": "自然风光", "rating": 4.5, "visit_duration": 180, "ticket_price": 0, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "涠洲岛", "city": "北海", "province": "广西壮族自治区", "description": "中国最年轻的火山岛，国家5A级景区。鳄鱼山火山口和天主教堂是必游景点，潜水可观赏珊瑚礁。", "lat": 21.0400, "lng": 109.1150, "category": "自然风光", "rating": 4.5, "visit_duration": 360, "ticket_price": 115, "need_reservation": False, "opening_hours": "全天开放"},
    {"name": "南山文化旅游区", "city": "三亚", "province": "海南省", "description": "国家5A级景区，拥有108米高的南山海上观音圣像。佛教文化与热带海洋风光完美融合。", "lat": 18.3090, "lng": 109.2060, "category": "宗教文化", "rating": 4.6, "visit_duration": 180, "ticket_price": 150, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "呀诺达雨林", "city": "三亚", "province": "海南省", "description": "国家5A级景区，中国钻石级雨林。热带雨林茂密葱茏，踏瀑戏水和雨林滑索是特色体验。", "lat": 18.3770, "lng": 109.6790, "category": "自然风光", "rating": 4.5, "visit_duration": 240, "ticket_price": 168, "need_reservation": False, "opening_hours": "08:00-17:30"},
    {"name": "丽江古城", "city": "丽江", "province": "云南省", "description": "世界文化遗产，没有城墙的800年古城。四方街、大水车和木府展现纳西族建筑智慧，小桥流水酒吧街夜晚迷人。", "lat": 26.8750, "lng": 100.2370, "category": "历史文化", "rating": 4.6, "visit_duration": 240, "ticket_price": 50, "need_reservation": False, "opening_hours": "全天开放"},
]

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_keys = {(a["name"], a["city"]) for a in existing}

    added = 0
    skipped = 0
    for a in NEW_ATTRACTIONS:
        key = (a["name"], a["city"])
        if key in existing_keys:
            skipped += 1
            continue
        # Default image_url will be replaced by fetch_images.py
        if "image_url" not in a:
            a["image_url"] = f"https://picsum.photos/seed/{hash(a['name'])%1000}/600/400"
        existing.append(a)
        existing_keys.add(key)
        added += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new attractions, skipped {skipped} duplicates")
    print(f"Total: {len(existing)}")

if __name__ == "__main__":
    main()
