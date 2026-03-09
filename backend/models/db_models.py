"""
数据库模型定义
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database.db_config import Base


class PlayerModel(Base):
    """玩家数据表"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="农夫")
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    gold = Column(Integer, default=500)
    stamina = Column(Integer, default=100)
    max_stamina = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联表
    inventory = relationship("InventoryModel", back_populates="player")
    farm_fields = relationship("FarmFieldModel", back_populates="player")


class InventoryModel(Base):
    """背包物品表"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    item_id = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    
    # 关联表
    player = relationship("PlayerModel", back_populates="inventory")


class FarmFieldModel(Base):
    """农田表"""
    __tablename__ = "farm_fields"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    has_crop = Column(Integer, default=0)  # 0 or 1
    crop_type = Column(String, nullable=True)
    growth_stage = Column(Integer, default=0)
    growth_progress = Column(Integer, default=0)
    needs_water = Column(Integer, default=0)  # 0 or 1
    last_watered = Column(DateTime, nullable=True)
    
    # 关联表
    player = relationship("PlayerModel", back_populates="farm_fields")


class GameSaveModel(Base):
    """游戏存档表"""
    __tablename__ = "game_saves"
    
    id = Column(Integer, primary_key=True, index=True)
    save_name = Column(String, nullable=False, unique=True)
    player_name = Column(String, nullable=False)
    season = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    game_data = Column(JSON, nullable=False)  # 完整游戏数据 JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AchievementModel(Base):
    """成就表"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    achievement_id = Column(String, nullable=False)
    achievement_name = Column(String, nullable=False)
    unlocked = Column(Integer, default=0)  # 0 or 1
    unlocked_at = Column(DateTime, nullable=True)
    progress = Column(Integer, default=0)
    target = Column(Integer, default=0)
