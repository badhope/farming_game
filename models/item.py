"""
道具系统模块
提供道具获取、使用、合成等功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum


class ItemType(Enum):
    SEED = "seed"
    CROP = "crop"
    TOOL = "tool"
    FOOD = "food"
    MATERIAL = "material"
    DECORATION = "decoration"
    SPECIAL = "special"
    POTION = "potion"


class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


@dataclass
class ItemEffect:
    effect_type: str
    value: int
    duration: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "effect_type": self.effect_type,
            "value": self.value,
            "duration": self.duration
        }


@dataclass
class Item:
    item_id: str
    name: str
    item_type: ItemType
    description: str
    rarity: ItemRarity = ItemRarity.COMMON
    price: int = 0
    sell_price: int = 0
    stackable: bool = True
    max_stack: int = 99
    effects: List[ItemEffect] = field(default_factory=list)
    icon: str = "📦"
    
    def can_use(self) -> bool:
        return len(self.effects) > 0
    
    def get_effects_summary(self) -> str:
        if not self.effects:
            return "无效果"
        
        summaries = []
        for effect in self.effects:
            if effect.effect_type == "heal":
                summaries.append(f"恢复{effect.value}生命值")
            elif effect.effect_type == "energy":
                summaries.append(f"恢复{effect.value}体力")
            elif effect.effect_type == "speed":
                summaries.append(f"速度+{effect.value}%持续{effect.duration}秒")
            elif effect.effect_type == "luck":
                summaries.append(f"幸运+{effect.value}持续{effect.duration}秒")
        
        return ", ".join(summaries)


ITEM_DATABASE = {
    "speed_fertilizer": Item(
        item_id="speed_fertilizer",
        name="生长加速剂",
        item_type=ItemType.TOOL,
        description="使作物生长速度提升50%",
        rarity=ItemRarity.UNCOMMON,
        price=100,
        sell_price=50,
        icon="🧪",
        effects=[ItemEffect("growth_speed", 50, 7)]
    ),
    "quality_fertilizer": Item(
        item_id="quality_fertilizer",
        name="品质肥料",
        item_type=ItemType.TOOL,
        description="提升作物品质，售价提高25%",
        rarity=ItemRarity.RARE,
        price=200,
        sell_price=100,
        icon="🌱",
        effects=[ItemEffect("quality_boost", 25, 7)]
    ),
    "water_retention": Item(
        item_id="water_retention",
        name="保水剂",
        item_type=ItemType.TOOL,
        description="自动保持土壤湿润3天",
        rarity=ItemRarity.UNCOMMON,
        price=80,
        sell_price=40,
        icon="💧",
        effects=[ItemEffect("auto_water", 3, 0)]
    ),
    "health_potion": Item(
        item_id="health_potion",
        name="生命药水",
        item_type=ItemType.POTION,
        description="恢复50点生命值",
        rarity=ItemRarity.COMMON,
        price=50,
        sell_price=25,
        icon="❤️",
        effects=[ItemEffect("heal", 50, 0)]
    ),
    "energy_potion": Item(
        item_id="energy_potion",
        name="体力药水",
        item_type=ItemType.POTION,
        description="恢复30点体力",
        rarity=ItemRarity.COMMON,
        price=40,
        sell_price=20,
        icon="⚡",
        effects=[ItemEffect("energy", 30, 0)]
    ),
    "luck_potion": Item(
        item_id="luck_potion",
        name="幸运药水",
        item_type=ItemType.POTION,
        description="增加幸运值，持续1天",
        rarity=ItemRarity.RARE,
        price=150,
        sell_price=75,
        icon="🍀",
        effects=[ItemEffect("luck", 20, 1)]
    ),
    "pet_food_basic": Item(
        item_id="pet_food_basic",
        name="普通宠物粮",
        item_type=ItemType.FOOD,
        description="基础的宠物食物",
        rarity=ItemRarity.COMMON,
        price=20,
        sell_price=10,
        icon="🍖",
        effects=[ItemEffect("pet_hunger", 30, 0)]
    ),
    "pet_food_premium": Item(
        item_id="pet_food_premium",
        name="高级宠物粮",
        item_type=ItemType.FOOD,
        description="高级宠物食物，营养更丰富",
        rarity=ItemRarity.UNCOMMON,
        price=50,
        sell_price=25,
        icon="🥩",
        effects=[ItemEffect("pet_hunger", 60, 0), ItemEffect("pet_happiness", 10, 0)]
    ),
    "wood": Item(
        item_id="wood",
        name="木材",
        item_type=ItemType.MATERIAL,
        description="基础建筑材料",
        rarity=ItemRarity.COMMON,
        price=10,
        sell_price=5,
        icon="🪵"
    ),
    "stone": Item(
        item_id="stone",
        name="石头",
        item_type=ItemType.MATERIAL,
        description="基础建筑材料",
        rarity=ItemRarity.COMMON,
        price=15,
        sell_price=8,
        icon="🪨"
    ),
    "iron_ore": Item(
        item_id="iron_ore",
        name="铁矿石",
        item_type=ItemType.MATERIAL,
        description="用于制作工具和建筑",
        rarity=ItemRarity.UNCOMMON,
        price=50,
        sell_price=25,
        icon="⛏️"
    ),
    "gold_ore": Item(
        item_id="gold_ore",
        name="金矿石",
        item_type=ItemType.MATERIAL,
        description="稀有矿石，价值连城",
        rarity=ItemRarity.RARE,
        price=200,
        sell_price=100,
        icon="🪙"
    ),
    "crystal": Item(
        item_id="crystal",
        name="水晶",
        item_type=ItemType.MATERIAL,
        description="神秘的晶体，蕴含能量",
        rarity=ItemRarity.EPIC,
        price=500,
        sell_price=250,
        icon="💎"
    ),
    "magic_seed": Item(
        item_id="magic_seed",
        name="魔法种子",
        item_type=ItemType.SEED,
        description="神秘的种子，可能长出任何作物",
        rarity=ItemRarity.RARE,
        price=300,
        sell_price=150,
        icon="✨"
    ),
    "golden_seed": Item(
        item_id="golden_seed",
        name="黄金种子",
        item_type=ItemType.SEED,
        description="必定长出高品质作物",
        rarity=ItemRarity.EPIC,
        price=500,
        sell_price=250,
        icon="🌟"
    ),
    "treasure_map": Item(
        item_id="treasure_map",
        name="藏宝图",
        item_type=ItemType.SPECIAL,
        description="指向隐藏宝藏的地图",
        rarity=ItemRarity.RARE,
        price=100,
        sell_price=50,
        icon="🗺️"
    ),
    "mystery_box": Item(
        item_id="mystery_box",
        name="神秘盒子",
        item_type=ItemType.SPECIAL,
        description="打开可获得随机物品",
        rarity=ItemRarity.UNCOMMON,
        price=80,
        sell_price=40,
        icon="🎁"
    ),
    "flower_pot": Item(
        item_id="flower_pot",
        name="花盆",
        item_type=ItemType.DECORATION,
        description="装饰你的家",
        rarity=ItemRarity.COMMON,
        price=30,
        sell_price=15,
        icon="🪴"
    ),
    "lamp": Item(
        item_id="lamp",
        name="台灯",
        item_type=ItemType.DECORATION,
        description="温馨的照明",
        rarity=ItemRarity.COMMON,
        price=50,
        sell_price=25,
        icon="💡"
    ),
    "painting": Item(
        item_id="painting",
        name="画作",
        item_type=ItemType.DECORATION,
        description="精美的艺术品",
        rarity=ItemRarity.UNCOMMON,
        price=100,
        sell_price=50,
        icon="🖼️"
    ),
}


@dataclass
class Recipe:
    recipe_id: str
    name: str
    ingredients: Dict[str, int]
    result: str
    result_amount: int = 1
    required_level: int = 1
    craft_time: int = 0
    description: str = ""


RECIPES = {
    "basic_fertilizer": Recipe(
        recipe_id="basic_fertilizer",
        name="基础肥料",
        ingredients={"wood": 2, "stone": 1},
        result="speed_fertilizer",
        result_amount=1,
        required_level=1,
        description="制作基础肥料"
    ),
    "quality_fertilizer_recipe": Recipe(
        recipe_id="quality_fertilizer_recipe",
        name="品质肥料",
        ingredients={"wood": 3, "iron_ore": 1},
        result="quality_fertilizer",
        result_amount=1,
        required_level=3,
        description="制作品质肥料"
    ),
    "health_potion_recipe": Recipe(
        recipe_id="health_potion_recipe",
        name="生命药水",
        ingredients={"crystal": 1},
        result="health_potion",
        result_amount=2,
        required_level=2,
        description="制作生命药水"
    ),
    "energy_potion_recipe": Recipe(
        recipe_id="energy_potion_recipe",
        name="体力药水",
        ingredients={"wood": 5},
        result="energy_potion",
        result_amount=1,
        required_level=1,
        description="制作体力药水"
    ),
    "pet_food_basic_recipe": Recipe(
        recipe_id="pet_food_basic_recipe",
        name="普通宠物粮",
        ingredients={"wood": 1, "stone": 1},
        result="pet_food_basic",
        result_amount=3,
        required_level=1,
        description="制作宠物食物"
    ),
}


class ItemManager:
    
    def __init__(self):
        self.inventory: Dict[str, int] = {}
        self.max_slots: int = 30
        self.on_item_change: Optional[Callable] = None
        
        self._init_starting_items()
    
    def _init_starting_items(self):
        self.inventory = {
            "speed_fertilizer": 2,
            "health_potion": 1,
            "pet_food_basic": 5,
        }
    
    def get_item_data(self, item_id: str) -> Optional[Item]:
        return ITEM_DATABASE.get(item_id)
    
    def add_item(self, item_id: str, amount: int = 1) -> Tuple[bool, str]:
        if item_id not in ITEM_DATABASE:
            return False, f"未知道具: {item_id}"
        
        item = ITEM_DATABASE[item_id]
        
        if not item.stackable and item_id in self.inventory:
            return False, f"该道具不可堆叠"
        
        current = self.inventory.get(item_id, 0)
        
        if current + amount > item.max_stack:
            amount = item.max_stack - current
        
        if amount <= 0:
            return False, "道具数量已达上限"
        
        self.inventory[item_id] = current + amount
        
        if self.on_item_change:
            self.on_item_change("add", item_id, amount)
        
        return True, f"获得 {item.icon} {item.name} x{amount}"
    
    def remove_item(self, item_id: str, amount: int = 1) -> Tuple[bool, str]:
        if item_id not in self.inventory:
            return False, f"没有该道具"
        
        if self.inventory[item_id] < amount:
            return False, f"道具数量不足"
        
        self.inventory[item_id] -= amount
        
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
        
        item = ITEM_DATABASE.get(item_id)
        item_name = item.name if item else item_id
        
        if self.on_item_change:
            self.on_item_change("remove", item_id, amount)
        
        return True, f"使用 {item_name} x{amount}"
    
    def use_item(self, item_id: str, context: Dict = None) -> Tuple[bool, str, Dict]:
        if item_id not in self.inventory:
            return False, "没有该道具", {}
        
        item = ITEM_DATABASE.get(item_id)
        if not item:
            return False, "未知道具", {}
        
        if not item.can_use():
            return False, "该道具无法使用", {}
        
        success, msg = self.remove_item(item_id, 1)
        if not success:
            return False, msg, {}
        
        effects_result = {}
        for effect in item.effects:
            effects_result[effect.effect_type] = effect.value
        
        return True, f"使用了 {item.name}", effects_result
    
    def has_item(self, item_id: str, amount: int = 1) -> bool:
        return self.inventory.get(item_id, 0) >= amount
    
    def get_item_count(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)
    
    def get_inventory_list(self) -> List[Dict]:
        result = []
        for item_id, count in self.inventory.items():
            item = ITEM_DATABASE.get(item_id)
            if item:
                result.append({
                    "item_id": item_id,
                    "name": item.name,
                    "icon": item.icon,
                    "type": item.item_type.value,
                    "rarity": item.rarity.value,
                    "count": count,
                    "description": item.description,
                    "can_use": item.can_use(),
                    "sell_price": item.sell_price
                })
        return result
    
    def sell_item(self, item_id: str, amount: int = 1) -> Tuple[bool, int, str]:
        if not self.has_item(item_id, amount):
            return False, 0, "道具数量不足"
        
        item = ITEM_DATABASE.get(item_id)
        if not item:
            return False, 0, "未知道具"
        
        total_price = item.sell_price * amount
        
        success, msg = self.remove_item(item_id, amount)
        if not success:
            return False, 0, msg
        
        return True, total_price, f"出售 {item.name} x{amount}，获得 {total_price} 金币"
    
    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        return RECIPES.get(recipe_id)
    
    def can_craft(self, recipe_id: str) -> Tuple[bool, str]:
        recipe = RECIPES.get(recipe_id)
        if not recipe:
            return False, "未知配方"
        
        for ingredient_id, required in recipe.ingredients.items():
            if not self.has_item(ingredient_id, required):
                item = ITEM_DATABASE.get(ingredient_id)
                item_name = item.name if item else ingredient_id
                return False, f"缺少材料: {item_name}"
        
        return True, "可以制作"
    
    def craft(self, recipe_id: str) -> Tuple[bool, str]:
        recipe = RECIPES.get(recipe_id)
        if not recipe:
            return False, "未知配方"
        
        can_craft, msg = self.can_craft(recipe_id)
        if not can_craft:
            return False, msg
        
        for ingredient_id, required in recipe.ingredients.items():
            self.remove_item(ingredient_id, required)
        
        result_item = ITEM_DATABASE.get(recipe.result)
        self.add_item(recipe.result, recipe.result_amount)
        
        result_name = result_item.name if result_item else recipe.result
        
        return True, f"成功制作 {result_name} x{recipe.result_amount}"
    
    def get_available_recipes(self) -> List[Dict]:
        result = []
        for recipe_id, recipe in RECIPES.items():
            can_craft, _ = self.can_craft(recipe_id)
            result_item = ITEM_DATABASE.get(recipe.result)
            
            result.append({
                "recipe_id": recipe_id,
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": recipe.ingredients,
                "result": recipe.result,
                "result_name": result_item.name if result_item else recipe.result,
                "result_icon": result_item.icon if result_item else "📦",
                "result_amount": recipe.result_amount,
                "required_level": recipe.required_level,
                "can_craft": can_craft
            })
        
        return result
    
    def get_total_value(self) -> int:
        total = 0
        for item_id, count in self.inventory.items():
            item = ITEM_DATABASE.get(item_id)
            if item:
                total += item.sell_price * count
        return total
    
    def get_save_data(self) -> Dict:
        return {
            "inventory": self.inventory.copy(),
            "max_slots": self.max_slots
        }
    
    def load_save_data(self, data: Dict):
        self.inventory = data.get("inventory", {})
        self.max_slots = data.get("max_slots", 30)
