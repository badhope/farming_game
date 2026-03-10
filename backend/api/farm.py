"""
农场管理 API
处理农田、作物、种植等相关操作
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.services.game_session import game_service

router = APIRouter()


# ============ Schema 定义 ============

class PlantRequest(BaseModel):
    """种植请求"""
    row: int
    col: int
    crop_name: str


class WaterRequest(BaseModel):
    """浇水请求"""
    row: int
    col: int


class HarvestRequest(BaseModel):
    """收获请求"""
    row: int
    col: int


class ClearRequest(BaseModel):
    """清空地块请求"""
    row: int
    col: int


# ============ API 端点 ============

@router.get("/status")
async def get_farm_status() -> Dict[str, Any]:
    """获取农场状态"""
    if not game_service.has_active_game():
        return {
            "has_game": False,
            "message": "没有进行中的游戏",
        }
    
    state = game_service._get_game_state()
    return {
        "has_game": True,
        "season": state.season,
        "day": state.day,
        "year": state.year,
        "weather": state.weather,
    }


@router.get("/plots")
async def get_plots() -> List[Dict[str, Any]]:
    """获取所有农田信息"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    plots = game_service.get_farm_plots()
    return [plot.__dict__ for plot in plots]


@router.post("/plant")
async def plant_crop(request: PlantRequest) -> Dict[str, Any]:
    """种植作物"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏，请先创建新游戏"}
    
    result = game_service.plant_crop(request.row, request.col, request.crop_name)
    return result


@router.post("/water")
async def water_crop(request: WaterRequest) -> Dict[str, Any]:
    """浇水"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    result = game_service.water_crop(request.row, request.col)
    return result


@router.post("/harvest")
async def harvest_crop(request: HarvestRequest) -> Dict[str, Any]:
    """收获作物"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    result = game_service.harvest_crop(request.row, request.col)
    return result


@router.post("/clear")
async def clear_plot(request: ClearRequest) -> Dict[str, Any]:
    """清空地块"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    result = game_service.clear_plot(request.row, request.col)
    return result


@router.get("/crops")
async def get_available_crops() -> List[Dict[str, Any]]:
    """获取可种植作物列表"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    return game_service.get_available_crops()


@router.get("/time")
async def get_time_status() -> Dict[str, Any]:
    """获取时间和天气状态"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    gm = game_service.get_current_game()
    return {
        "year": gm.time_system.year,
        "day": gm.time_system.day,
        "season": gm.time_system.season.value,
        "weather": gm.time_system.weather.value,
        "tomorrow_weather": gm.time_system.tomorrow_weather.value if gm.time_system.tomorrow_weather else None,
        "date_string": gm.time_system.get_date_string(),
        "season_progress": gm.time_system.get_season_progress(),
        "year_progress": gm.time_system.get_year_progress(),
        "total_days": gm.time_system.get_total_days(),
    }
