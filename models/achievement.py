"""
成就数据模型
定义成就类的数据结构
"""

from dataclasses import dataclass, field
from typing import Callable, Optional
from datetime import datetime


@dataclass
class Achievement:
    """
    成就数据类
    
    属性：
        id: 成就唯一标识符
        name: 成就名称（含图标）
        description: 成就描述
        condition: 解锁条件描述
        reward_text: 解锁奖励文本
        unlocked: 是否已解锁
        unlocked_date: 解锁日期时间
        progress_current: 当前进度
        progress_target: 目标进度
    """
    id: str
    name: str
    description: str
    condition: str = ""
    reward_text: str = ""
    unlocked: bool = False
    unlocked_date: Optional[str] = None
    progress_current: int = 0
    progress_target: int = 0
    
    def unlock(self) -> bool:
        """
        解锁成就
        
        Returns:
            bool: 是否成功解锁（False表示已解锁）
        """
        if self.unlocked:
            return False
        
        self.unlocked = True
        self.unlocked_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.progress_current = self.progress_target
        return True
    
    def set_progress(self, current: int) -> None:
        """
        设置当前进度
        
        Args:
            current: 当前进度值
        """
        self.progress_current = current
    
    def get_progress_percentage(self) -> float:
        """
        获取进度百分比
        
        Returns:
            float: 0.0 到 100.0 之间的百分比值
        """
        if self.progress_target <= 0:
            return 100.0 if self.unlocked else 0.0
        
        percentage = (self.progress_current / self.progress_target) * 100
        return min(100.0, round(percentage, 1))
    
    def get_progress_bar(self, length: int = 20) -> str:
        """
        获取进度条字符串
        
        Args:
            length: 进度条长度
            
        Returns:
            str: 进度条字符串，如 "████████░░░░ 60%"
        """
        if self.progress_target <= 0:
            return "▓" * length + " 100%" if self.unlocked else "░" * length + " 0%"
        
        filled = int((self.progress_current / self.progress_target) * length)
        filled = min(filled, length)
        empty = length - filled
        
        bar = "▓" * filled + "░" * empty
        percentage = self.get_progress_percentage()
        
        return f"{bar} {percentage}%"
    
    def get_display_status(self) -> str:
        """
        获取显示状态
        
        Returns:
            str: 状态字符串
        """
        if self.unlocked:
            return "✅ 已解锁"
        return "⬜ 未解锁"
    
    def get_full_info(self) -> str:
        """
        获取完整信息文本
        
        Returns:
            str: 完整信息
        """
        lines = [
            f"{'='*40}",
            f"🏆 {self.name}",
            f"{'='*40}",
            f"📝 描述: {self.description}",
            f"📋 条件: {self.condition}",
            f"🎁 奖励: {self.reward_text}",
            f"📊 进度: {self.get_progress_bar()}",
            f"📌 状态: {self.get_display_status()}",
        ]
        
        if self.unlocked and self.unlocked_date:
            lines.append(f"🕐 解锁时间: {self.unlocked_date}")
        
        lines.append("=" * 40)
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        status = "✅" if self.unlocked else "⬜"
        return f"{status} {self.name}"
    
    def __repr__(self) -> str:
        return (
            f"Achievement(id='{self.id}', name='{self.name}', "
            f"unlocked={self.unlocked})"
        )


@dataclass
class AchievementManager:
    """
    成就管理器类
    
    管理所有成就的集合
    """
    achievements: dict = field(default_factory=dict)
    
    def add_achievement(self, achievement: Achievement) -> None:
        """
        添加成就
        
        Args:
            achievement: 成就对象
        """
        self.achievements[achievement.id] = achievement
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """
        获取成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            Optional[Achievement]: 成就对象，不存在返回None
        """
        return self.achievements.get(achievement_id)
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """
        解锁成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            bool: 是否成功解锁
        """
        achievement = self.get_achievement(achievement_id)
        if achievement is None:
            return False
        
        return achievement.unlock()
    
    def is_unlocked(self, achievement_id: str) -> bool:
        """
        检查成就是否已解锁
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            bool: 是否已解锁
        """
        achievement = self.get_achievement(achievement_id)
        return achievement.unlocked if achievement else False
    
    def get_unlocked_count(self) -> int:
        """
        获取已解锁成就数量
        
        Returns:
            int: 已解锁数量
        """
        return sum(1 for a in self.achievements.values() if a.unlocked)
    
    def get_total_count(self) -> int:
        """
        获取总成就数量
        
        Returns:
            int: 总数量
        """
        return len(self.achievements)
    
    def get_all_achievements(self) -> list:
        """
        获取所有成就列表
        
        Returns:
            list: 成就列表
        """
        return list(self.achievements.values())
    
    def get_unlocked_achievements(self) -> list:
        """
        获取已解锁成就列表
        
        Returns:
            list: 已解锁成就列表
        """
        return [a for a in self.achievements.values() if a.unlocked]
    
    def get_locked_achievements(self) -> list:
        """
        获取未解锁成就列表
        
        Returns:
            list: 未解锁成就列表
        """
        return [a for a in self.achievements.values() if not a.unlocked]
    
    def get_completion_percentage(self) -> float:
        """
        获取完成百分比
        
        Returns:
            float: 完成百分比
        """
        if self.get_total_count() == 0:
            return 0.0
        
        return round(
            (self.get_unlocked_count() / self.get_total_count()) * 100, 1
        )
    
    def set_achievement_progress(
        self, achievement_id: str, current: int
    ) -> None:
        """
        设置成就进度
        
        Args:
            achievement_id: 成就ID
            current: 当前进度
        """
        achievement = self.get_achievement(achievement_id)
        if achievement:
            achievement.set_progress(current)
    
    def get_summary(self) -> str:
        """
        获取成就摘要
        
        Returns:
            str: 摘要文本
        """
        lines = [
            f"\n{'='*50}",
            f"🏆 成就系统",
            f"{'='*50}",
            f"📊 完成度: {self.get_unlocked_count()}/{self.get_total_count()} "
            f"({self.get_completion_percentage()}%)",
            f"{'='*50}",
        ]
        
        # 已解锁成就
        unlocked = self.get_unlocked_achievements()
        if unlocked:
            lines.append("\n✅ 已解锁成就:")
            for a in unlocked:
                lines.append(f"   {a.name} - {a.description}")
        
        # 未解锁成就
        locked = self.get_locked_achievements()
        if locked:
            lines.append("\n⬜ 未解锁成就:")
            for a in locked:
                progress_bar = a.get_progress_bar(10)
                lines.append(
                    f"   {a.name} - {a.description} [{progress_bar}]"
                )
        
        lines.append("\n" + "=" * 50)
        
        return "\n".join(lines)
    
    def __len__(self) -> int:
        return len(self.achievements)
    
    def __contains__(self, achievement_id: str) -> bool:
        return achievement_id in self.achievements
    
    def __iter__(self):
        return iter(self.achievements.values())
