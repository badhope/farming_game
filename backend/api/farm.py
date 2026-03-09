"""
农场管理 API
处理农田、作物、种植等相关操作
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()


# ============ Schema 定义 ============

class PlotInfo(BaseModel):
    """农田信息"""
    row: int
    col: int
    has_crop: bool
    crop_type: str | None = None
    growth_stage: int = 0
    needs_water: bool = False


class FarmAction(BaseModel):
    """农场操作"""
    action: str  # "plant", "water", "harvest", "clear"
    row: int
    col: int
    crop_type: str | None = None


# ============ API 端点 ============

@router.get("/status")
async def get_farm_status():
    """获取农场状态"""
    # TODO: 实现农场状态获取
    return {
        "plots": [],
        "season": "spring",
        "day": 1,
        "weather": "sunny",
    }


@router.get("/plots")
async def get_plots() -> List[PlotInfo]:
    """获取所有农田信息"""
    # TODO: 实现农田数据获取
    return []


@router.post("/action")
async def perform_action(action: FarmAction):
    """执行农场操作"""
    # TODO: 实现农场操作逻辑
    return {"success": True, "message": f"执行操作：{action.action}"}


@router.get("/crops")
async def get_available_crops():
    """获取可种植作物列表"""
    # TODO: 从配置中读取作物数据
    return {
        "crops": [
            {"id": "turnip", "name": "萝卜", "season": "spring", "growth_days": 4},
            {"id": "potato", "name": "土豆", "season": "spring", "growth_days": 6},
            {"id": "tomato", "name": "番茄", "season": "summer", "growth_days": 11},
            {"id": "corn", "name": "玉米", "season": "summer", "growth_days": 14},
        ]
    }
