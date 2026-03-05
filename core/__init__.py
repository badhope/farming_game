"""
core 包初始化文件
导出核心系统模块，方便统一导入
"""

from core.time_system import TimeSystem
from core.economy import EconomySystem, TransactionResult
from core.game_manager import GameManager, DayResult
from core.api_manager import APIManager, APIConfig, APIType, MockAPIResponse
from core.renderer import (
    Renderer, Color, Vector2, Particle, ParticleEmitter, ParticleType,
    LightSource, AnimationSystem, PostProcessor, ShaderEffect,
    GrayscaleEffect, WaveEffect, GlowEffect
)
from core.dynamics import (
    ProbabilityEngine, DamageCalculator, GrowthCalculator, 
    EconomyCalculator, BalanceSystem, StatSystem, DynamicStat, StatModifier
)
from core.game_systems import IntegratedGameSystem, GameContext, PlayerState, WorldState, GamePhase


__all__ = [
    "TimeSystem",
    "EconomySystem",
    "TransactionResult",
    "GameManager",
    "DayResult",
    "APIManager",
    "APIConfig",
    "APIType",
    "MockAPIResponse",
    "Renderer",
    "Color",
    "Vector2",
    "Particle",
    "ParticleEmitter",
    "ParticleType",
    "LightSource",
    "AnimationSystem",
    "PostProcessor",
    "ShaderEffect",
    "GrayscaleEffect",
    "WaveEffect",
    "GlowEffect",
    "ProbabilityEngine",
    "DamageCalculator",
    "GrowthCalculator",
    "EconomyCalculator",
    "BalanceSystem",
    "StatSystem",
    "DynamicStat",
    "StatModifier",
    "IntegratedGameSystem",
    "GameContext",
    "PlayerState",
    "WorldState",
    "GamePhase",
]
