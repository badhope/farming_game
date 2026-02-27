"""
游戏配置文件
包含所有游戏常量、作物数据、成就数据等
"""

from enum import Enum
from typing import List


# ==================== 枚举定义 ====================

class Season(Enum):
    """季节枚举"""
    SPRING = "春天"
    SUMMER = "夏天"
    AUTUMN = "秋天"
    WINTER = "冬天"


class Weather(Enum):
    """天气枚举"""
    SUNNY = "☀️ 晴天"
    RAINY = "🌧️ 雨天"
    CLOUDY = "☁️ 阴天"
    STORMY = "⛈️ 暴风雨"


class CropType(Enum):
    """作物类型"""
    VEGETABLE = "蔬菜"
    FRUIT = "水果"
    GRAIN = "谷物"
    FLOWER = "花卉"


# ==================== 游戏常量 ====================

class GameConfig:
    """游戏配置常量"""
    
    # 时间设置
    DAYS_PER_SEASON = 28          # 每季天数
    SEASONS_PER_YEAR = 4          # 每年季节数
    
    # 初始设置
    INITIAL_MONEY = 500           # 初始金币
    INITIAL_PLOT_SIZE = 3         # 初始田地大小 (3x3)
    MAX_UPGRADE_LEVEL = 4         # 最大升级等级
    
    # 升级费用公式: (当前等级 + 1) * UPGRADE_COST_MULTIPLIER
    UPGRADE_COST_MULTIPLIER = 2000
    
    # 天气概率权重 [晴天, 雨天, 阴天, 暴风雨]
    WEATHER_WEIGHTS = {
        Season.SPRING: [0.40, 0.35, 0.20, 0.05],
        Season.SUMMER: [0.60, 0.15, 0.20, 0.05],
        Season.AUTUMN: [0.45, 0.30, 0.20, 0.05],
        Season.WINTER: [0.30, 0.20, 0.45, 0.05],
    }
    
    # 暴风雨损坏作物概率
    STORM_DAMAGE_CHANCE = 0.30
    
    # 存档文件名
    SAVE_FILENAME = "save.json"
    
    # 自动保存间隔（天数）
    AUTO_SAVE_INTERVAL = 7


# ==================== 作物数据 ====================

class CropData:
    """作物数据配置
    
    数据结构：
        name: 作物名称
        seed_price: 种子价格
        sell_price: 出售价格
        grow_days: 生长天数
        seasons: 适宜季节列表
        water_needed: 每天需浇水次数
        emoji: 显示图标
        crop_type: 作物类型
    """
    
    # 作物配置字典
    CROPS = {
        # ========== 蔬菜类 ==========
        "土豆": {
            "seed_price": 50,
            "sell_price": 120,
            "grow_days": 3,
            "seasons": [Season.SPRING, Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🥔",
            "crop_type": CropType.VEGETABLE,
            "description": "常见蔬菜，生长周期短，适合新手。"
        },
        "胡萝卜": {
            "seed_price": 40,
            "sell_price": 90,
            "grow_days": 2,
            "seasons": [Season.SPRING, Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🥕",
            "crop_type": CropType.VEGETABLE,
            "description": "生长最快的作物，收益稳定。"
        },
        "番茄": {
            "seed_price": 80,
            "sell_price": 200,
            "grow_days": 5,
            "seasons": [Season.SUMMER],
            "water_needed": 2,
            "emoji": "🍅",
            "crop_type": CropType.VEGETABLE,
            "description": "夏季特产，需水量大，收益可观。"
        },
        "玉米": {
            "seed_price": 100,
            "sell_price": 250,
            "grow_days": 6,
            "seasons": [Season.SUMMER, Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🌽",
            "crop_type": CropType.VEGETABLE,
            "description": "适应性强，可在夏秋两季种植。"
        },
        "南瓜": {
            "seed_price": 120,
            "sell_price": 320,
            "grow_days": 7,
            "seasons": [Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🎃",
            "crop_type": CropType.VEGETABLE,
            "description": "秋季代表作物，生长周期较长。"
        },
        "茄子": {
            "seed_price": 70,
            "sell_price": 180,
            "grow_days": 4,
            "seasons": [Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🍆",
            "crop_type": CropType.VEGETABLE,
            "description": "秋季蔬菜，性价比不错。"
        },
        "白菜": {
            "seed_price": 30,
            "sell_price": 70,
            "grow_days": 3,
            "seasons": [Season.SPRING, Season.AUTUMN, Season.WINTER],
            "water_needed": 1,
            "emoji": "🥬",
            "crop_type": CropType.VEGETABLE,
            "description": "适应性强，三季可种，价格便宜。"
        },
        
        # ========== 水果类 ==========
        "西瓜": {
            "seed_price": 150,
            "sell_price": 400,
            "grow_days": 8,
            "seasons": [Season.SUMMER],
            "water_needed": 2,
            "emoji": "🍉",
            "crop_type": CropType.FRUIT,
            "description": "夏季高价值水果，需水量大。"
        },
        "草莓": {
            "seed_price": 200,
            "sell_price": 500,
            "grow_days": 10,
            "seasons": [Season.SPRING],
            "water_needed": 2,
            "emoji": "🍓",
            "crop_type": CropType.FRUIT,
            "description": "春季珍品，价格昂贵，值得投资。"
        },
        "葡萄": {
            "seed_price": 300,
            "sell_price": 800,
            "grow_days": 14,
            "seasons": [Season.SUMMER, Season.AUTUMN],
            "water_needed": 2,
            "emoji": "🍇",
            "crop_type": CropType.FRUIT,
            "description": "高价值水果，生长周期长，收益最高。"
        },
        
        # ========== 谷物类 ==========
        "小麦": {
            "seed_price": 20,
            "sell_price": 50,
            "grow_days": 4,
            "seasons": [Season.SPRING, Season.SUMMER, Season.AUTUMN],
            "water_needed": 1,
            "emoji": "🌾",
            "crop_type": CropType.GRAIN,
            "description": "最便宜的作物，三季可种，适合大规模种植。"
        },
        
        # ========== 花卉类 ==========
        "向日葵": {
            "seed_price": 250,
            "sell_price": 600,
            "grow_days": 12,
            "seasons": [Season.SUMMER],
            "water_needed": 1,
            "emoji": "🌻",
            "crop_type": CropType.FLOWER,
            "description": "夏季花卉，高价值，装饰农场。"
        },
    }
    
    @classmethod
    def get_crop_names(cls) -> List[str]:
        """获取所有作物名称列表"""
        return list(cls.CROPS.keys())
    
    @classmethod
    def get_crop_by_season(cls, season: Season) -> List[str]:
        """获取指定季节可种植的作物"""
        return [
            name for name, data in cls.CROPS.items()
            if season in data["seasons"]
        ]


# ==================== 成就数据 ====================

class AchievementData:
    """成就数据配置"""
    
    ACHIEVEMENTS = {
        "first_harvest": {
            "name": "🌾 初次收获",
            "description": "收获第一个作物",
            "condition": "harvest_count >= 1",
            "reward_text": "开启你的农场之旅！"
        },
        "farmer_100": {
            "name": "👨‍🌾 小农夫",
            "description": "累计收获100个作物",
            "condition": "harvest_count >= 100",
            "reward_text": "你已经入门了！"
        },
        "farmer_500": {
            "name": "🧑‍🌾 经验农夫",
            "description": "累计收获500个作物",
            "condition": "harvest_count >= 500",
            "reward_text": "经验丰富的农夫！"
        },
        "farmer_1000": {
            "name": "👨‍🌾 农场大师",
            "description": "累计收获1000个作物",
            "condition": "harvest_count >= 1000",
            "reward_text": "传奇农夫诞生！"
        },
        "millionaire": {
            "name": "💰 百万富翁",
            "description": "累计赚取1,000,000金币",
            "condition": "total_earnings >= 1000000",
            "reward_text": "财富自由达成！"
        },
        "all_crops": {
            "name": "🌱 作物收藏家",
            "description": "种植过所有种类的作物（12种）",
            "condition": "crops_grown_count >= 12",
            "reward_text": "全作物收藏达成！"
        },
        "survive_year": {
            "name": "📅 度过四季",
            "description": "经历过完整的四个季节",
            "condition": "years_passed >= 1",
            "reward_text": "四季轮回，生生不息！"
        },
        "storm_survivor": {
            "name": "⛈️ 暴风雨幸存者",
            "description": "在暴风雨中保住所有作物",
            "condition": "storm_survived == True",
            "reward_text": "风雨无阻！"
        },
        "max_farm": {
            "name": "🏘️ 农场大亨",
            "description": "将农场升级到最高等级",
            "condition": "upgrade_level >= 4",
            "reward_text": "顶级农场达成！"
        },
        "rich_harvest": {
            "name": "🎃 丰收之王",
            "description": "单日收获10个以上作物",
            "condition": "single_day_harvest >= 10",
            "reward_text": "大丰收！"
        },
    }
    
    @classmethod
    def get_achievement_ids(cls) -> List[str]:
        """获取所有成就ID列表"""
        return list(cls.ACHIEVEMENTS.keys())


# ==================== 显示配置 ====================

class DisplayConfig:
    """显示相关配置"""
    
    # 分隔线宽度
    LINE_WIDTH = 60
    
    # 分隔线字符
    LINE_CHAR = "="
    SUB_LINE_CHAR = "-"
    
    # 生长阶段图标
    GROWTH_STAGES = {
        0: "🔘",  # 种子
        1: "🌱",  # 发芽
        2: "🌿",  # 生长中
        3: "🌳",  # 接近成熟
        4: "✨",  # 成熟可收获
    }
    
    # 地块图标
    EMPTY_PLOT = "⬜"
    WATERED_ICON = "💧"
    MATURE_ICON = "✨"
