"""
动物系统模块
管理农场动物的饲养和产出
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class AnimalType(Enum):
    CHICKEN = "鸡"
    COW = "牛"
    PIG = "猪"
    SHEEP = "羊"
    DUCK = "鸭"
    RABBIT = "兔子"


class AnimalMood(Enum):
    HAPPY = "开心"
    NORMAL = "普通"
    SAD = "难过"
    SICK = "生病"


@dataclass
class AnimalProduct:
    name: str
    base_price: int
    quality_levels: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.quality_levels:
            self.quality_levels = {
                "普通": 1.0,
                "优质": 1.5,
                "极品": 2.0
            }


@dataclass
class Animal:
    name: str
    animal_type: AnimalType
    age: int = 0
    health: int = 100
    happiness: int = 100
    hunger: int = 100
    days_owned: int = 0
    is_fed: bool = False
    is_petted: bool = False
    
    @property
    def mood(self) -> AnimalMood:
        if self.health < 30:
            return AnimalMood.SICK
        elif self.happiness < 30:
            return AnimalMood.SAD
        elif self.happiness > 70 and self.health > 70:
            return AnimalMood.HAPPY
        return AnimalMood.NORMAL
    
    def feed(self) -> bool:
        if self.is_fed:
            return False
        self.is_fed = True
        self.hunger = min(100, self.hunger + 30)
        self.health = min(100, self.health + 5)
        return True
    
    def pet(self) -> bool:
        if self.is_petted:
            return False
        self.is_petted = True
        self.happiness = min(100, self.happiness + 15)
        return True
    
    def new_day(self) -> dict:
        self.days_owned += 1
        self.age += 1
        
        changes = {"happiness": 0, "health": 0, "hunger": 0}
        
        if not self.is_fed:
            self.hunger = max(0, self.hunger - 20)
            self.happiness = max(0, self.happiness - 10)
            changes["hunger"] = -20
            changes["happiness"] = -10
        
        if self.hunger < 30:
            self.health = max(0, self.health - 5)
            changes["health"] = -5
        
        self.is_fed = False
        self.is_petted = False
        
        return changes
    
    def can_produce(self) -> bool:
        return self.is_fed and self.health > 50 and self.happiness > 30
    
    def get_production_quality(self) -> str:
        if self.health > 90 and self.happiness > 90:
            return "极品"
        elif self.health > 70 and self.happiness > 70:
            return "优质"
        return "普通"


ANIMAL_DATA = {
    AnimalType.CHICKEN: {
        "name": "母鸡",
        "price": 500,
        "product": AnimalProduct("鸡蛋", 50),
        "feed_cost": 10,
        "emoji": "🐔"
    },
    AnimalType.COW: {
        "name": "奶牛",
        "price": 2000,
        "product": AnimalProduct("牛奶", 150),
        "feed_cost": 30,
        "emoji": "🐄"
    },
    AnimalType.PIG: {
        "name": "猪",
        "price": 1500,
        "product": AnimalProduct("松露", 300),
        "feed_cost": 25,
        "emoji": "🐷"
    },
    AnimalType.SHEEP: {
        "name": "绵羊",
        "price": 1200,
        "product": AnimalProduct("羊毛", 100),
        "feed_cost": 20,
        "emoji": "🐑"
    },
    AnimalType.DUCK: {
        "name": "鸭子",
        "price": 600,
        "product": AnimalProduct("鸭蛋", 60),
        "feed_cost": 12,
        "emoji": "🦆"
    },
    AnimalType.RABBIT: {
        "name": "兔子",
        "price": 400,
        "product": AnimalProduct("兔毛", 80),
        "feed_cost": 8,
        "emoji": "🐰"
    }
}


class AnimalManager:
    def __init__(self):
        self.animals: List[Animal] = []
        self.max_animals = 10
        self.building_level = 1
    
    def can_add_animal(self) -> bool:
        return len(self.animals) < self.max_animals
    
    def add_animal(self, animal_type: AnimalType, name: str = None) -> tuple:
        if not self.can_add_animal():
            return (False, "动物栏已满！")
        
        data = ANIMAL_DATA.get(animal_type)
        if not data:
            return (False, "未知的动物类型！")
        
        animal_name = name or f"{data['name']}{len(self.animals) + 1}"
        animal = Animal(name=animal_name, animal_type=animal_type)
        self.animals.append(animal)
        
        return (True, f"成功购买了一只{data['emoji']} {animal_name}！")
    
    def remove_animal(self, index: int) -> tuple:
        if 0 <= index < len(self.animals):
            animal = self.animals.pop(index)
            data = ANIMAL_DATA.get(animal.animal_type)
            sell_price = data["price"] // 2 if data else 0
            return (True, f"出售了{animal.name}，获得{sell_price}金币", sell_price)
        return (False, "无效的动物索引", 0)
    
    def feed_animal(self, index: int) -> tuple:
        if 0 <= index < len(self.animals):
            animal = self.animals[index]
            if animal.feed():
                return (True, f"给{animal.name}喂食成功！")
            return (False, f"{animal.name}今天已经喂过了")
        return (False, "无效的动物索引")
    
    def feed_all(self) -> tuple:
        fed_count = 0
        for animal in self.animals:
            if animal.feed():
                fed_count += 1
        return (True, f"成功喂食了{fed_count}只动物")
    
    def pet_animal(self, index: int) -> tuple:
        if 0 <= index < len(self.animals):
            animal = self.animals[index]
            if animal.pet():
                return (True, f"抚摸了{animal.name}，它看起来很开心！")
            return (False, f"{animal.name}今天已经被抚摸过了")
        return (False, "无效的动物索引")
    
    def collect_products(self) -> tuple:
        products = {}
        total_value = 0
        
        for animal in self.animals:
            if animal.can_produce():
                data = ANIMAL_DATA.get(animal.animal_type)
                if data:
                    product = data["product"]
                    quality = animal.get_production_quality()
                    multiplier = product.quality_levels.get(quality, 1.0)
                    value = int(product.base_price * multiplier)
                    
                    product_name = f"{quality}{product.name}"
                    if product_name not in products:
                        products[product_name] = {"count": 0, "value": value}
                    products[product_name]["count"] += 1
                    total_value += value
        
        return (True, products, total_value)
    
    def advance_day(self) -> dict:
        results = {
            "changes": [],
            "sick_animals": [],
            "products": {}
        }
        
        for animal in self.animals:
            changes = animal.new_day()
            if changes["health"] < 0 or changes["happiness"] < 0:
                results["changes"].append({
                    "name": animal.name,
                    "changes": changes
                })
            if animal.mood == AnimalMood.SICK:
                results["sick_animals"].append(animal.name)
        
        _, products, _ = self.collect_products()
        results["products"] = products
        
        return results
    
    def upgrade_building(self) -> tuple:
        if self.building_level >= 5:
            return (False, "动物栏已达最高等级！")
        self.building_level += 1
        self.max_animals = 10 + self.building_level * 5
        return (True, f"动物栏升级成功！最大容量：{self.max_animals}")
    
    def get_animal_by_index(self, index: int) -> Optional[Animal]:
        if 0 <= index < len(self.animals):
            return self.animals[index]
        return None
    
    def get_all_animals(self) -> List[Animal]:
        return self.animals.copy()
    
    def get_total_feed_cost(self) -> int:
        return sum(
            ANIMAL_DATA.get(a.animal_type, {}).get("feed_cost", 0)
            for a in self.animals
            if not a.is_fed
        )
    
    def to_dict(self) -> dict:
        return {
            "animals": [
                {
                    "name": a.name,
                    "type": a.animal_type.value,
                    "age": a.age,
                    "health": a.health,
                    "happiness": a.happiness,
                    "hunger": a.hunger,
                    "days_owned": a.days_owned
                }
                for a in self.animals
            ],
            "building_level": self.building_level,
            "max_animals": self.max_animals
        }
    
    def from_dict(self, data: dict):
        self.building_level = data.get("building_level", 1)
        self.max_animals = data.get("max_animals", 10)
        self.animals = []
        
        for a_data in data.get("animals", []):
            animal_type = None
            for t in AnimalType:
                if t.value == a_data["type"]:
                    animal_type = t
                    break
            
            if animal_type:
                animal = Animal(
                    name=a_data["name"],
                    animal_type=animal_type,
                    age=a_data.get("age", 0),
                    health=a_data.get("health", 100),
                    happiness=a_data.get("happiness", 100),
                    hunger=a_data.get("hunger", 100),
                    days_owned=a_data.get("days_owned", 0)
                )
                self.animals.append(animal)
