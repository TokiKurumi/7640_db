"""
COMP7640 E-Commerce Platform - FastAPI主应用
采用分层架构:
  - Models: 数据模型层 (Pydantic)
  - Routes: 接口层 (REST API)
  - Services: 业务逻辑层
  - DAO: 数据访问层 (数据库)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# 导入路由
from routes import router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="COMP7640 E-Commerce Platform API",
    description="多供应商电商平台 REST API",
    version="2.0.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)


# 启动和关闭事件
@app.on_event("startup")
async def startup():
    """应用启动事件"""
    logger.info("E-Commerce Platform API 启动中...")


@app.on_event("shutdown")
async def shutdown():
    """应用关闭事件"""
    logger.info("E-Commerce Platform API 关闭中...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
