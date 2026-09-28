"""健康检查接口的响应结构。"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
