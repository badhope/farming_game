from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SyncStatus(str, Enum):
    SYNCED = "synced"
    PENDING = "pending"
    CONFLICT = "conflict"


class Platform(str, Enum):
    WEB = "web"
    DESKTOP = "desktop"
    MOBILE = "mobile"


class PlayerData(BaseModel):
    level: int = 1
    experience: int = 0
    gold: int = 1000
    energy: int = 100
    max_energy: int = 100


class FarmPlot(BaseModel):
    id: int
    crop_id: Optional[str] = None
    planted_at: Optional[str] = None
    water_level: int = 0
    is_mature: bool = False


class FarmData(BaseModel):
    plots: List[FarmPlot] = []
    unlock_count: int = 6


class InventoryItem(BaseModel):
    item_id: str
    quantity: int = 1


class InventoryData(BaseModel):
    items: Dict[str, int] = {}
    seeds: Dict[str, int] = {}


class AchievementProgress(BaseModel):
    achievement_id: str
    unlocked_at: Optional[str] = None
    progress: int = 0


class StatisticsData(BaseModel):
    total_harvests: int = 0
    total_earnings: int = 0
    total_playtime: int = 0
    crops_planted: int = 0
    crops_harvested: int = 0
    items_purchased: int = 0


class GameSave(BaseModel):
    user_id: str
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    platform: Platform = Platform.WEB
    player: PlayerData = Field(default_factory=PlayerData)
    farm: FarmData = Field(default_factory=FarmData)
    inventory: InventoryData = Field(default_factory=InventoryData)
    achievements: List[str] = []
    achievement_progress: List[AchievementProgress] = []
    statistics: StatisticsData = Field(default_factory=StatisticsData)
    synced_at: Optional[datetime] = None


class SyncRequest(BaseModel):
    client_data: GameSave
    last_sync_timestamp: Optional[datetime] = None


class SyncResponse(BaseModel):
    server_data: GameSave
    sync_status: SyncStatus
    conflicts: List[str] = []
    message: str


class SyncStatusResponse(BaseModel):
    user_id: str
    last_sync: Optional[datetime] = None
    pending_changes: int = 0
    status: SyncStatus


class CloudSaveResponse(BaseModel):
    saves: List[GameSave]
    total: int
