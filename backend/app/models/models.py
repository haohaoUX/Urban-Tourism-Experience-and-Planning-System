"""ORM 模型：与数据库设计文档中的表结构一一对应。"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base

# 主键类型：MySQL 用 BIGINT，SQLite 用 INTEGER
# （SQLite 只有 INTEGER PRIMARY KEY 才会作为 rowid 自动递增）
PKType = BigInteger().with_variant(Integer, "sqlite")


class POI(Base):
    __tablename__ = "poi"

    poi_id = Column(PKType, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False, index=True)
    district = Column(String(20), nullable=False, index=True)
    address = Column(String(200))
    longitude = Column(Numeric(10, 6), nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    description = Column(Text)
    open_time = Column(String(100))
    stay_minutes = Column(Integer)
    ticket = Column(String(50))
    cost = Column(String(50))
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    route_items = relationship("RouteItem", back_populates="poi")


class Route(Base):
    __tablename__ = "route"

    route_id = Column(PKType, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    gen_mode = Column(String(20), nullable=False)
    total_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    items = relationship(
        "RouteItem",
        back_populates="route",
        cascade="all, delete-orphan",
        order_by="RouteItem.seq",
    )


class RouteItem(Base):
    __tablename__ = "route_item"

    item_id = Column(PKType, primary_key=True, autoincrement=True)
    route_id = Column(
        BigInteger,
        ForeignKey("route.route_id", ondelete="CASCADE"),
        nullable=False,
    )
    poi_id = Column(BigInteger, ForeignKey("poi.poi_id"), nullable=False)
    seq = Column(Integer, nullable=False)
    user_note = Column(String(50))

    __table_args__ = (
        UniqueConstraint("route_id", "poi_id", name="uq_route_poi"),
        UniqueConstraint("route_id", "seq", name="uq_route_seq"),
    )

    route = relationship("Route", back_populates="items")
    poi = relationship("POI")


class Tag(Base):
    __tablename__ = "tag"

    tag_id = Column(PKType, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


class POITag(Base):
    __tablename__ = "poi_tag"

    poi_id = Column(
        BigInteger,
        ForeignKey("poi.poi_id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = Column(
        BigInteger,
        ForeignKey("tag.tag_id", ondelete="CASCADE"),
        primary_key=True,
    )


class Favorite(Base):
    __tablename__ = "favorite"

    favorite_id = Column(PKType, primary_key=True, autoincrement=True)
    poi_id = Column(
        BigInteger,
        ForeignKey("poi.poi_id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.now)


class Visited(Base):
    __tablename__ = "visited"

    visited_id = Column(PKType, primary_key=True, autoincrement=True)
    poi_id = Column(
        BigInteger,
        ForeignKey("poi.poi_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    marked_at = Column(DateTime, default=datetime.now)
