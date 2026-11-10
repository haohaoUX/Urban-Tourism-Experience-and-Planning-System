"""应用配置：通过 .env 覆盖默认值，默认使用 SQLite，可切换 MySQL。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "南昌旅游路线规划工具"
    # 默认 SQLite；MySQL 示例：
    # mysql+pymysql://root:密码@127.0.0.1:3306/nanchang_trip?charset=utf8mb4
    DATABASE_URL: str = "sqlite:///./nanchang_trip.sqlite3"

    # 高德开放平台凭据（模拟地图阶段留空，接入真实地图时填写）
    AMAP_KEY: str = ""
    AMAP_SECRET: str = ""


settings = Settings()
