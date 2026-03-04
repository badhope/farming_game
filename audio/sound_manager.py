"""
音效管理器模块
负责游戏音效的播放和管理
"""

import threading
import time
from typing import Dict, Optional
import os
import pygame


class SoundManager:
    """
    音效管理器类
    管理游戏中的各种音效播放
    """
    
    def __init__(self):
        """初始化音效管理器"""
        self.sounds_enabled = True
        self.volume = 0.7
        self._sound_cache: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self._music_playing = False
        
        # 初始化pygame mixer
        try:
            pygame.mixer.init()
            self._initialize_sounds()
        except Exception as e:
            print(f"初始化音效系统失败: {e}")
            self.sounds_enabled = False
    
    def _initialize_sounds(self):
        """初始化音效文件"""
        # 定义音效映射（使用免费的开源音效）
        # 这些是示例URL，实际使用时需要下载到本地
        self._sound_cache = {
            'plant': None,  # 将被替换为实际的音效对象
            'water': None,
            'harvest': None,
            'buy': None,
            'sell': None,
            'achievement': None,
            'error': None,
            'success': None,
            'day_advance': None,
            'rain': None,
            'storm': None
        }
        
        # 尝试加载音效（使用在线免费音效）
        try:
            # 这里使用免费的音效URL，实际项目中应该下载到本地
            import urllib.request
            import tempfile
            
            # 音效URL映射
            sound_urls = {
                'plant': 'https://assets.mixkit.co/sfx/preview/mixkit-plant-growth-1638.mp3',
                'water': 'https://assets.mixkit.co/sfx/preview/mixkit-water-droplets-1624.mp3',
                'harvest': 'https://assets.mixkit.co/sfx/preview/mixkit-bell-notification-938.mp3',
                'buy': 'https://assets.mixkit.co/sfx/preview/mixkit-coin-win-210.mp3',
                'sell': 'https://assets.mixkit.co/sfx/preview/mixkit-coin-win-210.mp3',
                'achievement': 'https://assets.mixkit.co/sfx/preview/mixkit-achievement-bell-600.mp3',
                'error': 'https://assets.mixkit.co/sfx/preview/mixkit-wrong-answer-fail-notification-946.mp3',
                'success': 'https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3',
                'day_advance': 'https://assets.mixkit.co/sfx/preview/mixkit-positive-interface-beep-221.mp3',
                'rain': 'https://assets.mixkit.co/sfx/preview/mixkit-rain-on-window-1247.mp3',
                'storm': 'https://assets.mixkit.co/sfx/preview/mixkit-storm-with-thunder-1255.mp3'
            }
            
            for sound_type, url in sound_urls.items():
                try:
                    # 下载音效到临时文件
                    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                        urllib.request.urlretrieve(url, tmp.name)
                        tmp_path = tmp.name
                    
                    # 加载音效
                    sound = pygame.mixer.Sound(tmp_path)
                    sound.set_volume(self.volume)
                    self._sound_cache[sound_type] = sound
                    
                    # 清理临时文件
                    os.unlink(tmp_path)
                except Exception as e:
                    print(f"加载音效 {sound_type} 失败: {e}")
                    self._sound_cache[sound_type] = None
        except Exception as e:
            print(f"加载音效失败: {e}")
    
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
        
        # 更新所有音效的音量
        for sound in self._sound_cache.values():
            if sound:
                sound.set_volume(self.volume)
    
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
            sound = self._sound_cache.get(sound_type)
            if sound:
                sound.play()
            else:
                # 回退到emoji反馈
                emoji_map = {
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
                emoji = emoji_map.get(sound_type, '🔔')
                print(f"[SOUND] {emoji}")
        except Exception as e:
            print(f"音效播放失败: {e}")
    
    def play_background_music(self):
        """播放背景音乐"""
        if not self.sounds_enabled or self._music_playing:
            return
        
        try:
            # 使用免费的背景音乐
            import urllib.request
            import tempfile
            
            # 田园风格的背景音乐
            music_url = 'https://assets.mixkit.co/sfx/preview/mixkit-soft-ambient-meditation-1633.mp3'
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                urllib.request.urlretrieve(music_url, tmp.name)
                tmp_path = tmp.name
            
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.set_volume(self.volume * 0.5)  # 背景音乐音量稍低
            pygame.mixer.music.play(-1)  # 循环播放
            
            # 清理临时文件
            os.unlink(tmp_path)
            
            self._music_playing = True
            print("[MUSIC] ♪ 播放田园背景音乐...")
        except Exception as e:
            print(f"播放背景音乐失败: {e}")
    
    def stop_background_music(self):
        """停止背景音乐"""
        if self._music_playing:
            try:
                pygame.mixer.music.stop()
                self._music_playing = False
                print("[MUSIC] ■ 停止背景音乐")
            except Exception as e:
                print(f"停止背景音乐失败: {e}")
