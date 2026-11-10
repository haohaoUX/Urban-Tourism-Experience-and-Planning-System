"""路线接口：生成、查询、重命名、微调、复制、删除。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import POI, Route, RouteItem
from app.schemas.schemas import (
    ApiResponse,
    RouteCreate,
    RouteItemOut,
    RouteItemsUpdate,
    RouteOut,
    RouteSummary,
)
from app.services.algorithm import estimate_total_minutes, nearest_neighbor

router = APIRouter(prefix="/api/routes", tags=["路线"])


def build_route_out(route: Route) -> RouteOut:
    return RouteOut(
        route_id=route.route_id,
        name=route.name,
        gen_mode=route.gen_mode,
        total_minutes=route.total_minutes,
        items=[
            RouteItemOut(
                seq=item.seq,
                poi_id=item.poi_id,
                name=item.poi.name,
                stay_minutes=item.poi.stay_minutes,
                user_note=item.user_note,
            )
            for item in route.items
        ],
    )


@router.post("", status_code=201, response_model=ApiResponse[RouteOut])
def create_route(payload: RouteCreate, db: Session = Depends(get_db)):
    if not payload.poi_ids:
        raise HTTPException(status_code=422, detail="请先添加点位")
    if len(set(payload.poi_ids)) != len(payload.poi_ids):
        raise HTTPException(status_code=409, detail="同一点位不能重复")

    pois = (
        db.query(POI)
        .filter(POI.poi_id.in_(payload.poi_ids), POI.status == 1)
        .all()
    )
    if len(pois) != len(set(payload.poi_ids)):
        raise HTTPException(status_code=400, detail="存在无效点位")

    by_id = {p.poi_id: p for p in pois}
    ordered = [by_id[i] for i in payload.poi_ids]
    if any(p.type == "facility" for p in ordered):
        raise HTTPException(
            status_code=400, detail="配套服务点位不能加入路线"
        )

    if payload.gen_mode == "smart":
        ordered = nearest_neighbor(ordered)

    route_count = db.query(Route).count()
    route = Route(
        name=payload.name or f"路线{route_count + 1}",
        gen_mode=payload.gen_mode,
        total_minutes=estimate_total_minutes(ordered, payload.travel_mode),
    )
    db.add(route)
    db.flush()
    for seq, poi in enumerate(ordered, start=1):
        db.add(
            RouteItem(
                route_id=route.route_id, poi_id=poi.poi_id, seq=seq
            )
        )
    db.commit()
    db.refresh(route)
    return ApiResponse(message="路线生成成功", data=build_route_out(route))


@router.get("", response_model=ApiResponse[list[RouteSummary]])
def list_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).order_by(Route.route_id).all()
    return ApiResponse(
        data=[
            RouteSummary(
                route_id=r.route_id,
                name=r.name,
                gen_mode=r.gen_mode,
                poi_count=len(r.items),
                total_minutes=r.total_minutes,
                created_at=r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
            for r in routes
        ]
    )


@router.get("/{route_id}", response_model=ApiResponse[RouteOut])
def route_detail(route_id: int, db: Session = Depends(get_db)):
    route = db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")
    return ApiResponse(data=build_route_out(route))


@router.patch("/{route_id}", response_model=ApiResponse[RouteSummary])
def rename_route(
    route_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    route = db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")
    name = (payload.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="路线名称不能为空")
    route.name = name[:100]
    db.commit()
    return ApiResponse(
        data=RouteSummary(
            route_id=route.route_id,
            name=route.name,
            gen_mode=route.gen_mode,
            poi_count=len(route.items),
            total_minutes=route.total_minutes,
        )
    )


@router.put("/{route_id}/items", response_model=ApiResponse[RouteOut])
def update_items(
    route_id: int,
    payload: RouteItemsUpdate,
    db: Session = Depends(get_db),
):
    route = db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")

    poi_ids = [it.poi_id for it in payload.items]
    if len(set(poi_ids)) != len(poi_ids):
        raise HTTPException(status_code=409, detail="点位不能重复")

    pois = (
        db.query(POI).filter(POI.poi_id.in_(poi_ids)).all()
    )
    if len(pois) != len(set(poi_ids)):
        raise HTTPException(status_code=400, detail="存在无效点位")

    note_by_id = {it.poi_id: it.user_note for it in payload.items}
    by_id = {p.poi_id: p for p in pois}
    ordered = [by_id[i] for i in poi_ids]

    # 清除旧行程，按新顺序重建
    db.query(RouteItem).filter(
        RouteItem.route_id == route_id
    ).delete()
    db.flush()
    for seq, poi in enumerate(ordered, start=1):
        db.add(
            RouteItem(
                route_id=route_id,
                poi_id=poi.poi_id,
                seq=seq,
                user_note=note_by_id.get(poi.poi_id),
            )
        )
    route.total_minutes = estimate_total_minutes(ordered)
    db.commit()
    db.refresh(route)
    return ApiResponse(data=build_route_out(route))


@router.post("/{route_id}/copy", status_code=201,
             response_model=ApiResponse[RouteOut])
def copy_route(route_id: int, db: Session = Depends(get_db)):
    source = db.get(Route, route_id)
    if not source:
        raise HTTPException(status_code=404, detail="路线不存在")

    copy = Route(
        name=f"{source.name} 副本",
        gen_mode=source.gen_mode,
        total_minutes=source.total_minutes,
    )
    db.add(copy)
    db.flush()
    for item in source.items:
        db.add(
            RouteItem(
                route_id=copy.route_id,
                poi_id=item.poi_id,
                seq=item.seq,
                user_note=item.user_note,
            )
        )
    db.commit()
    db.refresh(copy)
    return ApiResponse(message="复制成功", data=build_route_out(copy))


@router.delete("/{route_id}", response_model=ApiResponse)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")
    db.delete(route)
    db.commit()
    return ApiResponse(message="路线已删除")
