"""Pydantic 请求/响应模型。"""
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


class Page(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]


# ---------- 点位 ----------
class POIOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    poi_id: int
    name: str
    type: str
    district: str
    address: Optional[str] = None
    longitude: float
    latitude: float
    description: Optional[str] = None
    open_time: Optional[str] = None
    stay_minutes: Optional[int] = None
    ticket: Optional[str] = None
    cost: Optional[str] = None


class NearbyPOI(BaseModel):
    poi_id: int
    name: str
    type: str
    district: str
    distance: int
    stay_minutes: Optional[int] = None


# ---------- 路线 ----------
class RouteCreate(BaseModel):
    name: Optional[str] = None
    gen_mode: str = Field(pattern="^(smart|manual)$")
    poi_ids: List[int]
    travel_mode: str = Field(
        default="driving", pattern="^(driving|walking)$"
    )


class RouteItemOut(BaseModel):
    seq: int
    poi_id: int
    name: str
    stay_minutes: Optional[int] = None
    user_note: Optional[str] = None


class RouteOut(BaseModel):
    route_id: int
    name: str
    gen_mode: str
    total_minutes: Optional[int] = None
    items: List[RouteItemOut]


class RouteSummary(BaseModel):
    route_id: int
    name: str
    gen_mode: str
    poi_count: int
    total_minutes: Optional[int] = None
    created_at: Optional[str] = None


class RouteRename(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ItemUpdate(BaseModel):
    poi_id: int
    user_note: Optional[str] = Field(default=None, max_length=50)


class RouteItemsUpdate(BaseModel):
    items: List[ItemUpdate]
