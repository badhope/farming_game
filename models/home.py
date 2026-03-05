"""
家庭建设系统模块
提供房屋升级、家具摆放、房间装饰等功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum


class RoomType(Enum):
    BEDROOM = "bedroom"
    LIVING_ROOM = "living_room"
    KITCHEN = "kitchen"
    STORAGE = "storage"
    GARDEN = "garden"
    STUDY = "study"


class FurnitureCategory(Enum):
    BED = "bed"
    TABLE = "table"
    CHAIR = "chair"
    DECORATION = "decoration"
    LIGHTING = "lighting"
    STORAGE = "storage"
    APPLIANCE = "appliance"


@dataclass
class Furniture:
    furniture_id: str
    name: str
    category: FurnitureCategory
    description: str
    icon: str
    price: int = 0
    comfort_bonus: int = 0
    storage_bonus: int = 0
    special_effect: Optional[str] = None
    required_room: Optional[RoomType] = None


@dataclass
class Room:
    room_type: RoomType
    name: str
    level: int = 1
    max_level: int = 5
    furniture: Dict[str, Furniture] = field(default_factory=dict)
    is_unlocked: bool = False
    
    def get_comfort_level(self) -> int:
        total = 0
        for f in self.furniture.values():
            total += f.comfort_bonus
        return total
    
    def can_upgrade(self) -> bool:
        return self.level < self.max_level
    
    def get_upgrade_cost(self) -> int:
        return self.level * 1000


@dataclass
class Home:
    home_level: int = 1
    max_level: int = 5
    rooms: Dict[RoomType, Room] = field(default_factory=dict)
    total_comfort: int = 0
    total_storage: int = 0
    
    def __post_init__(self):
        if not self.rooms:
            self.rooms = {
                RoomType.BEDROOM: Room(RoomType.BEDROOM, "卧室", is_unlocked=True),
                RoomType.LIVING_ROOM: Room(RoomType.LIVING_ROOM, "客厅", is_unlocked=True),
            }
    
    def can_upgrade(self) -> bool:
        return self.home_level < self.max_level
    
    def get_upgrade_cost(self) -> int:
        return self.home_level * 5000
    
    def upgrade(self) -> bool:
        if not self.can_upgrade():
            return False
        
        self.home_level += 1
        
        if self.home_level == 2:
            self.rooms[RoomType.KITCHEN] = Room(RoomType.KITCHEN, "厨房", is_unlocked=True)
        elif self.home_level == 3:
            self.rooms[RoomType.STORAGE] = Room(RoomType.STORAGE, "储藏室", is_unlocked=True)
        elif self.home_level == 4:
            self.rooms[RoomType.GARDEN] = Room(RoomType.GARDEN, "花园", is_unlocked=True)
        elif self.home_level == 5:
            self.rooms[RoomType.STUDY] = Room(RoomType.STUDY, "书房", is_unlocked=True)
        
        return True
    
    def update_stats(self):
        self.total_comfort = 0
        self.total_storage = 0
        
        for room in self.rooms.values():
            if room.is_unlocked:
                self.total_comfort += room.get_comfort_level()
                for furniture in room.furniture.values():
                    self.total_storage += furniture.storage_bonus


FURNITURE_DATABASE = {
    "basic_bed": Furniture(
        furniture_id="basic_bed",
        name="普通床铺",
        category=FurnitureCategory.BED,
        description="简单的床铺，提供基本的休息功能",
        icon="🛏️",
        price=200,
        comfort_bonus=5,
        required_room=RoomType.BEDROOM
    ),
    "comfortable_bed": Furniture(
        furniture_id="comfortable_bed",
        name="舒适床铺",
        category=FurnitureCategory.BED,
        description="柔软舒适的床铺，恢复更多体力",
        icon="🛏️",
        price=500,
        comfort_bonus=15,
        special_effect="energy_boost",
        required_room=RoomType.BEDROOM
    ),
    "luxury_bed": Furniture(
        furniture_id="luxury_bed",
        name="豪华床铺",
        category=FurnitureCategory.BED,
        description="顶级床铺，极致舒适",
        icon="🛏️",
        price=1500,
        comfort_bonus=30,
        special_effect="full_recover",
        required_room=RoomType.BEDROOM
    ),
    "wooden_table": Furniture(
        furniture_id="wooden_table",
        name="木桌",
        category=FurnitureCategory.TABLE,
        description="简单的木制桌子",
        icon="🪑",
        price=100,
        comfort_bonus=2,
        required_room=RoomType.LIVING_ROOM
    ),
    "dining_table": Furniture(
        furniture_id="dining_table",
        name="餐桌",
        category=FurnitureCategory.TABLE,
        description="家庭用餐的好地方",
        icon="🍽️",
        price=300,
        comfort_bonus=8,
        required_room=RoomType.LIVING_ROOM
    ),
    "bookshelf": Furniture(
        furniture_id="bookshelf",
        name="书架",
        category=FurnitureCategory.STORAGE,
        description="存放书籍和物品",
        icon="📚",
        price=200,
        comfort_bonus=3,
        storage_bonus=20,
        required_room=RoomType.STUDY
    ),
    "cabinet": Furniture(
        furniture_id="cabinet",
        name="储物柜",
        category=FurnitureCategory.STORAGE,
        description="大型储物空间",
        icon="🗄️",
        price=400,
        comfort_bonus=1,
        storage_bonus=50,
        required_room=RoomType.STORAGE
    ),
    "lamp": Furniture(
        furniture_id="lamp",
        name="台灯",
        category=FurnitureCategory.LIGHTING,
        description="温馨的照明",
        icon="💡",
        price=50,
        comfort_bonus=2
    ),
    "chandelier": Furniture(
        furniture_id="chandelier",
        name="吊灯",
        category=FurnitureCategory.LIGHTING,
        description="华丽的照明装饰",
        icon="💡",
        price=300,
        comfort_bonus=8
    ),
    "flower_pot": Furniture(
        furniture_id="flower_pot",
        name="花盆",
        category=FurnitureCategory.DECORATION,
        description="美丽的植物装饰",
        icon="🪴",
        price=30,
        comfort_bonus=3
    ),
    "painting": Furniture(
        furniture_id="painting",
        name="画作",
        category=FurnitureCategory.DECORATION,
        description="精美的艺术品",
        icon="🖼️",
        price=150,
        comfort_bonus=5
    ),
    "tv": Furniture(
        furniture_id="tv",
        name="电视机",
        category=FurnitureCategory.APPLIANCE,
        description="娱乐设施",
        icon="📺",
        price=500,
        comfort_bonus=10,
        required_room=RoomType.LIVING_ROOM
    ),
    "refrigerator": Furniture(
        furniture_id="refrigerator",
        name="冰箱",
        category=FurnitureCategory.APPLIANCE,
        description="储存食物",
        icon="🧊",
        price=600,
        comfort_bonus=5,
        storage_bonus=30,
        required_room=RoomType.KITCHEN
    ),
    "stove": Furniture(
        furniture_id="stove",
        name="炉灶",
        category=FurnitureCategory.APPLIANCE,
        description="烹饪美食",
        icon="🍳",
        price=400,
        comfort_bonus=5,
        special_effect="cooking_bonus",
        required_room=RoomType.KITCHEN
    ),
    "garden_bench": Furniture(
        furniture_id="garden_bench",
        name="花园长椅",
        category=FurnitureCategory.DECORATION,
        description="在花园中休息",
        icon="🪑",
        price=200,
        comfort_bonus=8,
        required_room=RoomType.GARDEN
    ),
    "fountain": Furniture(
        furniture_id="fountain",
        name="喷泉",
        category=FurnitureCategory.DECORATION,
        description="美丽的喷泉装饰",
        icon="⛲",
        price=1000,
        comfort_bonus=20,
        special_effect="luck_bonus",
        required_room=RoomType.GARDEN
    ),
}


class HomeManager:
    
    def __init__(self):
        self.home: Home = Home()
        self.owned_furniture: Dict[str, int] = {}
        self.on_home_upgrade: Optional[Callable] = None
        self.on_furniture_place: Optional[Callable] = None
        
        self._init_starting_furniture()
    
    def _init_starting_furniture(self):
        self.owned_furniture = {
            "basic_bed": 1,
            "wooden_table": 1,
            "lamp": 2,
            "flower_pot": 1
        }
    
    def get_home_level(self) -> int:
        return self.home.home_level
    
    def get_home_info(self) -> Dict:
        return {
            "level": self.home.home_level,
            "max_level": self.home.max_level,
            "can_upgrade": self.home.can_upgrade(),
            "upgrade_cost": self.home.get_upgrade_cost(),
            "total_comfort": self.home.total_comfort,
            "total_storage": self.home.total_storage,
            "rooms": self._get_rooms_info()
        }
    
    def _get_rooms_info(self) -> List[Dict]:
        rooms_info = []
        for room_type, room in self.home.rooms.items():
            if room.is_unlocked:
                rooms_info.append({
                    "type": room_type.value,
                    "name": room.name,
                    "level": room.level,
                    "comfort": room.get_comfort_level(),
                    "furniture_count": len(room.furniture),
                    "can_upgrade": room.can_upgrade(),
                    "upgrade_cost": room.get_upgrade_cost()
                })
        return rooms_info
    
    def upgrade_home(self, player_money: int) -> Tuple[bool, str]:
        if not self.home.can_upgrade():
            return False, "房屋已达最高等级！"
        
        cost = self.home.get_upgrade_cost()
        if player_money < cost:
            return False, f"金币不足！需要 {cost} 金币"
        
        if self.home.upgrade():
            self.home.update_stats()
            
            if self.on_home_upgrade:
                self.on_home_upgrade(self.home.home_level)
            
            return True, f"房屋升级成功！现在是 {self.home.home_level} 级"
        
        return False, "升级失败"
    
    def upgrade_room(self, room_type: RoomType, player_money: int) -> Tuple[bool, str]:
        if room_type not in self.home.rooms:
            return False, "未知房间"
        
        room = self.home.rooms[room_type]
        if not room.is_unlocked:
            return False, "房间未解锁"
        
        if not room.can_upgrade():
            return False, "房间已达最高等级"
        
        cost = room.get_upgrade_cost()
        if player_money < cost:
            return False, f"金币不足！需要 {cost} 金币"
        
        room.level += 1
        self.home.update_stats()
        
        return True, f"{room.name}升级成功！现在是 {room.level} 级"
    
    def buy_furniture(self, furniture_id: str, player_money: int) -> Tuple[bool, str]:
        if furniture_id not in FURNITURE_DATABASE:
            return False, "未知家具"
        
        furniture = FURNITURE_DATABASE[furniture_id]
        if player_money < furniture.price:
            return False, f"金币不足！需要 {furniture.price} 金币"
        
        if furniture_id in self.owned_furniture:
            self.owned_furniture[furniture_id] += 1
        else:
            self.owned_furniture[furniture_id] = 1
        
        return True, f"购买了 {furniture.icon} {furniture.name}"
    
    def place_furniture(self, furniture_id: str, room_type: RoomType) -> Tuple[bool, str]:
        if furniture_id not in FURNITURE_DATABASE:
            return False, "未知家具"
        
        if furniture_id not in self.owned_furniture or self.owned_furniture[furniture_id] <= 0:
            return False, "没有该家具"
        
        if room_type not in self.home.rooms:
            return False, "未知房间"
        
        room = self.home.rooms[room_type]
        if not room.is_unlocked:
            return False, "房间未解锁"
        
        furniture = FURNITURE_DATABASE[furniture_id]
        
        if furniture.required_room and furniture.required_room != room_type:
            return False, f"该家具只能放在{furniture.required_room.value}"
        
        import uuid
        instance_id = str(uuid.uuid4())[:8]
        room.furniture[instance_id] = furniture
        
        self.owned_furniture[furniture_id] -= 1
        if self.owned_furniture[furniture_id] <= 0:
            del self.owned_furniture[furniture_id]
        
        self.home.update_stats()
        
        if self.on_furniture_place:
            self.on_furniture_place(room_type, furniture)
        
        return True, f"在{room.name}放置了 {furniture.icon} {furniture.name}"
    
    def remove_furniture(self, instance_id: str, room_type: RoomType) -> Tuple[bool, str]:
        if room_type not in self.home.rooms:
            return False, "未知房间"
        
        room = self.home.rooms[room_type]
        if instance_id not in room.furniture:
            return False, "找不到该家具"
        
        furniture = room.furniture[instance_id]
        del room.furniture[instance_id]
        
        if furniture.furniture_id in self.owned_furniture:
            self.owned_furniture[furniture.furniture_id] += 1
        else:
            self.owned_furniture[furniture.furniture_id] = 1
        
        self.home.update_stats()
        
        return True, f"移除了 {furniture.icon} {furniture.name}"
    
    def get_shop_furniture(self) -> List[Dict]:
        result = []
        for furniture_id, furniture in FURNITURE_DATABASE.items():
            result.append({
                "furniture_id": furniture_id,
                "name": furniture.name,
                "category": furniture.category.value,
                "description": furniture.description,
                "icon": furniture.icon,
                "price": furniture.price,
                "comfort_bonus": furniture.comfort_bonus,
                "storage_bonus": furniture.storage_bonus,
                "special_effect": furniture.special_effect,
                "required_room": furniture.required_room.value if furniture.required_room else None,
                "owned": self.owned_furniture.get(furniture_id, 0)
            })
        return result
    
    def get_room_furniture(self, room_type: RoomType) -> List[Dict]:
        if room_type not in self.home.rooms:
            return []
        
        room = self.home.rooms[room_type]
        result = []
        
        for instance_id, furniture in room.furniture.items():
            result.append({
                "instance_id": instance_id,
                "furniture_id": furniture.furniture_id,
                "name": furniture.name,
                "icon": furniture.icon,
                "comfort_bonus": furniture.comfort_bonus,
                "storage_bonus": furniture.storage_bonus
            })
        
        return result
    
    def get_daily_bonus(self) -> Dict:
        comfort = self.home.total_comfort
        
        energy_bonus = comfort // 10
        luck_bonus = min(10, comfort // 20)
        
        return {
            "energy_bonus": energy_bonus,
            "luck_bonus": luck_bonus,
            "storage_bonus": self.home.total_storage
        }
    
    def get_save_data(self) -> Dict:
        rooms_data = {}
        for room_type, room in self.home.rooms.items():
            rooms_data[room_type.value] = {
                "level": room.level,
                "is_unlocked": room.is_unlocked,
                "furniture": {
                    iid: f.furniture_id for iid, f in room.furniture.items()
                }
            }
        
        return {
            "home_level": self.home.home_level,
            "rooms": rooms_data,
            "owned_furniture": self.owned_furniture.copy()
        }
    
    def load_save_data(self, data: Dict):
        self.home.home_level = data.get("home_level", 1)
        
        rooms_data = data.get("rooms", {})
        for room_type_str, room_data in rooms_data.items():
            try:
                room_type = RoomType(room_type_str)
                if room_type in self.home.rooms:
                    room = self.home.rooms[room_type]
                    room.level = room_data.get("level", 1)
                    room.is_unlocked = room_data.get("is_unlocked", False)
                    
                    room.furniture = {}
                    for instance_id, furniture_id in room_data.get("furniture", {}).items():
                        if furniture_id in FURNITURE_DATABASE:
                            room.furniture[instance_id] = FURNITURE_DATABASE[furniture_id]
            except ValueError:
                pass
        
        self.owned_furniture = data.get("owned_furniture", {})
        self.home.update_stats()
