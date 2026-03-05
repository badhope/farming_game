"""
像素艺术地图系统模块
提供多种环境和地图类型
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class MapType(Enum):
    FARM = "farm"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    TOWN = "town"
    CAVE = "cave"
    BEACH = "beach"
    DESERT = "desert"


class TileType(Enum):
    GRASS = "grass"
    DIRT = "dirt"
    WATER = "water"
    STONE = "stone"
    SAND = "sand"
    TREE = "tree"
    FLOWER = "flower"
    PATH = "path"
    BUILDING = "building"
    CROP = "crop"
    FENCE = "fence"
    SNOW = "snow"
    LAVA = "lava"


@dataclass
class Tile:
    tile_type: TileType
    color: str
    walkable: bool = True
    interactable: bool = False
    description: str = ""
    emoji: str = "⬜"
    
    def get_display_char(self) -> str:
        return self.emoji


@dataclass
class MapArea:
    name: str
    map_type: MapType
    width: int
    height: int
    tiles: List[List[Tile]] = field(default_factory=list)
    spawn_points: List[Tuple[int, int]] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)
    weather_effect: Optional[str] = None
    ambient_sound: Optional[str] = None


class PixelArtAssets:
    
    TILE_ASSETS = {
        TileType.GRASS: Tile(
            tile_type=TileType.GRASS,
            color="#7CFC00",
            walkable=True,
            description="青草地",
            emoji="🟩"
        ),
        TileType.DIRT: Tile(
            tile_type=TileType.DIRT,
            color="#8B4513",
            walkable=True,
            interactable=True,
            description="耕地",
            emoji="🟫"
        ),
        TileType.WATER: Tile(
            tile_type=TileType.WATER,
            color="#1E90FF",
            walkable=False,
            description="水域",
            emoji="🟦"
        ),
        TileType.STONE: Tile(
            tile_type=TileType.STONE,
            color="#808080",
            walkable=True,
            description="石头",
            emoji="⬜"
        ),
        TileType.SAND: Tile(
            tile_type=TileType.SAND,
            color="#F4A460",
            walkable=True,
            description="沙地",
            emoji="🟨"
        ),
        TileType.TREE: Tile(
            tile_type=TileType.TREE,
            color="#228B22",
            walkable=False,
            interactable=True,
            description="树木",
            emoji="🌲"
        ),
        TileType.FLOWER: Tile(
            tile_type=TileType.FLOWER,
            color="#FF69B4",
            walkable=True,
            interactable=True,
            description="花朵",
            emoji="🌸"
        ),
        TileType.PATH: Tile(
            tile_type=TileType.PATH,
            color="#D2691E",
            walkable=True,
            description="小路",
            emoji="🟤"
        ),
        TileType.BUILDING: Tile(
            tile_type=TileType.BUILDING,
            color="#8B0000",
            walkable=False,
            interactable=True,
            description="建筑",
            emoji="🏠"
        ),
        TileType.CROP: Tile(
            tile_type=TileType.CROP,
            color="#32CD32",
            walkable=True,
            interactable=True,
            description="作物",
            emoji="🌾"
        ),
        TileType.FENCE: Tile(
            tile_type=TileType.FENCE,
            color="#A0522D",
            walkable=False,
            description="围栏",
            emoji="🚧"
        ),
        TileType.SNOW: Tile(
            tile_type=TileType.SNOW,
            color="#FFFAFA",
            walkable=True,
            description="雪地",
            emoji="⬜"
        ),
        TileType.LAVA: Tile(
            tile_type=TileType.LAVA,
            color="#FF4500",
            walkable=False,
            description="岩浆",
            emoji="🔥"
        ),
    }
    
    CHARACTER_SPRITES = {
        "farmer_male": {
            "idle": "👨‍🌾",
            "walk": "🚶",
            "work": "🧑‍🌾",
            "rest": "😴"
        },
        "farmer_female": {
            "idle": "👩‍🌾",
            "walk": "🚶‍♀️",
            "work": "👩‍🌾",
            "rest": "😴"
        },
        "npc_merchant": {
            "idle": "🧑‍💼",
            "talk": "🗣️"
        },
        "npc_farmer": {
            "idle": "👴",
            "talk": "🗣️"
        },
        "npc_child": {
            "idle": "👧",
            "play": "🏃‍♀️"
        }
    }
    
    BUILDING_SPRITES = {
        "house": {"emoji": "🏠", "name": "农舍", "size": (2, 2)},
        "barn": {"emoji": "🐄", "name": "畜棚", "size": (3, 2)},
        "coop": {"emoji": "🐔", "name": "鸡舍", "size": (2, 2)},
        "greenhouse": {"emoji": "🏡", "name": "温室", "size": (3, 3)},
        "well": {"emoji": "🪣", "name": "水井", "size": (1, 1)},
        "mill": {"emoji": "🏭", "name": "磨坊", "size": (2, 2)},
        "shop": {"emoji": "🏪", "name": "商店", "size": (2, 2)},
        "stable": {"emoji": "🐴", "name": "马厩", "size": (2, 2)},
        "mansion": {"emoji": "🏰", "name": "豪宅", "size": (4, 3)},
        "cave_entrance": {"emoji": "🕳️", "name": "矿洞入口", "size": (1, 1)},
    }
    
    FURNITURE_SPRITES = {
        "table": {"emoji": "🪑", "name": "桌子", "comfort": 5},
        "chair": {"emoji": "🪑", "name": "椅子", "comfort": 3},
        "bed": {"emoji": "🛏️", "name": "床", "comfort": 20},
        "cabinet": {"emoji": "🗄️", "name": "柜子", "storage": 20},
        "lamp": {"emoji": "💡", "name": "灯", "comfort": 2},
        "fireplace": {"emoji": "🔥", "name": "壁炉", "comfort": 15},
        "rug": {"emoji": "🟫", "name": "地毯", "comfort": 5},
        "bookshelf": {"emoji": "📚", "name": "书架", "comfort": 8},
        "tv": {"emoji": "📺", "name": "电视", "comfort": 10},
        "kitchen": {"emoji": "🍳", "name": "厨房", "comfort": 12},
    }
    
    CROP_SPRITES = {
        "seed": {"emoji": "🌱", "stage": 0},
        "sprout": {"emoji": "🌿", "stage": 1},
        "growing": {"emoji": "🪴", "stage": 2},
        "mature": {"emoji": "🌾", "stage": 3},
        "potato": {"emoji": "🥔", "name": "土豆"},
        "carrot": {"emoji": "🥕", "name": "胡萝卜"},
        "wheat": {"emoji": "🌾", "name": "小麦"},
        "tomato": {"emoji": "🍅", "name": "番茄"},
        "corn": {"emoji": "🌽", "name": "玉米"},
        "pumpkin": {"emoji": "🎃", "name": "南瓜"},
        "watermelon": {"emoji": "🍉", "name": "西瓜"},
        "strawberry": {"emoji": "🍓", "name": "草莓"},
        "grape": {"emoji": "🍇", "name": "葡萄"},
        "sunflower": {"emoji": "🌻", "name": "向日葵"},
        "rose": {"emoji": "🌹", "name": "玫瑰"},
        "tulip": {"emoji": "🌷", "name": "郁金香"},
    }
    
    ANIMAL_SPRITES = {
        "chicken": {"emoji": "🐔", "name": "鸡", "product": "鸡蛋"},
        "cow": {"emoji": "🐄", "name": "牛", "product": "牛奶"},
        "pig": {"emoji": "🐷", "name": "猪", "product": "松露"},
        "sheep": {"emoji": "🐑", "name": "羊", "product": "羊毛"},
        "horse": {"emoji": "🐴", "name": "马", "product": None},
        "duck": {"emoji": "🦆", "name": "鸭", "product": "鸭蛋"},
        "goat": {"emoji": "🐐", "name": "山羊", "product": "山羊奶"},
        "rabbit": {"emoji": "🐰", "name": "兔子", "product": "兔毛"},
    }
    
    WEATHER_EFFECTS = {
        "sunny": {"emoji": "☀️", "color": "#FFD700", "effect": "growth_boost"},
        "rainy": {"emoji": "🌧️", "color": "#4682B4", "effect": "auto_water"},
        "stormy": {"emoji": "⛈️", "color": "#2F4F4F", "effect": "crop_damage"},
        "snowy": {"emoji": "❄️", "color": "#FFFAFA", "effect": "slow_growth"},
        "windy": {"emoji": "💨", "color": "#87CEEB", "effect": "seed_spread"},
        "foggy": {"emoji": "🌫️", "color": "#D3D3D3", "effect": "visibility_low"},
    }
    
    @classmethod
    def get_tile(cls, tile_type: TileType) -> Tile:
        return cls.TILE_ASSETS.get(tile_type, cls.TILE_ASSETS[TileType.GRASS])
    
    @classmethod
    def get_character_sprite(cls, character_type: str, action: str = "idle") -> str:
        sprites = cls.CHARACTER_SPRITES.get(character_type, {})
        return sprites.get(action, sprites.get("idle", "👤"))
    
    @classmethod
    def get_building_sprite(cls, building_type: str) -> Dict:
        return cls.BUILDING_SPRITES.get(building_type, {"emoji": "🏠", "name": "建筑", "size": (1, 1)})
    
    @classmethod
    def get_furniture_sprite(cls, furniture_type: str) -> Dict:
        return cls.FURNITURE_SPRITES.get(furniture_type, {"emoji": "📦", "name": "家具", "comfort": 0})
    
    @classmethod
    def get_crop_sprite(cls, crop_type: str, stage: int = 3) -> str:
        if crop_type in cls.CROP_SPRITES:
            return cls.CROP_SPRITES[crop_type]["emoji"]
        stages = ["seed", "sprout", "growing", "mature"]
        stage_name = stages[min(stage, 3)]
        return cls.CROP_SPRITES.get(stage_name, {"emoji": "🌱"})["emoji"]
    
    @classmethod
    def get_animal_sprite(cls, animal_type: str) -> Dict:
        return cls.ANIMAL_SPRITES.get(animal_type, {"emoji": "🐾", "name": "动物", "product": None})


class MapGenerator:
    
    MAP_TEMPLATES = {
        MapType.FARM: {
            "base_tile": TileType.GRASS,
            "features": [TileType.DIRT, TileType.FENCE, TileType.BUILDING],
            "water_chance": 0.05,
            "tree_chance": 0.1
        },
        MapType.FOREST: {
            "base_tile": TileType.GRASS,
            "features": [TileType.TREE, TileType.FLOWER],
            "water_chance": 0.1,
            "tree_chance": 0.4
        },
        MapType.MOUNTAIN: {
            "base_tile": TileType.STONE,
            "features": [TileType.TREE, TileType.STONE],
            "water_chance": 0.05,
            "tree_chance": 0.15
        },
        MapType.LAKE: {
            "base_tile": TileType.WATER,
            "features": [TileType.GRASS, TileType.SAND],
            "water_chance": 0.7,
            "tree_chance": 0.05
        },
        MapType.TOWN: {
            "base_tile": TileType.PATH,
            "features": [TileType.BUILDING, TileType.FLOWER],
            "water_chance": 0.02,
            "tree_chance": 0.08
        },
        MapType.CAVE: {
            "base_tile": TileType.STONE,
            "features": [TileType.STONE, TileType.LAVA],
            "water_chance": 0.1,
            "tree_chance": 0.0
        },
        MapType.BEACH: {
            "base_tile": TileType.SAND,
            "features": [TileType.WATER, TileType.GRASS],
            "water_chance": 0.3,
            "tree_chance": 0.05
        },
        MapType.DESERT: {
            "base_tile": TileType.SAND,
            "features": [TileType.STONE, TileType.SAND],
            "water_chance": 0.02,
            "tree_chance": 0.02
        }
    }
    
    @classmethod
    def generate_map(cls, map_type: MapType, width: int, height: int, name: str = "") -> MapArea:
        template = cls.MAP_TEMPLATES.get(map_type, cls.MAP_TEMPLATES[MapType.FARM])
        
        tiles = []
        base_tile = PixelArtAssets.get_tile(template["base_tile"])
        
        for y in range(height):
            row = []
            for x in range(width):
                tile = cls._generate_tile(x, y, width, height, template, base_tile)
                row.append(tile)
            tiles.append(row)
        
        spawn_points = cls._generate_spawn_points(width, height, tiles)
        
        return MapArea(
            name=name or f"{map_type.value.capitalize()} Map",
            map_type=map_type,
            width=width,
            height=height,
            tiles=tiles,
            spawn_points=spawn_points
        )
    
    @classmethod
    def _generate_tile(cls, x: int, y: int, width: int, height: int, 
                       template: Dict, base_tile: Tile) -> Tile:
        tile = base_tile
        
        if random.random() < template["water_chance"]:
            tile = PixelArtAssets.get_tile(TileType.WATER)
        elif random.random() < template["tree_chance"]:
            tile = PixelArtAssets.get_tile(TileType.TREE)
        elif random.random() < 0.05 and template["features"]:
            feature_type = random.choice(template["features"])
            tile = PixelArtAssets.get_tile(feature_type)
        
        return tile
    
    @classmethod
    def _generate_spawn_points(cls, width: int, height: int, tiles: List[List[Tile]]) -> List[Tuple[int, int]]:
        spawn_points = []
        for _ in range(3):
            for attempt in range(10):
                x = random.randint(1, width - 2)
                y = random.randint(1, height - 2)
                if tiles[y][x].walkable:
                    spawn_points.append((x, y))
                    break
        return spawn_points


class MapManager:
    
    def __init__(self):
        self.maps: Dict[str, MapArea] = {}
        self.current_map: Optional[str] = None
        self.player_position: Tuple[int, int] = (0, 0)
        
        self._init_default_maps()
    
    def _init_default_maps(self):
        self.maps["farm"] = MapGenerator.generate_map(MapType.FARM, 20, 15, "我的农场")
        self.maps["forest"] = MapGenerator.generate_map(MapType.FOREST, 25, 20, "神秘森林")
        self.maps["town"] = MapGenerator.generate_map(MapType.TOWN, 30, 25, "星露谷镇")
        self.maps["mountain"] = MapGenerator.generate_map(MapType.MOUNTAIN, 20, 20, "高山矿区")
        self.maps["beach"] = MapGenerator.generate_map(MapType.BEACH, 25, 15, "海边沙滩")
        
        self.current_map = "farm"
        if self.maps["farm"].spawn_points:
            self.player_position = self.maps["farm"].spawn_points[0]
    
    def get_current_map(self) -> Optional[MapArea]:
        return self.maps.get(self.current_map)
    
    def get_map(self, map_name: str) -> Optional[MapArea]:
        return self.maps.get(map_name)
    
    def change_map(self, map_name: str) -> bool:
        if map_name in self.maps:
            self.current_map = map_name
            new_map = self.maps[map_name]
            if new_map.spawn_points:
                self.player_position = new_map.spawn_points[0]
            return True
        return False
    
    def move_player(self, dx: int, dy: int) -> bool:
        current_map = self.get_current_map()
        if not current_map:
            return False
        
        new_x = self.player_position[0] + dx
        new_y = self.player_position[1] + dy
        
        if 0 <= new_x < current_map.width and 0 <= new_y < current_map.height:
            if current_map.tiles[new_y][new_x].walkable:
                self.player_position = (new_x, new_y)
                return True
        
        return False
    
    def get_player_position(self) -> Tuple[int, int]:
        return self.player_position
    
    def get_tile_at_player(self) -> Optional[Tile]:
        current_map = self.get_current_map()
        if current_map:
            x, y = self.player_position
            if 0 <= y < len(current_map.tiles) and 0 <= x < len(current_map.tiles[0]):
                return current_map.tiles[y][x]
        return None
    
    def get_visible_area(self, radius: int = 5) -> List[List[Tile]]:
        current_map = self.get_current_map()
        if not current_map:
            return []
        
        px, py = self.player_position
        visible = []
        
        for y in range(max(0, py - radius), min(current_map.height, py + radius + 1)):
            row = []
            for x in range(max(0, px - radius), min(current_map.width, px + radius + 1)):
                row.append(current_map.tiles[y][x])
            visible.append(row)
        
        return visible
    
    def add_map(self, name: str, map_area: MapArea) -> None:
        self.maps[name] = map_area
    
    def get_save_data(self) -> Dict:
        return {
            "current_map": self.current_map,
            "player_position": list(self.player_position),
            "maps": list(self.maps.keys())
        }
    
    def load_save_data(self, data: Dict) -> None:
        self.current_map = data.get("current_map", "farm")
        pos = data.get("player_position", [0, 0])
        self.player_position = (pos[0], pos[1])
