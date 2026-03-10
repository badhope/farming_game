"""
玩家数据模型
定义玩家类的数据结构
"""

from dataclasses import dataclass, field
from typing import Dict, Set, List
from config.settings import GameConfig


@dataclass
class PlayerStats:
    """
    玩家统计数据类
    
    记录玩家的各项游戏数据统计
    """
    total_harvested: int = 0          # 总收获数量
    total_earnings: int = 0           # 累计收入
    total_spent: int = 0              # 累计支出
    crops_grown: Set[str] = field(default_factory=set)  # 种植过的作物类型
    days_played: int = 0              # 游戏天数
    max_money_held: int = 0           # 持有过的最大金币数
    storm_survived: bool = False      # 是否在暴风雨中保住所有作物
    single_day_harvest: int = 0       # 单日最大收获数
    today_harvest: int = 0            # 今日收获数
    
    def add_harvest(self, count: int = 1) -> None:
        """添加收获记录"""
        self.total_harvested += count
        self.today_harvest += count
        
        # 更新单日最大收获
        if self.today_harvest > self.single_day_harvest:
            self.single_day_harvest = self.today_harvest
    
    def add_earnings(self, amount: int) -> None:
        """添加收入记录"""
        self.total_earnings += amount
    
    def add_expense(self, amount: int) -> None:
        """添加支出记录"""
        self.total_spent += amount
    
    def add_crop_grown(self, crop_name: str) -> None:
        """记录种植过的作物"""
        self.crops_grown.add(crop_name)
    
    def reset_daily_stats(self) -> None:
        """重置每日统计"""
        self.today_harvest = 0
    
    def get_crops_grown_count(self) -> int:
        """获取种植过的作物种类数量"""
        return len(self.crops_grown)


@dataclass
class Player:
    """
    玩家数据类
    
    属性：
        name: 玩家名称
        money: 当前金币
        inventory: 背包（收获物）
        seeds: 拥有的种子
        stats: 统计数据
        upgrade_level: 农场等级
        unlocked_achievements: 已解锁成就列表
    """
    name: str = "农夫"
    money: int = GameConfig.INITIAL_MONEY
    level: int = 1
    exp: int = 0
    stamina: int = 100
    max_stamina: int = 100
    inventory: Dict[str, int] = field(default_factory=dict)
    seeds: Dict[str, int] = field(default_factory=dict)
    stats: PlayerStats = field(default_factory=PlayerStats)
    upgrade_level: int = 0
    unlocked_achievements: List[str] = field(default_factory=list)
    
    # ========== 金币操作 ==========
    
    def can_afford(self, amount: int) -> bool:
        """
        检查是否有足够的金币
        
        Args:
            amount: 需要的金币数量
            
        Returns:
            bool: 是否负担得起
        """
        return self.money >= amount
    
    def spend_money(self, amount: int) -> bool:
        """
        花费金币
        
        Args:
            amount: 花费的金币数量
            
        Returns:
            bool: 是否花费成功
        """
        if not self.can_afford(amount):
            return False
        
        self.money -= amount
        self.stats.add_expense(amount)
        return True
    
    def earn_money(self, amount: int) -> None:
        """
        赚取金币
        
        Args:
            amount: 赚取的金币数量
        """
        self.money += amount
        self.stats.add_earnings(amount)
        
        # 更新最大持有金币
        if self.money > self.stats.max_money_held:
            self.stats.max_money_held = self.money
    
    # ========== 背包操作 ==========
    
    def add_to_inventory(self, item_name: str, count: int = 1) -> None:
        """
        添加物品到背包
        
        Args:
            item_name: 物品名称
            count: 数量
        """
        if item_name in self.inventory:
            self.inventory[item_name] += count
        else:
            self.inventory[item_name] = count
        
        self.stats.add_harvest(count)
    
    def remove_from_inventory(self, item_name: str, count: int = 1) -> bool:
        """
        从背包移除物品
        
        Args:
            item_name: 物品名称
            count: 数量
            
        Returns:
            bool: 是否移除成功
        """
        if item_name not in self.inventory:
            return False
        
        if self.inventory[item_name] < count:
            return False
        
        self.inventory[item_name] -= count
        
        # 如果数量归零，删除该物品
        if self.inventory[item_name] <= 0:
            del self.inventory[item_name]
        
        return True
    
    def get_inventory_count(self, item_name: str) -> int:
        """
        获取背包中某物品的数量
        
        Args:
            item_name: 物品名称
            
        Returns:
            int: 物品数量
        """
        return self.inventory.get(item_name, 0)
    
    def has_item(self, item_name: str, count: int = 1) -> bool:
        """
        检查是否有足够的物品
        
        Args:
            item_name: 物品名称
            count: 需要的数量
            
        Returns:
            bool: 是否有足够的物品
        """
        return self.get_inventory_count(item_name) >= count
    
    def get_total_inventory_count(self) -> int:
        """
        获取背包总物品数量
        
        Returns:
            int: 总数量
        """
        return sum(self.inventory.values())
    
    # ========== 种子操作 ==========
    
    def add_seeds(self, seed_name: str, count: int = 1) -> None:
        """
        添加种子
        
        Args:
            seed_name: 种子名称
            count: 数量
        """
        if seed_name in self.seeds:
            self.seeds[seed_name] += count
        else:
            self.seeds[seed_name] = count
    
    def remove_seeds(self, seed_name: str, count: int = 1) -> bool:
        """
        移除种子
        
        Args:
            seed_name: 种子名称
            count: 数量
            
        Returns:
            bool: 是否移除成功
        """
        if seed_name not in self.seeds:
            return False
        
        if self.seeds[seed_name] < count:
            return False
        
        self.seeds[seed_name] -= count
        
        if self.seeds[seed_name] <= 0:
            del self.seeds[seed_name]
        
        return True
    
    def get_seed_count(self, seed_name: str) -> int:
        """
        获取某类种子的数量
        
        Args:
            seed_name: 种子名称
            
        Returns:
            int: 种子数量
        """
        return self.seeds.get(seed_name, 0)
    
    def has_seeds(self, seed_name: str, count: int = 1) -> bool:
        """
        检查是否有足够的种子
        
        Args:
            seed_name: 种子名称
            count: 需要的数量
            
        Returns:
            bool: 是否有足够的种子
        """
        return self.get_seed_count(seed_name) >= count
    
    def get_total_seed_count(self) -> int:
        """
        获取种子总数量
        
        Returns:
            int: 总数量
        """
        return sum(self.seeds.values())
    
    # ========== 成就操作 ==========
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """
        解锁成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            bool: 是否新解锁（False表示已解锁）
        """
        if achievement_id in self.unlocked_achievements:
            return False
        
        self.unlocked_achievements.append(achievement_id)
        return True
    
    def has_achievement(self, achievement_id: str) -> bool:
        """
        检查是否已解锁某成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            bool: 是否已解锁
        """
        return achievement_id in self.unlocked_achievements
    
    def get_achievement_count(self) -> int:
        """
        获取已解锁成就数量
        
        Returns:
            int: 成就数量
        """
        return len(self.unlocked_achievements)
    
    # ========== 农场升级 ==========
    
    def can_upgrade(self) -> bool:
        """
        检查是否可以升级农场
        
        Returns:
            bool: 是否可以升级
        """
        return self.upgrade_level < GameConfig.MAX_UPGRADE_LEVEL
    
    def get_upgrade_cost(self) -> int:
        """
        获取下次升级费用
        
        Returns:
            int: 升级费用
        """
        return (self.upgrade_level + 1) * GameConfig.UPGRADE_COST_MULTIPLIER
    
    def upgrade_farm(self) -> bool:
        """
        升级农场
        
        Returns:
            bool: 是否升级成功
        """
        if not self.can_upgrade():
            return False
        
        cost = self.get_upgrade_cost()
        if not self.can_afford(cost):
            return False
        
        self.spend_money(cost)
        self.upgrade_level += 1
        return True
    
    def get_plot_size(self) -> int:
        """
        获取当前农田大小
        
        Returns:
            int: 农田边长
        """
        return GameConfig.INITIAL_PLOT_SIZE + self.upgrade_level
    
    # ========== 其他方法 ==========
    
    def new_day(self) -> None:
        """
        新的一天（重置每日统计）
        """
        self.stats.days_played += 1
        self.stats.reset_daily_stats()
    
    def get_summary(self) -> str:
        """
        获取玩家信息摘要
        
        Returns:
            str: 摘要文本
        """
        return (
            f"👤 {self.name}\n"
            f"💰 金币: {self.money}\n"
            f"📦 收获物: {self.get_total_inventory_count()}件\n"
            f"🌱 种子: {self.get_total_seed_count()}个\n"
            f"🏆 成就: {self.get_achievement_count()}个\n"
            f"🏘️ 农场等级: Lv.{self.upgrade_level + 1}\n"
            f"📊 累计收入: {self.stats.total_earnings}金币"
        )
    
    def __str__(self) -> str:
        return f"Player(name='{self.name}', money={self.money})"
    
    def __repr__(self) -> str:
        return (
            f"Player(name='{self.name}', money={self.money}, "
            f"level={self.upgrade_level})"
        )
