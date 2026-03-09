"""
models 包初始化文件
导出核心数据模型类，为 Web API 做准备
"""

# 核心农场模型
from models.crop import Crop
from models.plot import Plot
from models.player import Player, PlayerStats

# 农场经营系统
from models.farming_system import (
    FarmingManager, FarmField, PlantedCrop, CropInfo, 
    CropRegistry, CropStage, CropQuality
)

# 天气和时间系统
from models.weather import Weather, WeatherEffect, WeatherAgricultureSystem, Season

# 物品和背包系统
from models.item import Item, ItemManager, ItemType, ItemRarity
from models.inventory_system_simple import (
    SimpleInventory, ItemInstance, ItemFactory, ItemTemplate,
    InventorySlot, StorageContainer, ItemCategory
)

# 成就和等级系统
from models.achievement import Achievement, AchievementManager
from models.level_system import LevelSystem

# 建筑系统
from models.building_system import (
    BuildingManager, BuildingInfo, PlacedBuilding, 
    BuildingRegistry, BuildingType, BuildingRequirement
)

# 家园系统
from models.home import HomeManager, Home, Room, Furniture, RoomType

# 动物系统
from models.animal import Animal, AnimalManager, AnimalType, AnimalMood, AnimalProduct

# 体力系统
from models.stamina import StaminaSystem, ActionType, StaminaConfig, ActionCost

# 土壤系统
from models.soil import SoilQuality, FertilizerType, Fertilizer, SoilState, FertilizerRegistry, SoilManager

# 随机事件
from models.random_events import RandomEventManager, RandomEvent, RandomEventType, EventPriority

# 交互系统（NPC、任务、声望）
from models.interaction_system import (
    InteractionSystem, RelationshipManager, ReputationManager, QuestManager,
    CharacterRelationship, RelationshipType, RelationshipEvent,
    FactionReputation, ReputationLevel, FactionType,
    Quest, QuestObjective, QuestReward, QuestType, QuestStatus, QuestGenerator,
    InteractionType
)


__all__ = [
    # 核心模型
    "Crop",
    "Plot",
    "Player",
    "PlayerStats",
    
    # 农场经营
    "FarmingManager",
    "FarmField",
    "PlantedCrop",
    "CropInfo",
    "CropRegistry",
    "CropStage",
    "CropQuality",
    
    # 天气系统
    "Weather",
    "WeatherEffect",
    "WeatherAgricultureSystem",
    "Season",
    
    # 物品系统
    "Item",
    "ItemManager",
    "ItemType",
    "ItemRarity",
    "SimpleInventory",
    "ItemInstance",
    "ItemFactory",
    "ItemTemplate",
    "InventorySlot",
    "StorageContainer",
    "ItemCategory",
    
    # 成就和等级
    "Achievement",
    "AchievementManager",
    "LevelSystem",
    
    # 建筑系统
    "BuildingManager",
    "BuildingInfo",
    "PlacedBuilding",
    "BuildingRegistry",
    "BuildingType",
    "BuildingRequirement",
    
    # 家园系统
    "HomeManager",
    "Home",
    "Room",
    "Furniture",
    "RoomType",
    
    # 动物系统
    "Animal",
    "AnimalManager",
    "AnimalType",
    "AnimalMood",
    "AnimalProduct",
    
    # 体力系统
    "StaminaSystem",
    "ActionType",
    "StaminaConfig",
    "ActionCost",
    
    # 土壤系统
    "SoilQuality",
    "FertilizerType",
    "Fertilizer",
    "SoilState",
    "FertilizerRegistry",
    "SoilManager",
    
    # 随机事件
    "RandomEventManager",
    "RandomEvent",
    "RandomEventType",
    "EventPriority",
    
    # 交互系统
    "InteractionSystem",
    "RelationshipManager",
    "ReputationManager",
    "QuestManager",
    "CharacterRelationship",
    "RelationshipType",
    "RelationshipEvent",
    "FactionReputation",
    "ReputationLevel",
    "FactionType",
    "Quest",
    "QuestObjective",
    "QuestReward",
    "QuestType",
    "QuestStatus",
    "QuestGenerator",
    "InteractionType",
]
