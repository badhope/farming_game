"""
core 包初始化文件
导出核心系统模块，方便统一导入
"""

from core.time_system import TimeSystem
from core.economy import EconomySystem, TransactionResult
from core.game_manager import GameManager, DayResult


# 导出的类列表
__all__ = [
    "TimeSystem",
    "EconomySystem",
    "TransactionResult",
    "GameManager",
    "DayResult",
]
