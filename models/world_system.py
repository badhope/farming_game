"""
世界设计系统模块
提供生物群系、开放世界地图、天气和昼夜循环系统
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import random
import math


class BiomeType(Enum):
    PLAINS = "平原"
    FOREST = "森林"
    MOUNTAIN = "山脉"
    DESERT = "沙漠"
    SNOW = "雪原"
    SWAMP = "沼泽"
    OCEAN = "海洋"
    LAKE = "湖泊"
    RIVER = "河流"
    VOLCANIC = "火山"
    JUNGLE = "丛林"
    TUNDRA = "苔原"
    SAVANNA = "草原"
    MAGICAL = "魔法之地"
    RUINS = "遗迹"


class WeatherIntensity(Enum):
    NONE = "无"
    LIGHT = "轻微"
    MODERATE = "中等"
    HEAVY = "强烈"
    EXTREME = "极端"


class TimeOfDay(Enum):
    DAWN = "黎明"
    MORNING = "上午"
    NOON = "正午"
    AFTERNOON = "下午"
    DUSK = "黄昏"
    EVENING = "傍晚"
    NIGHT = "夜晚"
    MIDNIGHT = "深夜"


class MoonPhase(Enum):
    NEW_MOON = "新月"
    WAXING_CRESCENT = "蛾眉月"
    FIRST_QUARTER = "上弦月"
    WAXING_GIBBOUS = "盈凸月"
    FULL_MOON = "满月"
    WANING_GIBBOUS = "亏凸月"
    LAST_QUARTER = "下弦月"
    WANING_CRESCENT = "残月"


@dataclass
class BiomeResources:
    common: List[str] = field(default_factory=list)
    uncommon: List[str] = field(default_factory=list)
    rare: List[str] = field(default_factory=list)
    legendary: List[str] = field(default_factory=list)
    
    def get_resources_by_rarity(self, rarity: str) -> List[str]:
        return getattr(self, rarity.lower(), [])


@dataclass
class BiomeCreatures:
    passive: List[str] = field(default_factory=list)
    neutral: List[str] = field(default_factory=list)
    hostile: List[str] = field(default_factory=list)
    boss: List[str] = field(default_factory=list)
    
    def get_spawnable_creatures(self, danger_level: int) -> List[str]:
        creatures = self.passive.copy()
        if danger_level >= 1:
            creatures.extend(self.neutral)
        if danger_level >= 2:
            creatures.extend(self.hostile)
        if danger_level >= 3:
            creatures.extend(self.boss)
        return creatures


@dataclass
class BiomeWeather:
    common_weather: List[str] = field(default_factory=list)
    rare_weather: List[str] = field(default_factory=list)
    extreme_weather: List[str] = field(default_factory=list)
    weather_duration_modifier: float = 1.0


@dataclass
class Biome:
    biome_id: str
    biome_type: BiomeType
    name: str
    description: str
    icon: str
    
    temperature_range: Tuple[int, int] = (10, 30)
    humidity_range: Tuple[int, int] = (30, 70)
    danger_level: int = 1
    
    resources: BiomeResources = field(default_factory=BiomeResources)
    creatures: BiomeCreatures = field(default_factory=BiomeCreatures)
    weather: BiomeWeather = field(default_factory=BiomeWeather)
    
    travel_cost: int = 1
    is_discovered: bool = False
    is_accessible: bool = True
    required_level: int = 1
    required_items: List[str] = field(default_factory=list)
    
    points_of_interest: List[str] = field(default_factory=list)
    hidden_secrets: List[str] = field(default_factory=list)
    
    ambient_sounds: List[str] = field(default_factory=list)
    background_color: str = "#90EE90"
    
    def get_temperature(self) -> int:
        return random.randint(self.temperature_range[0], self.temperature_range[1])
    
    def get_humidity(self) -> int:
        return random.randint(self.humidity_range[0], self.humidity_range[1])
    
    def discover(self) -> Tuple[bool, str]:
        if self.is_discovered:
            return False, "已经发现过这个区域了"
        self.is_discovered = True
        return True, f"发现了新区域：{self.name}！"


@dataclass
class WorldTile:
    x: int
    y: int
    biome_type: BiomeType
    elevation: int = 0
    moisture: int = 0
    temperature: int = 20
    
    is_explored: bool = False
    is_accessible: bool = True
    is_interest_point: bool = False
    
    resources_depleted: Dict[str, int] = field(default_factory=dict)
    creature_spawn_timer: int = 0
    
    custom_features: List[str] = field(default_factory=list)
    structures: List[str] = field(default_factory=list)
    
    def get_coordinates(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def distance_to(self, other: 'WorldTile') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class WorldRegion:
    region_id: str
    name: str
    description: str
    icon: str
    
    tiles: Set[Tuple[int, int]] = field(default_factory=set)
    dominant_biome: BiomeType = BiomeType.PLAINS
    
    is_discovered: bool = False
    discovery_progress: int = 0
    total_tiles: int = 0
    
    region_level: int = 1
    danger_rating: int = 1
    
    local_factions: List[str] = field(default_factory=list)
    region_quests: List[str] = field(default_factory=list)
    
    def get_discovery_percentage(self) -> float:
        if self.total_tiles == 0:
            return 0.0
        return (self.discovery_progress / self.total_tiles) * 100


@dataclass
class PointOfInterest:
    poi_id: str
    name: str
    description: str
    icon: str
    poi_type: str
    
    coordinates: Tuple[int, int] = (0, 0)
    is_discovered: bool = False
    is_accessible: bool = True
    
    required_level: int = 1
    required_items: List[str] = field(default_factory=list)
    required_quests: List[str] = field(default_factory=list)
    
    rewards: Dict[str, any] = field(default_factory=dict)
    encounters: List[str] = field(default_factory=list)
    
    visit_count: int = 0
    last_visit_day: int = -1
    reset_days: int = 7
    
    def can_visit(self, player_level: int, inventory: Dict, completed_quests: List[str]) -> Tuple[bool, str]:
        if player_level < self.required_level:
            return False, f"需要等级 {self.required_level}"
        
        for item in self.required_items:
            if item not in inventory:
                return False, f"需要物品：{item}"
        
        for quest in self.required_quests:
            if quest not in completed_quests:
                return False, f"需要完成任务：{quest}"
        
        return True, "可以访问"


@dataclass
class DynamicWeather:
    weather_type: str
    intensity: WeatherIntensity
    duration_hours: int
    remaining_hours: int
    
    wind_speed: int = 0
    wind_direction: int = 0
    precipitation: float = 0.0
    
    effects: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    
    def advance_hour(self) -> bool:
        self.remaining_hours -= 1
        return self.remaining_hours <= 0
    
    def get_effects(self) -> Dict[str, float]:
        base_effects = self.effects.copy()
        intensity_mult = {
            WeatherIntensity.NONE: 0.0,
            WeatherIntensity.LIGHT: 0.5,
            WeatherIntensity.MODERATE: 1.0,
            WeatherIntensity.HEAVY: 1.5,
            WeatherIntensity.EXTREME: 2.5
        }
        
        mult = intensity_mult.get(self.intensity, 1.0)
        for key in base_effects:
            base_effects[key] *= mult
        
        return base_effects


@dataclass
class DayNightCycle:
    current_hour: int = 6
    current_day: int = 1
    day_length_hours: int = 24
    
    dawn_start: int = 5
    dawn_end: int = 7
    dusk_start: int = 18
    dusk_end: int = 20
    
    def get_time_of_day(self) -> TimeOfDay:
        hour = self.current_hour % 24
        
        if self.dawn_start <= hour < self.dawn_end:
            return TimeOfDay.DAWN
        elif self.dawn_end <= hour < 12:
            return TimeOfDay.MORNING
        elif hour == 12:
            return TimeOfDay.NOON
        elif 13 <= hour < self.dusk_start:
            return TimeOfDay.AFTERNOON
        elif self.dusk_start <= hour < self.dusk_end:
            return TimeOfDay.DUSK
        elif self.dusk_end <= hour < 22:
            return TimeOfDay.EVENING
        elif 22 <= hour or hour < 2:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.MIDNIGHT
    
    def get_moon_phase(self) -> MoonPhase:
        phase_index = (self.current_day % 8)
        return list(MoonPhase)[phase_index]
    
    def get_ambient_light(self) -> float:
        hour = self.current_hour % 24
        time = self.get_time_of_day()
        
        light_levels = {
            TimeOfDay.DAWN: 0.6,
            TimeOfDay.MORNING: 0.9,
            TimeOfDay.NOON: 1.0,
            TimeOfDay.AFTERNOON: 0.85,
            TimeOfDay.DUSK: 0.5,
            TimeOfDay.EVENING: 0.3,
            TimeOfDay.NIGHT: 0.15,
            TimeOfDay.MIDNIGHT: 0.1
        }
        
        base_light = light_levels.get(time, 0.5)
        
        if time == TimeOfDay.NIGHT:
            moon = self.get_moon_phase()
            moon_bonus = {
                MoonPhase.FULL_MOON: 0.15,
                MoonPhase.WAXING_GIBBOUS: 0.1,
                MoonPhase.WANING_GIBBOUS: 0.1,
                MoonPhase.FIRST_QUARTER: 0.05,
                MoonPhase.LAST_QUARTER: 0.05,
            }
            base_light += moon_bonus.get(moon, 0)
        
        return base_light
    
    def advance_hour(self, hours: int = 1):
        self.current_hour += hours
        while self.current_hour >= 24:
            self.current_hour -= 24
            self.current_day += 1
    
    def is_daytime(self) -> bool:
        time = self.get_time_of_day()
        return time in [TimeOfDay.DAWN, TimeOfDay.MORNING, TimeOfDay.NOON, 
                       TimeOfDay.AFTERNOON, TimeOfDay.DUSK]
    
    def get_time_string(self) -> str:
        hour = self.current_hour % 24
        return f"{hour:02d}:00"
    
    def get_day_night_effects(self) -> Dict[str, any]:
        time = self.get_time_of_day()
        effects = {
            "visibility": self.get_ambient_light(),
            "spawn_modifier": 1.0,
            "enemy_types": [],
            "special_events": []
        }
        
        if time in [TimeOfDay.NIGHT, TimeOfDay.MIDNIGHT]:
            effects["spawn_modifier"] = 1.5
            effects["enemy_types"] = ["夜间生物", "幽灵", "暗影怪物"]
            effects["special_events"] = ["月光祝福", "暗影侵袭"]
        elif time == TimeOfDay.DAWN:
            effects["special_events"] = ["晨露收集"]
        elif time == TimeOfDay.DUSK:
            effects["special_events"] = ["黄昏狩猎"]
        
        return effects


class BiomeRegistry:
    
    BIOMES = {}
    
    @classmethod
    def _init_biomes(cls):
        if cls.BIOMES:
            return
        
        cls.BIOMES = {
            BiomeType.PLAINS: Biome(
                biome_id="plains",
                biome_type=BiomeType.PLAINS,
                name="宁静平原",
                description="广阔的平原，适合农耕和放牧。",
                icon="🌾",
                temperature_range=(15, 30),
                humidity_range=(40, 60),
                danger_level=1,
                resources=BiomeResources(
                    common=["小麦", "野草", "石头"],
                    uncommon=["药草", "野花"],
                    rare=["稀有种子"],
                    legendary=["古代遗物"]
                ),
                creatures=BiomeCreatures(
                    passive=["兔子", "鹿", "野鸡"],
                    neutral=["野马", "狐狸"],
                    hostile=["野狼"]
                ),
                weather=BiomeWeather(
                    common_weather=["晴天", "多云", "小雨"],
                    rare_weather=["暴风雨"],
                    extreme_weather=["龙卷风"]
                ),
                travel_cost=1,
                background_color="#90EE90"
            ),
            BiomeType.FOREST: Biome(
                biome_id="forest",
                biome_type=BiomeType.FOREST,
                name="神秘森林",
                description="茂密的森林，蕴藏着丰富的资源。",
                icon="🌲",
                temperature_range=(10, 25),
                humidity_range=(60, 90),
                danger_level=2,
                resources=BiomeResources(
                    common=["木材", "野果", "蘑菇"],
                    uncommon=["药草", "树脂", "野蜂蜜"],
                    rare=["灵木", "稀有蘑菇"],
                    legendary=["世界树碎片"]
                ),
                creatures=BiomeCreatures(
                    passive=["松鼠", "小鸟", "蝴蝶"],
                    neutral=["野猪", "熊"],
                    hostile=["狼群", "巨型蜘蛛"],
                    boss=["森林守护者"]
                ),
                weather=BiomeWeather(
                    common_weather=["多云", "小雨", "雾"],
                    rare_weather=["暴风雨"],
                    extreme_weather=["山洪"]
                ),
                travel_cost=2,
                background_color="#228B22"
            ),
            BiomeType.MOUNTAIN: Biome(
                biome_id="mountain",
                biome_type=BiomeType.MOUNTAIN,
                name="巍峨山脉",
                description="高耸入云的山脉，蕴藏着珍贵的矿石。",
                icon="⛰️",
                temperature_range=(-10, 20),
                humidity_range=(20, 50),
                danger_level=3,
                resources=BiomeResources(
                    common=["石头", "铁矿"],
                    uncommon=["铜矿", "银矿"],
                    rare=["金矿", "秘银"],
                    legendary=["龙晶", "星陨石"]
                ),
                creatures=BiomeCreatures(
                    passive=["山羊", "鹰"],
                    neutral=["雪豹"],
                    hostile=["石巨人", "山妖"],
                    boss=["山脉之王"]
                ),
                weather=BiomeWeather(
                    common_weather=["晴天", "大风", "雪"],
                    rare_weather=["暴风雪"],
                    extreme_weather=["雪崩"]
                ),
                travel_cost=3,
                background_color="#808080"
            ),
            BiomeType.DESERT: Biome(
                biome_id="desert",
                biome_type=BiomeType.DESERT,
                name="炙热沙漠",
                description="无垠的沙漠，隐藏着古老的秘密。",
                icon="🏜️",
                temperature_range=(30, 50),
                humidity_range=(0, 20),
                danger_level=3,
                resources=BiomeResources(
                    common=["沙子", "仙人掌"],
                    uncommon=["沙漠玫瑰", "古币"],
                    rare=["沙漠宝石", "古代卷轴"],
                    legendary=["法老宝藏"]
                ),
                creatures=BiomeCreatures(
                    passive=["骆驼", "蜥蜴"],
                    neutral=["蝎子"],
                    hostile=["沙虫", "木乃伊"],
                    boss=["沙漠领主"]
                ),
                weather=BiomeWeather(
                    common_weather=["晴天", "大风"],
                    rare_weather=["沙尘暴"],
                    extreme_weather=["超级沙尘暴"]
                ),
                travel_cost=3,
                background_color="#F4A460"
            ),
            BiomeType.SNOW: Biome(
                biome_id="snow",
                biome_type=BiomeType.SNOW,
                name="永冻雪原",
                description="终年积雪的北方雪原。",
                icon="❄️",
                temperature_range=(-30, -5),
                humidity_range=(30, 60),
                danger_level=4,
                resources=BiomeResources(
                    common=["冰", "雪"],
                    uncommon=["寒铁矿", "冰晶"],
                    rare=["永冻冰", "极光石"],
                    legendary=["冰龙鳞片"]
                ),
                creatures=BiomeCreatures(
                    passive=["企鹅", "海豹"],
                    neutral=["北极熊", "雪狼"],
                    hostile=["冰巨人", "雪怪"],
                    boss=["冰霜巨龙"]
                ),
                weather=BiomeWeather(
                    common_weather=["雪", "多云"],
                    rare_weather=["暴风雪"],
                    extreme_weather=["极寒风暴"]
                ),
                travel_cost=4,
                background_color="#FFFAFA"
            ),
            BiomeType.SWAMP: Biome(
                biome_id="swamp",
                biome_type=BiomeType.SWAMP,
                name="幽暗沼泽",
                description="阴暗潮湿的沼泽地带，危机四伏。",
                icon="🐊",
                temperature_range=(20, 35),
                humidity_range=(80, 100),
                danger_level=4,
                resources=BiomeResources(
                    common=["泥炭", "芦苇"],
                    uncommon=["毒蘑菇", "沼气"],
                    rare=["沼泽精华", "诅咒之花"],
                    legendary=["巫妖之心"]
                ),
                creatures=BiomeCreatures(
                    passive=["青蛙", "蚊子"],
                    neutral=["鳄鱼", "水蛇"],
                    hostile=["沼泽怪物", "毒蚊群"],
                    boss=["沼泽女巫"]
                ),
                weather=BiomeWeather(
                    common_weather=["雾", "小雨"],
                    rare_weather=["毒雾"],
                    extreme_weather=["沼泽爆发"]
                ),
                travel_cost=3,
                background_color="#556B2F"
            ),
            BiomeType.VOLCANIC: Biome(
                biome_id="volcanic",
                biome_type=BiomeType.VOLCANIC,
                name="烈焰火山",
                description="炽热的火山地带，充满危险与机遇。",
                icon="🌋",
                temperature_range=(40, 80),
                humidity_range=(10, 30),
                danger_level=5,
                resources=BiomeResources(
                    common=["黑曜石", "硫磺"],
                    uncommon=["火焰晶石", "熔岩铁"],
                    rare=["凤凰灰", "龙血石"],
                    legendary=["炎魔之心"]
                ),
                creatures=BiomeCreatures(
                    passive=["火蜥蜴"],
                    neutral=["熔岩兽"],
                    hostile=["火焰元素", "炎魔"],
                    boss=["火焰领主"]
                ),
                weather=BiomeWeather(
                    common_weather=["晴天", "火山灰"],
                    rare_weather=["火山喷发"],
                    extreme_weather=["大爆发"]
                ),
                travel_cost=5,
                background_color="#8B0000"
            ),
            BiomeType.MAGICAL: Biome(
                biome_id="magical",
                biome_type=BiomeType.MAGICAL,
                name="魔法之地",
                description="充满魔力的神秘区域，现实与幻想交织。",
                icon="✨",
                temperature_range=(10, 25),
                humidity_range=(40, 60),
                danger_level=5,
                resources=BiomeResources(
                    common=["魔法水晶", "星尘"],
                    uncommon=["魔力矿石", "精灵之尘"],
                    rare=["龙晶", "时间碎片"],
                    legendary=["创世之石"]
                ),
                creatures=BiomeCreatures(
                    passive=["精灵", "小妖精"],
                    neutral=["独角兽", "凤凰"],
                    hostile=["暗影元素", "魔法构造体"],
                    boss=["大魔法师"]
                ),
                weather=BiomeWeather(
                    common_weather=["极光", "魔法雨"],
                    rare_weather=["魔力风暴"],
                    extreme_weather=["次元裂隙"]
                ),
                travel_cost=4,
                background_color="#9370DB"
            ),
            BiomeType.RUINS: Biome(
                biome_id="ruins",
                biome_type=BiomeType.RUINS,
                name="古代遗迹",
                description="古老文明的遗迹，埋藏着无数秘密。",
                icon="🏛️",
                temperature_range=(15, 30),
                humidity_range=(30, 50),
                danger_level=5,
                resources=BiomeResources(
                    common=["古代砖石", "陶片"],
                    uncommon=["古代钱币", "卷轴碎片"],
                    rare=["古代神器碎片", "封印之书"],
                    legendary=["创世神器"]
                ),
                creatures=BiomeCreatures(
                    passive=["石像鬼(休眠)"],
                    neutral=["古代守卫"],
                    hostile=["亡灵", "诅咒之影"],
                    boss=["遗迹守护者"]
                ),
                weather=BiomeWeather(
                    common_weather=["晴天", "雾"],
                    rare_weather=["诅咒之雾"],
                    extreme_weather=["亡灵复苏"]
                ),
                travel_cost=4,
                background_color="#696969"
            ),
        }
    
    @classmethod
    def get_biome(cls, biome_type: BiomeType) -> Optional[Biome]:
        cls._init_biomes()
        return cls.BIOMES.get(biome_type)
    
    @classmethod
    def get_all_biomes(cls) -> List[Biome]:
        cls._init_biomes()
        return list(cls.BIOMES.values())
    
    @classmethod
    def get_biomes_by_danger_level(cls, max_danger: int) -> List[Biome]:
        cls._init_biomes()
        return [b for b in cls.BIOMES.values() if b.danger_level <= max_danger]


class WorldMap:
    
    def __init__(self, width: int = 100, height: int = 100, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 999999)
        
        self.tiles: Dict[Tuple[int, int], WorldTile] = {}
        self.regions: Dict[str, WorldRegion] = {}
        self.points_of_interest: Dict[str, PointOfInterest] = {}
        
        self.player_position: Tuple[int, int] = (width // 2, height // 2)
        self.discovered_tiles: Set[Tuple[int, int]] = set()
        
        self._generate_world()
    
    def _generate_world(self):
        random.seed(self.seed)
        
        for x in range(self.width):
            for y in range(self.height):
                biome_type = self._determine_biome(x, y)
                elevation = self._calculate_elevation(x, y)
                moisture = self._calculate_moisture(x, y)
                temperature = self._calculate_temperature(x, y, elevation)
                
                self.tiles[(x, y)] = WorldTile(
                    x=x,
                    y=y,
                    biome_type=biome_type,
                    elevation=elevation,
                    moisture=moisture,
                    temperature=temperature
                )
        
        self._generate_regions()
        self._generate_points_of_interest()
        
        center_x, center_y = self.player_position
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                pos = (center_x + dx, center_y + dy)
                if pos in self.tiles:
                    self.discovered_tiles.add(pos)
                    self.tiles[pos].is_explored = True
    
    def _determine_biome(self, x: int, y: int) -> BiomeType:
        noise = self._simplex_noise(x * 0.1, y * 0.1)
        moisture_noise = self._simplex_noise(x * 0.05 + 1000, y * 0.05 + 1000)
        temp_noise = self._simplex_noise(x * 0.03 + 2000, y * 0.03 + 2000)
        
        temperature = temp_noise * 50
        moisture = moisture_noise * 100
        
        if temperature < -15:
            return BiomeType.SNOW
        elif temperature > 35:
            if moisture < 30:
                return BiomeType.DESERT
            else:
                return BiomeType.VOLCANIC
        elif moisture > 80:
            return BiomeType.SWAMP
        elif noise > 0.3:
            return BiomeType.MOUNTAIN
        elif moisture > 60:
            return BiomeType.FOREST
        else:
            return BiomeType.PLAINS
    
    def _simplex_noise(self, x: float, y: float) -> float:
        return (math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1.0 * 2 - 1
    
    def _calculate_elevation(self, x: int, y: int) -> int:
        base = self._simplex_noise(x * 0.05, y * 0.05)
        return int((base + 1) * 50)
    
    def _calculate_moisture(self, x: int, y: int) -> int:
        base = self._simplex_noise(x * 0.08 + 500, y * 0.08 + 500)
        return int((base + 1) * 50)
    
    def _calculate_temperature(self, x: int, y: int, elevation: int) -> int:
        latitude_factor = abs(y - self.height // 2) / (self.height // 2)
        base_temp = 30 - latitude_factor * 40
        elevation_penalty = elevation * 0.1
        return int(base_temp - elevation_penalty)
    
    def _generate_regions(self):
        region_id = 0
        visited = set()
        
        for pos, tile in self.tiles.items():
            if pos in visited:
                continue
            
            region_tiles = self._flood_fill_region(pos, tile.biome_type, visited)
            if len(region_tiles) >= 10:
                biome = BiomeRegistry.get_biome(tile.biome_type)
                region = WorldRegion(
                    region_id=f"region_{region_id}",
                    name=f"{biome.name if biome else '未知区域'} #{region_id}",
                    description=biome.description if biome else "",
                    icon=biome.icon if biome else "❓",
                    tiles=region_tiles,
                    dominant_biome=tile.biome_type,
                    total_tiles=len(region_tiles),
                    danger_rating=biome.danger_level if biome else 1
                )
                self.regions[region.region_id] = region
                region_id += 1
    
    def _flood_fill_region(self, start: Tuple[int, int], biome_type: BiomeType, 
                           visited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        region = set()
        queue = [start]
        
        while queue:
            pos = queue.pop(0)
            if pos in visited:
                continue
            if pos not in self.tiles:
                continue
            if self.tiles[pos].biome_type != biome_type:
                continue
            
            visited.add(pos)
            region.add(pos)
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if new_pos not in visited:
                    queue.append(new_pos)
        
        return region
    
    def _generate_points_of_interest(self):
        poi_templates = [
            ("神秘洞穴", "隐藏着宝藏的洞穴", "🕳️", "cave"),
            ("古老神殿", "供奉着古老神明的神殿", "⛩️", "temple"),
            ("废弃矿坑", "曾经繁荣的矿坑", "⛏️", "mine"),
            ("精灵村落", "精灵们的隐秘居所", "🧚", "village"),
            ("巨龙巢穴", "传说中巨龙的栖息地", "🐉", "lair"),
            ("魔法塔", "古代法师的居所", "🗼", "tower"),
            ("温泉", "恢复体力的天然温泉", "♨️", "spring"),
            ("藏宝点", "埋藏着宝藏的地点", "💰", "treasure"),
        ]
        
        poi_id = 0
        for _ in range(20):
            x = random.randint(5, self.width - 5)
            y = random.randint(5, self.height - 5)
            
            template = random.choice(poi_templates)
            poi = PointOfInterest(
                poi_id=f"poi_{poi_id}",
                name=template[0],
                description=template[1],
                icon=template[2],
                poi_type=template[3],
                coordinates=(x, y),
                required_level=random.randint(1, 10)
            )
            
            self.points_of_interest[poi.poi_id] = poi
            if (x, y) in self.tiles:
                self.tiles[(x, y)].is_interest_point = True
            
            poi_id += 1
    
    def get_tile(self, x: int, y: int) -> Optional[WorldTile]:
        return self.tiles.get((x, y))
    
    def get_player_tile(self) -> Optional[WorldTile]:
        return self.tiles.get(self.player_position)
    
    def move_player(self, dx: int, dy: int) -> Tuple[bool, str, Optional[WorldTile]]:
        new_x = self.player_position[0] + dx
        new_y = self.player_position[1] + dy
        
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False, "无法移动到地图边界外", None
        
        new_pos = (new_x, new_y)
        tile = self.tiles.get(new_pos)
        
        if not tile:
            return False, "该位置不存在", None
        
        self.player_position = new_pos
        
        if new_pos not in self.discovered_tiles:
            self.discovered_tiles.add(new_pos)
            tile.is_explored = True
            return True, f"发现了新区域！", tile
        
        return True, "", tile
    
    def get_nearby_tiles(self, radius: int = 3) -> List[WorldTile]:
        result = []
        px, py = self.player_position
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                pos = (px + dx, py + dy)
                if pos in self.tiles and pos in self.discovered_tiles:
                    result.append(self.tiles[pos])
        
        return result
    
    def get_nearby_poi(self, radius: int = 5) -> List[PointOfInterest]:
        result = []
        px, py = self.player_position
        
        for poi in self.points_of_interest.values():
            if poi.is_discovered:
                dist = math.sqrt((poi.coordinates[0] - px) ** 2 + 
                               (poi.coordinates[1] - py) ** 2)
                if dist <= radius:
                    result.append(poi)
        
        return result
    
    def explore_tile(self, x: int, y: int) -> Tuple[bool, str, List[str]]:
        tile = self.tiles.get((x, y))
        if not tile:
            return False, "该位置不存在", []
        
        if tile.is_explored:
            return False, "已经探索过了", []
        
        tile.is_explored = True
        self.discovered_tiles.add((x, y))
        
        discoveries = []
        biome = BiomeRegistry.get_biome(tile.biome_type)
        
        if biome:
            for resource in biome.resources.common:
                if random.random() < 0.3:
                    discoveries.append(resource)
            for resource in biome.resources.uncommon:
                if random.random() < 0.1:
                    discoveries.append(resource)
        
        return True, f"探索了{biome.name if biome else '未知区域'}", discoveries
    
    def get_save_data(self) -> Dict:
        return {
            "seed": self.seed,
            "player_position": self.player_position,
            "discovered_tiles": list(self.discovered_tiles),
            "poi_discovered": [poi.poi_id for poi in self.points_of_interest.values() if poi.is_discovered]
        }
    
    def load_save_data(self, data: Dict):
        self.seed = data.get("seed", self.seed)
        self.player_position = tuple(data.get("player_position", self.player_position))
        self.discovered_tiles = set(tuple(t) for t in data.get("discovered_tiles", []))
        
        for poi_id in data.get("poi_discovered", []):
            if poi_id in self.points_of_interest:
                self.points_of_interest[poi_id].is_discovered = True
        
        for pos in self.discovered_tiles:
            if pos in self.tiles:
                self.tiles[pos].is_explored = True


class WeatherSystem:
    
    def __init__(self):
        self.current_weather: Optional[DynamicWeather] = None
        self.weather_history: List[Dict] = []
        self.forecast: List[Dict] = []
        
        self.temperature: int = 20
        self.humidity: int = 50
        self.wind_speed: int = 5
        self.wind_direction: int = 0
        
        self._generate_initial_weather()
    
    def _generate_initial_weather(self):
        weather_types = ["晴天", "多云", "小雨", "大风"]
        weather = random.choice(weather_types)
        
        self.current_weather = DynamicWeather(
            weather_type=weather,
            intensity=WeatherIntensity.LIGHT,
            duration_hours=random.randint(4, 12),
            remaining_hours=random.randint(4, 12),
            wind_speed=random.randint(0, 20),
            effects=self._get_weather_effects(weather)
        )
    
    def _get_weather_effects(self, weather_type: str) -> Dict[str, float]:
        effects = {
            "晴天": {"growth": 1.1, "stamina": 1.0, "visibility": 1.0},
            "多云": {"growth": 1.0, "stamina": 1.0, "visibility": 0.9},
            "小雨": {"growth": 1.2, "stamina": 0.9, "visibility": 0.7},
            "大雨": {"growth": 1.3, "stamina": 0.8, "visibility": 0.5},
            "暴风雨": {"growth": 0.5, "stamina": 0.6, "visibility": 0.3},
            "雪": {"growth": 0.3, "stamina": 0.7, "visibility": 0.6},
            "暴风雪": {"growth": 0.1, "stamina": 0.5, "visibility": 0.2},
            "雾": {"growth": 0.9, "stamina": 1.0, "visibility": 0.4},
            "沙尘暴": {"growth": 0.4, "stamina": 0.7, "visibility": 0.2},
            "热浪": {"growth": 0.7, "stamina": 0.6, "visibility": 0.8},
        }
        return effects.get(weather_type, {"growth": 1.0, "stamina": 1.0, "visibility": 1.0})
    
    def advance_hour(self):
        if self.current_weather:
            if self.current_weather.advance_hour():
                self._generate_new_weather()
        
        self.temperature += random.randint(-2, 2)
        self.temperature = max(-30, min(50, self.temperature))
        
        self.humidity += random.randint(-5, 5)
        self.humidity = max(0, min(100, self.humidity))
    
    def _generate_new_weather(self):
        weather_chances = {
            "晴天": 30,
            "多云": 25,
            "小雨": 15,
            "大雨": 10,
            "暴风雨": 5,
            "雪": 5,
            "雾": 5,
            "大风": 5
        }
        
        if self.temperature < 0:
            weather_chances["雪"] = 30
            weather_chances["小雨"] = 5
        elif self.temperature > 35:
            weather_chances["热浪"] = 10
        
        weather_types = list(weather_chances.keys())
        weights = list(weather_chances.values())
        
        new_weather = random.choices(weather_types, weights=weights)[0]
        
        intensity_chances = {
            WeatherIntensity.LIGHT: 50,
            WeatherIntensity.MODERATE: 30,
            WeatherIntensity.HEAVY: 15,
            WeatherIntensity.EXTREME: 5
        }
        
        intensities = list(intensity_chances.keys())
        intensity_weights = list(intensity_chances.values())
        intensity = random.choices(intensities, weights=intensity_weights)[0]
        
        self.current_weather = DynamicWeather(
            weather_type=new_weather,
            intensity=intensity,
            duration_hours=random.randint(4, 24),
            remaining_hours=random.randint(4, 24),
            wind_speed=random.randint(0, 30),
            effects=self._get_weather_effects(new_weather)
        )
    
    def generate_forecast(self, hours: int = 24):
        self.forecast = []
        current = self.current_weather
        
        for h in range(hours):
            if current and current.remaining_hours > h:
                self.forecast.append({
                    "hour": h,
                    "weather": current.weather_type,
                    "intensity": current.intensity.value
                })
            else:
                weather_chances = ["晴天", "多云", "小雨"]
                self.forecast.append({
                    "hour": h,
                    "weather": random.choice(weather_chances),
                    "intensity": WeatherIntensity.LIGHT.value
                })
    
    def get_weather_display(self) -> str:
        if not self.current_weather:
            return "☀️ 天气未知"
        
        weather_icons = {
            "晴天": "☀️",
            "多云": "☁️",
            "小雨": "🌧️",
            "大雨": "🌧️",
            "暴风雨": "⛈️",
            "雪": "❄️",
            "暴风雪": "❄️",
            "雾": "🌫️",
            "沙尘暴": "🏜️",
            "热浪": "🔥"
        }
        
        icon = weather_icons.get(self.current_weather.weather_type, "🌤️")
        return f"{icon} {self.current_weather.weather_type} ({self.current_weather.intensity.value})"
    
    def get_weather_effects(self) -> Dict[str, float]:
        if not self.current_weather:
            return {"growth": 1.0, "stamina": 1.0, "visibility": 1.0}
        return self.current_weather.get_effects()
    
    def get_save_data(self) -> Dict:
        return {
            "weather_type": self.current_weather.weather_type if self.current_weather else "晴天",
            "intensity": self.current_weather.intensity.value if self.current_weather else "无",
            "remaining_hours": self.current_weather.remaining_hours if self.current_weather else 0,
            "temperature": self.temperature,
            "humidity": self.humidity
        }
    
    def load_save_data(self, data: Dict):
        weather_type = data.get("weather_type", "晴天")
        intensity_str = data.get("intensity", "轻微")
        
        intensity_map = {
            "无": WeatherIntensity.NONE,
            "轻微": WeatherIntensity.LIGHT,
            "中等": WeatherIntensity.MODERATE,
            "强烈": WeatherIntensity.HEAVY,
            "极端": WeatherIntensity.EXTREME
        }
        
        self.current_weather = DynamicWeather(
            weather_type=weather_type,
            intensity=intensity_map.get(intensity_str, WeatherIntensity.LIGHT),
            duration_hours=data.get("remaining_hours", 8),
            remaining_hours=data.get("remaining_hours", 8),
            effects=self._get_weather_effects(weather_type)
        )
        
        self.temperature = data.get("temperature", 20)
        self.humidity = data.get("humidity", 50)


class WorldManager:
    
    def __init__(self, map_width: int = 100, map_height: int = 100):
        self.world_map = WorldMap(map_width, map_height)
        self.day_night_cycle = DayNightCycle()
        self.weather_system = WeatherSystem()
        
        self.total_play_time: int = 0
        self.events_log: List[Dict] = []
    
    def advance_time(self, hours: int = 1):
        for _ in range(hours):
            self.day_night_cycle.advance_hour(1)
            self.weather_system.advance_hour()
            self.total_play_time += 1
            
            self._check_time_events()
    
    def _check_time_events(self):
        time = self.day_night_cycle.get_time_of_day()
        
        if time == TimeOfDay.DAWN and self.day_night_cycle.current_hour == self.day_night_cycle.dawn_start:
            self.events_log.append({
                "type": "dawn",
                "message": "黎明到来，新的一天开始了！"
            })
        
        if time == TimeOfDay.DUSK and self.day_night_cycle.current_hour == self.day_night_cycle.dusk_start:
            self.events_log.append({
                "type": "dusk",
                "message": "黄昏降临，夜晚即将来临..."
            })
    
    def get_current_state(self) -> Dict:
        return {
            "time": self.day_night_cycle.get_time_string(),
            "time_of_day": self.day_night_cycle.get_time_of_day().value,
            "day": self.day_night_cycle.current_day,
            "moon_phase": self.day_night_cycle.get_moon_phase().value,
            "weather": self.weather_system.get_weather_display(),
            "temperature": self.weather_system.temperature,
            "humidity": self.weather_system.humidity,
            "ambient_light": self.day_night_cycle.get_ambient_light(),
            "player_position": self.world_map.player_position,
            "current_biome": self._get_current_biome_name()
        }
    
    def _get_current_biome_name(self) -> str:
        tile = self.world_map.get_player_tile()
        if tile:
            biome = BiomeRegistry.get_biome(tile.biome_type)
            return biome.name if biome else "未知"
        return "未知"
    
    def move_player(self, direction: str) -> Tuple[bool, str]:
        directions = {
            "north": (0, -1),
            "south": (0, 1),
            "east": (1, 0),
            "west": (-1, 0),
            "northeast": (1, -1),
            "northwest": (-1, -1),
            "southeast": (1, 1),
            "southwest": (-1, 1)
        }
        
        if direction not in directions:
            return False, "无效的方向"
        
        dx, dy = directions[direction]
        success, message, tile = self.world_map.move_player(dx, dy)
        
        if success and tile:
            biome = BiomeRegistry.get_biome(tile.biome_type)
            biome_name = biome.name if biome else "未知区域"
            
            self.advance_time(1)
            
            return True, f"向{direction}移动，到达{biome_name}。{message}"
        
        return False, message
    
    def explore_current_tile(self) -> Tuple[bool, str, List[str]]:
        px, py = self.world_map.player_position
        success, message, discoveries = self.world_map.explore_tile(px, py)
        
        if success:
            self.advance_time(2)
        
        return success, message, discoveries
    
    def get_minimap_data(self, radius: int = 5) -> List[List[str]]:
        tiles = self.world_map.get_nearby_tiles(radius)
        px, py = self.world_map.player_position
        
        minimap = [["❓" for _ in range(radius * 2 + 1)] for _ in range(radius * 2 + 1)]
        
        biome_icons = {
            BiomeType.PLAINS: "🌾",
            BiomeType.FOREST: "🌲",
            BiomeType.MOUNTAIN: "⛰️",
            BiomeType.DESERT: "🏜️",
            BiomeType.SNOW: "❄️",
            BiomeType.SWAMP: "🐊",
            BiomeType.VOLCANIC: "🌋",
            BiomeType.MAGICAL: "✨",
            BiomeType.RUINS: "🏛️",
        }
        
        for tile in tiles:
            dx = tile.x - px + radius
            dy = tile.y - py + radius
            
            if 0 <= dx < radius * 2 + 1 and 0 <= dy < radius * 2 + 1:
                icon = biome_icons.get(tile.biome_type, "❓")
                minimap[dy][dx] = icon
        
        minimap[radius][radius] = "👤"
        
        return minimap
    
    def get_save_data(self) -> Dict:
        return {
            "world_map": self.world_map.get_save_data(),
            "day_night": {
                "current_hour": self.day_night_cycle.current_hour,
                "current_day": self.day_night_cycle.current_day
            },
            "weather": self.weather_system.get_save_data(),
            "total_play_time": self.total_play_time
        }
    
    def load_save_data(self, data: Dict):
        if "world_map" in data:
            self.world_map.load_save_data(data["world_map"])
        
        if "day_night" in data:
            self.day_night_cycle.current_hour = data["day_night"].get("current_hour", 6)
            self.day_night_cycle.current_day = data["day_night"].get("current_day", 1)
        
        if "weather" in data:
            self.weather_system.load_save_data(data["weather"])
        
        self.total_play_time = data.get("total_play_time", 0)
