"""
FastAPI 主应用
农场模拟游戏 Web API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.middleware.performance import PerformanceMonitorMiddleware

from backend.api import farm, player, ai, game, shop, auth, sync, health


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    
    app = FastAPI(
        title="农场模拟器 API",
        description="AI 驱动的农场模拟游戏 Web API",
        version="3.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    
    # 性能监控中间件
    app.add_middleware(PerformanceMonitorMiddleware, slow_request_threshold=1.0)
    
    # 配置 CORS（允许前端访问）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React 开发服务器
            "http://127.0.0.1:3000",
            "http://localhost:5173",  # Vite 开发服务器
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(health.router, prefix="", tags=["健康检查"])
    app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
    app.include_router(sync.router, prefix="/api/sync", tags=["数据同步"])
    app.include_router(farm.router, prefix="/api/farm", tags=["农场管理"])
    app.include_router(player.router, prefix="/api/player", tags=["玩家数据"])
    app.include_router(ai.router, prefix="/api/ai", tags=["AI 功能"])
    app.include_router(game.router, prefix="/api/game", tags=["游戏控制"])
    app.include_router(shop.router, prefix="/api/shop", tags=["商店"])
    
    @app.get("/api/health", tags=["健康检查"])
    async def health_check():
        """健康检查接口"""
        return {"status": "ok", "version": "3.0.0"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
