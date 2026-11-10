"""路线生成算法与时长估算（详细设计文档的代码实现）。"""
import math
from typing import List


def haversine_km(a, b) -> float:
    """两点间球面距离（公里），a/b 为含 latitude/longitude 的对象。"""
    lat1, lng1 = float(a.latitude), float(a.longitude)
    lat2, lng2 = float(b.latitude), float(b.longitude)
    radius = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    h = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lng / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(h))


def nearest_neighbor(pois: List) -> List:
    """顺路最优：最近邻启发式排序，起点取清单第一个。"""
    remaining = list(pois)
    ordered = [remaining.pop(0)]
    while remaining:
        current = ordered[-1]
        best = min(remaining, key=lambda p: haversine_km(current, p))
        ordered.append(best)
        remaining.remove(best)
    return ordered


def estimate_total_minutes(ordered_pois, travel_mode: str = "driving") -> int:
    """总时长 = 停留时长之和 + 通勤兜底估算（真实地图接入后可替换为高德时长）。"""
    stay = sum(p.stay_minutes or 0 for p in ordered_pois)
    speed_kmh = 30 if travel_mode == "driving" else 5
    commute = 0
    for a, b in zip(ordered_pois, ordered_pois[1:]):
        km = haversine_km(a, b)
        commute += round(km / speed_kmh * 60)
    return stay + commute


def format_duration(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    if h:
        return f"{h}小时" + (f"{m}分钟" if m else "")
    return f"{m}分钟"
