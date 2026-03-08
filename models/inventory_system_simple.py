"""
农场库存系统模块
简化的库存管理，专注于农场物品
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ItemCategory(Enum):
    """物品分类 - 农场主题"""
    SEED = "种子"
    CROP = "农作物"
    FOOD = "食物"
    TOOL = "工具"
    MATERIAL = "材料"
    GIFT = "礼物"
    MISC = "杂项"


@dataclass
class ItemTemplate:
    """物品模板定义"""
    item_id: str
    name: str
    category: ItemCategory
    icon: str
    description: str
    stack_size: int = 99
    buy_price: int = 0
    sell_price: int = 0


@dataclass
class ItemInstance:
    """物品实例"""
    template: ItemTemplate
    quantity: int = 1
    quality: str = "普通"
    
    def get_total_value(self) -> int:
        """计算总价值"""
        return self.template.sell_price * self.quantity
    
    def can_stack_with(self, other: 'ItemInstance') -> bool:
        """判断是否可以堆叠"""
        return (self.template.item_id == other.template.item_id and 
                self.quality == other.quality)


@dataclass
class InventorySlot:
    """背包格子"""
    item: Optional[ItemInstance] = None
    locked: bool = False
    
    def is_empty(self) -> bool:
        return self.item is None
    
    def add_item(self, item: ItemInstance) -> int:
        """
        添加物品到格子
        返回无法放入的数量
        """
        if self.is_empty():
            self.item = item
            return 0
        
        if not self.item.can_stack_with(item):
            return item.quantity
        
        max_stack = self.item.template.stack_size
        space_available = max_stack - self.item.quantity
        to_add = min(space_available, item.quantity)
        
        self.item.quantity += to_add
        return item.quantity - to_add
    
    def remove_item(self, count: int) -> Optional[ItemInstance]:
        """从格子中取出物品"""
        if self.is_empty():
            return None
        
        take = min(count, self.item.quantity)
        removed = ItemInstance(
            template=self.item.template,
            quantity=take,
            quality=self.item.quality
        )
        
        self.item.quantity -= take
        if self.item.quantity <= 0:
            self.item = None
        
        return removed


class SimpleInventory:
    """简易背包系统"""
    
    def __init__(self, capacity: int = 36):
        self.capacity = capacity
        self.slots: List[InventorySlot] = [
            InventorySlot() for _ in range(capacity)
        ]
    
    def add_item(self, item: ItemInstance) -> bool:
        """添加物品到背包"""
        remaining = item.quantity
        
        for slot in self.slots:
            if remaining <= 0:
                break
            if not slot.is_empty() and slot.item.can_stack_with(item):
                remaining = slot.add_item(ItemInstance(
                    template=item.template,
                    quantity=remaining,
                    quality=item.quality
                ))
        
        if remaining > 0:
            for slot in self.slots:
                if remaining <= 0:
                    break
                if slot.is_empty():
                    remaining = slot.add_item(ItemInstance(
                        template=item.template,
                        quantity=remaining,
                        quality=item.quality
                    ))
        
        return remaining <= 0
    
    def remove_item(self, item_id: str, count: int) -> bool:
        """从背包移除物品"""
        removed = 0
        for slot in self.slots:
            if removed >= count:
                break
            if not slot.is_empty() and slot.item.template.item_id == item_id:
                item = slot.remove_item(count - removed)
                if item:
                    removed += item.quantity
        
        return removed >= count
    
    def has_item(self, item_id: str, count: int = 1) -> bool:
        """检查是否有指定物品"""
        total = sum(
            slot.item.quantity 
            for slot in self.slots 
            if not slot.is_empty() and slot.item.template.item_id == item_id
        )
        return total >= count
    
    def get_item_count(self, item_id: str) -> int:
        """获取物品数量"""
        return sum(
            slot.item.quantity 
            for slot in self.slots 
            if not slot.is_empty() and slot.item.template.item_id == item_id
        )
    
    def get_items_by_category(self, category: ItemCategory) -> List[ItemInstance]:
        """按分类获取物品"""
        return [
            slot.item 
            for slot in self.slots 
            if not slot.is_empty() and slot.item.template.category == category
        ]
    
    def get_all_items(self) -> List[ItemInstance]:
        """获取所有物品"""
        return [slot.item for slot in self.slots if not slot.is_empty()]
    
    def count_empty_slots(self) -> int:
        """计算空格子数量"""
        return sum(1 for slot in self.slots if slot.is_empty())
    
    def is_full(self) -> bool:
        """背包是否已满"""
        return self.count_empty_slots() == 0


@dataclass
class StorageContainer:
    """存储容器（箱子/仓库）"""
    container_id: str
    name: str
    capacity: int
    slots: List[InventorySlot] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.slots:
            self.slots = [InventorySlot() for _ in range(self.capacity)]
    
    def get_inventory(self) -> SimpleInventory:
        """获取容器内的物品"""
        inv = SimpleInventory(self.capacity)
        inv.slots = self.slots
        return inv


class ItemFactory:
    """物品工厂"""
    
    _templates: Dict[str, ItemTemplate] = {}
    
    @classmethod
    def register_template(cls, template: ItemTemplate):
        cls._templates[template.item_id] = template
    
    @classmethod
    def create_item(cls, item_id: str, quantity: int = 1) -> Optional[ItemInstance]:
        """根据模板 ID 创建物品实例"""
        template = cls._templates.get(item_id)
        if template:
            return ItemInstance(template=template, quantity=quantity)
        return None
    
    @classmethod
    def get_template(cls, item_id: str) -> Optional[ItemTemplate]:
        """获取物品模板"""
        return cls._templates.get(item_id)
