"""路线算法单元测试：覆盖正常、边界与异常场景。

被测模块：app/services/algorithm.py
"""
from types import SimpleNamespace

import pytest

from app.services.algorithm import (
    estimate_total_minutes,
    format_duration,
    haversine_km,
    nearest_neighbor,
)


def poi(poi_id: int, latitude: float, longitude: float, stay_minutes: int = 0):
    """构造只含算法所需字段的点位替身，避免测试依赖数据库模型。"""
    return SimpleNamespace(
        poi_id=poi_id,
        latitude=latitude,
        longitude=longitude,
        stay_minutes=stay_minutes,
    )


class TestHaversine:
    def test_same_point_returns_zero(self):
        a = poi(1, 28.68, 115.89)
        assert haversine_km(a, a) == pytest.approx(0.0, abs=1e-9)

    def test_one_hundredth_degree_latitude_is_about_one_kilometre(self):
        # 纬度 0.01 度约等于 1.112 km，用于固定距离量级，防止单位换算写错
        a = poi(1, 28.68, 115.89)
        b = poi(2, 28.69, 115.89)
        assert haversine_km(a, b) == pytest.approx(1.112, abs=0.05)

    def test_distance_is_symmetric(self):
        a = poi(1, 28.68, 115.89)
        b = poi(2, 28.70, 115.92)
        assert haversine_km(a, b) == pytest.approx(haversine_km(b, a), abs=1e-9)

    def test_string_coordinates_are_accepted(self):
        # 数据库 Numeric 字段读出的可能是 Decimal，算法内部需自行转 float
        a = poi(1, "28.68", "115.89")
        b = poi(2, "28.70", "115.92")
        assert haversine_km(a, b) > 0


class TestNearestNeighbor:
    def test_first_poi_stays_first(self):
        start = poi(1, 28.68, 115.89)
        ordered = nearest_neighbor([start, poi(2, 28.90, 116.10), poi(3, 28.60, 115.80)])
        assert ordered[0] is start

    def test_visits_every_poi_exactly_once(self):
        pois = [poi(1, 28.68, 115.89), poi(2, 28.70, 115.90), poi(3, 28.72, 115.92)]
        ordered = nearest_neighbor(pois)
        assert len(ordered) == len(pois)
        assert sorted(p.poi_id for p in ordered) == sorted(p.poi_id for p in pois)

    def test_picks_the_nearest_remaining_poi(self):
        start = poi(1, 28.680, 115.890)
        near = poi(2, 28.681, 115.891)   # ~0.15 km
        far = poi(3, 29.000, 116.200)    # ~40 km
        ordered = nearest_neighbor([start, far, near])
        assert [p.poi_id for p in ordered] == [1, 2, 3]

    def test_single_poi_returns_itself(self):
        only = poi(1, 28.68, 115.89)
        assert nearest_neighbor([only]) == [only]

    def test_empty_input_returns_empty_list(self):
        # 接口层已拦截空清单，算法层仍需返回空列表而不是抛 IndexError
        assert nearest_neighbor([]) == []


class TestEstimateTotalMinutes:
    def test_single_poi_costs_only_its_stay_minutes(self):
        assert estimate_total_minutes([poi(1, 28.68, 115.89, stay_minutes=90)]) == 90

    def test_stay_minutes_of_all_pois_are_summed(self):
        pois = [poi(1, 28.68, 115.89, 60), poi(2, 28.69, 115.89, 30)]
        total = estimate_total_minutes(pois, "walking")
        assert total >= 90

    def test_walking_takes_longer_than_driving(self):
        pois = [poi(1, 28.68, 115.89), poi(2, 28.72, 115.95)]
        assert estimate_total_minutes(pois, "walking") > estimate_total_minutes(pois, "driving")

    def test_empty_list_returns_zero(self):
        assert estimate_total_minutes([]) == 0

    def test_result_is_integer(self):
        pois = [poi(1, 28.68, 115.89, 15), poi(2, 28.69, 115.90, 15)]
        assert isinstance(estimate_total_minutes(pois), int)


class TestFormatDuration:
    @pytest.mark.parametrize(
        ("minutes", "expected"),
        [
            (0, "0分钟"),
            (45, "45分钟"),
            (60, "1小时"),
            (90, "1小时30分钟"),
            (150, "2小时30分钟"),
        ],
    )
    def test_formats_minutes_into_readable_text(self, minutes, expected):
        assert format_duration(minutes) == expected
