"""
技能系统模块
管理玩家的各项技能等级和效果
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class SkillType(Enum):
    """技能类型枚举"""
    FARMING = "农业"
    WATERING = "浇水"
    HARVESTING = "收获"
    TRADING = "交易"
    ANIMAL_CARE = "畜牧"
    CRAFTING = "制作"
    FISHING = "钓鱼"
    MINING = "采矿"


@dataclass
class SkillLevel:
    """技能等级数据"""
    level: int = 1
    experience: int = 0
    
    def get_experience_for_next_level(self) -> int:
        """获取升级所需经验值"""
        return int(100 * (self.level ** 1.5))
    
    def add_experience(self, amount: int) -> bool:
        """
        添加经验值
        
        Returns:
            bool: 是否升级
        """
        self.experience += amount
        required = self.get_experience_for_next_level()
        
        if self.experience >= required:
            self.experience -= required
            self.level += 1
            return True
        return False
    
    def get_progress_percentage(self) -> float:
        """获取当前等级进度百分比"""
        required = self.get_experience_for_next_level()
        return min(100.0, (self.experience / required) * 100)


@dataclass
class Skill:
    """技能类"""
    skill_type: SkillType
    name: str
    description: str
    icon: str
    level_data: SkillLevel = field(default_factory=SkillLevel)
    
    @property
    def level(self) -> int:
        return self.level_data.level
    
    @property
    def experience(self) -> int:
        return self.level_data.experience
    
    def add_exp(self, amount: int) -> bool:
        """添加经验并返回是否升级"""
        return self.level_data.add_experience(amount)
    
    def get_progress(self) -> float:
        """获取升级进度"""
        return self.level_data.get_progress_percentage()
    
    def get_bonus(self) -> float:
        """获取技能加成百分比"""
        return 1.0 + (self.level - 1) * 0.1


class SkillManager:
    """技能管理器"""
    
    def __init__(self):
        self.skills: Dict[SkillType, Skill] = {}
        self._init_skills()
    
    def _init_skills(self):
        """初始化所有技能"""
        skill_data = {
            SkillType.FARMING: ("🌱 农业技能", "提高作物生长速度和产量", "🌱"),
            SkillType.WATERING: ("💧 浇水技能", "减少浇水次数需求", "💧"),
            SkillType.HARVESTING: ("🌾 收获技能", "增加收获品质和数量", "🌾"),
            SkillType.TRADING: ("💰 交易技能", "提高出售价格和购买折扣", "💰"),
            SkillType.ANIMAL_CARE: ("🐄 畜牧技能", "提高动物产出和好感度", "🐄"),
            SkillType.CRAFTING: ("🔨 制作技能", "解锁更多配方和提高品质", "🔨"),
            SkillType.FISHING: ("🎣 钓鱼技能", "提高钓鱼成功率和品质", "🎣"),
            SkillType.MINING: ("⛏️ 采矿技能", "提高采矿效率和稀有度", "⛏️"),
        }
        
        for skill_type, (name, desc, icon) in skill_data.items():
            self.skills[skill_type] = Skill(
                skill_type=skill_type,
                name=name,
                description=desc,
                icon=icon
            )
    
    def get_skill(self, skill_type: SkillType) -> Optional[Skill]:
        """获取技能"""
        return self.skills.get(skill_type)
    
    def get_skill_level(self, skill_type: SkillType) -> int:
        """获取技能等级"""
        skill = self.get_skill(skill_type)
        return skill.level if skill else 1
    
    def add_experience(self, skill_type: SkillType, amount: int) -> tuple:
        """
        添加技能经验
        
        Returns:
            tuple: (是否升级, 新等级)
        """
        skill = self.get_skill(skill_type)
        if skill:
            leveled_up = skill.add_exp(amount)
            return (leveled_up, skill.level)
        return (False, 1)
    
    def get_all_skills(self) -> List[Skill]:
        """获取所有技能"""
        return list(self.skills.values())
    
    def get_total_level(self) -> int:
        """获取总技能等级"""
        return sum(skill.level for skill in self.skills.values())
    
    def get_farming_bonus(self) -> float:
        """获取农业加成"""
        return self.skills[SkillType.FARMING].get_bonus()
    
    def get_trading_bonus(self) -> float:
        """获取交易加成"""
        return self.skills[SkillType.TRADING].get_bonus()
    
    def get_harvest_bonus(self) -> float:
        """获取收获加成"""
        return self.skills[SkillType.HARVESTING].get_bonus()
    
    def to_dict(self) -> dict:
        """转换为字典用于存档"""
        return {
            skill_type.value: {
                "level": skill.level_data.level,
                "experience": skill.level_data.experience
            }
            for skill_type, skill in self.skills.items()
        }
    
    def from_dict(self, data: dict):
        """从字典加载"""
        for skill_type, skill in self.skills.items():
            if skill_type.value in data:
                skill_data = data[skill_type.value]
                skill.level_data.level = skill_data.get("level", 1)
                skill.level_data.experience = skill_data.get("experience", 0)
