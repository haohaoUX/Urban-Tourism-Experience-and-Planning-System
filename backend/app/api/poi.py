"""点位接口：列表筛选、详情、周边。"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import POI
from app.schemas.schemas import ApiResponse, NearbyPOI, Page, POIOut
from app.services.algorithm import haversine_km

router = APIRouter(prefix="/api/pois", tags=["点位"])


@router.get("", response_model=ApiResponse[Page[POIOut]])
def list_pois(
    type: Optional[str] = None,
    district: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(POI).filter(POI.status == 1)
    if type:
        query = query.filter(POI.type.in_(type.split(",")))
    if district:
        query = query.filter(POI.district.in_(district.split(",")))
    if keyword:
        query = query.filter(POI.name.like(f"%{keyword}%"))

    total = query.count()
    items = (
        query.offset((page - 1) * page_size).limit(page_size).all()
    )
    return ApiResponse(
        data=Page(
            total=total, page=page, page_size=page_size, items=items
        )
    )


@router.get("/{poi_id}", response_model=ApiResponse[POIOut])
def poi_detail(poi_id: int, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if not poi:
        raise HTTPException(status_code=404, detail="点位不存在")
    return ApiResponse(data=poi)


@router.get("/{poi_id}/nearby", response_model=ApiResponse[list[NearbyPOI]])
def nearby(
    poi_id: int,
    radius: int = Query(500, ge=100, le=2000),
    type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    center = db.get(POI, poi_id)
    if not center:
        raise HTTPException(status_code=404, detail="点位不存在")

    query = db.query(POI).filter(
        POI.poi_id != poi_id, POI.status == 1
    )
    if type:
        query = query.filter(POI.type.in_(type.split(",")))

    result = []
    for poi in query.all():
        meters = round(haversine_km(center, poi) * 1000)
        if meters <= radius:
            result.append(
                NearbyPOI(
                    poi_id=poi.poi_id,
                    name=poi.name,
                    type=poi.type,
                    district=poi.district,
                    distance=meters,
                    stay_minutes=poi.stay_minutes,
                )
            )
    result.sort(key=lambda x: x.distance)
    return ApiResponse(data=result)
