"""
游戏会话管理服务
管理游戏状态，提供核心游戏逻辑的 API 接口
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from config.settings import GameConfig, CropData, Season, Weather
from core.game_manager import GameManager
from core.time_system import TimeSystem
from core.economy import EconomySystem
from ai import AIFarmAssistant, AIPlantingAdvisor, AIFarmAnalyzer


@dataclass
class GameState:
    """游戏状态数据类"""
    season: str
    day: int
    year: int
    weather: str
    player_name: str
    gold: int
    level: int
    exp: int
    stamina: int
    max_stamina: int
    plot_size: int
    difficulty: str = "normal"
    game_number: int = 1
    total_games_played: int = 0


@dataclass
class PlotData:
    """农田地块数据"""
    row: int
    col: int
    has_crop: bool
    crop_name: Optional[str]
    crop_emoji: Optional[str]
    growth_stage: int
    growth_progress: float
    needs_water: bool
    days_since_planted: int
    is_mature: bool


class GameSessionService:
    """
    游戏会话服务
    
    管理游戏实例状态，提供核心游戏逻辑接口
    """
    
    def __init__(self):
        self._current_game: Optional[GameManager] = None
        self._save_path = "saves"
        os.makedirs(self._save_path, exist_ok=True)
    
    def create_new_game(self, player_name: str = "农夫", difficulty: str = "normal") -> GameState:
        """创建新游戏"""
        self._current_game = GameManager(difficulty=difficulty)
        self._current_game.player.name = player_name
        return self._get_game_state()
    
    def start_new_game_plus(self) -> GameState:
        """开始新游戏+，继承部分进度"""
        if not self._current_game:
            raise RuntimeError("No active game session")
        
        old_gm = self._current_game
        old_difficulty = getattr(old_gm, 'difficulty', 'normal')
        old_total_games = getattr(old_gm, 'total_games_played', 0)
        
        self._current_game = GameManager(difficulty=old_difficulty)
        self._current_game.player.name = old_gm.player.name
        self._current_game.player.money = GameConfig.Difficulty.INITIAL_MONEY.get(
            old_difficulty, GameConfig.Difficulty.INITIAL_MONEY[GameConfig.Difficulty.NORMAL]
        )
        self._current_game.player.max_stamina = GameConfig.Difficulty.INITIAL_STAMINA.get(
            old_difficulty, GameConfig.Difficulty.INITIAL_STAMINA[GameConfig.Difficulty.NORMAL]
        )
        self._current_game.player.stamina = self._current_game.player.max_stamina
        
        self._current_game.total_games_played = old_total_games + 1
        self._current_game.game_number = self._current_game.total_games_played
        
        self._current_game.player.inventory = {}
        self._current_game.player.seeds = {}
        
        return self._get_game_state()
    
    def get_current_game(self) -> Optional[GameManager]:
        """获取当前游戏实例"""
        return self._current_game
    
    def has_active_game(self) -> bool:
        """检查是否有进行中的游戏"""
        return self._current_game is not None
    
    def _get_game_state(self) -> GameState:
        """获取当前游戏状态"""
        if not self._current_game:
            raise RuntimeError("No active game session")
        
        gm = self._current_game
        time_sys = gm.time_system
        
        return GameState(
            season=time_sys.season.value,
            day=time_sys.day,
            year=time_sys.year,
            weather=gm.time_system.weather.value,
            player_name=gm.player.name,
            gold=gm.player.money,
            level=gm.player.level,
            exp=gm.player.exp,
            stamina=gm.player.stamina,
            max_stamina=gm.player.max_stamina,
            plot_size=gm.player.get_plot_size(),
            difficulty=getattr(gm, 'difficulty', 'normal'),
            game_number=getattr(gm, 'game_number', 1),
            total_games_played=getattr(gm, 'total_games_played', 0),
        )
    
    def get_farm_plots(self) -> List[PlotData]:
        """获取所有农田数据"""
        if not self._current_game:
            raise RuntimeError("No active game session")
        
        plots = []
        for row_idx, row in enumerate(self._current_game.plots):
            for col_idx, plot in enumerate(row):
                plot_data = PlotData(
                    row=row_idx,
                    col=col_idx,
                    has_crop=not plot.is_empty(),
                    crop_name=plot.crop.name if plot.crop else None,
                    crop_emoji=plot.crop.emoji if plot.crop else None,
                    growth_stage=plot.growth_stage,
                    growth_progress=plot.get_growth_progress(),
                    needs_water=not plot.watered_today if plot.crop else False,
                    days_since_planted=self._current_game.time_system.day - plot.planted_day if plot.crop else 0,
                    is_mature=plot.is_mature(),
                )
                plots.append(plot_data)
        
        return plots
    
    def plant_crop(self, row: int, col: int, crop_name: str) -> Dict[str, Any]:
        """种植作物"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        
        # 检查位置有效性
        if row < 0 or row >= len(gm.plots) or col < 0 or col >= len(gm.plots[0]):
            return {"success": False, "message": "无效的田地位置"}
        
        plot = gm.plots[row][col]
        
        # 检查是否已有作物
        if not plot.is_empty():
            return {"success": False, "message": "这块地已经有作物了"}
        
        # 获取作物数据
        crop_data = CropData.CROPS.get(crop_name)
        if not crop_data:
            return {"success": False, "message": f"未知的作物: {crop_name}"}
        
        # 检查季节
        current_season = gm.time_system.season
        if current_season not in crop_data["seasons"]:
            return {"success": False, "message": f"{current_season.value}不适合种植{crop_name}"}
        
        # 检查金币
        seed_price = crop_data["seed_price"]
        if gm.player.money < seed_price:
            return {"success": False, "message": f"金币不足，需要 {seed_price} 金币"}
        
        # 扣除金币并种植
        gm.player.money -= seed_price
        from models.crop import Crop
        plot.crop = Crop(
            name=crop_name,
            seed_price=seed_price,
            sell_price=crop_data["sell_price"],
            grow_days=crop_data["grow_days"],
            seasons=crop_data["seasons"],
            water_needed=crop_data["water_needed"],
            emoji=crop_data["emoji"],
            crop_type=crop_data["crop_type"],
            description=crop_data.get("description", ""),
        )
        plot.planted_day = gm.time_system.day
        plot.watered_today = False
        plot.growth_stage = 0
        plot.days_watered = 0
        
        return {
            "success": True, 
            "message": f"成功种植 {crop_name}！花费 {seed_price} 金币",
            "remaining_gold": gm.player.money,
        }
    
    def water_crop(self, row: int, col: int) -> Dict[str, Any]:
        """浇水"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        
        if row < 0 or row >= len(gm.plots) or col < 0 or col >= len(gm.plots[0]):
            return {"success": False, "message": "无效的田地位置"}
        
        plot = gm.plots[row][col]
        
        if plot.is_empty():
            return {"success": False, "message": "这块地是空的"}
        
        if plot.watered_today:
            return {"success": False, "message": "今天已经浇过水了"}
        
        # 浇水
        plot.watered_today = True
        plot.days_watered += 1
        
        return {"success": True, "message": "浇水成功！"}
    
    def harvest_crop(self, row: int, col: int) -> Dict[str, Any]:
        """收获作物"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        
        if row < 0 or row >= len(gm.plots) or col < 0 or col >= len(gm.plots[0]):
            return {"success": False, "message": "无效的田地位置"}
        
        plot = gm.plots[row][col]
        
        if plot.is_empty():
            return {"success": False, "message": "这块地是空的"}
        
        if not plot.is_mature():
            return {"success": False, "message": "作物还没有成熟"}
        
        # 收获
        crop = plot.crop
        sell_price = crop.sell_price
        gm.player.money += sell_price
        
        # 清空地块
        plot.crop = None
        plot.planted_day = 0
        plot.watered_today = False
        plot.growth_stage = 0
        plot.days_watered = 0
        
        return {
            "success": True,
            "message": f"收获了 {crop.name}！获得 {sell_price} 金币",
            "earned_gold": sell_price,
            "remaining_gold": gm.player.money,
        }
    
    def clear_plot(self, row: int, col: int) -> Dict[str, Any]:
        """清空地块"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        
        if row < 0 or row >= len(gm.plots) or col < 0 or col >= len(gm.plots[0]):
            return {"success": False, "message": "无效的田地位置"}
        
        plot = gm.plots[row][col]
        
        if plot.is_empty():
            return {"success": False, "message": "这块地已经是空的"}
        
        # 清空
        plot.crop = None
        plot.planted_day = 0
        plot.watered_today = False
        plot.growth_stage = 0
        plot.days_watered = 0
        
        return {"success": True, "message": "地块已清空"}
    
    def advance_day(self) -> Dict[str, Any]:
        """推进到下一天"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        
        # 使用 GameManager 的 advance_day 方法
        result = gm.advance_day()
        
        # 获取新状态
        new_state = self._get_game_state()
        
        return {
            "success": True,
            "message": f"第 {new_state.day} 天 - {new_state.season} {new_state.year}年",
            "crops_grown": result.crops_grown,
            "crops_matured": result.crops_matured,
            "events": result.events,
            "new_state": asdict(new_state),
        }
    
    def get_available_crops(self) -> List[Dict[str, Any]]:
        """获取可种植作物列表"""
        if not self._current_game:
            return []
        
        current_season = self._current_game.time_system.season
        crops = []
        
        for name, data in CropData.CROPS.items():
            if current_season in data["seasons"]:
                crops.append({
                    "id": name,
                    "name": name,
                    "emoji": data["emoji"],
                    "seed_price": data["seed_price"],
                    "sell_price": data["sell_price"],
                    "grow_days": data["grow_days"],
                    "season": current_season.value,
                    "description": data.get("description", ""),
                })
        
        return crops
    
    def save_game(self, save_name: str = "save") -> Dict[str, Any]:
        """保存游戏"""
        if not self._current_game:
            return {"success": False, "message": "没有进行中的游戏"}
        
        gm = self._current_game
        save_data = {
            "version": "4.1.0",
            "player": {
                "name": gm.player.name,
                "gold": gm.player.money,
                "level": gm.player.level,
                "exp": gm.player.exp,
                "stamina": gm.player.stamina,
                "max_stamina": gm.player.max_stamina,
            },
            "game": {
                "difficulty": getattr(gm, 'difficulty', 'normal'),
                "game_number": getattr(gm, 'game_number', 1),
                "total_games_played": getattr(gm, 'total_games_played', 0),
            },
            "time": {
                "season": gm.time_system.season.value,
                "day": gm.time_system.day,
                "year": gm.time_system.year,
                "weather": gm.time_system.weather.value,
            },
            "plots": [],
        }
        
        # 保存农田数据
        for row in gm.plots:
            row_data = []
            for plot in row:
                row_data.append({
                    "has_crop": not plot.is_empty(),
                    "crop_name": plot.crop.name if plot.crop else None,
                    "planted_day": plot.planted_day,
                    "watered_today": plot.watered_today,
                    "growth_stage": plot.growth_stage,
                    "days_watered": plot.days_watered,
                })
            save_data["plots"].append(row_data)
        
        # 写入文件
        save_file = os.path.join(self._save_path, f"{save_name}.json")
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        return {"success": True, "message": f"游戏已保存: {save_name}"}
    
    def load_game(self, save_name: str = "save") -> Dict[str, Any]:
        """加载游戏"""
        save_file = os.path.join(self._save_path, f"{save_name}.json")
        
        if not os.path.exists(save_file):
            return {"success": False, "message": f"存档不存在: {save_name}"}
        
        try:
            with open(save_file, "r", encoding="utf-8") as f:
                save_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            return {"success": False, "message": f"读取存档失败: {str(e)}"}
        
        if "version" not in save_data or "player" not in save_data:
            return {"success": False, "message": "存档文件格式不正确"}
        
        try:
            self._current_game = GameManager()
            
            player_data = save_data["player"]
            self._current_game.player.name = player_data.get("name", "农夫")
            self._current_game.player.money = player_data.get("gold", 500)
            self._current_game.player.level = player_data.get("level", 1)
            self._current_game.player.exp = player_data.get("exp", 0)
            self._current_game.player.stamina = player_data.get("stamina", 100)
            self._current_game.player.max_stamina = player_data.get("max_stamina", 100)
            
            time_data = save_data.get("time", {})
            try:
                self._current_game.time_system.season = Season(time_data.get("season", "春天"))
            except ValueError:
                self._current_game.time_system.season = Season.SPRING
            self._current_game.time_system.day = time_data.get("day", 1)
            self._current_game.time_system.year = time_data.get("year", 1)
            try:
                self._current_game.time_system.weather = Weather(time_data.get("weather", "晴天"))
            except ValueError:
                self._current_game.time_system.weather = Weather.SUNNY
            
            plots_data = save_data.get("plots", [])
            for row_idx, row_data in enumerate(plots_data):
                if row_idx >= len(self._current_game.plots):
                    break
                for col_idx, plot_data in enumerate(row_data):
                    if col_idx >= len(self._current_game.plots[row_idx]):
                        break
                    plot = self._current_game.plots[row_idx][col_idx]
                    if plot_data.get("has_crop"):
                        crop_name = plot_data.get("crop_name")
                        if crop_name and crop_name in CropData.CROPS:
                            data = CropData.CROPS[crop_name]
                            from models.crop import Crop
                            plot.crop = Crop(
                                name=crop_name,
                                seed_price=data["seed_price"],
                                sell_price=data["sell_price"],
                                grow_days=data["grow_days"],
                                seasons=data["seasons"],
                                water_needed=data["water_needed"],
                                emoji=data["emoji"],
                                crop_type=data["crop_type"],
                                description=data.get("description", ""),
                            )
                    plot.planted_day = plot_data.get("planted_day", 0)
                    plot.watered_today = plot_data.get("watered_today", False)
                    plot.growth_stage = plot_data.get("growth_stage", 0)
                    plot.days_watered = plot_data.get("days_watered", 0)
            
            state = self._get_game_state()
            return {"success": True, "message": f"游戏已加载: {save_name}", "state": asdict(state)}
        except Exception as e:
            return {"success": False, "message": f"加载存档失败: {str(e)}"}
    
    def get_save_files(self) -> List[str]:
        """获取存档列表"""
        saves = []
        for f in os.listdir(self._save_path):
            if f.endswith(".json"):
                saves.append(f[:-5])  # 移除 .json
        return saves
    
    # ========== AI 集成 ==========
    
    def chat_with_ai(self, message: str) -> Dict[str, Any]:
        """与 AI 助手对话"""
        if not self._current_game:
            return {"response": "没有进行中的游戏，请先创建新游戏"}
        
        game_state = {
            "season": self._current_game.time_system.season.value,
            "day": self._current_game.time_system.day,
            "year": self._current_game.time_system.year,
            "gold": self._current_game.player.money,
            "level": self._current_game.player.level,
        }
        
        response = self._current_game.ai_assistant.chat(message, game_state)
        return {"response": response}
    
    def get_planting_advice(self) -> List[Dict[str, Any]]:
        """获取种植建议"""
        if not self._current_game:
            return []
        
        season = self._current_game.time_system.season.value
        days_remaining = GameConfig.DAYS_PER_SEASON - self._current_game.time_system.day
        budget = self._current_game.player.money
        
        advice = self._current_game.ai_advisor.get_best_crop(season, days_remaining, budget)
        
        if advice["success"]:
            return [advice]
        return []
    
    def analyze_farm(self) -> Dict[str, Any]:
        """分析农场"""
        if not self._current_game:
            return {"score": 0, "message": "没有进行中的游戏"}
        
        plots_data = []
        for row in self._current_game.plots:
            for plot in row:
                plots_data.append({
                    "has_crop": not plot.is_empty(),
                    "is_mature": plot.is_mature(),
                    "needs_water": not plot.watered_today if plot.crop else False,
                })
        
        game_state = {
            "gold": self._current_game.player.money,
            "level": self._current_game.player.level,
            "season": self._current_game.time_system.season.value,
            "plots": plots_data,
        }
        
        analysis = self._current_game.ai_analyzer.analyze(game_state)
        return analysis


# 全局游戏会话服务实例
game_service = GameSessionService()
