"""
MMORPG风格库存系统模块
提供完整的库存管理、装备槽位、存储系统和银行功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import random


class ItemCategory(Enum):
    WEAPON = "武器"
    ARMOR = "护甲"
    ACCESSORY = "饰品"
    CONSUMABLE = "消耗品"
    MATERIAL = "材料"
    QUEST = "任务物品"
    TREASURE = "宝藏"
    SEED = "种子"
    FOOD = "食物"
    TOOL = "工具"
    DECORATION = "装饰"
    MISC = "杂项"


class EquipmentSlot(Enum):
    HEAD = "头部"
    CHEST = "胸部"
    LEGS = "腿部"
    FEET = "脚部"
    HANDS = "手部"
    MAIN_HAND = "主手"
    OFF_HAND = "副手"
    NECK = "颈部"
    RING1 = "戒指1"
    RING2 = "戒指2"
    TRINKET = "饰品"


class ItemRarity(Enum):
    COMMON = "普通"
    UNCOMMON = "优秀"
    RARE = "稀有"
    EPIC = "史诗"
    LEGENDARY = "传说"
    MYTHIC = "神话"


class StatType(Enum):
    STRENGTH = "力量"
    AGILITY = "敏捷"
    INTELLIGENCE = "智力"
    VITALITY = "体力"
    LUCK = "幸运"
    ATTACK = "攻击力"
    DEFENSE = "防御力"
    SPEED = "速度"
    CRITICAL = "暴击率"
    DODGE = "闪避率"


@dataclass
class ItemStats:
    stats: Dict[StatType, int] = field(default_factory=dict)
    
    def add_stat(self, stat_type: StatType, value: int):
        self.stats[stat_type] = self.stats.get(stat_type, 0) + value
    
    def get_stat(self, stat_type: StatType) -> int:
        return self.stats.get(stat_type, 0)
    
    def get_total_power(self) -> int:
        return sum(self.stats.values())
    
    def get_stats_display(self) -> List[str]:
        return [f"{stat.value}: +{value}" for stat, value in self.stats.items() if value > 0]


@dataclass
class ItemEffect:
    effect_id: str
    name: str
    description: str
    trigger: str
    value: int = 0
    duration: int = 0
    cooldown: int = 0
    chance: float = 1.0


@dataclass
class ItemInstance:
    instance_id: str
    item_id: str
    name: str
    category: ItemCategory
    rarity: ItemRarity
    icon: str
    
    stack_size: int = 1
    max_stack: int = 1
    
    stats: ItemStats = field(default_factory=ItemStats)
    effects: List[ItemEffect] = field(default_factory=list)
    
    level_requirement: int = 1
    class_requirement: str = ""
    
    buy_price: int = 0
    sell_price: int = 0
    
    durability: int = 100
    max_durability: int = 100
    enhancement_level: int = 0
    max_enhancement: int = 10
    
    is_equipped: bool = False
    equipped_slot: Optional[EquipmentSlot] = None
    
    is_bound: bool = False
    is_quest_item: bool = False
    
    description: str = ""
    flavor_text: str = ""
    
    created_time: int = 0
    
    def can_stack(self) -> bool:
        return self.max_stack > 1
    
    def can_equip(self) -> bool:
        return self.category in [ItemCategory.WEAPON, ItemCategory.ARMOR, ItemCategory.ACCESSORY]
    
    def get_equipment_slot(self) -> Optional[EquipmentSlot]:
        slot_mapping = {
            ItemCategory.WEAPON: EquipmentSlot.MAIN_HAND,
            ItemCategory.ARMOR: EquipmentSlot.CHEST,
            ItemCategory.ACCESSORY: EquipmentSlot.TRINKET
        }
        return slot_mapping.get(self.category)
    
    def enhance(self) -> Tuple[bool, str]:
        if self.enhancement_level >= self.max_enhancement:
            return False, "已达最高强化等级"
        
        success_rate = max(0.1, 1.0 - self.enhancement_level * 0.1)
        
        if random.random() < success_rate:
            self.enhancement_level += 1
            
            for stat_type in self.stats.stats:
                self.stats.stats[stat_type] = int(self.stats.stats[stat_type] * 1.1)
            
            return True, f"强化成功！当前等级：+{self.enhancement_level}"
        else:
            if self.enhancement_level > 5:
                self.enhancement_level -= 1
                return False, f"强化失败！等级下降至+{self.enhancement_level}"
            return False, "强化失败！"
    
    def repair(self, amount: int = 50) -> Tuple[bool, str]:
        if self.durability >= self.max_durability:
            return False, "无需修理"
        
        self.durability = min(self.max_durability, self.durability + amount)
        return True, f"修复了{amount}点耐久度"
    
    def use_durability(self, amount: int = 1) -> bool:
        if self.durability <= 0:
            return False
        
        self.durability = max(0, self.durability - amount)
        return True
    
    def get_sell_price(self) -> int:
        base = self.sell_price
        enhancement_bonus = 1 + self.enhancement_level * 0.1
        durability_penalty = self.durability / self.max_durability
        
        return int(base * enhancement_bonus * durability_penalty)
    
    def get_full_name(self) -> str:
        if self.enhancement_level > 0:
            return f"+{self.enhancement_level} {self.name}"
        return self.name
    
    def get_rarity_color(self) -> str:
        colors = {
            ItemRarity.COMMON: "#FFFFFF",
            ItemRarity.UNCOMMON: "#1EFF00",
            ItemRarity.RARE: "#0070DD",
            ItemRarity.EPIC: "#A335EE",
            ItemRarity.LEGENDARY: "#FF8000",
            ItemRarity.MYTHIC: "#E6CC80"
        }
        return colors.get(self.rarity, "#FFFFFF")


@dataclass
class InventorySlot:
    slot_index: int
    item: Optional[ItemInstance] = None
    
    def is_empty(self) -> bool:
        return self.item is None
    
    def can_add(self, item: ItemInstance) -> bool:
        if self.is_empty():
            return True
        if self.item.can_stack() and self.item.item_id == item.item_id:
            return self.item.stack_size + item.stack_size <= self.item.max_stack
        return False
    
    def add_item(self, item: ItemInstance) -> Tuple[bool, int]:
        if self.is_empty():
            self.item = item
            return True, item.stack_size
        
        if self.can_add(item):
            space = self.item.max_stack - self.item.stack_size
            add_amount = min(space, item.stack_size)
            self.item.stack_size += add_amount
            return True, add_amount
        
        return False, 0


@dataclass
class EquipmentSet:
    name: str
    set_bonus: List[ItemEffect] = field(default_factory=list)
    required_items: List[str] = field(default_factory=list)
    
    def get_set_bonus(self, equipped_count: int) -> List[ItemEffect]:
        bonuses = []
        for i, effect in enumerate(self.set_bonus):
            if equipped_count >= (i + 1) * 2:
                bonuses.append(effect)
        return bonuses


@dataclass
class StorageContainer:
    container_id: str
    name: str
    icon: str
    slots: List[InventorySlot] = field(default_factory=list)
    max_slots: int = 20
    
    is_unlocked: bool = True
    unlock_cost: int = 0
    
    def __post_init__(self):
        if not self.slots:
            self.slots = [InventorySlot(i) for i in range(self.max_slots)]
    
    def get_used_slots(self) -> int:
        return sum(1 for slot in self.slots if not slot.is_empty())
    
    def get_empty_slots(self) -> List[int]:
        return [i for i, slot in enumerate(self.slots) if slot.is_empty()]
    
    def add_item(self, item: ItemInstance) -> Tuple[bool, int, str]:
        remaining = item.stack_size
        
        if item.can_stack():
            for slot in self.slots:
                if not slot.is_empty() and slot.can_add(item):
                    success, added = slot.add_item(item)
                    if success:
                        remaining -= added
                        if remaining <= 0:
                            return True, item.stack_size, "物品已添加"
        
        while remaining > 0:
            empty_slots = self.get_empty_slots()
            if not empty_slots:
                added = item.stack_size - remaining
                if added > 0:
                    return True, added, f"背包已满，添加了{added}个物品"
                return False, 0, "背包已满"
            
            new_item = ItemInstance(
                instance_id=f"{item.instance_id}_{len(empty_slots)}",
                item_id=item.item_id,
                name=item.name,
                category=item.category,
                rarity=item.rarity,
                icon=item.icon,
                stack_size=min(remaining, item.max_stack),
                max_stack=item.max_stack,
                stats=item.stats,
                effects=item.effects,
                buy_price=item.buy_price,
                sell_price=item.sell_price,
                description=item.description
            )
            
            slot_idx = empty_slots[0]
            self.slots[slot_idx].add_item(new_item)
            remaining -= new_item.stack_size
        
        return True, item.stack_size, "物品已添加"
    
    def remove_item(self, slot_index: int, amount: int = 1) -> Tuple[bool, Optional[ItemInstance], str]:
        if slot_index < 0 or slot_index >= len(self.slots):
            return False, None, "无效的槽位"
        
        slot = self.slots[slot_index]
        if slot.is_empty():
            return False, None, "槽位为空"
        
        if slot.item.stack_size < amount:
            return False, None, "物品数量不足"
        
        if amount == slot.item.stack_size:
            item = slot.item
            slot.item = None
            return True, item, f"取出了{item.get_full_name()}"
        
        removed = ItemInstance(
            instance_id=f"{slot.item.instance_id}_split",
            item_id=slot.item.item_id,
            name=slot.item.name,
            category=slot.item.category,
            rarity=slot.item.rarity,
            icon=slot.item.icon,
            stack_size=amount,
            max_stack=slot.item.max_stack,
            buy_price=slot.item.buy_price,
            sell_price=slot.item.sell_price,
            description=slot.item.description
        )
        
        slot.item.stack_size -= amount
        return True, removed, f"取出了{amount}个{slot.item.name}"
    
    def get_item_at(self, slot_index: int) -> Optional[ItemInstance]:
        if 0 <= slot_index < len(self.slots):
            return self.slots[slot_index].item
        return None
    
    def sort_by_name(self):
        items = [slot.item for slot in self.slots if not slot.is_empty()]
        items.sort(key=lambda x: x.name)
        
        for slot in self.slots:
            slot.item = None
        
        for i, item in enumerate(items):
            self.slots[i].item = item
    
    def sort_by_rarity(self):
        rarity_order = {
            ItemRarity.MYTHIC: 0,
            ItemRarity.LEGENDARY: 1,
            ItemRarity.EPIC: 2,
            ItemRarity.RARE: 3,
            ItemRarity.UNCOMMON: 4,
            ItemRarity.COMMON: 5
        }
        
        items = [slot.item for slot in self.slots if not slot.is_empty()]
        items.sort(key=lambda x: rarity_order.get(x.rarity, 5))
        
        for slot in self.slots:
            slot.item = None
        
        for i, item in enumerate(items):
            self.slots[i].item = item
    
    def sort_by_category(self):
        items = [slot.item for slot in self.slots if not slot.is_empty()]
        items.sort(key=lambda x: x.category.value)
        
        for slot in self.slots:
            slot.item = None
        
        for i, item in enumerate(items):
            self.slots[i].item = item


@dataclass
class BankAccount:
    account_id: str
    owner_name: str
    
    gold: int = 0
    max_gold: int = 10000000
    
    storage: StorageContainer = field(default_factory=lambda: StorageContainer("bank", "银行", "🏦", max_slots=50))
    
    interest_rate: float = 0.01
    last_interest_day: int = 0
    
    def deposit_gold(self, amount: int) -> Tuple[bool, str]:
        if amount <= 0:
            return False, "无效的金额"
        
        if self.gold + amount > self.max_gold:
            return False, "银行存款已达上限"
        
        self.gold += amount
        return True, f"存入{amount}金币"
    
    def withdraw_gold(self, amount: int) -> Tuple[bool, int, str]:
        if amount <= 0:
            return False, 0, "无效的金额"
        
        if self.gold < amount:
            actual = self.gold
            self.gold = 0
            return True, actual, f"取出了{actual}金币（余额不足）"
        
        self.gold -= amount
        return True, amount, f"取出{amount}金币"
    
    def calculate_interest(self, current_day: int) -> int:
        days_passed = current_day - self.last_interest_day
        if days_passed <= 0:
            return 0
        
        interest = int(self.gold * self.interest_rate * days_passed)
        self.last_interest_day = current_day
        return interest
    
    def collect_interest(self, current_day: int) -> Tuple[bool, int, str]:
        interest = self.calculate_interest(current_day)
        if interest <= 0:
            return False, 0, "没有可领取的利息"
        
        self.gold += interest
        return True, interest, f"领取了{interest}金币利息"


@dataclass
class EquipmentManager:
    equipped_items: Dict[EquipmentSlot, Optional[ItemInstance]] = field(default_factory=dict)
    set_bonuses: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        for slot in EquipmentSlot:
            if slot not in self.equipped_items:
                self.equipped_items[slot] = None
    
    def equip(self, item: ItemInstance, slot: Optional[EquipmentSlot] = None) -> Tuple[bool, Optional[ItemInstance], str]:
        if not item.can_equip():
            return False, None, "该物品无法装备"
        
        target_slot = slot or item.get_equipment_slot()
        if not target_slot:
            return False, None, "无法确定装备槽位"
        
        old_item = self.equipped_items.get(target_slot)
        
        if old_item:
            old_item.is_equipped = False
            old_item.equipped_slot = None
        
        self.equipped_items[target_slot] = item
        item.is_equipped = True
        item.equipped_slot = target_slot
        
        return True, old_item, f"装备了{item.get_full_name()}"
    
    def unequip(self, slot: EquipmentSlot) -> Tuple[bool, Optional[ItemInstance], str]:
        item = self.equipped_items.get(slot)
        if not item:
            return False, None, "该槽位没有装备"
        
        item.is_equipped = False
        item.equipped_slot = None
        self.equipped_items[slot] = None
        
        return True, item, f"卸下了{item.get_full_name()}"
    
    def get_total_stats(self) -> ItemStats:
        total = ItemStats()
        
        for item in self.equipped_items.values():
            if item:
                for stat_type, value in item.stats.stats.items():
                    total.add_stat(stat_type, value)
        
        return total
    
    def get_equipped_items_list(self) -> List[Tuple[EquipmentSlot, Optional[ItemInstance]]]:
        return [(slot, item) for slot, item in self.equipped_items.items()]
    
    def get_empty_slots(self) -> List[EquipmentSlot]:
        return [slot for slot, item in self.equipped_items.items() if item is None]
    
    def repair_all(self) -> Tuple[int, int]:
        repaired_count = 0
        total_repaired = 0
        
        for item in self.equipped_items.values():
            if item and item.durability < item.max_durability:
                old_dur = item.durability
                item.repair(item.max_durability - item.durability)
                repaired_count += 1
                total_repaired += item.durability - old_dur
        
        return repaired_count, total_repaired


class ItemFactory:
    
    @staticmethod
    def create_item(item_id: str, **kwargs) -> ItemInstance:
        item_templates = {
            "iron_sword": {
                "name": "铁剑",
                "category": ItemCategory.WEAPON,
                "rarity": ItemRarity.COMMON,
                "icon": "⚔️",
                "stats": ItemStats({StatType.ATTACK: 10}),
                "buy_price": 100,
                "sell_price": 50,
                "description": "基础的铁制长剑"
            },
            "steel_sword": {
                "name": "钢剑",
                "category": ItemCategory.WEAPON,
                "rarity": ItemRarity.UNCOMMON,
                "icon": "🗡️",
                "stats": ItemStats({StatType.ATTACK: 25, StatType.CRITICAL: 5}),
                "buy_price": 300,
                "sell_price": 150,
                "description": "精钢打造的利剑"
            },
            "legendary_blade": {
                "name": "传说之刃",
                "category": ItemCategory.WEAPON,
                "rarity": ItemRarity.LEGENDARY,
                "icon": "⚡",
                "stats": ItemStats({StatType.ATTACK: 100, StatType.CRITICAL: 20, StatType.SPEED: 10}),
                "buy_price": 10000,
                "sell_price": 5000,
                "description": "传说中的神兵利器",
                "effects": [ItemEffect("lightning_strike", "雷击", "攻击时有几率触发闪电", "attack", 50, 0, 0, 0.1)]
            },
            "leather_armor": {
                "name": "皮甲",
                "category": ItemCategory.ARMOR,
                "rarity": ItemRarity.COMMON,
                "icon": "🥋",
                "stats": ItemStats({StatType.DEFENSE: 15}),
                "buy_price": 150,
                "sell_price": 75,
                "description": "简单的皮革护甲"
            },
            "plate_armor": {
                "name": "板甲",
                "category": ItemCategory.ARMOR,
                "rarity": ItemRarity.RARE,
                "icon": "🛡️",
                "stats": ItemStats({StatType.DEFENSE: 50, StatType.VITALITY: 20}),
                "buy_price": 800,
                "sell_price": 400,
                "description": "重型板甲，提供优秀防护"
            },
            "health_potion": {
                "name": "生命药水",
                "category": ItemCategory.CONSUMABLE,
                "rarity": ItemRarity.COMMON,
                "icon": "❤️",
                "max_stack": 20,
                "buy_price": 50,
                "sell_price": 25,
                "description": "恢复50点生命值",
                "effects": [ItemEffect("heal", "治疗", "恢复生命值", "use", 50)]
            },
            "mana_potion": {
                "name": "魔力药水",
                "category": ItemCategory.CONSUMABLE,
                "rarity": ItemRarity.COMMON,
                "icon": "💙",
                "max_stack": 20,
                "buy_price": 50,
                "sell_price": 25,
                "description": "恢复50点魔力值",
                "effects": [ItemEffect("mana", "恢复魔力", "恢复魔力值", "use", 50)]
            },
            "iron_ore": {
                "name": "铁矿石",
                "category": ItemCategory.MATERIAL,
                "rarity": ItemRarity.COMMON,
                "icon": "⛏️",
                "max_stack": 99,
                "buy_price": 10,
                "sell_price": 5,
                "description": "基础的矿石材料"
            },
            "gold_ore": {
                "name": "金矿石",
                "category": ItemCategory.MATERIAL,
                "rarity": ItemRarity.RARE,
                "icon": "🪙",
                "max_stack": 99,
                "buy_price": 100,
                "sell_price": 50,
                "description": "珍贵的金矿石"
            },
            "crystal": {
                "name": "水晶",
                "category": ItemCategory.MATERIAL,
                "rarity": ItemRarity.EPIC,
                "icon": "💎",
                "max_stack": 50,
                "buy_price": 500,
                "sell_price": 250,
                "description": "蕴含魔力的水晶"
            },
            "treasure_chest": {
                "name": "宝箱",
                "category": ItemCategory.TREASURE,
                "rarity": ItemRarity.RARE,
                "icon": "📦",
                "buy_price": 0,
                "sell_price": 100,
                "description": "打开可获得随机物品",
                "effects": [ItemEffect("open_chest", "开启宝箱", "随机获得物品", "use", 0)]
            },
        }
        
        template = item_templates.get(item_id)
        if not template:
            template = {
                "name": item_id,
                "category": ItemCategory.MISC,
                "rarity": ItemRarity.COMMON,
                "icon": "📦",
                "buy_price": 10,
                "sell_price": 5,
                "description": "未知物品"
            }
        
        instance_id = f"{item_id}_{random.randint(100000, 999999)}"
        
        return ItemInstance(
            instance_id=instance_id,
            item_id=item_id,
            name=template.get("name", item_id),
            category=template.get("category", ItemCategory.MISC),
            rarity=template.get("rarity", ItemRarity.COMMON),
            icon=template.get("icon", "📦"),
            stack_size=kwargs.get("stack_size", 1),
            max_stack=template.get("max_stack", 1),
            stats=template.get("stats", ItemStats()),
            effects=template.get("effects", []),
            buy_price=template.get("buy_price", 0),
            sell_price=template.get("sell_price", 0),
            description=template.get("description", ""),
            flavor_text=template.get("flavor_text", ""),
            created_time=kwargs.get("created_time", 0)
        )


class MMORPGInventorySystem:
    
    def __init__(self, player_name: str = "Player"):
        self.player_name = player_name
        
        self.main_inventory = StorageContainer("main", "背包", "🎒", max_slots=40)
        self.equipment = EquipmentManager()
        self.bank = BankAccount("bank_1", player_name)
        
        self.gold: int = 1000
        self.current_day: int = 1
        
        self.category_filters: Set[ItemCategory] = set()
        self.sort_mode: str = "name"
        
        self.transaction_history: List[Dict] = []
    
    def add_item(self, item: ItemInstance) -> Tuple[bool, int, str]:
        success, amount, message = self.main_inventory.add_item(item)
        
        if success:
            self._log_transaction("add", item.item_id, amount)
        
        return success, amount, message
    
    def remove_item(self, slot_index: int, amount: int = 1) -> Tuple[bool, Optional[ItemInstance], str]:
        success, item, message = self.main_inventory.remove_item(slot_index, amount)
        
        if success and item:
            self._log_transaction("remove", item.item_id, amount)
        
        return success, item, message
    
    def use_item(self, slot_index: int) -> Tuple[bool, str, Dict]:
        item = self.main_inventory.get_item_at(slot_index)
        if not item:
            return False, "没有找到物品", {}
        
        if item.category not in [ItemCategory.CONSUMABLE, ItemCategory.FOOD]:
            return False, "该物品无法使用", {}
        
        effects_result = {}
        for effect in item.effects:
            effects_result[effect.effect_id] = effect.value
        
        success, _, message = self.remove_item(slot_index, 1)
        
        if success:
            self._log_transaction("use", item.item_id, 1)
            return True, f"使用了{item.name}", effects_result
        
        return False, message, {}
    
    def equip_item(self, slot_index: int, target_slot: Optional[EquipmentSlot] = None) -> Tuple[bool, str]:
        item = self.main_inventory.get_item_at(slot_index)
        if not item:
            return False, "没有找到物品"
        
        if not item.can_equip():
            return False, "该物品无法装备"
        
        success, old_item, message = self.equipment.equip(item, target_slot)
        
        if success:
            self.main_inventory.remove_item(slot_index, item.stack_size)
            
            if old_item:
                self.main_inventory.add_item(old_item)
            
            self._log_transaction("equip", item.item_id, 1)
        
        return success, message
    
    def unequip_item(self, slot: EquipmentSlot) -> Tuple[bool, str]:
        success, item, message = self.equipment.unequip(slot)
        
        if success and item:
            add_success, _, add_message = self.main_inventory.add_item(item)
            if not add_success:
                self.equipment.equip(item, slot)
                return False, "背包已满，无法卸下装备"
            
            self._log_transaction("unequip", item.item_id, 1)
        
        return success, message
    
    def enhance_item(self, slot_index: int) -> Tuple[bool, str]:
        item = self.main_inventory.get_item_at(slot_index)
        if not item:
            return False, "没有找到物品"
        
        enhance_cost = (item.enhancement_level + 1) * 100
        if self.gold < enhance_cost:
            return False, f"金币不足，需要{enhance_cost}金币"
        
        self.gold -= enhance_cost
        success, message = item.enhance()
        
        self._log_transaction("enhance", item.item_id, 1, {"cost": enhance_cost})
        
        return success, message
    
    def repair_item(self, slot_index: int) -> Tuple[bool, str, int]:
        item = self.main_inventory.get_item_at(slot_index)
        if not item:
            return False, "没有找到物品", 0
        
        repair_cost = (item.max_durability - item.durability) * 2
        if self.gold < repair_cost:
            return False, f"金币不足，需要{repair_cost}金币", 0
        
        self.gold -= repair_cost
        success, message = item.repair()
        
        self._log_transaction("repair", item.item_id, 1, {"cost": repair_cost})
        
        return success, message, repair_cost
    
    def sell_item(self, slot_index: int, amount: int = 1) -> Tuple[bool, int, str]:
        item = self.main_inventory.get_item_at(slot_index)
        if not item:
            return False, 0, "没有找到物品"
        
        if item.is_bound:
            return False, 0, "绑定物品无法出售"
        
        actual_amount = min(amount, item.stack_size)
        total_price = item.get_sell_price() * actual_amount
        
        success, removed_item, message = self.remove_item(slot_index, actual_amount)
        
        if success:
            self.gold += total_price
            self._log_transaction("sell", item.item_id, actual_amount, {"price": total_price})
            return True, total_price, f"出售了{actual_amount}个{item.name}，获得{total_price}金币"
        
        return False, 0, message
    
    def buy_item(self, item_id: str, amount: int = 1) -> Tuple[bool, str]:
        template_item = ItemFactory.create_item(item_id)
        
        total_price = template_item.buy_price * amount
        if self.gold < total_price:
            return False, f"金币不足，需要{total_price}金币"
        
        template_item.stack_size = amount
        success, added, message = self.add_item(template_item)
        
        if success:
            self.gold -= template_item.buy_price * added
            self._log_transaction("buy", item_id, added, {"price": template_item.buy_price * added})
            return True, f"购买了{added}个{template_item.name}"
        
        return False, message
    
    def deposit_to_bank(self, slot_index: int, amount: int = 1) -> Tuple[bool, str]:
        success, item, message = self.main_inventory.remove_item(slot_index, amount)
        
        if success and item:
            bank_success, _, bank_message = self.bank.storage.add_item(item)
            if bank_success:
                self._log_transaction("deposit", item.item_id, amount)
                return True, f"存入了{amount}个{item.name}到银行"
            else:
                self.main_inventory.add_item(item)
                return False, bank_message
        
        return False, message
    
    def withdraw_from_bank(self, slot_index: int, amount: int = 1) -> Tuple[bool, str]:
        success, item, message = self.bank.storage.remove_item(slot_index, amount)
        
        if success and item:
            inv_success, _, inv_message = self.main_inventory.add_item(item)
            if inv_success:
                self._log_transaction("withdraw", item.item_id, amount)
                return True, f"取出了{amount}个{item.name}"
            else:
                self.bank.storage.add_item(item)
                return False, inv_message
        
        return False, message
    
    def deposit_gold(self, amount: int) -> Tuple[bool, str]:
        if amount > self.gold:
            return False, "金币不足"
        
        success, message = self.bank.deposit_gold(amount)
        if success:
            self.gold -= amount
            self._log_transaction("deposit_gold", "gold", amount)
        
        return success, message
    
    def withdraw_gold(self, amount: int) -> Tuple[bool, str]:
        success, actual, message = self.bank.withdraw_gold(amount)
        if success:
            self.gold += actual
            self._log_transaction("withdraw_gold", "gold", actual)
        
        return success, message
    
    def collect_bank_interest(self) -> Tuple[bool, int, str]:
        success, interest, message = self.bank.collect_interest(self.current_day)
        if success:
            self._log_transaction("interest", "gold", interest)
        return success, interest, message
    
    def sort_inventory(self, mode: str = "name"):
        self.sort_mode = mode
        
        if mode == "name":
            self.main_inventory.sort_by_name()
        elif mode == "rarity":
            self.main_inventory.sort_by_rarity()
        elif mode == "category":
            self.main_inventory.sort_by_category()
    
    def filter_by_category(self, category: Optional[ItemCategory] = None):
        if category:
            self.category_filters.add(category)
        else:
            self.category_filters.clear()
    
    def get_filtered_items(self) -> List[Tuple[int, ItemInstance]]:
        items = []
        
        for i, slot in enumerate(self.main_inventory.slots):
            if not slot.is_empty():
                if self.category_filters:
                    if slot.item.category in self.category_filters:
                        items.append((i, slot.item))
                else:
                    items.append((i, slot.item))
        
        return items
    
    def get_inventory_value(self) -> int:
        total = 0
        for slot in self.main_inventory.slots:
            if not slot.is_empty():
                total += slot.item.get_sell_price() * slot.item.stack_size
        return total
    
    def get_equipment_summary(self) -> Dict:
        total_stats = self.equipment.get_total_stats()
        
        return {
            "total_power": total_stats.get_total_power(),
            "stats": {stat.value: value for stat, value in total_stats.stats.items()},
            "equipped_count": sum(1 for item in self.equipment.equipped_items.values() if item is not None),
            "empty_slots": [slot.value for slot in self.equipment.get_empty_slots()]
        }
    
    def get_full_status(self) -> Dict:
        return {
            "gold": self.gold,
            "bank_gold": self.bank.gold,
            "inventory_used": self.main_inventory.get_used_slots(),
            "inventory_total": self.main_inventory.max_slots,
            "bank_used": self.bank.storage.get_used_slots(),
            "bank_total": self.bank.storage.max_slots,
            "equipment": self.get_equipment_summary(),
            "total_value": self.gold + self.bank.gold + self.get_inventory_value()
        }
    
    def _log_transaction(self, action: str, item_id: str, amount: int, extra: Dict = None):
        self.transaction_history.append({
            "day": self.current_day,
            "action": action,
            "item_id": item_id,
            "amount": amount,
            "extra": extra or {}
        })
        
        if len(self.transaction_history) > 100:
            self.transaction_history = self.transaction_history[-100:]
    
    def advance_day(self):
        self.current_day += 1
    
    def get_save_data(self) -> Dict:
        return {
            "player_name": self.player_name,
            "gold": self.gold,
            "current_day": self.current_day,
            "bank": {
                "gold": self.bank.gold,
                "last_interest_day": self.bank.last_interest_day
            },
            "inventory": [
                {
                    "slot": i,
                    "item_id": slot.item.item_id,
                    "stack_size": slot.item.stack_size,
                    "durability": slot.item.durability,
                    "enhancement_level": slot.item.enhancement_level,
                    "is_bound": slot.item.is_bound
                } for i, slot in enumerate(self.main_inventory.slots) if not slot.is_empty()
            ],
            "equipment": {
                slot.value: {
                    "item_id": item.item_id,
                    "durability": item.durability,
                    "enhancement_level": item.enhancement_level
                } for slot, item in self.equipment.equipped_items.items() if item is not None
            },
            "bank_storage": [
                {
                    "slot": i,
                    "item_id": slot.item.item_id,
                    "stack_size": slot.item.stack_size
                } for i, slot in enumerate(self.bank.storage.slots) if not slot.is_empty()
            ]
        }
    
    def load_save_data(self, data: Dict):
        self.player_name = data.get("player_name", "Player")
        self.gold = data.get("gold", 1000)
        self.current_day = data.get("current_day", 1)
        
        bank_data = data.get("bank", {})
        self.bank.gold = bank_data.get("gold", 0)
        self.bank.last_interest_day = bank_data.get("last_interest_day", 0)
        
        for item_data in data.get("inventory", []):
            item = ItemFactory.create_item(item_data["item_id"])
            item.stack_size = item_data.get("stack_size", 1)
            item.durability = item_data.get("durability", 100)
            item.enhancement_level = item_data.get("enhancement_level", 0)
            item.is_bound = item_data.get("is_bound", False)
            
            slot_idx = item_data["slot"]
            if 0 <= slot_idx < len(self.main_inventory.slots):
                self.main_inventory.slots[slot_idx].item = item
        
        for slot_str, item_data in data.get("equipment", {}).items():
            slot = EquipmentSlot(slot_str)
            item = ItemFactory.create_item(item_data["item_id"])
            item.durability = item_data.get("durability", 100)
            item.enhancement_level = item_data.get("enhancement_level", 0)
            item.is_equipped = True
            item.equipped_slot = slot
            self.equipment.equipped_items[slot] = item
        
        for item_data in data.get("bank_storage", []):
            item = ItemFactory.create_item(item_data["item_id"])
            item.stack_size = item_data.get("stack_size", 1)
            
            slot_idx = item_data["slot"]
            if 0 <= slot_idx < len(self.bank.storage.slots):
                self.bank.storage.slots[slot_idx].item = item
