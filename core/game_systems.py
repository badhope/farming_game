"""
游戏系统整合模块
整合所有游戏系统，实现系统间的联动机制
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random
from datetime import datetime

from models.stamina import StaminaSystem, ActionType
from models.soil import SoilManager, FertilizerType
from models.weather import WeatherAgricultureSystem, WeatherType
from models.level_system import LevelSystem
from models.animal import AnimalManager, AnimalType
from models.color_system import ColorCustomizationSystem
from core.dynamics import (
    ProbabilityEngine, DamageCalculator, GrowthCalculator, 
    EconomyCalculator, BalanceSystem, StatSystem, DynamicStat, StatModifier
)


class GamePhase(Enum):
    EARLY = "early"
    MID = "mid"
    LATE = "late"
    ENDGAME = "endgame"


@dataclass
class GameContext:
    day: int = 1
    season: str = "spring"
    year: int = 1
    phase: GamePhase = GamePhase.EARLY
    total_playtime: float = 0.0
    session_count: int = 0


@dataclass
class PlayerState:
    name: str = "农夫"
    level: int = 1
    exp: int = 0
    money: int = 500
    stamina: int = 100
    max_stamina: int = 100
    reputation: int = 0
    karma: int = 0
    
    skills: Dict[str, int] = field(default_factory=lambda: {
        "farming": 1,
        "mining": 1,
        "fishing": 1,
        "combat": 1,
        "cooking": 1,
        "crafting": 1
    })
    
    skill_exp: Dict[str, int] = field(default_factory=dict)


@dataclass
class WorldState:
    weather: str = "sunny"
    temperature: int = 20
    humidity: int = 50
    
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    world_flags: Dict[str, bool] = field(default_factory=dict)
    unlocked_areas: List[str] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)


class IntegratedGameSystem:
    
    def __init__(self):
        self.context = GameContext()
        self.player_state = PlayerState()
        self.world_state = WorldState()
        
        self.stamina_system = StaminaSystem()
        self.soil_manager = SoilManager()
        self.weather_system = WeatherAgricultureSystem()
        self.level_system = LevelSystem()
        self.animal_manager = AnimalManager()
        self.color_system = ColorCustomizationSystem()
        
        self.stat_system = StatSystem()
        self.balance_system = BalanceSystem()
        
        self._init_stat_system()
        self._init_balance_system()
        
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.pending_events: List[Dict] = []
        
        self.on_day_advance: Optional[Callable] = None
        self.on_level_up: Optional[Callable] = None
        self.on_stamina_exhausted: Optional[Callable] = None
        self.on_weather_change: Optional[Callable] = None
    
    def _init_stat_system(self):
        self.stat_system.add_stat("strength", 10, 1, 100)
        self.stat_system.add_stat("agility", 10, 1, 100)
        self.stat_system.add_stat("intelligence", 10, 1, 100)
        self.stat_system.add_stat("endurance", 10, 1, 100)
        self.stat_system.add_stat("luck", 10, 1, 100)
        
        self.stat_system.set_formula(
            "max_stamina",
            "100 + endurance * 5",
            ["endurance"]
        )
        
        self.stat_system.set_formula(
            "carry_capacity",
            "20 + strength * 2",
            ["strength"]
        )
        
        self.stat_system.set_formula(
            "crit_chance",
            "0.05 + luck * 0.01",
            ["luck"]
        )
    
    def _init_balance_system(self):
        self.balance_system.set_base_value("exp_per_level", 100)
        self.balance_system.set_multiplier("exp_growth", 1.5)
        
        self.balance_system.set_base_value("crop_value", 50)
        self.balance_system.set_multiplier("crop_value_growth", 1.1)
        
        self.balance_system.set_threshold("stamina_cost", 1, 50)
        self.balance_system.set_threshold("reward_multiplier", 0.5, 3.0)
    
    def register_event_handler(self, event_type: str, handler: Callable):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit_event(self, event_type: str, data: Dict = None):
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            handler(data or {})
    
    def perform_action(self, action_type: ActionType, count: int = 1, 
                       context: Dict = None) -> Dict:
        context = context or {}
        
        stamina_cost = self._calculate_stamina_cost(action_type, context)
        
        if not self.stamina_system.can_perform_action(action_type, count):
            return {
                "success": False,
                "message": "体力不足！",
                "stamina_needed": stamina_cost * count
            }
        
        result = self.stamina_system.perform_action(action_type, count)
        
        if result["success"]:
            self._apply_action_effects(action_type, context)
            
            exp_gained = self._calculate_exp_gain(action_type, context)
            self._add_exp(exp_gained)
            
            self._check_skill_progression(action_type)
        
        return result
    
    def _calculate_stamina_cost(self, action_type: ActionType, context: Dict) -> int:
        base_cost = self.stamina_system.get_action_cost(action_type)
        
        weather_modifier = self.weather_system.get_stamina_modifier()
        
        skill = self._get_relevant_skill(action_type)
        skill_reduction = 1 - self.player_state.skills.get(skill, 1) * 0.02
        
        final_cost = int(base_cost * weather_modifier * skill_reduction)
        
        return self.balance_system.clamp_value("stamina_cost", final_cost)
    
    def _get_relevant_skill(self, action_type: ActionType) -> str:
        skill_mapping = {
            ActionType.PLANT: "farming",
            ActionType.WATER: "farming",
            ActionType.HARVEST: "farming",
            ActionType.EXPLORE: "mining",
            ActionType.FEED_ANIMAL: "farming",
            ActionType.CRAFT: "crafting",
            ActionType.BUILD: "crafting",
            ActionType.FISH: "fishing",
            ActionType.MINE: "mining",
        }
        return skill_mapping.get(action_type, "farming")
    
    def _apply_action_effects(self, action_type: ActionType, context: Dict):
        if action_type == ActionType.PLANT:
            self._handle_plant_action(context)
        elif action_type == ActionType.HARVEST:
            self._handle_harvest_action(context)
        elif action_type == ActionType.EXPLORE:
            self._handle_explore_action(context)
    
    def _handle_plant_action(self, context: Dict):
        row, col = context.get("position", (0, 0))
        crop_type = context.get("crop_type", "")
        
        soil_state = self.soil_manager.get_soil_state(row, col)
        if soil_state:
            growth_multiplier = soil_state.get_growth_multiplier()
            weather_modifier = self.weather_system.get_crop_growth_modifier(crop_type)
    
    def _handle_harvest_action(self, context: Dict):
        crop_type = context.get("crop_type", "")
        quality = context.get("quality", 1.0)
        
        luck = self.stat_system.get_stat("luck")
        crit, multiplier = ProbabilityEngine.critical_hit(0.05, luck * 0.01)
        
        if crit:
            quality *= multiplier
    
    def _handle_explore_action(self, context: Dict):
        area = context.get("area", "forest")
        
        luck = self.stat_system.get_stat("luck")
        if ProbabilityEngine.chance(0.1 + luck * 0.01):
            self._trigger_random_event(area)
    
    def _trigger_random_event(self, area: str):
        events = [
            {"type": "treasure", "message": "发现了宝藏！", "rewards": {"money": 100}},
            {"type": "encounter", "message": "遇到了旅行商人！", "rewards": {"item": "rare_seed"}},
            {"type": "danger", "message": "遇到了野兽！", "damage": 10},
            {"type": "secret", "message": "发现了秘密地点！", "rewards": {"exp": 50}},
        ]
        
        event = random.choice(events)
        self.pending_events.append(event)
        self.emit_event("random_event", event)
    
    def _calculate_exp_gain(self, action_type: ActionType, context: Dict) -> int:
        base_exp = {
            ActionType.PLANT: 5,
            ActionType.WATER: 2,
            ActionType.HARVEST: 10,
            ActionType.EXPLORE: 20,
            ActionType.FEED_ANIMAL: 3,
            ActionType.CRAFT: 15,
            ActionType.BUILD: 25,
            ActionType.FISH: 15,
            ActionType.MINE: 20,
        }
        
        exp = base_exp.get(action_type, 5)
        
        level_modifier = 1 + self.player_state.level * 0.05
        
        return int(exp * level_modifier)
    
    def _add_exp(self, amount: int):
        result = self.level_system.add_exp(amount)
        self.player_state.exp += amount
        
        for level in result.get("level_ups", []):
            self.player_state.level = level
            self._on_level_up(level)
    
    def _on_level_up(self, new_level: int):
        self.stamina_system.upgrade_max_stamina(10)
        self.player_state.max_stamina = self.stamina_system.max_stamina
        
        self.color_system.unlock_color_by_level(new_level)
        
        self.emit_event("level_up", {"level": new_level})
        
        if self.on_level_up:
            self.on_level_up(new_level)
    
    def _check_skill_progression(self, action_type: ActionType):
        skill = self._get_relevant_skill(action_type)
        current_level = self.player_state.skills.get(skill, 1)
        
        exp_gain = random.randint(1, 3)
        current_exp = self.player_state.skill_exp.get(skill, 0)
        new_exp = current_exp + exp_gain
        
        exp_needed = current_level * 100
        
        if new_exp >= exp_needed:
            self.player_state.skills[skill] = current_level + 1
            self.player_state.skill_exp[skill] = new_exp - exp_needed
            self.emit_event("skill_up", {"skill": skill, "level": current_level + 1})
        else:
            self.player_state.skill_exp[skill] = new_exp
    
    def advance_day(self) -> Dict:
        result = {
            "day": self.context.day,
            "events": [],
            "changes": {}
        }
        
        self.context.day += 1
        self.context.total_playtime += 24
        
        stamina_result = self.stamina_system.new_day()
        self.player_state.stamina = self.stamina_system.current_stamina
        
        weather_result = self.weather_system.advance_day()
        if weather_result.get("weather_changed"):
            self.world_state.weather = self.weather_system.current_weather.value
            result["events"].append(f"天气变化：{self.weather_system.get_weather_display()}")
        
        for row in range(self.soil_manager.plot_size):
            for col in range(self.soil_manager.plot_size):
                soil_result = self.soil_manager.new_day(row, col, True, True)
                if soil_result.get("fertilizer_expired"):
                    result["events"].append(f"地块({row},{col})的肥料效果已消失")
        
        animal_result = self.animal_manager.advance_day()
        for change in animal_result.get("changes", []):
            result["events"].append(f"动物状态变化：{change}")
        
        if self.context.day % 28 == 0:
            self._advance_season()
        
        self._update_game_phase()
        
        if self.on_day_advance:
            self.on_day_advance(result)
        
        self.emit_event("day_advance", result)
        
        return result
    
    def _advance_season(self):
        seasons = ["spring", "summer", "autumn", "winter"]
        current_index = seasons.index(self.context.season) if self.context.season in seasons else 0
        
        next_index = (current_index + 1) % 4
        self.context.season = seasons[next_index]
        
        if next_index == 0:
            self.context.year += 1
    
    def _update_game_phase(self):
        total_days = self.context.day + (self.context.year - 1) * 112
        
        if total_days < 28:
            self.context.phase = GamePhase.EARLY
        elif total_days < 84:
            self.context.phase = GamePhase.MID
        elif total_days < 168:
            self.context.phase = GamePhase.LATE
        else:
            self.context.phase = GamePhase.ENDGAME
    
    def calculate_crop_yield(self, crop_type: str, quality: float, 
                             soil_row: int, soil_col: int) -> Dict:
        base_yield = random.randint(1, 3)
        
        soil_state = self.soil_manager.get_soil_state(soil_row, soil_col)
        soil_bonus = soil_state.get_quality_bonus() if soil_state else 0
        
        weather_modifier = self.weather_system.get_crop_growth_modifier(crop_type)
        
        farming_skill = self.player_state.skills.get("farming", 1)
        skill_bonus = farming_skill * 0.05
        
        final_yield = int(base_yield * (1 + soil_bonus + skill_bonus) * weather_modifier)
        final_quality = quality * (1 + soil_bonus)
        
        return {
            "amount": max(1, final_yield),
            "quality": min(2.0, final_quality),
            "base_yield": base_yield
        }
    
    def calculate_item_price(self, item_type: str, quality: float, 
                             is_selling: bool = True) -> int:
        base_prices = {
            "crop": 50,
            "animal_product": 100,
            "mineral": 75,
            "fish": 60,
            "crafted": 150
        }
        
        base_price = base_prices.get(item_type, 50)
        
        quality_multiplier = 0.5 + quality
        
        reputation_modifier = 1 + self.player_state.reputation * 0.001
        
        if is_selling:
            price = base_price * quality_multiplier * reputation_modifier
        else:
            price = base_price / quality_multiplier / reputation_modifier
        
        return int(price)
    
    def get_game_summary(self) -> Dict:
        return {
            "player": {
                "name": self.player_state.name,
                "level": self.player_state.level,
                "money": self.player_state.money,
                "stamina": f"{self.player_state.stamina}/{self.player_state.max_stamina}",
                "reputation": self.player_state.reputation,
                "karma": self.player_state.karma
            },
            "world": {
                "day": self.context.day,
                "season": self.context.season,
                "year": self.context.year,
                "weather": self.world_state.weather,
                "phase": self.context.phase.value
            },
            "skills": self.player_state.skills,
            "relationships": dict(list(self.world_state.npc_relationships.items())[:5]),
            "animals": len(self.animal_manager.animals),
            "playtime_hours": round(self.context.total_playtime / 60, 1)
        }
    
    def get_save_data(self) -> Dict:
        return {
            "context": {
                "day": self.context.day,
                "season": self.context.season,
                "year": self.context.year,
                "phase": self.context.phase.value,
                "total_playtime": self.context.total_playtime,
                "session_count": self.context.session_count
            },
            "player_state": {
                "name": self.player_state.name,
                "level": self.player_state.level,
                "exp": self.player_state.exp,
                "money": self.player_state.money,
                "stamina": self.player_state.stamina,
                "max_stamina": self.player_state.max_stamina,
                "reputation": self.player_state.reputation,
                "karma": self.player_state.karma,
                "skills": self.player_state.skills,
                "skill_exp": self.player_state.skill_exp
            },
            "world_state": {
                "weather": self.world_state.weather,
                "temperature": self.world_state.temperature,
                "humidity": self.world_state.humidity,
                "npc_relationships": self.world_state.npc_relationships,
                "world_flags": self.world_state.world_flags,
                "unlocked_areas": self.world_state.unlocked_areas,
                "completed_quests": self.world_state.completed_quests
            },
            "stamina": self.stamina_system.get_save_data(),
            "soil": self.soil_manager.get_save_data(),
            "weather": self.weather_system.get_save_data(),
            "level": self.level_system.get_save_data(),
            "animals": self.animal_manager.to_dict(),
            "story": self.story_system.get_save_data(),
            "colors": self.color_system.get_save_data()
        }
    
    def load_save_data(self, data: Dict):
        context_data = data.get("context", {})
        self.context = GameContext(
            day=context_data.get("day", 1),
            season=context_data.get("season", "spring"),
            year=context_data.get("year", 1),
            phase=GamePhase(context_data.get("phase", "early")),
            total_playtime=context_data.get("total_playtime", 0),
            session_count=context_data.get("session_count", 0) + 1
        )
        
        player_data = data.get("player_state", {})
        self.player_state = PlayerState(
            name=player_data.get("name", "农夫"),
            level=player_data.get("level", 1),
            exp=player_data.get("exp", 0),
            money=player_data.get("money", 500),
            stamina=player_data.get("stamina", 100),
            max_stamina=player_data.get("max_stamina", 100),
            reputation=player_data.get("reputation", 0),
            karma=player_data.get("karma", 0),
            skills=player_data.get("skills", {"farming": 1}),
            skill_exp=player_data.get("skill_exp", {})
        )
        
        world_data = data.get("world_state", {})
        self.world_state = WorldState(
            weather=world_data.get("weather", "sunny"),
            temperature=world_data.get("temperature", 20),
            humidity=world_data.get("humidity", 50),
            npc_relationships=world_data.get("npc_relationships", {}),
            world_flags=world_data.get("world_flags", {}),
            unlocked_areas=world_data.get("unlocked_areas", []),
            completed_quests=world_data.get("completed_quests", [])
        )
        
        self.stamina_system.load_save_data(data.get("stamina", {}))
        self.soil_manager.load_save_data(data.get("soil", {}))
        self.weather_system.load_save_data(data.get("weather", {}))
        self.level_system.load_save_data(data.get("level", {}))
        self.animal_manager.from_dict(data.get("animals", {}))
        self.story_system.load_save_data(data.get("story", {}))
        self.color_system.load_save_data(data.get("colors", {}))
