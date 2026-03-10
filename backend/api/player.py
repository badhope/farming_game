"""
玩家数据 API
处理玩家信息、背包、成就等
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any

from backend.services.game_session import game_service

router = APIRouter()


# ============ Schema 定义 ============

class CreateGameRequest(BaseModel):
    """创建新游戏请求"""
    player_name: str = "农夫"
    difficulty: str = "normal"


class PlayerInfo(BaseModel):
    """玩家信息"""
    name: str
    level: int
    exp: int
    gold: int
    stamina: int
    max_stamina: int


# ============ API 端点 ============

@router.post("/create")
async def create_game(request: CreateGameRequest) -> Dict[str, Any]:
    """创建新游戏"""
    try:
        state = game_service.create_new_game(request.player_name, request.difficulty)
        return {
            "success": True,
            "message": f"欢迎，{request.player_name}！游戏开始！",
            "state": {
                "player_name": state.player_name,
                "gold": state.gold,
                "level": state.level,
                "exp": state.exp,
                "stamina": state.stamina,
                "max_stamina": state.max_stamina,
                "season": state.season,
                "day": state.day,
                "year": state.year,
                "weather": state.weather,
                "plot_size": state.plot_size,
            }
        }
    except Exception as e:
        return {"success": False, "message": f"创建游戏失败: {str(e)}"}


@router.get("/info")
async def get_player_info() -> Dict[str, Any]:
    """获取玩家信息"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    state = game_service._get_game_state()
    return {
        "name": state.player_name,
        "level": state.level,
        "exp": state.exp,
        "gold": state.gold,
        "stamina": state.stamina,
        "max_stamina": state.max_stamina,
    }


@router.post("/add_gold")
async def add_gold(amount: int) -> Dict[str, Any]:
    """增加金币（测试用）"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    gm = game_service.get_current_game()
    gm.player.gold += amount
    
    return {
        "success": True,
        "message": f"增加了 {amount} 金币",
        "gold": gm.player.gold,
    }


@router.get("/stats")
async def get_player_stats() -> Dict[str, Any]:
    """获取玩家统计数据"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    gm = game_service.get_current_game()
    
    # 统计作物数据
    total_plots = 0
    planted_plots = 0
    mature_plots = 0
    needs_water = 0
    
    for row in gm.plots:
        for plot in row:
            total_plots += 1
            if not plot.is_empty():
                planted_plots += 1
                if plot.is_mature():
                    mature_plots += 1
                if not plot.watered_today:
                    needs_water += 1
    
    return {
        "total_plots": total_plots,
        "planted_plots": planted_plots,
        "mature_plots": mature_plots,
        "empty_plots": total_plots - planted_plots,
        "needs_water": needs_water,
        "gold": gm.player.money,
        "level": gm.player.level,
        "exp": gm.player.exp,
    }


@router.get("/achievements")
async def get_achievements() -> List[Dict[str, Any]]:
    """获取成就列表"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    gm = game_service.get_current_game()
    achievements = []
    
    for achievement in gm.achievement_manager.achievements:
        achievements.append({
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "unlocked": achievement.unlocked,
            "progress": achievement.progress,
            "target": achievement.target,
            "reward_text": achievement.reward_text,
        })
    
    return achievements
