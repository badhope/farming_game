"""
entities 包初始化
导出所有实体类
"""

from entities.player import Player
from entities.identity import Identity, IdentitySystem
from entities.city import City, CitySystem

__all__ = [
    "Player",
    "Identity",
    "IdentitySystem",
    "City",
    "CitySystem",
]
