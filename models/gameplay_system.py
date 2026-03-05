"""
游戏机制系统模块
提供农耕系统、建筑系统和烹饪系统
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import random


class CropStage(Enum):
    SEED = "种子"
    SPROUT = "幼苗"
    GROWING = "成长中"
    MATURE = "成熟"
    WITHERED = "枯萎"


class CropQuality(Enum):
    POOR = "劣质"
    NORMAL = "普通"
    GOOD = "优质"
    EXCELLENT = "极品"
    LEGENDARY = "传说"


class Season(Enum):
    SPRING = "春季"
    SUMMER = "夏季"
    AUTUMN = "秋季"
    WINTER = "冬季"


class BuildingType(Enum):
    HOUSE = "住宅"
    BARN = "畜棚"
    SILO = "粮仓"
    GREENHOUSE = "温室"
    WELL = "水井"
    FENCE = "围栏"
    WORKSHOP = "工坊"
    KITCHEN = "厨房"
    STORAGE = "仓库"
    SHOP = "商店"
    DECORATION = "装饰"
    FARM = "农田"


class RecipeCategory(Enum):
    MAIN_DISH = "主菜"
    SOUP = "汤类"
    DESSERT = "甜点"
    DRINK = "饮品"
    SNACK = "小食"
    SPECIAL = "特色菜"


class FoodEffectType(Enum):
    HEALTH = "恢复生命"
    STAMINA = "恢复体力"
    BUFF_ATTACK = "攻击提升"
    BUFF_DEFENSE = "防御提升"
    BUFF_SPEED = "速度提升"
    BUFF_LUCK = "幸运提升"
    TEMP_REGEN = "持续恢复"


@dataclass
class CropInfo:
    crop_id: str
    name: str
    icon: str
    description: str
    
    seed_price: int = 10
    base_sell_price: int = 20
    
    grow_days: int = 5
    water_per_day: int = 1
    
    seasons: List[Season] = field(default_factory=list)
    
    min_temp: int = 5
    max_temp: int = 35
    min_humidity: int = 30
    max_humidity: int = 80
    
    base_yield: int = 3
    yield_variance: int = 1
    
    quality_modifiers: Dict[str, float] = field(default_factory=dict)
    
    requires_trellis: bool = False
    requires_greenhouse: bool = False
    
    exp_reward: int = 10


@dataclass
class PlantedCrop:
    crop_info: CropInfo
    planted_day: int = 0
    current_stage: CropStage = CropStage.SEED
    days_grown: int = 0
    water_level: int = 0
    health: int = 100
    quality: CropQuality = CropQuality.NORMAL
    
    fertilized: bool = False
    fertilizer_type: str = ""
    
    daily_growth_progress: float = 0.0
    
    def water(self, amount: int = 1):
        self.water_level = min(self.water_level + amount, 3)
    
    def advance_day(self, weather_effects: Dict, current_season: Season) -> Dict:
        result = {
            "growth": 0,
            "stage_change": False,
            "withered": False,
            "harvestable": False,
            "quality_change": False,
            "messages": []
        }
        
        if current_season not in self.crop_info.seasons and not self.fertilized:
            self.health -= 20
            result["messages"].append("季节不适合，作物健康下降")
        
        growth_rate = 1.0
        
        if self.water_level >= self.crop_info.water_per_day:
            growth_rate *= 1.2
            self.water_level -= self.crop_info.water_per_day
        else:
            growth_rate *= 0.5
            self.health -= 10
            result["messages"].append("缺水，生长减缓")
        
        growth_rate *= weather_effects.get("growth", 1.0)
        
        if self.fertilized:
            growth_rate *= 1.3
        
        self.daily_growth_progress += growth_rate
        self.days_grown += 1
        
        if self.daily_growth_progress >= 1.0:
            self.daily_growth_progress = 0.0
            result["growth"] = 1
        
        if self.health <= 0:
            self.current_stage = CropStage.WITHERED
            result["withered"] = True
            result["messages"].append("作物枯萎了")
            return result
        
        old_stage = self.current_stage
        progress = self.days_grown / self.crop_info.grow_days
        
        if progress >= 1.0:
            self.current_stage = CropStage.MATURE
            result["harvestable"] = True
        elif progress >= 0.7:
            self.current_stage = CropStage.GROWING
        elif progress >= 0.3:
            self.current_stage = CropStage.SPROUT
        
        if self.current_stage != old_stage:
            result["stage_change"] = True
            result["messages"].append(f"作物进入{self.current_stage.value}阶段")
        
        if random.random() < 0.1 and self.health < 70:
            old_quality = self.quality
            qualities = list(CropQuality)
            current_idx = qualities.index(self.quality)
            if current_idx > 0:
                self.quality = qualities[current_idx - 1]
                result["quality_change"] = True
        
        return result
    
    def harvest(self) -> Tuple[bool, int, CropQuality, str]:
        if self.current_stage != CropStage.MATURE:
            return False, 0, self.quality, "作物还未成熟"
        
        base_yield = self.crop_info.base_yield
        variance = random.randint(-self.crop_info.yield_variance, self.crop_info.yield_variance)
        yield_amount = max(1, base_yield + variance)
        
        quality_mult = {
            CropQuality.POOR: 0.5,
            CropQuality.NORMAL: 1.0,
            CropQuality.GOOD: 1.5,
            CropQuality.EXCELLENT: 2.0,
            CropQuality.LEGENDARY: 3.0
        }
        
        yield_amount = int(yield_amount * quality_mult.get(self.quality, 1.0))
        
        return True, yield_amount, self.quality, f"收获了{yield_amount}个{self.quality.value}{self.crop_info.name}"


@dataclass
class FarmField:
    field_id: str
    name: str
    size: int
    fertility: int = 100
    plots: Dict[int, Optional[PlantedCrop]] = field(default_factory=dict)
    
    is_watered: bool = False
    is_fertilized: bool = False
    
    upgrade_level: int = 1
    auto_water: bool = False
    greenhouse: bool = False
    
    def __post_init__(self):
        if not self.plots:
            for i in range(self.size):
                self.plots[i] = None
    
    def plant(self, plot_index: int, crop_info: CropInfo, day: int) -> Tuple[bool, str]:
        if plot_index < 0 or plot_index >= self.size:
            return False, "无效的地块"
        
        if self.plots.get(plot_index) is not None:
            return False, "该地块已有作物"
        
        if crop_info.requires_greenhouse and not self.greenhouse:
            return False, "需要温室才能种植此作物"
        
        self.plots[plot_index] = PlantedCrop(
            crop_info=crop_info,
            planted_day=day
        )
        
        return True, f"在{plot_index + 1}号地块种下了{crop_info.name}"
    
    def water_plot(self, plot_index: int) -> Tuple[bool, str]:
        if plot_index < 0 or plot_index >= self.size:
            return False, "无效的地块"
        
        crop = self.plots.get(plot_index)
        if crop is None:
            return False, "该地块没有作物"
        
        crop.water()
        return True, f"给{plot_index + 1}号地块浇水成功"
    
    def water_all(self) -> int:
        watered = 0
        for plot_index, crop in self.plots.items():
            if crop is not None:
                crop.water()
                watered += 1
        return watered
    
    def fertilize_plot(self, plot_index: int, fertilizer_type: str) -> Tuple[bool, str]:
        if plot_index < 0 or plot_index >= self.size:
            return False, "无效的地块"
        
        crop = self.plots.get(plot_index)
        if crop is None:
            return False, "该地块没有作物"
        
        if crop.fertilized:
            return False, "该地块已经施肥了"
        
        crop.fertilized = True
        crop.fertilizer_type = fertilizer_type
        return True, f"给{plot_index + 1}号地块施肥成功"
    
    def harvest_plot(self, plot_index: int) -> Tuple[bool, int, CropQuality, str]:
        if plot_index < 0 or plot_index >= self.size:
            return False, 0, CropQuality.NORMAL, "无效的地块"
        
        crop = self.plots.get(plot_index)
        if crop is None:
            return False, 0, CropQuality.NORMAL, "该地块没有作物"
        
        success, amount, quality, message = crop.harvest()
        
        if success:
            crop_name = crop.crop_info.name
            self.plots[plot_index] = None
            return True, amount, quality, message
        
        return False, 0, CropQuality.NORMAL, message
    
    def advance_day(self, weather_effects: Dict, current_season: Season) -> Dict:
        result = {
            "plots_advanced": 0,
            "plots_harvestable": 0,
            "plots_withered": 0,
            "harvest_ready": [],
            "messages": []
        }
        
        if self.auto_water:
            self.water_all()
        
        for plot_index, crop in self.plots.items():
            if crop is None:
                continue
            
            crop_result = crop.advance_day(weather_effects, current_season)
            result["plots_advanced"] += 1
            
            if crop_result["harvestable"]:
                result["plots_harvestable"] += 1
                result["harvest_ready"].append(plot_index)
            
            if crop_result["withered"]:
                result["plots_withered"] += 1
                self.plots[plot_index] = None
            
            result["messages"].extend(crop_result["messages"])
        
        self.fertility = max(0, self.fertility - 1)
        
        return result
    
    def get_empty_plots(self) -> List[int]:
        return [i for i, crop in self.plots.items() if crop is None]
    
    def get_harvestable_plots(self) -> List[int]:
        return [
            i for i, crop in self.plots.items() 
            if crop is not None and crop.current_stage == CropStage.MATURE
        ]


@dataclass
class BuildingRequirement:
    item_id: str
    item_name: str
    amount: int


@dataclass
class BuildingInfo:
    building_id: str
    name: str
    building_type: BuildingType
    icon: str
    description: str
    
    size: Tuple[int, int] = (1, 1)
    max_level: int = 3
    
    requirements: List[BuildingRequirement] = field(default_factory=list)
    build_time: int = 1
    build_cost: int = 100
    
    provides: List[str] = field(default_factory=list)
    capacity: int = 0
    
    daily_upkeep: int = 0
    daily_benefit: int = 0


@dataclass
class PlacedBuilding:
    building_info: BuildingInfo
    position: Tuple[int, int]
    level: int = 1
    is_complete: bool = False
    construction_progress: int = 0
    construction_days: int = 0
    
    current_storage: Dict[str, int] = field(default_factory=dict)
    assigned_workers: int = 0
    
    condition: int = 100
    
    def advance_day(self) -> Dict:
        result = {
            "completed": False,
            "benefits": {},
            "upkeep_cost": 0,
            "messages": []
        }
        
        if not self.is_complete:
            self.construction_progress += 1
            if self.construction_progress >= self.building_info.build_time:
                self.is_complete = True
                result["completed"] = True
                result["messages"].append(f"{self.building_info.name}建造完成！")
            return result
        
        self.condition = max(0, self.condition - 1)
        result["upkeep_cost"] = self.building_info.daily_upkeep
        
        for benefit in self.building_info.provides:
            result["benefits"][benefit] = self.level
        
        return result
    
    def upgrade(self) -> Tuple[bool, str]:
        if self.level >= self.building_info.max_level:
            return False, "已达最高等级"
        
        if not self.is_complete:
            return False, "建筑尚未完工"
        
        self.level += 1
        return True, f"{self.building_info.name}升级到{self.level}级"
    
    def repair(self, amount: int = 50) -> Tuple[bool, str]:
        if self.condition >= 100:
            return False, "建筑状态良好，无需修理"
        
        self.condition = min(100, self.condition + amount)
        return True, f"修复了{amount}点建筑状态"
    
    def store_item(self, item_id: str, amount: int) -> Tuple[bool, str]:
        if self.building_info.capacity <= 0:
            return False, "此建筑无法存储物品"
        
        current_total = sum(self.current_storage.values())
        if current_total + amount > self.building_info.capacity * self.level:
            return False, "存储空间不足"
        
        self.current_storage[item_id] = self.current_storage.get(item_id, 0) + amount
        return True, f"存储了{amount}个物品"
    
    def retrieve_item(self, item_id: str, amount: int) -> Tuple[bool, int, str]:
        if item_id not in self.current_storage:
            return False, 0, "没有该物品"
        
        if self.current_storage[item_id] < amount:
            amount = self.current_storage[item_id]
        
        self.current_storage[item_id] -= amount
        if self.current_storage[item_id] <= 0:
            del self.current_storage[item_id]
        
        return True, amount, f"取出了{amount}个物品"


@dataclass
class FoodEffect:
    effect_type: FoodEffectType
    value: int
    duration: int = 0
    
    def get_description(self) -> str:
        if self.duration > 0:
            return f"{self.effect_type.value}{self.value}，持续{self.duration}分钟"
        return f"{self.effect_type.value}{self.value}"


@dataclass
class Recipe:
    recipe_id: str
    name: str
    category: RecipeCategory
    icon: str
    description: str
    
    ingredients: Dict[str, int] = field(default_factory=dict)
    optional_ingredients: Dict[str, int] = field(default_factory=dict)
    
    cooking_time: int = 1
    difficulty: int = 1
    
    base_quality: CropQuality = CropQuality.NORMAL
    effects: List[FoodEffect] = field(default_factory=list)
    
    sell_price: int = 0
    exp_reward: int = 10
    
    unlock_condition: str = ""
    is_unlocked: bool = False


@dataclass
class CookedFood:
    recipe: Recipe
    quality: CropQuality
    quantity: int = 1
    created_day: int = 0
    
    def get_effects(self) -> List[FoodEffect]:
        quality_mult = {
            CropQuality.POOR: 0.7,
            CropQuality.NORMAL: 1.0,
            CropQuality.GOOD: 1.3,
            CropQuality.EXCELLENT: 1.6,
            CropQuality.LEGENDARY: 2.0
        }
        
        mult = quality_mult.get(self.quality, 1.0)
        
        enhanced_effects = []
        for effect in self.recipe.effects:
            enhanced = FoodEffect(
                effect_type=effect.effect_type,
                value=int(effect.value * mult),
                duration=int(effect.duration * mult)
            )
            enhanced_effects.append(enhanced)
        
        return enhanced_effects
    
    def get_sell_price(self) -> int:
        quality_mult = {
            CropQuality.POOR: 0.5,
            CropQuality.NORMAL: 1.0,
            CropQuality.GOOD: 1.5,
            CropQuality.EXCELLENT: 2.0,
            CropQuality.LEGENDARY: 3.0
        }
        return int(self.recipe.sell_price * quality_mult.get(self.quality, 1.0))


class CropRegistry:
    
    CROPS = {}
    
    @classmethod
    def _init_crops(cls):
        if cls.CROPS:
            return
        
        cls.CROPS = {
            "wheat": CropInfo(
                crop_id="wheat",
                name="小麦",
                icon="🌾",
                description="基础粮食作物",
                seed_price=10,
                base_sell_price=25,
                grow_days=4,
                seasons=[Season.SPRING, Season.AUTUMN],
                base_yield=5,
                exp_reward=5
            ),
            "carrot": CropInfo(
                crop_id="carrot",
                name="胡萝卜",
                icon="🥕",
                description="营养丰富的蔬菜",
                seed_price=15,
                base_sell_price=35,
                grow_days=5,
                seasons=[Season.SPRING, Season.AUTUMN],
                base_yield=4,
                exp_reward=8
            ),
            "tomato": CropInfo(
                crop_id="tomato",
                name="番茄",
                icon="🍅",
                description="多汁的红色果实",
                seed_price=20,
                base_sell_price=50,
                grow_days=7,
                seasons=[Season.SUMMER],
                base_yield=4,
                exp_reward=12
            ),
            "corn": CropInfo(
                crop_id="corn",
                name="玉米",
                icon="🌽",
                description="金黄的谷物",
                seed_price=25,
                base_sell_price=60,
                grow_days=8,
                seasons=[Season.SUMMER],
                base_yield=3,
                exp_reward=15
            ),
            "pumpkin": CropInfo(
                crop_id="pumpkin",
                name="南瓜",
                icon="🎃",
                description="秋季的象征",
                seed_price=30,
                base_sell_price=80,
                grow_days=10,
                seasons=[Season.AUTUMN],
                base_yield=2,
                exp_reward=20
            ),
            "strawberry": CropInfo(
                crop_id="strawberry",
                name="草莓",
                icon="🍓",
                description="甜美的红色浆果",
                seed_price=40,
                base_sell_price=100,
                grow_days=6,
                seasons=[Season.SPRING],
                base_yield=5,
                exp_reward=18,
                requires_trellis=False
            ),
            "watermelon": CropInfo(
                crop_id="watermelon",
                name="西瓜",
                icon="🍉",
                description="夏日清凉水果",
                seed_price=50,
                base_sell_price=150,
                grow_days=12,
                seasons=[Season.SUMMER],
                base_yield=2,
                exp_reward=25
            ),
            "grape": CropInfo(
                crop_id="grape",
                name="葡萄",
                icon="🍇",
                description="美味的紫色果实",
                seed_price=60,
                base_sell_price=180,
                grow_days=14,
                seasons=[Season.AUTUMN],
                base_yield=4,
                exp_reward=30,
                requires_trellis=True
            ),
            "potato": CropInfo(
                crop_id="potato",
                name="土豆",
                icon="🥔",
                description="耐储存的粮食",
                seed_price=12,
                base_sell_price=30,
                grow_days=6,
                seasons=[Season.SPRING, Season.AUTUMN],
                base_yield=6,
                exp_reward=10
            ),
            "cabbage": CropInfo(
                crop_id="cabbage",
                name="白菜",
                icon="🥬",
                description="常见的蔬菜",
                seed_price=15,
                base_sell_price=35,
                grow_days=5,
                seasons=[Season.SPRING, Season.AUTUMN, Season.WINTER],
                base_yield=4,
                exp_reward=8
            ),
            "pepper": CropInfo(
                crop_id="pepper",
                name="辣椒",
                icon="🌶️",
                description="辛辣的调味品",
                seed_price=25,
                base_sell_price=55,
                grow_days=7,
                seasons=[Season.SUMMER],
                base_yield=5,
                exp_reward=12
            ),
            "eggplant": CropInfo(
                crop_id="eggplant",
                name="茄子",
                icon="🍆",
                description="紫色的蔬菜",
                seed_price=22,
                base_sell_price=45,
                grow_days=8,
                seasons=[Season.SUMMER, Season.AUTUMN],
                base_yield=3,
                exp_reward=14
            ),
            "magic_herb": CropInfo(
                crop_id="magic_herb",
                name="魔法草",
                icon="🌿",
                description="蕴含魔力的神秘草药",
                seed_price=200,
                base_sell_price=500,
                grow_days=20,
                seasons=[Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER],
                base_yield=2,
                exp_reward=100,
                requires_greenhouse=True
            ),
            "golden_wheat": CropInfo(
                crop_id="golden_wheat",
                name="黄金麦",
                icon="✨",
                description="传说中的金色谷物",
                seed_price=500,
                base_sell_price=1000,
                grow_days=15,
                seasons=[Season.SUMMER],
                base_yield=3,
                exp_reward=150,
                requires_greenhouse=True
            ),
        }
    
    @classmethod
    def get_crop(cls, crop_id: str) -> Optional[CropInfo]:
        cls._init_crops()
        return cls.CROPS.get(crop_id)
    
    @classmethod
    def get_crops_by_season(cls, season: Season) -> List[CropInfo]:
        cls._init_crops()
        return [c for c in cls.CROPS.values() if season in c.seasons]
    
    @classmethod
    def get_all_crops(cls) -> List[CropInfo]:
        cls._init_crops()
        return list(cls.CROPS.values())


class BuildingRegistry:
    
    BUILDINGS = {}
    
    @classmethod
    def _init_buildings(cls):
        if cls.BUILDINGS:
            return
        
        cls.BUILDINGS = {
            "small_barn": BuildingInfo(
                building_id="small_barn",
                name="小型畜棚",
                building_type=BuildingType.BARN,
                icon="🏠",
                description="可以饲养少量动物",
                size=(2, 2),
                requirements=[
                    BuildingRequirement("wood", "木材", 20),
                    BuildingRequirement("stone", "石头", 10)
                ],
                build_time=2,
                build_cost=500,
                provides=["animal_housing"],
                capacity=5
            ),
            "large_barn": BuildingInfo(
                building_id="large_barn",
                name="大型畜棚",
                building_type=BuildingType.BARN,
                icon="🏡",
                description="可以饲养更多动物",
                size=(3, 3),
                requirements=[
                    BuildingRequirement("wood", "木材", 50),
                    BuildingRequirement("stone", "石头", 30),
                    BuildingRequirement("iron_ore", "铁矿石", 10)
                ],
                build_time=5,
                build_cost=2000,
                provides=["animal_housing", "auto_feeder"],
                capacity=15,
                max_level=3
            ),
            "silo": BuildingInfo(
                building_id="silo",
                name="粮仓",
                building_type=BuildingType.SILO,
                icon="🗼",
                description="存储大量粮食",
                size=(2, 2),
                requirements=[
                    BuildingRequirement("wood", "木材", 30),
                    BuildingRequirement("stone", "石头", 20)
                ],
                build_time=3,
                build_cost=800,
                provides=["storage"],
                capacity=500
            ),
            "greenhouse": BuildingInfo(
                building_id="greenhouse",
                name="温室",
                building_type=BuildingType.GREENHOUSE,
                icon="🏡",
                description="可以在任何季节种植作物",
                size=(4, 4),
                requirements=[
                    BuildingRequirement("wood", "木材", 100),
                    BuildingRequirement("glass", "玻璃", 50),
                    BuildingRequirement("iron_ore", "铁矿石", 20)
                ],
                build_time=7,
                build_cost=5000,
                provides=["all_season_farming"],
                capacity=0,
                max_level=3
            ),
            "well": BuildingInfo(
                building_id="well",
                name="水井",
                building_type=BuildingType.WELL,
                icon="🪣",
                description="提供自动浇水功能",
                size=(1, 1),
                requirements=[
                    BuildingRequirement("stone", "石头", 30),
                    BuildingRequirement("wood", "木材", 10)
                ],
                build_time=2,
                build_cost=300,
                provides=["auto_water"],
                capacity=0
            ),
            "kitchen": BuildingInfo(
                building_id="kitchen",
                name="厨房",
                building_type=BuildingType.KITCHEN,
                icon="🍳",
                description="可以烹饪各种美食",
                size=(2, 2),
                requirements=[
                    BuildingRequirement("wood", "木材", 40),
                    BuildingRequirement("stone", "石头", 20),
                    BuildingRequirement("iron_ore", "铁矿石", 15)
                ],
                build_time=3,
                build_cost=1000,
                provides=["cooking"],
                capacity=0,
                max_level=5
            ),
            "workshop": BuildingInfo(
                building_id="workshop",
                name="工坊",
                building_type=BuildingType.WORKSHOP,
                icon="🔨",
                description="可以制作工具和装备",
                size=(2, 3),
                requirements=[
                    BuildingRequirement("wood", "木材", 50),
                    BuildingRequirement("stone", "石头", 30),
                    BuildingRequirement("iron_ore", "铁矿石", 25)
                ],
                build_time=4,
                build_cost=1500,
                provides=["crafting"],
                capacity=0,
                max_level=5
            ),
            "storage_shed": BuildingInfo(
                building_id="storage_shed",
                name="储物棚",
                building_type=BuildingType.STORAGE,
                icon="📦",
                description="存储各种物品",
                size=(2, 2),
                requirements=[
                    BuildingRequirement("wood", "木材", 25),
                    BuildingRequirement("stone", "石头", 15)
                ],
                build_time=2,
                build_cost=400,
                provides=["storage"],
                capacity=200
            ),
            "fence": BuildingInfo(
                building_id="fence",
                name="围栏",
                building_type=BuildingType.FENCE,
                icon="🚧",
                description="保护农场不受野兽侵扰",
                size=(1, 1),
                requirements=[
                    BuildingRequirement("wood", "木材", 5)
                ],
                build_time=1,
                build_cost=50,
                provides=["protection"],
                capacity=0
            ),
            "shop": BuildingInfo(
                building_id="shop",
                name="商店",
                building_type=BuildingType.SHOP,
                icon="🏪",
                description="可以出售商品给访客",
                size=(3, 2),
                requirements=[
                    BuildingRequirement("wood", "木材", 60),
                    BuildingRequirement("stone", "石头", 40),
                    BuildingRequirement("gold_ore", "金矿石", 5)
                ],
                build_time=5,
                build_cost=3000,
                provides=["selling", "visitor_attraction"],
                capacity=0,
                daily_benefit=50
            ),
        }
    
    @classmethod
    def get_building(cls, building_id: str) -> Optional[BuildingInfo]:
        cls._init_buildings()
        return cls.BUILDINGS.get(building_id)
    
    @classmethod
    def get_buildings_by_type(cls, building_type: BuildingType) -> List[BuildingInfo]:
        cls._init_buildings()
        return [b for b in cls.BUILDINGS.values() if b.building_type == building_type]
    
    @classmethod
    def get_all_buildings(cls) -> List[BuildingInfo]:
        cls._init_buildings()
        return list(cls.BUILDINGS.values())


class RecipeRegistry:
    
    RECIPES = {}
    
    @classmethod
    def _init_recipes(cls):
        if cls.RECIPES:
            return
        
        cls.RECIPES = {
            "bread": Recipe(
                recipe_id="bread",
                name="面包",
                category=RecipeCategory.MAIN_DISH,
                icon="🍞",
                description="简单的主食",
                ingredients={"wheat": 3},
                cooking_time=1,
                difficulty=1,
                effects=[FoodEffect(FoodEffectType.STAMINA, 20)],
                sell_price=40,
                exp_reward=5,
                is_unlocked=True
            ),
            "carrot_soup": Recipe(
                recipe_id="carrot_soup",
                name="胡萝卜汤",
                category=RecipeCategory.SOUP,
                icon="🥣",
                description="营养丰富的汤品",
                ingredients={"carrot": 2, "potato": 1},
                cooking_time=2,
                difficulty=2,
                effects=[FoodEffect(FoodEffectType.HEALTH, 30), FoodEffect(FoodEffectType.STAMINA, 15)],
                sell_price=80,
                exp_reward=10,
                is_unlocked=True
            ),
            "tomato_salad": Recipe(
                recipe_id="tomato_salad",
                name="番茄沙拉",
                category=RecipeCategory.SNACK,
                icon="🥗",
                description="清爽的沙拉",
                ingredients={"tomato": 2},
                cooking_time=1,
                difficulty=1,
                effects=[FoodEffect(FoodEffectType.STAMINA, 25)],
                sell_price=60,
                exp_reward=8,
                is_unlocked=True
            ),
            "pumpkin_pie": Recipe(
                recipe_id="pumpkin_pie",
                name="南瓜派",
                category=RecipeCategory.DESSERT,
                icon="🥧",
                description="秋季甜点",
                ingredients={"pumpkin": 2, "wheat": 2},
                cooking_time=3,
                difficulty=3,
                effects=[FoodEffect(FoodEffectType.STAMINA, 40), FoodEffect(FoodEffectType.BUFF_LUCK, 10, 30)],
                sell_price=150,
                exp_reward=20,
                is_unlocked=True
            ),
            "strawberry_cake": Recipe(
                recipe_id="strawberry_cake",
                name="草莓蛋糕",
                category=RecipeCategory.DESSERT,
                icon="🍰",
                description="美味的甜点",
                ingredients={"strawberry": 3, "wheat": 2},
                cooking_time=4,
                difficulty=4,
                effects=[FoodEffect(FoodEffectType.HEALTH, 50), FoodEffect(FoodEffectType.BUFF_SPEED, 15, 60)],
                sell_price=250,
                exp_reward=30,
                unlock_condition="制作10个面包"
            ),
            "grape_juice": Recipe(
                recipe_id="grape_juice",
                name="葡萄汁",
                category=RecipeCategory.DRINK,
                icon="🍷",
                description="清爽的饮品",
                ingredients={"grape": 4},
                cooking_time=2,
                difficulty=2,
                effects=[FoodEffect(FoodEffectType.STAMINA, 35), FoodEffect(FoodEffectType.TEMP_REGEN, 5, 60)],
                sell_price=120,
                exp_reward=15,
                is_unlocked=True
            ),
            "spicy_pepper_dish": Recipe(
                recipe_id="spicy_pepper_dish",
                name="辣椒炒肉",
                category=RecipeCategory.MAIN_DISH,
                icon="🌶️",
                description="辛辣的主菜",
                ingredients={"pepper": 3, "meat": 1},
                cooking_time=3,
                difficulty=3,
                effects=[FoodEffect(FoodEffectType.BUFF_ATTACK, 20, 30), FoodEffect(FoodEffectType.STAMINA, 30)],
                sell_price=180,
                exp_reward=25,
                unlock_condition="收集10个辣椒"
            ),
            "vegetable_stew": Recipe(
                recipe_id="vegetable_stew",
                name="蔬菜炖菜",
                category=RecipeCategory.SOUP,
                icon="🍲",
                description="丰富的炖菜",
                ingredients={"carrot": 2, "potato": 2, "cabbage": 1, "tomato": 1},
                cooking_time=4,
                difficulty=3,
                effects=[
                    FoodEffect(FoodEffectType.HEALTH, 60),
                    FoodEffect(FoodEffectType.STAMINA, 40),
                    FoodEffect(FoodEffectType.BUFF_DEFENSE, 15, 30)
                ],
                sell_price=200,
                exp_reward=35,
                is_unlocked=True
            ),
            "magic_potion": Recipe(
                recipe_id="magic_potion",
                name="魔法药剂",
                category=RecipeCategory.SPECIAL,
                icon="🧪",
                description="神秘的药剂",
                ingredients={"magic_herb": 2, "crystal": 1},
                cooking_time=5,
                difficulty=5,
                effects=[
                    FoodEffect(FoodEffectType.HEALTH, 100),
                    FoodEffect(FoodEffectType.STAMINA, 100),
                    FoodEffect(FoodEffectType.BUFF_ATTACK, 30, 60),
                    FoodEffect(FoodEffectType.BUFF_DEFENSE, 30, 60)
                ],
                sell_price=1000,
                exp_reward=100,
                unlock_condition="种植魔法草"
            ),
            "golden_bread": Recipe(
                recipe_id="golden_bread",
                name="黄金面包",
                category=RecipeCategory.SPECIAL,
                icon="✨",
                description="传说中的美食",
                ingredients={"golden_wheat": 2, "magic_herb": 1},
                cooking_time=6,
                difficulty=5,
                effects=[
                    FoodEffect(FoodEffectType.HEALTH, 200),
                    FoodEffect(FoodEffectType.STAMINA, 200),
                    FoodEffect(FoodEffectType.BUFF_LUCK, 50, 120),
                    FoodEffect(FoodEffectType.TEMP_REGEN, 10, 120)
                ],
                sell_price=5000,
                exp_reward=200,
                unlock_condition="种植黄金麦"
            ),
        }
    
    @classmethod
    def get_recipe(cls, recipe_id: str) -> Optional[Recipe]:
        cls._init_recipes()
        return cls.RECIPES.get(recipe_id)
    
    @classmethod
    def get_recipes_by_category(cls, category: RecipeCategory) -> List[Recipe]:
        cls._init_recipes()
        return [r for r in cls.RECIPES.values() if r.category == category]
    
    @classmethod
    def get_unlocked_recipes(cls) -> List[Recipe]:
        cls._init_recipes()
        return [r for r in cls.RECIPES.values() if r.is_unlocked]
    
    @classmethod
    def get_all_recipes(cls) -> List[Recipe]:
        cls._init_recipes()
        return list(cls.RECIPES.values())


class FarmingManager:
    
    def __init__(self):
        self.fields: Dict[str, FarmField] = {}
        self.current_season: Season = Season.SPRING
        self.current_day: int = 1
        
        self.total_harvests: int = 0
        self.total_crops_grown: Dict[str, int] = {}
        
        self._init_fields()
    
    def _init_fields(self):
        self.fields["main"] = FarmField(
            field_id="main",
            name="主田",
            size=9
        )
    
    def add_field(self, field_id: str, name: str, size: int) -> Tuple[bool, str]:
        if field_id in self.fields:
            return False, "该田地已存在"
        
        self.fields[field_id] = FarmField(
            field_id=field_id,
            name=name,
            size=size
        )
        return True, f"创建了新田地：{name}"
    
    def plant_crop(self, field_id: str, plot_index: int, crop_id: str) -> Tuple[bool, str]:
        field = self.fields.get(field_id)
        if not field:
            return False, "找不到该田地"
        
        crop_info = CropRegistry.get_crop(crop_id)
        if not crop_info:
            return False, "未知的作物"
        
        success, message = field.plant(plot_index, crop_info, self.current_day)
        
        if success:
            crop_name = crop_info.name
            self.total_crops_grown[crop_name] = self.total_crops_grown.get(crop_name, 0) + 1
        
        return success, message
    
    def water_field(self, field_id: str, plot_index: int = None) -> Tuple[bool, str, int]:
        field = self.fields.get(field_id)
        if not field:
            return False, "找不到该田地", 0
        
        if plot_index is not None:
            success, message = field.water_plot(plot_index)
            return success, message, 1 if success else 0
        else:
            watered = field.water_all()
            return True, f"给{watered}个地块浇水", watered
    
    def fertilize_plot(self, field_id: str, plot_index: int, fertilizer_type: str) -> Tuple[bool, str]:
        field = self.fields.get(field_id)
        if not field:
            return False, "找不到该田地"
        
        return field.fertilize_plot(plot_index, fertilizer_type)
    
    def harvest_plot(self, field_id: str, plot_index: int) -> Tuple[bool, int, CropQuality, str]:
        field = self.fields.get(field_id)
        if not field:
            return False, 0, CropQuality.NORMAL, "找不到该田地"
        
        success, amount, quality, message = field.harvest_plot(plot_index)
        
        if success:
            self.total_harvests += 1
        
        return success, amount, quality, message
    
    def harvest_all_ready(self, field_id: str) -> Dict:
        field = self.fields.get(field_id)
        if not field:
            return {"success": False, "harvests": [], "total": 0}
        
        harvestable = field.get_harvestable_plots()
        results = []
        total = 0
        
        for plot_index in harvestable:
            success, amount, quality, message = field.harvest_plot(plot_index)
            if success:
                results.append({
                    "plot": plot_index,
                    "amount": amount,
                    "quality": quality.value
                })
                total += amount
                self.total_harvests += 1
        
        return {
            "success": True,
            "harvests": results,
            "total": total
        }
    
    def advance_day(self, weather_effects: Dict) -> Dict:
        result = {
            "fields": {},
            "total_harvestable": 0,
            "total_withered": 0,
            "messages": []
        }
        
        for field_id, field in self.fields.items():
            field_result = field.advance_day(weather_effects, self.current_season)
            result["fields"][field_id] = field_result
            result["total_harvestable"] += field_result["plots_harvestable"]
            result["total_withered"] += field_result["plots_withered"]
            result["messages"].extend(field_result["messages"])
        
        self.current_day += 1
        
        if self.current_day % 28 == 0:
            season_order = [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]
            current_idx = season_order.index(self.current_season)
            self.current_season = season_order[(current_idx + 1) % 4]
            result["messages"].append(f"季节变化：{self.current_season.value}到来了！")
        
        return result
    
    def get_field_status(self, field_id: str) -> Optional[Dict]:
        field = self.fields.get(field_id)
        if not field:
            return None
        
        return {
            "field_id": field.field_id,
            "name": field.name,
            "size": field.size,
            "fertility": field.fertility,
            "empty_plots": len(field.get_empty_plots()),
            "harvestable_plots": len(field.get_harvestable_plots()),
            "upgrade_level": field.upgrade_level,
            "auto_water": field.auto_water,
            "greenhouse": field.greenhouse
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_season": self.current_season.value,
            "current_day": self.current_day,
            "total_harvests": self.total_harvests,
            "total_crops_grown": self.total_crops_grown,
            "fields": {
                field_id: {
                    "name": field.name,
                    "size": field.size,
                    "fertility": field.fertility,
                    "upgrade_level": field.upgrade_level,
                    "auto_water": field.auto_water,
                    "greenhouse": field.greenhouse,
                    "plots": {
                        str(k): {
                            "crop_id": v.crop_info.crop_id,
                            "planted_day": v.planted_day,
                            "current_stage": v.current_stage.value,
                            "days_grown": v.days_grown,
                            "water_level": v.water_level,
                            "health": v.health,
                            "quality": v.quality.value,
                            "fertilized": v.fertilized
                        } for k, v in field.plots.items() if v is not None
                    }
                } for field_id, field in self.fields.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.current_season = Season(data.get("current_season", "春季"))
        self.current_day = data.get("current_day", 1)
        self.total_harvests = data.get("total_harvests", 0)
        self.total_crops_grown = data.get("total_crops_grown", {})
        
        for field_id, field_data in data.get("fields", {}).items():
            field = FarmField(
                field_id=field_id,
                name=field_data.get("name", "田地"),
                size=field_data.get("size", 9),
                fertility=field_data.get("fertility", 100),
                upgrade_level=field_data.get("upgrade_level", 1),
                auto_water=field_data.get("auto_water", False),
                greenhouse=field_data.get("greenhouse", False)
            )
            
            for plot_idx, plot_data in field_data.get("plots", {}).items():
                crop_info = CropRegistry.get_crop(plot_data["crop_id"])
                if crop_info:
                    planted = PlantedCrop(
                        crop_info=crop_info,
                        planted_day=plot_data.get("planted_day", 0),
                        current_stage=CropStage(plot_data.get("current_stage", "种子")),
                        days_grown=plot_data.get("days_grown", 0),
                        water_level=plot_data.get("water_level", 0),
                        health=plot_data.get("health", 100),
                        quality=CropQuality(plot_data.get("quality", "普通")),
                        fertilized=plot_data.get("fertilized", False)
                    )
                    field.plots[int(plot_idx)] = planted
            
            self.fields[field_id] = field


class BuildingManager:
    
    def __init__(self):
        self.buildings: Dict[str, PlacedBuilding] = {}
        self.grid: Dict[Tuple[int, int], str] = {}
        self.grid_size: Tuple[int, int] = (50, 50)
        
        self.total_buildings: int = 0
    
    def place_building(self, building_id: str, position: Tuple[int, int]) -> Tuple[bool, str]:
        building_info = BuildingRegistry.get_building(building_id)
        if not building_info:
            return False, "未知的建筑"
        
        x, y = position
        width, height = building_info.size
        
        if x < 0 or y < 0 or x + width > self.grid_size[0] or y + height > self.grid_size[1]:
            return False, "超出建筑范围"
        
        for dx in range(width):
            for dy in range(height):
                if (x + dx, y + dy) in self.grid:
                    return False, "该位置已有建筑"
        
        placed = PlacedBuilding(
            building_info=building_info,
            position=position
        )
        
        building_key = f"building_{self.total_buildings}"
        self.buildings[building_key] = placed
        
        for dx in range(width):
            for dy in range(height):
                self.grid[(x + dx, y + dy)] = building_key
        
        self.total_buildings += 1
        
        return True, f"开始建造{building_info.name}"
    
    def remove_building(self, building_key: str) -> Tuple[bool, str, int]:
        if building_key not in self.buildings:
            return False, "找不到该建筑", 0
        
        building = self.buildings[building_key]
        x, y = building.position
        width, height = building.building_info.size
        
        for dx in range(width):
            for dy in range(height):
                if (x + dx, y + dy) in self.grid:
                    del self.grid[(x + dx, y + dy)]
        
        del self.buildings[building_key]
        
        refund = building.building_info.build_cost // 2
        
        return True, f"拆除了{building.building_info.name}", refund
    
    def upgrade_building(self, building_key: str) -> Tuple[bool, str]:
        if building_key not in self.buildings:
            return False, "找不到该建筑"
        
        return self.buildings[building_key].upgrade()
    
    def repair_building(self, building_key: str, amount: int = 50) -> Tuple[bool, str]:
        if building_key not in self.buildings:
            return False, "找不到该建筑"
        
        return self.buildings[building_key].repair(amount)
    
    def advance_day(self) -> Dict:
        result = {
            "completed": [],
            "benefits": {},
            "upkeep_cost": 0,
            "messages": []
        }
        
        for building_key, building in self.buildings.items():
            building_result = building.advance_day()
            
            if building_result["completed"]:
                result["completed"].append(building_key)
            
            result["upkeep_cost"] += building_result["upkeep_cost"]
            
            for benefit, level in building_result["benefits"].items():
                if benefit not in result["benefits"]:
                    result["benefits"][benefit] = 0
                result["benefits"][benefit] += level
            
            result["messages"].extend(building_result["messages"])
        
        return result
    
    def get_buildings_by_type(self, building_type: BuildingType) -> List[PlacedBuilding]:
        return [b for b in self.buildings.values() if b.building_info.building_type == building_type]
    
    def get_building_at(self, position: Tuple[int, int]) -> Optional[PlacedBuilding]:
        building_key = self.grid.get(position)
        if building_key:
            return self.buildings.get(building_key)
        return None
    
    def get_save_data(self) -> Dict:
        return {
            "buildings": {
                key: {
                    "building_id": b.building_info.building_id,
                    "position": b.position,
                    "level": b.level,
                    "is_complete": b.is_complete,
                    "construction_progress": b.construction_progress,
                    "condition": b.condition,
                    "current_storage": b.current_storage
                } for key, b in self.buildings.items()
            },
            "total_buildings": self.total_buildings
        }
    
    def load_save_data(self, data: Dict):
        self.total_buildings = data.get("total_buildings", 0)
        
        for key, b_data in data.get("buildings", {}).items():
            building_info = BuildingRegistry.get_building(b_data["building_id"])
            if building_info:
                placed = PlacedBuilding(
                    building_info=building_info,
                    position=tuple(b_data["position"]),
                    level=b_data.get("level", 1),
                    is_complete=b_data.get("is_complete", False),
                    construction_progress=b_data.get("construction_progress", 0),
                    condition=b_data.get("condition", 100),
                    current_storage=b_data.get("current_storage", {})
                )
                self.buildings[key] = placed
                
                x, y = placed.position
                width, height = building_info.size
                for dx in range(width):
                    for dy in range(height):
                        self.grid[(x + dx, y + dy)] = key


class CookingManager:
    
    def __init__(self):
        self.unlocked_recipes: Set[str] = set()
        self.cooking_queue: List[Dict] = []
        self.cooked_items: Dict[str, CookedFood] = {}
        
        self.cooking_level: int = 1
        self.cooking_exp: int = 0
        
        self._init_unlocked_recipes()
    
    def _init_unlocked_recipes(self):
        for recipe in RecipeRegistry.get_all_recipes():
            if recipe.is_unlocked:
                self.unlocked_recipes.add(recipe.recipe_id)
    
    def unlock_recipe(self, recipe_id: str) -> Tuple[bool, str]:
        recipe = RecipeRegistry.get_recipe(recipe_id)
        if not recipe:
            return False, "未知的配方"
        
        if recipe_id in self.unlocked_recipes:
            return False, "已经解锁了该配方"
        
        self.unlocked_recipes.add(recipe_id)
        return True, f"解锁了新配方：{recipe.name}！"
    
    def can_cook(self, recipe_id: str, inventory: Dict[str, int]) -> Tuple[bool, str]:
        if recipe_id not in self.unlocked_recipes:
            return False, "尚未解锁该配方"
        
        recipe = RecipeRegistry.get_recipe(recipe_id)
        if not recipe:
            return False, "未知的配方"
        
        for ingredient, amount in recipe.ingredients.items():
            if inventory.get(ingredient, 0) < amount:
                return False, f"缺少材料：{ingredient}"
        
        return True, "可以烹饪"
    
    def cook(self, recipe_id: str, inventory: Dict[str, int], current_day: int) -> Tuple[bool, str, Optional[CookedFood]]:
        can_cook, message = self.can_cook(recipe_id, inventory)
        if not can_cook:
            return False, message, None
        
        recipe = RecipeRegistry.get_recipe(recipe_id)
        
        for ingredient, amount in recipe.ingredients.items():
            inventory[ingredient] = inventory.get(ingredient, 0) - amount
        
        quality = self._determine_quality(recipe.difficulty)
        
        cooked = CookedFood(
            recipe=recipe,
            quality=quality,
            quantity=1,
            created_day=current_day
        )
        
        self.cooking_exp += recipe.exp_reward
        self._check_level_up()
        
        return True, f"成功烹饪了{quality.value}{recipe.name}！", cooked
    
    def _determine_quality(self, difficulty: int) -> CropQuality:
        base_chance = 0.5 + (self.cooking_level * 0.05) - (difficulty * 0.1)
        base_chance = max(0.1, min(0.9, base_chance))
        
        roll = random.random()
        
        if roll < base_chance * 0.1:
            return CropQuality.LEGENDARY
        elif roll < base_chance * 0.3:
            return CropQuality.EXCELLENT
        elif roll < base_chance * 0.6:
            return CropQuality.GOOD
        elif roll < base_chance:
            return CropQuality.NORMAL
        else:
            return CropQuality.POOR
    
    def _check_level_up(self):
        exp_needed = self.cooking_level * 100
        while self.cooking_exp >= exp_needed:
            self.cooking_exp -= exp_needed
            self.cooking_level += 1
            exp_needed = self.cooking_level * 100
    
    def get_available_recipes(self, inventory: Dict[str, int]) -> List[Dict]:
        result = []
        
        for recipe_id in self.unlocked_recipes:
            recipe = RecipeRegistry.get_recipe(recipe_id)
            if recipe:
                can_cook, _ = self.can_cook(recipe_id, inventory)
                result.append({
                    "recipe_id": recipe_id,
                    "name": recipe.name,
                    "icon": recipe.icon,
                    "category": recipe.category.value,
                    "cooking_time": recipe.cooking_time,
                    "difficulty": recipe.difficulty,
                    "can_cook": can_cook,
                    "ingredients": recipe.ingredients,
                    "effects": [e.get_description() for e in recipe.effects]
                })
        
        return result
    
    def get_save_data(self) -> Dict:
        return {
            "unlocked_recipes": list(self.unlocked_recipes),
            "cooking_level": self.cooking_level,
            "cooking_exp": self.cooking_exp,
            "cooked_items": {
                k: {
                    "recipe_id": v.recipe.recipe_id,
                    "quality": v.quality.value,
                    "quantity": v.quantity,
                    "created_day": v.created_day
                } for k, v in self.cooked_items.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.unlocked_recipes = set(data.get("unlocked_recipes", []))
        self.cooking_level = data.get("cooking_level", 1)
        self.cooking_exp = data.get("cooking_exp", 0)
        
        for key, item_data in data.get("cooked_items", {}).items():
            recipe = RecipeRegistry.get_recipe(item_data["recipe_id"])
            if recipe:
                self.cooked_items[key] = CookedFood(
                    recipe=recipe,
                    quality=CropQuality(item_data.get("quality", "普通")),
                    quantity=item_data.get("quantity", 1),
                    created_day=item_data.get("created_day", 0)
                )


class GameplayManager:
    
    def __init__(self):
        self.farming = FarmingManager()
        self.building = BuildingManager()
        self.cooking = CookingManager()
        
        self.current_day: int = 1
        self.weather_effects: Dict = {"growth": 1.0, "stamina": 1.0, "visibility": 1.0}
    
    def advance_day(self) -> Dict:
        result = {
            "farming": self.farming.advance_day(self.weather_effects),
            "building": self.building.advance_day(),
            "day": self.current_day,
            "messages": []
        }
        
        self.current_day += 1
        
        result["messages"].extend(result["farming"]["messages"])
        result["messages"].extend(result["building"]["messages"])
        
        return result
    
    def set_weather_effects(self, effects: Dict):
        self.weather_effects = effects
    
    def get_full_status(self) -> Dict:
        return {
            "day": self.current_day,
            "season": self.farming.current_season.value,
            "farming": {
                "fields": {fid: self.farming.get_field_status(fid) for fid in self.farming.fields}
            },
            "building": {
                "total_buildings": self.building.total_buildings,
                "buildings": {k: {"name": b.building_info.name, "level": b.level} 
                            for k, b in self.building.buildings.items()}
            },
            "cooking": {
                "level": self.cooking.cooking_level,
                "unlocked_recipes": len(self.cooking.unlocked_recipes)
            }
        }
    
    def get_save_data(self) -> Dict:
        return {
            "current_day": self.current_day,
            "weather_effects": self.weather_effects,
            "farming": self.farming.get_save_data(),
            "building": self.building.get_save_data(),
            "cooking": self.cooking.get_save_data()
        }
    
    def load_save_data(self, data: Dict):
        self.current_day = data.get("current_day", 1)
        self.weather_effects = data.get("weather_effects", {"growth": 1.0})
        
        if "farming" in data:
            self.farming.load_save_data(data["farming"])
        if "building" in data:
            self.building.load_save_data(data["building"])
        if "cooking" in data:
            self.cooking.load_save_data(data["cooking"])
