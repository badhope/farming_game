"""
建筑系统模块
负责农场建筑的建造、升级和管理
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from config.enums import BuildingType
from config.config_loader import get_crop_config


@dataclass
class BuildingRequirement:
    """建筑需求"""
    level_required: int = 1
    money_required: int = 0
    buildings_required: List[str] = field(default_factory=list)
    materials_required: Dict[str, int] = field(default_factory=dict)


@dataclass
class BuildingInfo:
    """建筑信息"""
    building_id: str
    name: str
    building_type: BuildingType
    description: str
    icon: str
    
    build_cost: int = 0
    upgrade_cost: int = 0
    maintenance_cost: int = 0
    
    size_width: int = 1
    size_height: int = 1
    
    max_level: int = 5
    current_level: int = 1
    
    capacity: int = 0  # 容量（如畜棚可容纳动物数）
    production_rate: float = 1.0  # 生产速率加成
    
    requirements: BuildingRequirement = field(default_factory=BuildingRequirement)
    
    effects: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def from_config(cls, building_id: str, config: dict) -> 'BuildingInfo':
        """从配置创建建筑信息"""
        return cls(
            building_id=building_id,
            name=config.get('name', building_id),
            building_type=BuildingType(config.get('type', 'FARM')),
            description=config.get('description', ''),
            icon=config.get('emoji', '🏠'),
            build_cost=config.get('build_cost', 0),
            upgrade_cost=config.get('upgrade_cost', 0),
            size_width=config.get('width', 1),
            size_height=config.get('height', 1),
            max_level=config.get('max_level', 5),
            capacity=config.get('capacity', 0),
            production_rate=config.get('production_rate', 1.0),
        )


@dataclass
class PlacedBuilding:
    """已放置的建筑"""
    building_info: BuildingInfo
    position_x: int
    position_y: int
    
    placed_day: int = 0
    last_maintenance_day: int = 0
    
    is_functional: bool = True
    happiness: int = 100  # 建筑"心情"，影响生产效率
    
    def upgrade(self) -> bool:
        """升级建筑"""
        if self.building_info.current_level >= self.building_info.max_level:
            return False
        
        self.building_info.current_level += 1
        self._apply_level_bonuses()
        return True
    
    def _apply_level_bonuses(self):
        """应用等级加成"""
        level = self.building_info.current_level
        
        # 容量随等级提升
        if self.building_info.capacity > 0:
            self.building_info.capacity = int(
                self.building_info.capacity * (1 + (level - 1) * 0.2)
            )
        
        # 生产速率随等级提升
        self.building_info.production_rate = 1.0 + (level - 1) * 0.1
    
    def needs_maintenance(self, current_day: int, interval: int = 30) -> bool:
        """检查是否需要维护"""
        return current_day - self.last_maintenance_day >= interval
    
    def maintain(self, current_day: int):
        """维护建筑"""
        self.last_maintenance_day = current_day
        self.is_functional = True
        self.happiness = 100
    
    def get_production_multiplier(self) -> float:
        """获取生产倍率"""
        if not self.is_functional:
            return 0.0
        
        # 心情影响生产效率
        mood_multiplier = 0.5 + (self.happiness / 100) * 0.5
        
        return self.building_info.production_rate * mood_multiplier


class BuildingRegistry:
    """建筑注册表"""
    
    _buildings: Dict[str, BuildingInfo] = {}
    _initialized: bool = False
    
    # 默认建筑配置
    DEFAULT_BUILDINGS = {
        "house": {
            "name": "农舍",
            "type": "HOUSE",
            "description": "玩家的住所",
            "emoji": "🏠",
            "build_cost": 0,
            "upgrade_cost": 1000,
            "max_level": 5,
            "width": 3,
            "height": 2,
        },
        "barn": {
            "name": "畜棚",
            "type": "BARN",
            "description": "饲养动物的地方",
            "emoji": "🐄",
            "build_cost": 5000,
            "upgrade_cost": 2000,
            "max_level": 3,
            "capacity": 4,
            "width": 4,
            "height": 3,
        },
        "silo": {
            "name": "粮仓",
            "type": "SILO",
            "description": "储存作物的仓库",
            "emoji": "🌾",
            "build_cost": 2000,
            "upgrade_cost": 1000,
            "max_level": 3,
            "capacity": 100,
            "width": 2,
            "height": 2,
        },
        "greenhouse": {
            "name": "温室",
            "type": "GREENHOUSE",
            "description": "反季节种植作物",
            "emoji": "🏡",
            "build_cost": 10000,
            "upgrade_cost": 5000,
            "max_level": 2,
            "width": 5,
            "height": 3,
        },
        "well": {
            "name": "水井",
            "type": "WELL",
            "description": "提供灌溉用水",
            "emoji": "⛲",
            "build_cost": 1000,
            "upgrade_cost": 500,
            "max_level": 2,
            "width": 1,
            "height": 1,
        },
        "workshop": {
            "name": "工坊",
            "type": "WORKSHOP",
            "description": "制作工具和物品",
            "emoji": "🔨",
            "build_cost": 3000,
            "upgrade_cost": 1500,
            "max_level": 3,
            "width": 3,
            "height": 2,
        },
    }
    
    @classmethod
    def _init_buildings(cls):
        """初始化建筑注册表"""
        if cls._initialized:
            return
        
        # 注册默认建筑
        for building_id, config in cls.DEFAULT_BUILDINGS.items():
            building_info = BuildingInfo.from_config(building_id, config)
            cls._buildings[building_id] = building_info
        
        cls._initialized = True
    
    @classmethod
    def get_building(cls, building_id: str) -> Optional[BuildingInfo]:
        """获取建筑信息"""
        cls._init_buildings()
        return cls._buildings.get(building_id)
    
    @classmethod
    def get_all_buildings(cls) -> Dict[str, BuildingInfo]:
        """获取所有建筑"""
        cls._init_buildings()
        return cls._buildings.copy()
    
    @classmethod
    def get_buildings_by_type(cls, building_type: BuildingType) -> List[BuildingInfo]:
        """按类型获取建筑"""
        cls._init_buildings()
        return [
            b for b in cls._buildings.values()
            if b.building_type == building_type
        ]
    
    @classmethod
    def get_available_buildings(cls, player_level: int, money: int) -> List[BuildingInfo]:
        """获取玩家可建造的建筑"""
        cls._init_buildings()
        return [
            b for b in cls._buildings.values()
            if (b.building_info.requirements.level_required <= player_level and
                b.building_info.requirements.money_required <= money)
        ]


class BuildingManager:
    """建筑管理器"""
    
    def __init__(self):
        self.placed_buildings: List[PlacedBuilding] = []
        self.total_buildings_built = 0
        self.total_money_spent = 0
    
    def can_build_here(self, x: int, y: int, building: BuildingInfo) -> bool:
        """检查是否可以在指定位置建造"""
        # 检查边界和碰撞
        for placed in self.placed_buildings:
            if self._buildings_overlap(x, y, building, placed):
                return False
        return True
    
    def _buildings_overlap(self, x1: int, y1: int, b1: BuildingInfo, 
                           b2: PlacedBuilding) -> bool:
        """检查两个建筑是否重叠"""
        # 简单的矩形碰撞检测
        return not (
            x1 + b1.size_width <= b2.position_x or
            x1 >= b2.position_x + b2.building_info.size_width or
            y1 + b1.size_height <= b2.position_y or
            y1 >= b2.position_y + b2.building_info.size_height
        )
    
    def build_building(self, x: int, y: int, building_id: str, 
                       current_day: int) -> Tuple[bool, str]:
        """建造建筑"""
        building_info = BuildingRegistry.get_building(building_id)
        if not building_info:
            return False, f"未知的建筑：{building_id}"
        
        if not self.can_build_here(x, y, building_info):
            return False, "此位置无法建造（与其他建筑重叠）"
        
        placed = PlacedBuilding(
            building_info=building_info,
            position_x=x,
            position_y=y,
            placed_day=current_day,
            last_maintenance_day=current_day,
        )
        
        self.placed_buildings.append(placed)
        self.total_buildings_built += 1
        self.total_money_spent += building_info.build_cost
        
        return True, f"建造了{building_info.name}"
    
    def upgrade_building(self, building: PlacedBuilding) -> Tuple[bool, str]:
        """升级建筑"""
        if building.upgrade():
            return True, f"{building.building_info.name}升级到{building.building_info.current_level}级"
        return False, "已达最高等级"
    
    def demolish_building(self, building: PlacedBuilding) -> Tuple[bool, str]:
        """拆除建筑"""
        self.placed_buildings.remove(building)
        return True, f"拆除了{building.building_info.name}"
    
    def maintain_building(self, building: PlacedBuilding, current_day: int, 
                         cost: int) -> Tuple[bool, str]:
        """维护建筑"""
        building.maintain(current_day)
        self.total_money_spent += cost
        return True, f"维护了{building.building_info.name}"
    
    def get_building_at(self, x: int, y: int) -> Optional[PlacedBuilding]:
        """获取指定位置的建筑"""
        for building in self.placed_buildings:
            if (building.position_x <= x < building.position_x + building.building_info.size_width and
                building.position_y <= y < building.position_y + building.building_info.size_height):
                return building
        return None
    
    def get_buildings_by_type(self, building_type: BuildingType) -> List[PlacedBuilding]:
        """按类型获取建筑"""
        return [
            b for b in self.placed_buildings
            if b.building_info.building_type == building_type
        ]
    
    def get_functional_buildings(self) -> List[PlacedBuilding]:
        """获取正常运作的建筑"""
        return [b for b in self.placed_buildings if b.is_functional]
    
    def get_buildings_needing_maintenance(self, current_day: int, 
                                          interval: int = 30) -> List[PlacedBuilding]:
        """获取需要维护的建筑"""
        return [
            b for b in self.placed_buildings
            if b.needs_maintenance(current_day, interval)
        ]
    
    def get_total_production_bonus(self, stat: str) -> float:
        """获取某项属性的总加成"""
        total = 1.0
        for building in self.placed_buildings:
            if building.is_functional:
                bonus = building.building_info.effects.get(stat, 0)
                total *= (1 + bonus)
        return total
    
    def get_storage_capacity(self) -> int:
        """获取总存储容量"""
        total = 0
        for building in self.placed_buildings:
            if building.is_functional:
                if building.building_info.building_type in [BuildingType.SILO, BuildingType.STORAGE]:
                    total += building.building_info.capacity
        return total
    
    def get_animal_capacity(self) -> int:
        """获取动物总容量"""
        total = 0
        for building in self.placed_buildings:
            if building.is_functional:
                if building.building_info.building_type == BuildingType.BARN:
                    total += building.building_info.capacity
        return total
