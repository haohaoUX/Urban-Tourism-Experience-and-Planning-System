"""FastAPI 应用入口。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import poi, route
from app.core.config import settings
from app.core.database import Base, engine

# 开发期自动建表；正式环境改用数据库迁移脚本
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(poi.router)
app.include_router(route.router)


@app.get("/", tags=["系统"])
def root():
    return {
        "code": 0,
        "message": settings.APP_NAME,
        "data": {"api_docs": "/docs"},
    }
