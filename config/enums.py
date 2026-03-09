"""
游戏枚举统一配置文件
所有枚举类型定义在此文件中，避免重复定义
"""

from enum import Enum


# ==================== 季节 ====================

class Season(Enum):
    """季节枚举"""
    SPRING = "春天"
    SUMMER = "夏天"
    AUTUMN = "秋天"
    WINTER = "冬天"


# ==================== 天气 ====================

class Weather(Enum):
    """天气枚举"""
    SUNNY = "晴天"
    RAINY = "雨天"
    CLOUDY = "阴天"
    STORMY = "暴风雨"
    SNOWY = "下雪"
    WINDY = "大风"
    FOGGY = "大雾"
    DROUGHT = "干旱"
    HEATWAVE = "热浪"


# ==================== 作物类型 ====================

class CropType(Enum):
    """作物类型"""
    VEGETABLE = "蔬菜"
    FRUIT = "水果"
    GRAIN = "谷物"
    FLOWER = "花卉"


# ==================== 作物阶段 ====================

class CropStage(Enum):
    """作物生长阶段"""
    SEED = "种子"
    SPROUT = "幼苗"
    GROWING = "成长中"
    MATURE = "成熟"
    WITHERED = "枯萎"


# ==================== 作物品质 ====================

class CropQuality(Enum):
    """作物品质"""
    POOR = "劣质"
    NORMAL = "普通"
    GOOD = "优质"
    EXCELLENT = "极品"
    LEGENDARY = "传说"


# ==================== 物品分类 ====================

class ItemCategory(Enum):
    """物品分类"""
    SEED = "种子"
    CROP = "农作物"
    FOOD = "食物"
    TOOL = "工具"
    MATERIAL = "材料"
    GIFT = "礼物"
    MISC = "杂项"


# ==================== 建筑类型 ====================

class BuildingType(Enum):
    """建筑类型"""
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


# ==================== 配方分类 ====================

class RecipeCategory(Enum):
    """配方分类"""
    MAIN_DISH = "主菜"
    SOUP = "汤类"
    DESSERT = "甜点"
    DRINK = "饮品"
    SNACK = "小食"
    SPECIAL = "特色菜"


# ==================== 食物效果类型 ====================

class FoodEffectType(Enum):
    """食物效果类型"""
    HEALTH = "恢复生命"
    STAMINA = "恢复体力"
    BUFF_ATTACK = "攻击提升"
    BUFF_DEFENSE = "防御提升"
    BUFF_SPEED = "速度提升"
    BUFF_LUCK = "幸运提升"
    TEMP_REGEN = "持续恢复"


# ==================== 土壤质量 ====================

class SoilQuality(Enum):
    """土壤质量"""
    POOR = "贫瘠"
    NORMAL = "普通"
    GOOD = "肥沃"
    EXCELLENT = "极佳"


# ==================== 肥料类型 ====================

class FertilizerType(Enum):
    """肥料类型"""
    BASIC = "基础肥料"
    QUALITY = "优质肥料"
    SPEED = "速效肥料"
    ORGANIC = "有机肥料"


# ==================== 动物类型 ====================

class AnimalType(Enum):
    """动物类型"""
    CHICKEN = "鸡"
    DUCK = "鸭"
    COW = "牛"
    SHEEP = "羊"
    PIG = "猪"
    HORSE = "马"


# ==================== 宠物类型 ====================

class PetType(Enum):
    """宠物类型"""
    DOG = "狗"
    CAT = "猫"
    RABBIT = "兔子"
    BIRD = "鸟"


# ==================== 季节对应的天气概率 ====================

SEASON_WEATHER_PROBABILITIES = {
    Season.SPRING: {
        Weather.SUNNY: 0.40,
        Weather.RAINY: 0.35,
        Weather.CLOUDY: 0.20,
        Weather.STORMY: 0.05,
    },
    Season.SUMMER: {
        Weather.SUNNY: 0.60,
        Weather.RAINY: 0.15,
        Weather.CLOUDY: 0.20,
        Weather.STORMY: 0.05,
    },
    Season.AUTUMN: {
        Weather.SUNNY: 0.45,
        Weather.RAINY: 0.30,
        Weather.CLOUDY: 0.20,
        Weather.STORMY: 0.05,
    },
    Season.WINTER: {
        Weather.SUNNY: 0.30,
        Weather.RAINY: 0.20,
        Weather.CLOUDY: 0.45,
        Weather.STORMY: 0.05,
    },
}


# ==================== 辅助函数 ====================

def get_season_from_index(index: int) -> Season:
    """从索引获取季节"""
    seasons = [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]
    return seasons[index % 4]


def get_seasons_for_crop_growth() -> dict:
    """获取作物生长季节映射"""
    return {
        Season.SPRING: ["春天作物"],
        Season.SUMMER: ["夏天作物"],
        Season.AUTUMN: ["秋天作物"],
        Season.WINTER: ["冬天作物"],
    }
