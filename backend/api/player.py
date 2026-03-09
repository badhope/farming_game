"""
玩家数据 API
处理玩家信息、背包、成就等
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()


# ============ Schema 定义 ============

class PlayerInfo(BaseModel):
    """玩家信息"""
    name: str
    level: int
    exp: int
    gold: int
    stamina: int
    max_stamina: int


class InventoryItem(BaseModel):
    """背包物品"""
    item_id: str
    name: str
    quantity: int
    item_type: str


# ============ API 端点 ============

@router.get("/info")
async def get_player_info() -> PlayerInfo:
    """获取玩家信息"""
    # TODO: 实现玩家数据获取
    return PlayerInfo(
        name="农夫",
        level=1,
        exp=0,
        gold=500,
        stamina=100,
        max_stamina=100,
    )


@router.get("/inventory")
async def get_inventory() -> List[InventoryItem]:
    """获取背包物品"""
    # TODO: 实现背包数据获取
    return []


@router.post("/inventory/use")
async def use_item(item_id: str, quantity: int = 1):
    """使用物品"""
    # TODO: 实现物品使用逻辑
    return {"success": True, "message": f"使用物品：{item_id}"}


@router.get("/achievements")
async def get_achievements():
    """获取成就列表"""
    # TODO: 实现成就数据获取
    return {"achievements": []}


@router.get("/stats")
async def get_player_stats():
    """获取玩家统计数据"""
    # TODO: 实现统计数据获取
    return {
        "total_crops_planted": 0,
        "total_crops_harvested": 0,
        "total_gold_earned": 0,
        "days_played": 0,
    }
