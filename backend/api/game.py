"""
游戏控制 API
处理游戏进度、时间推进、存档等
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

router = APIRouter()


# ============ Schema 定义 ============

class GameStatus(BaseModel):
    """游戏状态"""
    is_running: bool
    season: str
    day: int
    year: int
    weather: str


class SaveGameRequest(BaseModel):
    """保存游戏请求"""
    save_name: str


class LoadGameRequest(BaseModel):
    """加载游戏请求"""
    save_name: str


# ============ API 端点 ============

@router.get("/status")
async def get_game_status() -> GameStatus:
    """获取游戏状态"""
    # TODO: 实现游戏状态获取
    return GameStatus(
        is_running=True,
        season="spring",
        day=1,
        year=1,
        weather="sunny",
    )


@router.post("/advance_day")
async def advance_day():
    """推进到下一天"""
    # TODO: 实现时间推进逻辑
    return {
        "success": True,
        "new_day": 2,
        "new_weather": "sunny",
        "events": [],
    }


@router.post("/save")
async def save_game(request: SaveGameRequest):
    """保存游戏"""
    # TODO: 实现存档逻辑
    return {"success": True, "message": f"游戏已保存到：{request.save_name}"}


@router.post("/load")
async def load_game(request: LoadGameRequest):
    """加载游戏"""
    # TODO: 实现读档逻辑
    return {"success": True, "message": f"游戏已从：{request.save_name} 加载"}


@router.get("/saves")
async def list_saves():
    """获取存档列表"""
    # TODO: 实现存档列表获取
    return {"saves": []}


@router.delete("/save/{save_name}")
async def delete_save(save_name: str):
    """删除存档"""
    # TODO: 实现存档删除逻辑
    return {"success": True, "message": f"存档 {save_name} 已删除"}
