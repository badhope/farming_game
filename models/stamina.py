"""
体力值系统模块
管理玩家体力消耗和恢复
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Callable
from enum import Enum


class ActionType(Enum):
    PLANT = "plant"
    WATER = "water"
    HARVEST = "harvest"
    EXPLORE = "explore"
    FEED_ANIMAL = "feed_animal"
    CRAFT = "craft"
    BUILD = "build"
    FISH = "fish"
    MINE = "mine"


@dataclass
class StaminaConfig:
    max_stamina: int = 100
    min_stamina: int = 0
    regen_rate: int = 5
    regen_interval: int = 60
    rest_bonus: int = 20
    food_bonus: Dict = field(default_factory=lambda: {
        "bread": 15,
        "apple": 10,
        "meat": 25,
        "energy_drink": 40,
        "cooked_meal": 35
    })


@dataclass
class ActionCost:
    action_type: ActionType
    base_cost: int
    description: str


class StaminaSystem:
    
    ACTION_COSTS = {
        ActionType.PLANT: ActionCost(ActionType.PLANT, 5, "种植作物"),
        ActionType.WATER: ActionCost(ActionType.WATER, 2, "浇水"),
        ActionType.HARVEST: ActionCost(ActionType.HARVEST, 3, "收获作物"),
        ActionType.EXPLORE: ActionCost(ActionType.EXPLORE, 15, "户外探险"),
        ActionType.FEED_ANIMAL: ActionCost(ActionType.FEED_ANIMAL, 3, "喂养动物"),
        ActionType.CRAFT: ActionCost(ActionType.CRAFT, 8, "制作物品"),
        ActionType.BUILD: ActionCost(ActionType.BUILD, 12, "建造建筑"),
        ActionType.FISH: ActionCost(ActionType.FISH, 10, "钓鱼"),
        ActionType.MINE: ActionCost(ActionType.MINE, 15, "采矿"),
    }
    
    def __init__(self, config: Optional[StaminaConfig] = None):
        self.config = config or StaminaConfig()
        self.current_stamina: int = self.config.max_stamina
        self.max_stamina: int = self.config.max_stamina
        self.stamina_modifier: float = 1.0
        self.on_stamina_change: Optional[Callable] = None
        self.on_exhausted: Optional[Callable] = None
        self.is_exhausted: bool = False
    
    def get_stamina(self) -> int:
        return self.current_stamina
    
    def get_max_stamina(self) -> int:
        return self.max_stamina
    
    def get_stamina_percentage(self) -> float:
        return self.current_stamina / self.max_stamina if self.max_stamina > 0 else 0.0
    
    def can_perform_action(self, action_type: ActionType, count: int = 1) -> bool:
        cost = self.get_action_cost(action_type) * count
        return self.current_stamina >= cost
    
    def get_action_cost(self, action_type: ActionType) -> int:
        action_cost = self.ACTION_COSTS.get(action_type)
        if action_cost:
            return int(action_cost.base_cost * self.stamina_modifier)
        return 5
    
    def perform_action(self, action_type: ActionType, count: int = 1) -> Dict:
        cost = self.get_action_cost(action_type) * count
        
        if not self.can_perform_action(action_type, count):
            return {
                "success": False,
                "message": "体力不足！",
                "stamina_needed": cost,
                "current_stamina": self.current_stamina
            }
        
        self.current_stamina -= cost
        self._check_exhaustion()
        
        if self.on_stamina_change:
            self.on_stamina_change(self.current_stamina, self.max_stamina)
        
        action_cost = self.ACTION_COSTS.get(action_type)
        action_name = action_cost.description if action_cost else "动作"
        
        return {
            "success": True,
            "message": f"执行{action_name}消耗 {cost} 体力",
            "stamina_used": cost,
            "current_stamina": self.current_stamina
        }
    
    def restore_stamina(self, amount: int) -> Dict:
        old_stamina = self.current_stamina
        self.current_stamina = min(self.max_stamina, self.current_stamina + amount)
        restored = self.current_stamina - old_stamina
        
        if self.is_exhausted and self.current_stamina > 20:
            self.is_exhausted = False
        
        if self.on_stamina_change:
            self.on_stamina_change(self.current_stamina, self.max_stamina)
        
        return {
            "restored": restored,
            "current_stamina": self.current_stamina,
            "max_stamina": self.max_stamina
        }
    
    def eat_food(self, food_type: str) -> Dict:
        food_bonus = self.config.food_bonus.get(food_type, 10)
        result = self.restore_stamina(food_bonus)
        result["food_type"] = food_type
        result["message"] = f"食用{food_type}恢复了 {result['restored']} 体力"
        return result
    
    def rest(self, hours: int = 1) -> Dict:
        bonus = self.config.rest_bonus * hours
        result = self.restore_stamina(bonus)
        result["message"] = f"休息{hours}小时恢复了 {result['restored']} 体力"
        return result
    
    def new_day(self) -> Dict:
        self.current_stamina = self.max_stamina
        self.is_exhausted = False
        
        if self.on_stamina_change:
            self.on_stamina_change(self.current_stamina, self.max_stamina)
        
        return {
            "restored": self.max_stamina,
            "message": "新的一天，体力已完全恢复！"
        }
    
    def upgrade_max_stamina(self, amount: int = 10) -> Dict:
        self.max_stamina += amount
        self.current_stamina += amount
        
        if self.on_stamina_change:
            self.on_stamina_change(self.current_stamina, self.max_stamina)
        
        return {
            "new_max": self.max_stamina,
            "message": f"最大体力提升 {amount} 点！"
        }
    
    def set_modifier(self, modifier: float) -> None:
        self.stamina_modifier = max(0.5, min(2.0, modifier))
    
    def _check_exhaustion(self) -> None:
        if self.current_stamina <= 0:
            self.is_exhausted = True
            if self.on_exhausted:
                self.on_exhausted()
    
    def get_stamina_status(self) -> Dict:
        return {
            "current": self.current_stamina,
            "max": self.max_stamina,
            "percentage": self.get_stamina_percentage(),
            "is_exhausted": self.is_exhausted,
            "modifier": self.stamina_modifier
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_stamina": self.current_stamina,
            "max_stamina": self.max_stamina,
            "stamina_modifier": self.stamina_modifier,
            "is_exhausted": self.is_exhausted
        }
    
    def load_save_data(self, data: Dict) -> None:
        self.current_stamina = data.get("current_stamina", self.config.max_stamina)
        self.max_stamina = data.get("max_stamina", self.config.max_stamina)
        self.stamina_modifier = data.get("stamina_modifier", 1.0)
        self.is_exhausted = data.get("is_exhausted", False)
