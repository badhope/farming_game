"""
游戏数据配置加载器
从 JSON 文件加载作物、成就等配置数据
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """配置文件加载器"""
    
    _instance: Optional['ConfigLoader'] = None
    _data_dir: Path
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 获取 data 目录路径
        self._data_dir = Path(__file__).parent.parent / 'data'
        
        # 缓存加载的数据
        self._crop_data: Optional[Dict] = None
        self._achievement_data: Optional[Dict] = None
        
        self._initialized = True
    
    def _load_json(self, filename: str) -> Dict:
        """加载 JSON 文件"""
        filepath = self._data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"配置文件不存在：{filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_crop_data(self) -> Dict[str, Any]:
        """获取作物配置数据"""
        if self._crop_data is None:
            data = self._load_json('crops.json')
            self._crop_data = data.get('crops', {})
        return self._crop_data
    
    def get_achievement_data(self) -> Dict[str, Any]:
        """获取成就配置数据"""
        if self._achievement_data is None:
            data = self._load_json('achievements.json')
            self._achievement_data = data.get('achievements', {})
        return self._achievement_data
    
    def get_crop_by_id(self, crop_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取作物配置"""
        crops = self.get_crop_data()
        return crops.get(crop_id)
    
    def get_all_crop_ids(self) -> list:
        """获取所有作物 ID"""
        return list(self.get_crop_data().keys())
    
    def get_achievement_by_id(self, achievement_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取成就配置"""
        achievements = self.get_achievement_data()
        return achievements.get(achievement_id)
    
    def get_all_achievement_ids(self) -> list:
        """获取所有成就 ID"""
        return list(self.get_achievement_data().keys())
    
    def reload(self):
        """重新加载所有配置"""
        self._crop_data = None
        self._achievement_data = None
        self.get_crop_data()
        self.get_achievement_data()


# 全局配置加载器实例
config_loader = ConfigLoader()


def get_crop_config(crop_id: str) -> Optional[Dict[str, Any]]:
    """便捷函数：获取作物配置"""
    return config_loader.get_crop_by_id(crop_id)


def get_achievement_config(achievement_id: str) -> Optional[Dict[str, Any]]:
    """便捷函数：获取成就配置"""
    return config_loader.get_achievement_by_id(achievement_id)
