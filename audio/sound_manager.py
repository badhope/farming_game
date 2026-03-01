"""
音效管理器模块
负责游戏音效的播放和管理
"""

import threading
import time
from typing import Dict, Optional
import os


class SoundManager:
    """
    音效管理器类
    管理游戏中的各种音效播放
    """
    
    def __init__(self):
        """初始化音效管理器"""
        self.sounds_enabled = True
        self.volume = 0.7
        self._sound_cache: Dict[str, str] = {}
        self._initialize_sounds()
    
    def _initialize_sounds(self):
        """初始化音效文件路径"""
        # 定义音效映射
        self._sound_cache = {
            'plant': '🌱',
            'water': '💧',
            'harvest': '🎉',
            'buy': '💰',
            'sell': '💸',
            'achievement': '🏆',
            'error': '❌',
            'success': '✅',
            'day_advance': '🌅',
            'rain': '🌧️',
            'storm': '⛈️'
        }
    
    def enable_sound(self):
        """启用音效"""
        self.sounds_enabled = True
    
    def disable_sound(self):
        """禁用音效"""
        self.sounds_enabled = False
    
    def set_volume(self, volume: float):
        """
        设置音量
        
        Args:
            volume: 音量值 (0.0-1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
    
    def play_sound(self, sound_type: str):
        """
        播放音效
        
        Args:
            sound_type: 音效类型
        """
        if not self.sounds_enabled:
            return
        
        # 在后台线程中播放音效，避免阻塞主线程
        thread = threading.Thread(target=self._play_sound_async, args=(sound_type,))
        thread.daemon = True
        thread.start()
    
    def _play_sound_async(self, sound_type: str):
        """
        异步播放音效
        
        Args:
            sound_type: 音效类型
        """
        try:
            # 获取对应的emoji符号作为简单的声音反馈
            emoji = self._sound_cache.get(sound_type, '🔔')
            
            # 打印音效符号（可以被终端捕获显示）
            print(f"[SOUND] {emoji}", end='', flush=True)
            
            # 简单的延迟模拟音效播放
            time.sleep(0.1)
            print()  # 换行
            
        except Exception as e:
            print(f"音效播放失败: {e}")
    
    def play_background_music(self):
        """播放背景音乐（占位方法）"""
        if not self.sounds_enabled:
            return
        
        print("[MUSIC] ♪ 播放田园背景音乐...")
    
    def stop_background_music(self):
        """停止背景音乐（占位方法）"""
        print("[MUSIC] ■ 停止背景音乐")
