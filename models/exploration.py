"""
户外探险系统模块
提供探索区域、随机事件、资源收集等功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import random


class AreaType(Enum):
    FOREST = "forest"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    CAVE = "cave"
    SECRET_GARDEN = "secret_garden"
    RUINS = "ruins"


class EventType(Enum):
    TREASURE = "treasure"
    BATTLE = "battle"
    PUZZLE = "puzzle"
    NPC = "npc"
    WEATHER = "weather"
    DISCOVERY = "discovery"
    DANGER = "danger"


@dataclass
class ExplorationReward:
    money: int = 0
    items: Dict[str, int] = field(default_factory=dict)
    exp: int = 0
    special: Optional[str] = None


@dataclass
class RandomEvent:
    event_id: str
    event_type: EventType
    title: str
    description: str
    choices: List[Dict] = field(default_factory=list)
    rewards: Optional[ExplorationReward] = None
    penalties: Optional[ExplorationReward] = None
    required_level: int = 1
    probability: float = 1.0


@dataclass
class ExplorationArea:
    area_id: str
    area_type: AreaType
    name: str
    description: str
    icon: str
    required_level: int = 1
    energy_cost: int = 20
    time_cost: int = 1
    possible_events: List[str] = field(default_factory=list)
    possible_rewards: Dict[str, float] = field(default_factory=dict)
    is_unlocked: bool = False
    times_explored: int = 0


AREAS = {
    AreaType.FOREST: ExplorationArea(
        area_id="forest",
        area_type=AreaType.FOREST,
        name="🌲 神秘森林",
        description="一片茂密的森林，传说中隐藏着许多宝藏。",
        icon="🌲",
        required_level=5,
        energy_cost=15,
        time_cost=1,
        possible_events=["forest_treasure", "wild_animal", "lost_traveler", "berry_bush"],
        possible_rewards={"wood": 0.6, "stone": 0.3, "iron_ore": 0.1}
    ),
    AreaType.MOUNTAIN: ExplorationArea(
        area_id="mountain",
        area_type=AreaType.MOUNTAIN,
        name="⛰️ 高山矿区",
        description="蕴藏丰富矿石的山脉，但也有危险。",
        icon="⛰️",
        required_level=8,
        energy_cost=25,
        time_cost=2,
        possible_events=["mine_shaft", "rock_slide", "ore_vein", "mountain_spirit"],
        possible_rewards={"stone": 0.5, "iron_ore": 0.3, "gold_ore": 0.15, "crystal": 0.05}
    ),
    AreaType.LAKE: ExplorationArea(
        area_id="lake",
        area_type=AreaType.LAKE,
        name="🏞️ 宁静湖泊",
        description="美丽的湖泊，可以钓鱼和放松。",
        icon="🏞️",
        required_level=3,
        energy_cost=10,
        time_cost=1,
        possible_events=["fishing_spot", "water_spirit", "sunken_treasure", "peaceful_rest"],
        possible_rewards={"food": 0.7, "treasure_map": 0.1}
    ),
    AreaType.CAVE: ExplorationArea(
        area_id="cave",
        area_type=AreaType.CAVE,
        name="🕳️ 深邃洞穴",
        description="黑暗的洞穴，充满了未知和危险。",
        icon="🕳️",
        required_level=10,
        energy_cost=30,
        time_cost=3,
        possible_events=["bat_swarm", "hidden_chamber", "crystal_cave", "ancient_ruins"],
        possible_rewards={"crystal": 0.3, "gold_ore": 0.3, "rare_gem": 0.1}
    ),
    AreaType.SECRET_GARDEN: ExplorationArea(
        area_id="secret_garden",
        area_type=AreaType.SECRET_GARDEN,
        name="🌸 秘密花园",
        description="传说中的神秘花园，四季花开。",
        icon="🌸",
        required_level=12,
        energy_cost=20,
        time_cost=2,
        possible_events=["flower_fairy", "magic_plant", "garden_treasure", "healing_spring"],
        possible_rewards={"magic_seed": 0.4, "golden_seed": 0.1, "rare_flower": 0.3}
    ),
    AreaType.RUINS: ExplorationArea(
        area_id="ruins",
        area_type=AreaType.RUINS,
        name="🏛️ 古老遗迹",
        description="古老的文明遗迹，隐藏着历史的秘密。",
        icon="🏛️",
        required_level=15,
        energy_cost=35,
        time_cost=4,
        possible_events=["ancient_puzzle", "ghost_encounter", "treasure_room", "curse"],
        possible_rewards={"ancient_artifact": 0.2, "treasure_map": 0.3, "crystal": 0.2}
    ),
}


EVENTS = {
    "forest_treasure": RandomEvent(
        event_id="forest_treasure",
        event_type=EventType.TREASURE,
        title="🌲 发现宝箱！",
        description="你在树丛中发现了一个古老的宝箱！",
        choices=[
            {"text": "打开宝箱", "success_rate": 0.8, "rewards": True},
            {"text": "小心检查陷阱", "success_rate": 0.95, "rewards": True}
        ],
        rewards=ExplorationReward(money=100, items={"wood": 5}, exp=30),
        probability=0.2
    ),
    "wild_animal": RandomEvent(
        event_id="wild_animal",
        event_type=EventType.DANGER,
        title="🐺 遭遇野狼！",
        description="一只野狼挡住了你的去路！",
        choices=[
            {"text": "战斗", "success_rate": 0.6, "rewards": True, "penalties": True},
            {"text": "逃跑", "success_rate": 0.8, "rewards": False},
            {"text": "投喂食物", "success_rate": 0.7, "rewards": True}
        ],
        rewards=ExplorationReward(money=50, exp=50),
        penalties=ExplorationReward(money=-50),
        probability=0.15
    ),
    "lost_traveler": RandomEvent(
        event_id="lost_traveler",
        event_type=EventType.NPC,
        title="🧑 迷路的旅人",
        description="你遇到了一个迷路的旅人，他看起来很疲惫。",
        choices=[
            {"text": "帮助他", "success_rate": 1.0, "rewards": True},
            {"text": "无视他", "success_rate": 1.0, "rewards": False}
        ],
        rewards=ExplorationReward(money=30, items={"treasure_map": 1}, exp=20),
        probability=0.1
    ),
    "berry_bush": RandomEvent(
        event_id="berry_bush",
        event_type=EventType.DISCOVERY,
        title="🫐 浆果丛",
        description="你发现了一片茂盛的浆果丛！",
        choices=[
            {"text": "采集浆果", "success_rate": 1.0, "rewards": True}
        ],
        rewards=ExplorationReward(items={"food": 3}, exp=10),
        probability=0.3
    ),
    "mine_shaft": RandomEvent(
        event_id="mine_shaft",
        event_type=EventType.DISCOVERY,
        title="⛏️ 矿井入口",
        description="你发现了一个废弃的矿井入口。",
        choices=[
            {"text": "进入探索", "success_rate": 0.7, "rewards": True, "penalties": True},
            {"text": "在入口搜索", "success_rate": 1.0, "rewards": True}
        ],
        rewards=ExplorationReward(items={"iron_ore": 3, "gold_ore": 1}, exp=40),
        penalties=ExplorationReward(money=-30),
        probability=0.2
    ),
    "ore_vein": RandomEvent(
        event_id="ore_vein",
        event_type=EventType.TREASURE,
        title="💎 矿脉！",
        description="你发现了一条闪闪发光的矿脉！",
        choices=[
            {"text": "开采", "success_rate": 1.0, "rewards": True}
        ],
        rewards=ExplorationReward(items={"iron_ore": 5, "gold_ore": 2}, exp=50),
        probability=0.15
    ),
    "fishing_spot": RandomEvent(
        event_id="fishing_spot",
        event_type=EventType.DISCOVERY,
        title="🎣 绝佳钓点",
        description="这里是个钓鱼的好地方！",
        choices=[
            {"text": "钓鱼", "success_rate": 0.9, "rewards": True}
        ],
        rewards=ExplorationReward(items={"food": 2}, exp=15),
        probability=0.4
    ),
    "sunken_treasure": RandomEvent(
        event_id="sunken_treasure",
        event_type=EventType.TREASURE,
        title="🌊 水下闪光",
        description="你看到水下有什么东西在闪光！",
        choices=[
            {"text": "潜水查看", "success_rate": 0.6, "rewards": True, "penalties": True},
            {"text": "用树枝捞", "success_rate": 0.4, "rewards": True}
        ],
        rewards=ExplorationReward(money=200, items={"treasure_map": 1}, exp=60),
        penalties=ExplorationReward(money=-20),
        probability=0.1
    ),
    "crystal_cave": RandomEvent(
        event_id="crystal_cave",
        event_type=EventType.DISCOVERY,
        title="💎 水晶洞穴",
        description="你进入了一个布满水晶的洞穴！",
        choices=[
            {"text": "采集水晶", "success_rate": 0.8, "rewards": True}
        ],
        rewards=ExplorationReward(items={"crystal": 2}, exp=80),
        probability=0.1
    ),
    "flower_fairy": RandomEvent(
        event_id="flower_fairy",
        event_type=EventType.NPC,
        title="🧚 花仙子",
        description="一位美丽的花仙子出现在你面前！",
        choices=[
            {"text": "与她交谈", "success_rate": 1.0, "rewards": True}
        ],
        rewards=ExplorationReward(items={"magic_seed": 2, "golden_seed": 1}, exp=100, special="fairy_blessing"),
        probability=0.05
    ),
    "ancient_puzzle": RandomEvent(
        event_id="ancient_puzzle",
        event_type=EventType.PUZZLE,
        title="🧩 古老谜题",
        description="你发现了一个古老的机关谜题。",
        choices=[
            {"text": "尝试解开", "success_rate": 0.5, "rewards": True, "penalties": True},
            {"text": "记录下来", "success_rate": 1.0, "rewards": False}
        ],
        rewards=ExplorationReward(money=500, items={"ancient_artifact": 1}, exp=150),
        penalties=ExplorationReward(money=-100),
        probability=0.1
    ),
}


class ExplorationManager:
    
    def __init__(self):
        self.areas: Dict[AreaType, ExplorationArea] = {}
        self.current_exploration: Optional[Dict] = None
        self.exploration_history: List[Dict] = []
        self.total_explorations: int = 0
        self.on_exploration_complete: Optional[Callable] = None
        
        self._init_areas()
    
    def _init_areas(self):
        for area_type, area in AREAS.items():
            self.areas[area_type] = area
        
        self.areas[AreaType.FOREST].is_unlocked = True
    
    def unlock_area(self, area_type: AreaType) -> bool:
        if area_type in self.areas:
            self.areas[area_type].is_unlocked = True
            return True
        return False
    
    def check_area_unlock(self, player_level: int) -> List[AreaType]:
        newly_unlocked = []
        
        for area_type, area in self.areas.items():
            if not area.is_unlocked and player_level >= area.required_level:
                area.is_unlocked = True
                newly_unlocked.append(area_type)
        
        return newly_unlocked
    
    def get_available_areas(self) -> List[Dict]:
        return [
            {
                "area_id": area.area_id,
                "area_type": area.area_type.value,
                "name": area.name,
                "description": area.description,
                "icon": area.icon,
                "energy_cost": area.energy_cost,
                "time_cost": area.time_cost,
                "required_level": area.required_level,
                "is_unlocked": area.is_unlocked,
                "times_explored": area.times_explored
            }
            for area in self.areas.values()
            if area.is_unlocked
        ]
    
    def start_exploration(self, area_type: AreaType, player_energy: int) -> Tuple[bool, str, Optional[Dict]]:
        if area_type not in self.areas:
            return False, "未知区域", None
        
        area = self.areas[area_type]
        
        if not area.is_unlocked:
            return False, f"需要等级 {area.required_level} 才能探索此区域", None
        
        if player_energy < area.energy_cost:
            return False, f"体力不足！需要 {area.energy_cost} 点体力", None
        
        self.current_exploration = {
            "area": area,
            "events": [],
            "rewards": ExplorationReward(),
            "started": True
        }
        
        return True, f"开始探索 {area.name}...", {"energy_cost": area.energy_cost}
    
    def process_exploration(self) -> Dict:
        if not self.current_exploration:
            return {"success": False, "message": "没有进行中的探索"}
        
        area = self.current_exploration["area"]
        events_result = []
        total_rewards = ExplorationReward()
        
        num_events = random.randint(1, 3)
        possible_events = [EVENTS[eid] for eid in area.possible_events if eid in EVENTS]
        
        if possible_events:
            selected_events = random.choices(
                possible_events,
                weights=[e.probability for e in possible_events],
                k=num_events
            )
            
            for event in selected_events:
                event_result = self._process_event(event)
                events_result.append(event_result)
                
                if event_result.get("rewards"):
                    rewards = event_result["rewards"]
                    total_rewards.money += rewards.money
                    total_rewards.exp += rewards.exp
                    for item_id, count in rewards.items.items():
                        if item_id in total_rewards.items:
                            total_rewards.items[item_id] += count
                        else:
                            total_rewards.items[item_id] = count
        
        for item_id, probability in area.possible_rewards.items():
            if random.random() < probability:
                count = random.randint(1, 3)
                if item_id in total_rewards.items:
                    total_rewards.items[item_id] += count
                else:
                    total_rewards.items[item_id] = count
        
        area.times_explored += 1
        self.total_explorations += 1
        
        self.current_exploration["events"] = events_result
        self.current_exploration["rewards"] = total_rewards
        
        return {
            "success": True,
            "area_name": area.name,
            "events": events_result,
            "rewards": {
                "money": total_rewards.money,
                "items": total_rewards.items,
                "exp": total_rewards.exp,
                "special": total_rewards.special
            }
        }
    
    def _process_event(self, event: RandomEvent) -> Dict:
        if not event.choices:
            return {
                "event_id": event.event_id,
                "title": event.title,
                "description": event.description,
                "success": True,
                "rewards": event.rewards
            }
        
        choice = random.choice(event.choices)
        success = random.random() < choice.get("success_rate", 1.0)
        
        result = {
            "event_id": event.event_id,
            "title": event.title,
            "description": event.description,
            "choice": choice["text"],
            "success": success
        }
        
        if success and choice.get("rewards") and event.rewards:
            result["rewards"] = event.rewards
            result["message"] = "成功了！"
        elif not success and choice.get("penalties") and event.penalties:
            result["penalties"] = event.penalties
            result["message"] = "失败了..."
        else:
            result["rewards"] = None
            result["message"] = "无事发生"
        
        return result
    
    def complete_exploration(self) -> Optional[Dict]:
        if not self.current_exploration:
            return None
        
        result = self.current_exploration.copy()
        self.exploration_history.append({
            "area": result["area"].area_type.value,
            "rewards": result["rewards"],
            "timestamp": self.total_explorations
        })
        
        self.current_exploration = None
        
        if self.on_exploration_complete:
            self.on_exploration_complete(result)
        
        return result
    
    def get_exploration_stats(self) -> Dict:
        area_stats = {}
        for area_type, area in self.areas.items():
            area_stats[area_type.value] = {
                "name": area.name,
                "times_explored": area.times_explored,
                "is_unlocked": area.is_unlocked
            }
        
        return {
            "total_explorations": self.total_explorations,
            "areas": area_stats
        }
    
    def get_save_data(self) -> Dict:
        return {
            "total_explorations": self.total_explorations,
            "exploration_history": self.exploration_history[-10:],
            "area_stats": {
                area_type.value: {
                    "is_unlocked": area.is_unlocked,
                    "times_explored": area.times_explored
                }
                for area_type, area in self.areas.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.total_explorations = data.get("total_explorations", 0)
        self.exploration_history = data.get("exploration_history", [])
        
        area_stats = data.get("area_stats", {})
        for area_type_str, stats in area_stats.items():
            try:
                area_type = AreaType(area_type_str)
                if area_type in self.areas:
                    self.areas[area_type].is_unlocked = stats.get("is_unlocked", False)
                    self.areas[area_type].times_explored = stats.get("times_explored", 0)
            except ValueError:
                pass
