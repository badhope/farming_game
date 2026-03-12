"""
API 路由模块
"""
from backend.api.farm import router as farm_router
from backend.api.player import router as player_router
from backend.api.ai import router as ai_router
from backend.api.game import router as game_router
from backend.api.shop import router as shop_router

__all__ = ["farm_router", "player_router", "ai_router", "game_router", "shop_router"]
