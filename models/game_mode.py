"""
游戏模式系统模块
提供经典模式、无限模式和冒险模式三种游戏模式
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import random


class GameModeType(Enum):
    CLASSIC = "classic"
    ENDLESS = "endless"
    ADVENTURE = "adventure"


@dataclass
class ModeObjective:
    objective_id: str
    description: str
    target_value: int
    current_value: int = 0
    is_completed: bool = False
    reward: Dict = field(default_factory=dict)


@dataclass
class ModeConfig:
    mode_type: GameModeType
    name: str
    description: str
    icon: str
    initial_money: int
    initial_plot_size: int
    has_time_limit: bool
    time_limit_days: int
    has_objectives: bool
    objectives: List[ModeObjective] = field(default_factory=list)
    modifiers: Dict = field(default_factory=dict)
    unlock_condition: Optional[Dict] = None


class GameModeManager:
    
    MODE_CONFIGS = {
        GameModeType.CLASSIC: ModeConfig(
            mode_type=GameModeType.CLASSIC,
            name="🌾 经典模式",
            description="传统的农场经营体验。\n\n按自己的节奏经营农场，\n没有时间限制，\n享受悠闲的田园生活。",
            icon="🌾",
            initial_money=500,
            initial_plot_size=3,
            has_time_limit=False,
            time_limit_days=0,
            has_objectives=False,
            modifiers={
                "exp_multiplier": 1.0,
                "money_multiplier": 1.0,
                "growth_speed": 1.0
            }
        ),
        GameModeType.ENDLESS: ModeConfig(
            mode_type=GameModeType.ENDLESS,
            name="♾️ 无限模式",
            description="没有限制的农场生活。\n\n无限金币、无限种子，\n专注于建设和装饰，\n打造你梦想中的农场。",
            icon="♾️",
            initial_money=999999,
            initial_plot_size=5,
            has_time_limit=False,
            time_limit_days=0,
            has_objectives=False,
            modifiers={
                "exp_multiplier": 0.5,
                "money_multiplier": 0.0,
                "growth_speed": 2.0,
                "free_seeds": True,
                "no_weather_damage": True
            },
            unlock_condition=None
        ),
        GameModeType.ADVENTURE: ModeConfig(
            mode_type=GameModeType.ADVENTURE,
            name="⚔️ 冒险模式",
            description="充满挑战的冒险之旅。\n\n完成各种目标，\n应对随机事件，\n成为传奇农场主！",
            icon="⚔️",
            initial_money=200,
            initial_plot_size=2,
            has_time_limit=True,
            time_limit_days=365,
            has_objectives=True,
            objectives=[
                ModeObjective(
                    objective_id="earn_10000",
                    description="累计赚取10,000金币",
                    target_value=10000,
                    reward={"money": 2000, "exp": 500}
                ),
                ModeObjective(
                    objective_id="harvest_200",
                    description="收获200个作物",
                    target_value=200,
                    reward={"money": 1500, "exp": 400}
                ),
                ModeObjective(
                    objective_id="reach_level_8",
                    description="达到8级",
                    target_value=8,
                    reward={"money": 3000, "exp": 800}
                ),
                ModeObjective(
                    objective_id="explore_10",
                    description="完成10次探险",
                    target_value=10,
                    reward={"money": 1000, "exp": 300}
                ),
                ModeObjective(
                    objective_id="complete_story",
                    description="完成主线剧情",
                    target_value=1,
                    reward={"money": 5000, "exp": 1000, "achievement": "adventure_master"}
                ),
            ],
            modifiers={
                "exp_multiplier": 1.5,
                "money_multiplier": 1.2,
                "growth_speed": 0.8,
                "random_events": True,
                "harder_weather": True
            },
            unlock_condition={"type": "level", "value": 3}
        ),
    }
    
    def __init__(self):
        self.current_mode: Optional[GameModeType] = None
        self.days_remaining: int = 0
        self.objectives_progress: Dict[str, int] = {}
        self.completed_objectives: List[str] = []
        self.unlocked_modes: List[GameModeType] = [GameModeType.CLASSIC, GameModeType.ENDLESS]
        self.on_objective_complete: Optional[Callable] = None
        self.on_mode_complete: Optional[Callable] = None
    
    def get_mode_config(self, mode_type: GameModeType) -> Optional[ModeConfig]:
        return self.MODE_CONFIGS.get(mode_type)
    
    def get_all_modes(self) -> Dict[GameModeType, ModeConfig]:
        return self.MODE_CONFIGS.copy()
    
    def is_mode_unlocked(self, mode_type: GameModeType) -> bool:
        return mode_type in self.unlocked_modes
    
    def unlock_mode(self, mode_type: GameModeType) -> bool:
        if mode_type not in self.unlocked_modes:
            self.unlocked_modes.append(mode_type)
            return True
        return False
    
    def check_unlock_conditions(self, player_level: int) -> List[GameModeType]:
        newly_unlocked = []
        
        for mode_type, config in self.MODE_CONFIGS.items():
            if mode_type in self.unlocked_modes:
                continue
            
            if config.unlock_condition:
                condition = config.unlock_condition
                if condition.get("type") == "level":
                    if player_level >= condition.get("value", 999):
                        self.unlock_mode(mode_type)
                        newly_unlocked.append(mode_type)
        
        return newly_unlocked
    
    def start_mode(self, mode_type: GameModeType) -> bool:
        if mode_type not in self.unlocked_modes:
            return False
        
        config = self.get_mode_config(mode_type)
        if not config:
            return False
        
        self.current_mode = mode_type
        self.days_remaining = config.time_limit_days if config.has_time_limit else -1
        
        self.objectives_progress = {}
        self.completed_objectives = []
        
        if config.has_objectives:
            for obj in config.objectives:
                self.objectives_progress[obj.objective_id] = 0
        
        return True
    
    def advance_day(self) -> Dict:
        result = {
            "days_remaining": self.days_remaining,
            "mode_complete": False,
            "failed": False
        }
        
        if self.days_remaining > 0:
            self.days_remaining -= 1
            result["days_remaining"] = self.days_remaining
            
            if self.days_remaining <= 0:
                result["mode_complete"] = True
                result["failed"] = not self._check_mode_completion()
                
                if self.on_mode_complete:
                    self.on_mode_complete(result["failed"])
        
        return result
    
    def update_objective(self, objective_id: str, value: int) -> Optional[Dict]:
        if not self.current_mode:
            return None
        
        config = self.get_mode_config(self.current_mode)
        if not config or not config.has_objectives:
            return None
        
        if objective_id in self.completed_objectives:
            return None
        
        self.objectives_progress[objective_id] = value
        
        for obj in config.objectives:
            if obj.objective_id == objective_id:
                if value >= obj.target_value and objective_id not in self.completed_objectives:
                    self.completed_objectives.append(objective_id)
                    
                    result = {
                        "objective": obj,
                        "reward": obj.reward,
                        "all_complete": self._check_all_objectives_complete()
                    }
                    
                    if self.on_objective_complete:
                        self.on_objective_complete(obj)
                    
                    return result
        
        return None
    
    def _check_mode_completion(self) -> bool:
        if not self.current_mode:
            return False
        
        config = self.get_mode_config(self.current_mode)
        if not config or not config.has_objectives:
            return True
        
        return self._check_all_objectives_complete()
    
    def _check_all_objectives_complete(self) -> bool:
        if not self.current_mode:
            return False
        
        config = self.get_mode_config(self.current_mode)
        if not config or not config.has_objectives:
            return True
        
        for obj in config.objectives:
            if obj.objective_id not in self.completed_objectives:
                return False
        
        return True
    
    def get_objectives_status(self) -> List[Dict]:
        if not self.current_mode:
            return []
        
        config = self.get_mode_config(self.current_mode)
        if not config or not config.has_objectives:
            return []
        
        result = []
        for obj in config.objectives:
            current = self.objectives_progress.get(obj.objective_id, 0)
            result.append({
                "id": obj.objective_id,
                "description": obj.description,
                "current": current,
                "target": obj.target_value,
                "progress": min(1.0, current / obj.target_value) if obj.target_value > 0 else 1.0,
                "completed": obj.objective_id in self.completed_objectives,
                "reward": obj.reward
            })
        
        return result
    
    def get_modifier(self, modifier_name: str) -> float:
        if not self.current_mode:
            return 1.0
        
        config = self.get_mode_config(self.current_mode)
        if config and modifier_name in config.modifiers:
            return config.modifiers[modifier_name]
        
        return 1.0
    
    def has_modifier(self, modifier_name: str) -> bool:
        if not self.current_mode:
            return False
        
        config = self.get_mode_config(self.current_mode)
        return config and modifier_name in config.modifiers
    
    def get_mode_summary(self) -> Dict:
        if not self.current_mode:
            return {}
        
        config = self.get_mode_config(self.current_mode)
        
        return {
            "mode_type": self.current_mode.value,
            "name": config.name if config else "",
            "days_remaining": self.days_remaining,
            "has_time_limit": config.has_time_limit if config else False,
            "objectives": self.get_objectives_status() if config and config.has_objectives else [],
            "completed_objectives": len(self.completed_objectives),
            "total_objectives": len(config.objectives) if config and config.has_objectives else 0
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_mode": self.current_mode.value if self.current_mode else None,
            "days_remaining": self.days_remaining,
            "objectives_progress": self.objectives_progress,
            "completed_objectives": self.completed_objectives,
            "unlocked_modes": [m.value for m in self.unlocked_modes]
        }
    
    def load_save_data(self, data: Dict):
        mode_str = data.get("current_mode")
        if mode_str:
            self.current_mode = GameModeType(mode_str)
        
        self.days_remaining = data.get("days_remaining", 0)
        self.objectives_progress = data.get("objectives_progress", {})
        self.completed_objectives = data.get("completed_objectives", [])
        
        self.unlocked_modes = [GameModeType(m) for m in data.get("unlocked_modes", ["classic"])]
