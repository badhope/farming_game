"""
宠物系统模块
提供宠物获取、培养、互动等功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import random


class PetType(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    HAMSTER = "hamster"


class PetMood(Enum):
    HAPPY = "happy"
    NORMAL = "normal"
    SAD = "sad"
    HUNGRY = "hungry"


class PetSkill(Enum):
    FETCH = "捡拾"
    GUARD = "看护"
    HEALING = "治愈"
    LUCK = "幸运"
    HARVEST_HELP = "收获助手"
    FIND_TREASURE = "寻宝"


@dataclass
class PetStats:
    hunger: int = 100
    happiness: int = 100
    health: int = 100
    energy: int = 100
    friendship: int = 0
    
    def is_hungry(self) -> bool:
        return self.hunger < 30
    
    def is_sad(self) -> bool:
        return self.happiness < 30
    
    def is_tired(self) -> bool:
        return self.energy < 30
    
    def get_mood(self) -> PetMood:
        if self.hunger < 30:
            return PetMood.HUNGRY
        elif self.happiness >= 70 and self.health >= 70:
            return PetMood.HAPPY
        elif self.happiness < 30 or self.health < 30:
            return PetMood.SAD
        else:
            return PetMood.NORMAL


@dataclass
class PetSkillData:
    skill: PetSkill
    level: int = 1
    exp: int = 0
    max_level: int = 5
    
    def get_exp_to_next(self) -> int:
        return self.level * 100
    
    def add_exp(self, amount: int) -> bool:
        self.exp += amount
        leveled_up = False
        
        while self.exp >= self.get_exp_to_next() and self.level < self.max_level:
            self.exp -= self.get_exp_to_next()
            self.level += 1
            leveled_up = True
        
        return leveled_up


PET_DATA = {
    PetType.DOG: {
        "name": "小狗",
        "emoji": "🐕",
        "description": "忠诚的伙伴，擅长捡拾和看护",
        "base_skills": [PetSkill.FETCH, PetSkill.GUARD],
        "max_friendship": 1000,
        "hunger_rate": 5,
        "happiness_rate": 3,
        "special_ability": "每天有几率自动收获成熟作物"
    },
    PetType.CAT: {
        "name": "小猫",
        "emoji": "🐱",
        "description": "可爱的伙伴，擅长寻宝和幸运",
        "base_skills": [PetSkill.FIND_TREASURE, PetSkill.LUCK],
        "max_friendship": 1000,
        "hunger_rate": 4,
        "happiness_rate": 4,
        "special_ability": "增加探险时发现稀有物品的概率"
    },
    PetType.BIRD: {
        "name": "小鸟",
        "emoji": "🐦",
        "description": "自由的伙伴，擅长寻宝和治愈",
        "base_skills": [PetSkill.FIND_TREASURE, PetSkill.HEALING],
        "max_friendship": 800,
        "hunger_rate": 6,
        "happiness_rate": 5,
        "special_ability": "每天有几率带回随机物品"
    },
    PetType.RABBIT: {
        "name": "小兔子",
        "emoji": "🐰",
        "description": "温顺的伙伴，擅长收获助手",
        "base_skills": [PetSkill.HARVEST_HELP, PetSkill.LUCK],
        "max_friendship": 800,
        "hunger_rate": 5,
        "happiness_rate": 4,
        "special_ability": "收获时有几率获得额外作物"
    },
    PetType.HAMSTER: {
        "name": "仓鼠",
        "emoji": "🐹",
        "description": "小巧的伙伴，擅长寻宝",
        "base_skills": [PetSkill.FIND_TREASURE],
        "max_friendship": 600,
        "hunger_rate": 8,
        "happiness_rate": 6,
        "special_ability": "每天有几率找到金币"
    },
}


@dataclass
class Pet:
    pet_id: str
    pet_type: PetType
    name: str
    stats: PetStats = field(default_factory=PetStats)
    skills: Dict[PetSkill, PetSkillData] = field(default_factory=dict)
    level: int = 1
    exp: int = 0
    days_owned: int = 0
    is_active: bool = True
    
    def __post_init__(self):
        if not self.skills:
            data = PET_DATA.get(self.pet_type, {})
            for skill in data.get("base_skills", []):
                self.skills[skill] = PetSkillData(skill=skill)
    
    @property
    def emoji(self) -> str:
        return PET_DATA.get(self.pet_type, {}).get("emoji", "🐾")
    
    @property
    def type_name(self) -> str:
        return PET_DATA.get(self.pet_type, {}).get("name", "宠物")
    
    @property
    def description(self) -> str:
        return PET_DATA.get(self.pet_type, {}).get("description", "")
    
    @property
    def special_ability(self) -> str:
        return PET_DATA.get(self.pet_type, {}).get("special_ability", "")
    
    def feed(self, food_quality: int = 1) -> Dict:
        result = {"success": False, "message": ""}
        
        if self.stats.hunger >= 100:
            result["message"] = f"{self.name}已经吃饱了！"
            return result
        
        hunger_restore = 20 * food_quality
        self.stats.hunger = min(100, self.stats.hunger + hunger_restore)
        self.stats.happiness = min(100, self.stats.happiness + 5)
        self.stats.friendship = min(1000, self.stats.friendship + 2)
        
        result["success"] = True
        result["message"] = f"给{self.name}喂食成功！饱食度+{hunger_restore}"
        return result
    
    def play(self) -> Dict:
        result = {"success": False, "message": "", "rewards": {}}
        
        if self.stats.energy < 20:
            result["message"] = f"{self.name}太累了，需要休息！"
            return result
        
        self.stats.energy -= 20
        self.stats.happiness = min(100, self.stats.happiness + 15)
        self.stats.friendship = min(1000, self.stats.friendship + 5)
        
        for skill_data in self.skills.values():
            if skill_data.add_exp(10):
                result["rewards"]["skill_level_up"] = skill_data.skill.value
        
        result["success"] = True
        result["message"] = f"和{self.name}玩耍很开心！"
        
        if random.random() < 0.3:
            bonus = random.choice(["money", "item"])
            if bonus == "money":
                result["rewards"]["money"] = random.randint(5, 20)
            else:
                result["rewards"]["item"] = {"种子": 1}
        
        return result
    
    def pet_care(self) -> Dict:
        result = {"success": False, "message": ""}
        
        self.stats.happiness = min(100, self.stats.happiness + 10)
        self.stats.friendship = min(1000, self.stats.friendship + 3)
        
        result["success"] = True
        result["message"] = f"抚摸{self.name}，它看起来很开心！"
        return result
    
    def heal(self) -> Dict:
        result = {"success": False, "message": ""}
        
        if self.stats.health >= 100:
            result["message"] = f"{self.name}很健康，不需要治疗！"
            return result
        
        self.stats.health = min(100, self.stats.health + 30)
        self.stats.happiness = min(100, self.stats.happiness + 5)
        
        result["success"] = True
        result["message"] = f"{self.name}恢复了健康！"
        return result
    
    def rest(self) -> Dict:
        result = {"success": True, "message": ""}
        
        self.stats.energy = min(100, self.stats.energy + 50)
        result["message"] = f"{self.name}休息得很好！"
        return result
    
    def new_day(self) -> Dict:
        result = {"events": [], "rewards": {}}
        
        data = PET_DATA.get(self.pet_type, {})
        self.stats.hunger = max(0, self.stats.hunger - data.get("hunger_rate", 5))
        self.stats.happiness = max(0, self.stats.happiness - data.get("happiness_rate", 3))
        self.days_owned += 1
        
        if self.stats.hunger < 20:
            result["events"].append(f"{self.name}很饿了！")
            self.stats.health = max(0, self.stats.health - 5)
        
        if self.stats.happiness < 20:
            result["events"].append(f"{self.name}不太开心...")
        
        if self.stats.friendship >= 100 and self.level < 10:
            exp_gain = self.stats.friendship // 100
            self.exp += exp_gain
            
            if self.exp >= self.level * 100:
                self.exp -= self.level * 100
                self.level += 1
                result["events"].append(f"{self.name}升级到{self.level}级了！")
        
        if self.is_active and self.stats.energy >= 30:
            self._trigger_special_ability(result)
        
        return result
    
    def _trigger_special_ability(self, result: Dict):
        if self.pet_type == PetType.DOG:
            if random.random() < 0.1 + self.level * 0.02:
                result["rewards"]["auto_harvest"] = True
                result["events"].append(f"{self.name}帮你收获了一些作物！")
        
        elif self.pet_type == PetType.CAT:
            if random.random() < 0.15 + self.level * 0.03:
                result["rewards"]["luck_bonus"] = True
        
        elif self.pet_type == PetType.BIRD:
            if random.random() < 0.2 + self.level * 0.02:
                items = ["种子", "金币", "材料"]
                result["rewards"]["found_item"] = random.choice(items)
                result["events"].append(f"{self.name}带回了东西！")
        
        elif self.pet_type == PetType.RABBIT:
            if random.random() < 0.1 + self.level * 0.02:
                result["rewards"]["extra_harvest"] = True
        
        elif self.pet_type == PetType.HAMSTER:
            if random.random() < 0.15 + self.level * 0.03:
                gold = random.randint(5, 15) * self.level
                result["rewards"]["money"] = gold
                result["events"].append(f"{self.name}找到了{gold}金币！")
    
    def get_skill_level(self, skill: PetSkill) -> int:
        if skill in self.skills:
            return self.skills[skill].level
        return 0
    
    def get_status_summary(self) -> str:
        mood = self.stats.get_mood()
        mood_emoji = {
            PetMood.HAPPY: "😊",
            PetMood.NORMAL: "😐",
            PetMood.SAD: "😢",
            PetMood.HUNGRY: "🍽️"
        }
        
        return (
            f"{self.emoji} {self.name} Lv.{self.level}\n"
            f"心情: {mood_emoji.get(mood, '😐')} {mood.value}\n"
            f"饱食: {'❤️' * (self.stats.hunger // 20)}{'🤍' * (5 - self.stats.hunger // 20)}\n"
            f"快乐: {'💛' * (self.stats.happiness // 20)}{'🤍' * (5 - self.stats.happiness // 20)}\n"
            f"好感: {self.stats.friendship}/1000"
        )
    
    def get_save_data(self) -> Dict:
        return {
            "pet_id": self.pet_id,
            "pet_type": self.pet_type.value,
            "name": self.name,
            "stats": {
                "hunger": self.stats.hunger,
                "happiness": self.stats.happiness,
                "health": self.stats.health,
                "energy": self.stats.energy,
                "friendship": self.stats.friendship,
            },
            "skills": {
                skill.value: {"level": data.level, "exp": data.exp}
                for skill, data in self.skills.items()
            },
            "level": self.level,
            "exp": self.exp,
            "days_owned": self.days_owned,
            "is_active": self.is_active,
        }
    
    @classmethod
    def from_save_data(cls, data: Dict) -> 'Pet':
        stats_data = data.get("stats", {})
        stats = PetStats(
            hunger=stats_data.get("hunger", 100),
            happiness=stats_data.get("happiness", 100),
            health=stats_data.get("health", 100),
            energy=stats_data.get("energy", 100),
            friendship=stats_data.get("friendship", 0),
        )
        
        pet = cls(
            pet_id=data.get("pet_id"),
            pet_type=PetType(data.get("pet_type")),
            name=data.get("name"),
            stats=stats,
            level=data.get("level", 1),
            exp=data.get("exp", 0),
            days_owned=data.get("days_owned", 0),
            is_active=data.get("is_active", True),
        )
        
        for skill_str, skill_data in data.get("skills", {}).items():
            skill = PetSkill(skill_str)
            pet.skills[skill] = PetSkillData(
                skill=skill,
                level=skill_data.get("level", 1),
                exp=skill_data.get("exp", 0)
            )
        
        return pet


class PetManager:
    
    def __init__(self):
        self.pets: Dict[str, Pet] = {}
        self.active_pet_id: Optional[str] = None
        self.on_pet_event: Optional[Callable] = None
        
        self._init_available_pets()
    
    def _init_available_pets(self):
        pass
    
    def create_pet(self, pet_type: PetType, name: str) -> Pet:
        import uuid
        pet_id = str(uuid.uuid4())[:8]
        
        pet = Pet(
            pet_id=pet_id,
            pet_type=pet_type,
            name=name
        )
        
        self.pets[pet_id] = pet
        
        if not self.active_pet_id:
            self.active_pet_id = pet_id
        
        return pet
    
    def get_pet(self, pet_id: str) -> Optional[Pet]:
        return self.pets.get(pet_id)
    
    def get_active_pet(self) -> Optional[Pet]:
        if self.active_pet_id:
            return self.pets.get(self.active_pet_id)
        return None
    
    def set_active_pet(self, pet_id: str) -> bool:
        if pet_id in self.pets:
            old_active = self.active_pet_id
            if old_active and old_active in self.pets:
                self.pets[old_active].is_active = False
            
            self.active_pet_id = pet_id
            self.pets[pet_id].is_active = True
            return True
        return False
    
    def feed_pet(self, pet_id: str, food_quality: int = 1) -> Dict:
        pet = self.get_pet(pet_id)
        if pet:
            return pet.feed(food_quality)
        return {"success": False, "message": "找不到宠物！"}
    
    def play_with_pet(self, pet_id: str) -> Dict:
        pet = self.get_pet(pet_id)
        if pet:
            return pet.play()
        return {"success": False, "message": "找不到宠物！"}
    
    def pet_the_pet(self, pet_id: str) -> Dict:
        pet = self.get_pet(pet_id)
        if pet:
            return pet.pet_care()
        return {"success": False, "message": "找不到宠物！"}
    
    def heal_pet(self, pet_id: str) -> Dict:
        pet = self.get_pet(pet_id)
        if pet:
            return pet.heal()
        return {"success": False, "message": "找不到宠物！"}
    
    def new_day_all(self) -> Dict:
        results = {}
        
        for pet_id, pet in self.pets.items():
            results[pet_id] = pet.new_day()
        
        return results
    
    def get_all_pets_summary(self) -> List[Dict]:
        return [
            {
                "pet_id": pet.pet_id,
                "name": pet.name,
                "type": pet.type_name,
                "emoji": pet.emoji,
                "level": pet.level,
                "mood": pet.stats.get_mood().value,
                "is_active": pet.is_active
            }
            for pet in self.pets.values()
        ]
    
    def get_save_data(self) -> Dict:
        return {
            "pets": [pet.get_save_data() for pet in self.pets.values()],
            "active_pet_id": self.active_pet_id,
        }
    
    def load_save_data(self, data: Dict):
        self.pets = {}
        
        for pet_data in data.get("pets", []):
            pet = Pet.from_save_data(pet_data)
            self.pets[pet.pet_id] = pet
        
        self.active_pet_id = data.get("active_pet_id")
