"""初始化点位数据。

运行方式（在 backend 目录下）：
    python scripts/init_data.py

说明：经纬度为 GCJ-02 近似值，用于中期演示，后续用高德数据校准。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.models import POI  # noqa: E402

RAW_POIS = [
    {
        "name": "滕王阁", "type": "spot", "district": "东湖区",
        "address": "仿古路58号", "longitude": 115.887, "latitude": 28.683,
        "description": "江南三大名楼之一，《滕王阁序》诞生地，登楼可俯瞰赣江两岸风光。",
        "open_time": "08:00 - 22:00", "stay_minutes": 90, "ticket": "门票 ¥50",
    },
    {
        "name": "秋水广场", "type": "spot", "district": "红谷滩区",
        "address": "赣江中大道", "longitude": 115.855, "latitude": 28.684,
        "description": "赣江西岸滨江广场，大型音乐喷泉与夜晚灯光秀是最大看点。",
        "open_time": "全天开放", "stay_minutes": 60,
    },
    {
        "name": "江西省博物馆", "type": "spot", "district": "红谷滩区",
        "address": "赣江北路", "longitude": 115.852, "latitude": 28.692,
        "description": "江西最大综合性博物馆，海昏侯墓出土文物常设展是镇馆之宝。",
        "open_time": "09:00 - 17:00（周一闭馆）", "stay_minutes": 120,
        "ticket": "免费预约",
    },
    {
        "name": "八一广场", "type": "spot", "district": "东湖区",
        "address": "北京西路", "longitude": 115.902, "latitude": 28.676,
        "description": "南昌城市中心地标，八一南昌起义纪念塔矗立于此。",
        "open_time": "全天开放", "stay_minutes": 40,
    },
    {
        "name": "八一起义纪念馆", "type": "spot", "district": "西湖区",
        "address": "中山路380号", "longitude": 115.892, "latitude": 28.678,
        "description": "全国重点文物保护单位，完整展示八一南昌起义历史。",
        "open_time": "09:00 - 17:30", "stay_minutes": 75, "ticket": "免费",
    },
    {
        "name": "万寿宫历史文化街区", "type": "leisure", "district": "西湖区",
        "address": "翠花街", "longitude": 115.885, "latitude": 28.673,
        "description": "赣派建筑历史街区，集非遗文创、特色小吃、夜景逛购于一体。",
        "open_time": "10:00 - 22:00", "stay_minutes": 90,
    },
    {
        "name": "绳金塔", "type": "spot", "district": "西湖区",
        "address": "绳金塔街", "longitude": 115.890, "latitude": 28.660,
        "description": "南昌古城镇城之宝，千年古塔周边已改造为市井美食街区。",
        "open_time": "09:00 - 21:00", "stay_minutes": 60,
    },
    {
        "name": "八一公园", "type": "spot", "district": "东湖区",
        "address": "民德路", "longitude": 115.905, "latitude": 28.682,
        "description": "市中心老牌城市公园，湖岛亭廊俱全，市民日常休闲去处。",
        "open_time": "全天开放", "stay_minutes": 45,
    },
    {
        "name": "天香园", "type": "spot", "district": "青山湖区",
        "address": "青山湖南大道", "longitude": 115.945, "latitude": 28.650,
        "description": "城市中的湿地候鸟乐园，盆景园林与白鹭栖息是特色。",
        "open_time": "08:00 - 17:30", "stay_minutes": 90, "ticket": "门票 ¥40",
    },
    {
        "name": "青山湖绿道", "type": "spot", "district": "青山湖区",
        "address": "青山湖沿岸", "longitude": 115.975, "latitude": 28.700,
        "description": "环绕青山湖的滨水绿道，适合骑行、散步与慢跑。",
        "open_time": "全天开放", "stay_minutes": 60,
    },
    {
        "name": "八大山人纪念馆", "type": "spot", "district": "青云谱区",
        "address": "青云谱路269号", "longitude": 115.910, "latitude": 28.605,
        "description": "建于青云谱道院旧址，纪念写意画大师八大山人。",
        "open_time": "09:00 - 17:00（周一闭馆）", "stay_minutes": 80,
        "ticket": "免费",
    },
    {
        "name": "小平小道陈列馆", "type": "spot", "district": "新建区",
        "address": "望城街道", "longitude": 115.780, "latitude": 28.690,
        "description": "邓小平同志曾劳动行走的小道改建而成的陈列馆。",
        "open_time": "09:00 - 17:00", "stay_minutes": 60, "ticket": "免费",
    },
    {
        "name": "老南昌瓦罐汤馆", "type": "food", "district": "西湖区",
        "address": "船山路", "longitude": 115.890, "latitude": 28.672,
        "description": "本地人气老店，瓦罐煨汤配拌粉是南昌经典早餐组合。",
        "open_time": "06:30 - 20:30", "stay_minutes": 40, "cost": "人均 ¥25 - 40",
    },
    {
        "name": "赣菜馆·藜蒿炒腊肉", "type": "food", "district": "东湖区",
        "address": "苏圃路", "longitude": 115.910, "latitude": 28.680,
        "description": "主打赣菜正餐，藜蒿炒腊肉、啤酒鸭、三杯鸡等招牌菜齐全。",
        "open_time": "10:30 - 21:30", "stay_minutes": 70, "cost": "人均 ¥60 - 90",
    },
    {
        "name": "公共卫生间", "type": "facility", "district": "东湖区",
        "address": "八一广场东侧", "longitude": 115.905, "latitude": 28.675,
        "description": "市政公共卫生间，干净整洁，全天开放。",
        "open_time": "全天开放",
    },
    {
        "name": "地铁滕王阁站", "type": "facility", "district": "东湖区",
        "address": "中山西路", "longitude": 115.875, "latitude": 28.682,
        "description": "地铁1号线站点，B口出站步行约800米可达滕王阁。",
        "open_time": "06:00 - 23:00",
    },
]


def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(POI).count() > 0:
            print("点位表非空，跳过初始化")
            return
        for row in RAW_POIS:
            db.add(POI(**row, status=1))
        db.commit()
        print(f"已写入 {len(RAW_POIS)} 个点位")
    finally:
        db.close()


if __name__ == "__main__":
    init()
