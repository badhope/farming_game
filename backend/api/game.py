"""
游戏控制 API
处理游戏进度、时间推进、存档等
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from backend.services.game_session import game_service

router = APIRouter()


# ============ Schema 定义 ============

class SaveGameRequest(BaseModel):
    """保存游戏请求"""
    save_name: str = "save"


class LoadGameRequest(BaseModel):
    """加载游戏请求"""
    save_name: str = "save"


# ============ API 端点 ============

@router.get("/status")
async def get_game_status() -> Dict[str, Any]:
    """获取游戏状态"""
    if not game_service.has_active_game():
        return {
            "has_game": False,
            "message": "没有进行中的游戏",
        }
    
    state = game_service._get_game_state()
    return {
        "has_game": True,
        "is_running": True,
        "season": state.season,
        "day": state.day,
        "year": state.year,
        "weather": state.weather,
    }


@router.post("/advance_day")
async def advance_day() -> Dict[str, Any]:
    """推进到下一天"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    result = game_service.advance_day()
    return result


@router.post("/save")
async def save_game(request: SaveGameRequest) -> Dict[str, Any]:
    """保存游戏"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    result = game_service.save_game(request.save_name)
    return result


@router.post("/load")
async def load_game(request: LoadGameRequest) -> Dict[str, Any]:
    """加载游戏"""
    result = game_service.load_game(request.save_name)
    return result


@router.get("/saves")
async def list_saves() -> Dict[str, Any]:
    """获取存档列表"""
    saves = game_service.get_save_files()
    return {
        "saves": saves,
        "count": len(saves),
    }


@router.delete("/save/{save_name}")
async def delete_save(save_name: str) -> Dict[str, Any]:
    """删除存档"""
    import os
    save_file = f"saves/{save_name}.json"
    
    if not os.path.exists(save_file):
        return {"success": False, "message": f"存档不存在: {save_name}"}
    
    os.remove(save_file)
    return {"success": True, "message": f"存档 {save_name} 已删除"}


@router.post("/reset")
async def reset_game() -> Dict[str, Any]:
    """重置游戏"""
    from backend.services.game_session import GameSessionService
    global game_service
    game_service = GameSessionService()
    
    return {"success": True, "message": "游戏已重置"}


@router.post("/new_game_plus")
async def start_new_game_plus() -> Dict[str, Any]:
    """开始新游戏+（多周目），继承部分进度"""
    if not game_service.has_active_game():
        return {"success": False, "message": "没有进行中的游戏"}
    
    gm = game_service.get_current_game()
    
    total_games = getattr(gm, 'total_games_played', 0) + 1
    
    result = game_service.start_new_game_plus()
    return {
        "success": True,
        "message": f"开始第{total_games}轮游戏！",
        "game_number": total_games,
    }


@router.get("/game_info")
async def get_game_info() -> Dict[str, Any]:
    """获取当前游戏信息（难度、周目等）"""
    if not game_service.has_active_game():
        return {
            "has_game": False,
        }
    
    state = game_service._get_game_state()
    return {
        "has_game": True,
        "difficulty": state.difficulty,
        "game_number": state.game_number,
        "total_games_played": state.total_games_played,
    }
