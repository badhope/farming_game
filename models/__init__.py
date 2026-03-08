"""
models 包初始化文件
导出所有数据模型类，方便统一导入
"""

from models.crop import Crop
from models.plot import Plot
from models.player import Player, PlayerStats
from models.achievement import Achievement, AchievementManager
from models.story import StoryManager, StoryChapter, StoryNode, StoryStatus
from models.level_system import LevelSystem, LevelReward, UnlockableContent, UnlockType
from models.game_mode import GameModeManager, GameModeType, ModeConfig
from models.pet import Pet, PetManager, PetType, PetMood, PetStats
from models.item import Item, ItemManager, ItemType, ItemRarity, Recipe
from models.exploration import ExplorationManager, ExplorationArea, RandomEvent, AreaType
from models.home import HomeManager, Home, Room, Furniture, RoomType
from models.animal import Animal, AnimalManager, AnimalType, AnimalMood, AnimalProduct
from models.stamina import StaminaSystem, ActionType, StaminaConfig, ActionCost
from models.pixel_map import MapType, TileType, PixelArtAssets, MapGenerator, MapManager, MapArea, Tile
from models.soil import SoilQuality, FertilizerType, Fertilizer, SoilState, FertilizerRegistry, SoilManager
from models.weather import WeatherType, WeatherEffect, WeatherAgricultureSystem, Season
from models.color_system import ColorCustomizationSystem, ColorRegistry, ColorPalette, ColorCategory, CustomColor
from models.random_events import RandomEventManager, RandomEvent, RandomEventType, EventPriority

from models.character_system import (
    EnhancedCharacterProfile, EnhancedCharacterManager, CharacterRegistry,
    VisualAppearance, Backstory, Personality, PersonalityTrait,
    DialogueTree, DialogueNode, DialogueChoice, DialogueCondition,
    ShopInventory, ShopItem, NPCArchetype
)
from models.world_system import (
    WorldManager, WorldMap, WeatherSystem, DayNightCycle,
    Biome, BiomeType, BiomeRegistry, WorldTile, WorldRegion,
    PointOfInterest, DynamicWeather, TimeOfDay, MoonPhase, WeatherIntensity
)
from models.farming_system import (
    FarmingManager, FarmField, PlantedCrop, CropInfo, 
    CropRegistry, CropStage, CropQuality
)
from models.building_system import (
    BuildingManager, BuildingInfo, PlacedBuilding, 
    BuildingRegistry, BuildingType, BuildingRequirement
)
from models.cooking_system import (
    CookingManager, Recipe, CookedFood, FoodEffect, 
    RecipeRegistry, RecipeCategory, FoodEffectType
)
from models.inventory_system_simple import (
    SimpleInventory, ItemInstance, ItemFactory, ItemTemplate,
    InventorySlot, StorageContainer, ItemCategory
)
from models.interaction_system import (
    InteractionSystem, RelationshipManager, ReputationManager, QuestManager,
    CharacterRelationship, RelationshipType, RelationshipEvent,
    FactionReputation, ReputationLevel, FactionType,
    Quest, QuestObjective, QuestReward, QuestType, QuestStatus, QuestGenerator,
    InteractionType
)


__all__ = [
    "Crop",
    "Plot",
    "Player",
    "PlayerStats",
    "Achievement",
    "AchievementManager",
    "StoryManager",
    "StoryChapter",
    "StoryNode",
    "StoryStatus",
    "LevelSystem",
    "LevelReward",
    "UnlockableContent",
    "UnlockType",
    "GameModeManager",
    "GameModeType",
    "ModeConfig",
    "Pet",
    "PetManager",
    "PetType",
    "PetMood",
    "PetStats",
    "Item",
    "ItemManager",
    "ItemType",
    "ItemRarity",
    "Recipe",
    "ExplorationManager",
    "ExplorationArea",
    "RandomEvent",
    "AreaType",
    "HomeManager",
    "Home",
    "Room",
    "Furniture",
    "RoomType",
    "Animal",
    "AnimalManager",
    "AnimalType",
    "AnimalMood",
    "AnimalProduct",
    "StaminaSystem",
    "ActionType",
    "StaminaConfig",
    "ActionCost",
    "MapType",
    "TileType",
    "PixelArtAssets",
    "MapGenerator",
    "MapManager",
    "MapArea",
    "Tile",
    "SoilQuality",
    "FertilizerType",
    "Fertilizer",
    "SoilState",
    "FertilizerRegistry",
    "SoilManager",
    "WeatherType",
    "WeatherEffect",
    "WeatherAgricultureSystem",
    "Season",
    "ColorCustomizationSystem",
    "ColorRegistry",
    "ColorPalette",
    "ColorCategory",
    "CustomColor",
    "RandomEventManager",
    "RandomEvent",
    "RandomEventType",
    "EventPriority",
    
    "EnhancedCharacterProfile",
    "EnhancedCharacterManager",
    "CharacterRegistry",
    "VisualAppearance",
    "Backstory",
    "Personality",
    "PersonalityTrait",
    "DialogueTree",
    "DialogueNode",
    "DialogueChoice",
    "DialogueCondition",
    "ShopInventory",
    "ShopItem",
    "NPCArchetype",
    
    "WorldManager",
    "WorldMap",
    "WeatherSystem",
    "DayNightCycle",
    "Biome",
    "BiomeType",
    "BiomeRegistry",
    "WorldTile",
    "WorldRegion",
    "PointOfInterest",
    "DynamicWeather",
    "TimeOfDay",
    "MoonPhase",
    "WeatherIntensity",
    
    "GameplayManager",
    "FarmingManager",
    "BuildingManager",
    "CookingManager",
    "FarmField",
    "PlantedCrop",
    "CropInfo",
    "CropStage",
    "CropQuality",
    "PlacedBuilding",
    "BuildingInfo",
    "BuildingType",
    "BuildingRegistry",
    "CookedFood",
    "FoodEffect",
    "FoodEffectType",
    "RecipeCategory",
    "RecipeRegistry",
    "CropRegistry",
    
    "SimpleInventory",
    "ItemInstance",
    "ItemFactory",
    "ItemTemplate",
    "InventorySlot",
    "StorageContainer",
    "ItemCategory",
    
    "InteractionSystem",
    "RelationshipManager",
    "ReputationManager",
    "QuestManager",
    "CharacterRelationship",
    "RelationshipType",
    "RelationshipEvent",
    "FactionReputation",
    "ReputationLevel",
    "Quest",
    "QuestObjective",
    "QuestReward",
    "QuestType",
    "QuestStatus",
    "QuestGenerator",
    "InteractionType",
]
