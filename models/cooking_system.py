"""
烹饪系统模块
负责食物烹饪、配方管理和食物效果
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random
from config.enums import RecipeCategory, FoodEffectType


@dataclass
class FoodEffect:
    """食物效果"""
    effect_type: FoodEffectType
    value: int
    duration: int = 0  # 持续回合数，0 表示立即生效
    
    def apply(self, target_stats: Dict) -> Dict:
        """应用效果到目标"""
        changes = {}
        
        if self.effect_type == FoodEffectType.HEALTH:
            changes['health'] = self.value
        elif self.effect_type == FoodEffectType.STAMINA:
            changes['stamina'] = self.value
        elif self.effect_type == FoodEffectType.BUFF_ATTACK:
            changes['attack_buff'] = self.value
        elif self.effect_type == FoodEffectType.BUFF_DEFENSE:
            changes['defense_buff'] = self.value
        elif self.effect_type == FoodEffectType.BUFF_SPEED:
            changes['speed_buff'] = self.value
        elif self.effect_type == FoodEffectType.BUFF_LUCK:
            changes['luck_buff'] = self.value
        
        return changes
    
    def get_display_text(self) -> str:
        """获取效果显示文本"""
        type_names = {
            FoodEffectType.HEALTH: "生命",
            FoodEffectType.STAMINA: "体力",
            FoodEffectType.BUFF_ATTACK: "攻击",
            FoodEffectType.BUFF_DEFENSE: "防御",
            FoodEffectType.BUFF_SPEED: "速度",
            FoodEffectType.BUFF_LUCK: "幸运",
        }
        
        type_name = type_names.get(self.effect_type, "未知")
        
        if self.duration > 0:
            return f"{type_name}+{self.value} ({self.duration}回合)"
        else:
            return f"{type_name}+{self.value}"


@dataclass
class Recipe:
    """烹饪配方"""
    recipe_id: str
    name: str
    description: str
    icon: str
    
    category: RecipeCategory
    
    ingredients: Dict[str, int] = field(default_factory=dict)
    cooking_time: int = 5  # 烹饪时间（回合）
    
    effects: List[FoodEffect] = field(default_factory=list)
    
    base_quality: int = 1
    max_quality: int = 5
    
    unlock_requirement: Optional[str] = None  # 解锁要求
    difficulty: int = 1  # 难度 1-5
    
    @classmethod
    def from_config(cls, recipe_id: str, config: dict) -> 'Recipe':
        """从配置创建配方"""
        effects = []
        for effect_config in config.get('effects', []):
            effect = FoodEffect(
                effect_type=FoodEffectType(effect_config.get('type', 'STAMINA')),
                value=effect_config.get('value', 0),
                duration=effect_config.get('duration', 0),
            )
            effects.append(effect)
        
        return cls(
            recipe_id=recipe_id,
            name=config.get('name', recipe_id),
            description=config.get('description', ''),
            icon=config.get('emoji', '🍳'),
            category=RecipeCategory(config.get('category', 'MAIN_DISH')),
            ingredients=config.get('ingredients', {}),
            cooking_time=config.get('cooking_time', 5),
            effects=effects,
            base_quality=config.get('base_quality', 1),
            difficulty=config.get('difficulty', 1),
        )


@dataclass
class CookedFood:
    """烹饪好的食物"""
    recipe: Recipe
    quality: int = 1
    cooked_by: str = ""
    cooked_day: int = 0
    
    freshness: int = 100  # 新鲜度
    max_freshness: int = 100
    
    def get_effect_multiplier(self) -> float:
        """获取效果倍率（基于品质和新鲜度）"""
        quality_mult = 0.5 + (self.quality / self.recipe.max_quality) * 0.5
        freshness_mult = self.freshness / 100.0
        return quality_mult * freshness_mult
    
    def apply_effects(self, target_stats: Dict) -> Dict:
        """应用食物效果"""
        multiplier = self.get_effect_multiplier()
        changes = {}
        
        for effect in self.recipe.effects:
            effect_changes = effect.apply(target_stats)
            for stat, value in effect_changes.items():
                changes[stat] = changes.get(stat, 0) + int(value * multiplier)
        
        # 消耗新鲜度
        self.freshness = max(0, self.freshness - 20)
        
        return changes
    
    def is_fresh(self) -> bool:
        """是否新鲜"""
        return self.freshness > 50
    
    def get_display_name(self) -> str:
        """获取显示名称"""
        quality_prefix = {
            1: "",
            2: "优质 ",
            3: "美味 ",
            4: "极品 ",
            5: "传说 ",
        }
        prefix = quality_prefix.get(self.quality, "")
        return f"{prefix}{self.recipe.name}"


class RecipeRegistry:
    """配方注册表"""
    
    _recipes: Dict[str, Recipe] = {}
    _initialized: bool = False
    
    # 默认配方
    DEFAULT_RECIPES = {
        "fried_egg": {
            "name": "煎蛋",
            "description": "简单的煎蛋",
            "emoji": "🍳",
            "category": "MAIN_DISH",
            "ingredients": {"egg": 1},
            "cooking_time": 3,
            "effects": [
                {"type": "STAMINA", "value": 20, "duration": 0}
            ],
            "difficulty": 1,
        },
        "salad": {
            "name": "沙拉",
            "description": "新鲜蔬菜沙拉",
            "emoji": "🥗",
            "category": "MAIN_DISH",
            "ingredients": {"tomato": 1, "cabbage": 1},
            "cooking_time": 2,
            "effects": [
                {"type": "HEALTH", "value": 15, "duration": 0},
                {"type": "STAMINA", "value": 10, "duration": 0}
            ],
            "difficulty": 1,
        },
        "soup": {
            "name": "蔬菜汤",
            "description": "温暖的蔬菜汤",
            "emoji": "🍲",
            "category": "SOUP",
            "ingredients": {"carrot": 1, "potato": 1},
            "cooking_time": 5,
            "effects": [
                {"type": "HEALTH", "value": 30, "duration": 0},
                {"type": "STAMINA", "value": 20, "duration": 0}
            ],
            "difficulty": 2,
        },
        "cake": {
            "name": "蛋糕",
            "description": "甜美的蛋糕",
            "emoji": "🎂",
            "category": "DESSERT",
            "ingredients": {"wheat": 2, "egg": 1},
            "cooking_time": 10,
            "effects": [
                {"type": "STAMINA", "value": 50, "duration": 0},
                {"type": "BUFF_LUCK", "value": 5, "duration": 3}
            ],
            "difficulty": 3,
        },
        "juice": {
            "name": "果汁",
            "description": "新鲜果汁",
            "emoji": "🧃",
            "category": "DRINK",
            "ingredients": {"watermelon": 1},
            "cooking_time": 2,
            "effects": [
                {"type": "STAMINA", "value": 15, "duration": 0}
            ],
            "difficulty": 1,
        },
    }
    
    @classmethod
    def _init_recipes(cls):
        """初始化配方注册表"""
        if cls._initialized:
            return
        
        # 注册默认配方
        for recipe_id, config in cls.DEFAULT_RECIPES.items():
            recipe = Recipe.from_config(recipe_id, config)
            cls._recipes[recipe_id] = recipe
        
        cls._initialized = True
    
    @classmethod
    def get_recipe(cls, recipe_id: str) -> Optional[Recipe]:
        """获取配方"""
        cls._init_recipes()
        return cls._recipes.get(recipe_id)
    
    @classmethod
    def get_all_recipes(cls) -> Dict[str, Recipe]:
        """获取所有配方"""
        cls._init_recipes()
        return cls._recipes.copy()
    
    @classmethod
    def get_recipes_by_category(cls, category: RecipeCategory) -> List[Recipe]:
        """按分类获取配方"""
        cls._init_recipes()
        return [
            r for r in cls._recipes.values()
            if r.category == category
        ]
    
    @classmethod
    def get_cookable_recipes(cls, inventory: Dict[str, int]) -> List[Recipe]:
        """获取可以烹饪的配方（基于背包物品）"""
        cls._init_recipes()
        cookable = []
        
        for recipe in cls._recipes.values():
            can_cook = True
            for ingredient, amount in recipe.ingredients.items():
                if inventory.get(ingredient, 0) < amount:
                    can_cook = False
                    break
            
            if can_cook:
                cookable.append(recipe)
        
        return cookable


class CookingManager:
    """烹饪管理器"""
    
    def __init__(self):
        self.cooked_foods: List[CookedFood] = []
        self.total_foods_cooked = 0
        self.perfect_dishes = 0  # 完美料理数量
        self.burnt_dishes = 0  # 失败料理数量
    
    def can_cook(self, recipe: Recipe, inventory: Dict[str, int]) -> Tuple[bool, str]:
        """检查是否可以烹饪"""
        for ingredient, amount in recipe.ingredients.items():
            if inventory.get(ingredient, 0) < amount:
                return False, f"缺少材料：{ingredient}"
        return True, "可以烹饪"
    
    def consume_ingredients(self, recipe: Recipe, inventory: Dict[str, int]) -> Dict[str, int]:
        """消耗材料"""
        new_inventory = inventory.copy()
        for ingredient, amount in recipe.ingredients.items():
            new_inventory[ingredient] = new_inventory.get(ingredient, 0) - amount
        return new_inventory
    
    def cook(self, recipe: Recipe, inventory: Dict[str, int], 
             cook_level: int = 1) -> Tuple[bool, Optional[CookedFood], str]:
        """
        烹饪食物
        返回：(是否成功，烹饪好的食物，消息)
        """
        can_cook, message = self.can_cook(recipe, inventory)
        if not can_cook:
            return False, None, message
        
        # 消耗材料
        new_inventory = self.consume_ingredients(recipe, inventory)
        
        # 计算品质（基于厨师等级和随机因素）
        base_quality = recipe.base_quality
        skill_bonus = min(3, cook_level // 2)
        random_bonus = random.randint(0, 2)
        
        final_quality = min(recipe.max_quality, base_quality + skill_bonus + random_bonus)
        
        # 判定是否失败（难度越高，失败率越高）
        fail_chance = 0.1 * recipe.difficulty
        if random.random() < fail_chance:
            self.burnt_dishes += 1
            return False, None, "烹饪失败了！"
        
        # 创建烹饪好的食物
        food = CookedFood(
            recipe=recipe,
            quality=final_quality,
            cooked_day=0,
        )
        
        self.cooked_foods.append(food)
        self.total_foods_cooked += 1
        
        # 记录完美料理
        if final_quality == recipe.max_quality:
            self.perfect_dishes += 1
        
        success = True
        message = f"烹饪了{food.get_display_name()}！"
        
        return success, food, message
    
    def eat(self, food: CookedFood, target_stats: Dict) -> Dict:
        """食用食物"""
        effects = food.apply_effects(target_stats)
        
        # 从列表中移除
        if food in self.cooked_foods:
            self.cooked_foods.remove(food)
        
        return effects
    
    def get_foods_by_quality(self, quality: int) -> List[CookedFood]:
        """按品质获取食物"""
        return [f for f in self.cooked_foods if f.quality == quality]
    
    def get_fresh_foods(self) -> List[CookedFood]:
        """获取新鲜的食物"""
        return [f for f in self.cooked_foods if f.is_fresh()]
    
    def get_expired_foods(self) -> List[CookedFood]:
        """获取过期的食物"""
        return [f for f in self.cooked_foods if f.freshness <= 0]
    
    def discard_food(self, food: CookedFood):
        """丢弃食物"""
        if food in self.cooked_foods:
            self.cooked_foods.remove(food)
    
    def get_cooking_stats(self) -> Dict:
        """获取烹饪统计"""
        return {
            "total_cooked": self.total_foods_cooked,
            "perfect_dishes": self.perfect_dishes,
            "burnt_dishes": self.burnt_dishes,
            "success_rate": (
                self.total_foods_cooked / 
                (self.total_foods_cooked + self.burnt_dishes)
                if (self.total_foods_cooked + self.burnt_dishes) > 0 else 0
            ),
        }
