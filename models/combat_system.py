"""
生化危机战斗系统模块
提供完整的战斗机制、角色成长体系和装备系统
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import random
import math


class DamageType(Enum):
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    ELECTRIC = "electric"
    TOXIC = "toxic"
    VIRAL = "viral"
    TRUE = "true"


class WeaponType(Enum):
    MELEE = "melee"
    PISTOL = "pistol"
    RIFLE = "rifle"
    SHOTGUN = "shotgun"
    EXPLOSIVE = "explosive"
    SPECIAL = "special"


class ArmorType(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    HAZMAT = "hazmat"
    STEALTH = "stealth"


class SkillType(Enum):
    COMBAT = "combat"
    SURVIVAL = "survival"
    MEDICAL = "medical"
    ENGINEERING = "engineering"
    LEADERSHIP = "leadership"
    STEALTH = "stealth"


class EnemyType(Enum):
    ZOMBIE = "zombie"
    RUNNER = "runner"
    TANK = "tank"
    SPITTER = "spitter"
    STALKER = "stalker"
    BOSS = "boss"
    MUTANT = "mutant"


@dataclass
class Weapon:
    weapon_id: str
    name: str
    weapon_type: WeaponType
    damage: int
    damage_type: DamageType
    range: int
    accuracy: float
    fire_rate: float
    ammo_type: str
    magazine_size: int
    durability: int
    max_durability: int
    level_requirement: int = 1
    special_effects: Dict = field(default_factory=dict)
    description: str = ""
    
    def get_effective_damage(self, attacker_stats: Dict) -> int:
        base_damage = self.damage
        strength_bonus = attacker_stats.get("strength", 0) * 0.5
        weapon_skill = attacker_stats.get(f"{self.weapon_type.value}_skill", 0) * 0.3
        
        effective = base_damage + strength_bonus + weapon_skill
        
        if self.durability < self.max_durability * 0.3:
            effective *= 0.7
        
        return int(effective)
    
    def use(self) -> bool:
        if self.durability <= 0:
            return False
        self.durability -= 1
        return True
    
    def repair(self, amount: int) -> int:
        self.durability = min(self.max_durability, self.durability + amount)
        return self.durability


@dataclass
class Armor:
    armor_id: str
    name: str
    armor_type: ArmorType
    defense: int
    resistance: Dict = field(default_factory=dict)
    durability: int = 100
    max_durability: int = 100
    movement_penalty: float = 0.0
    stealth_penalty: float = 0.0
    level_requirement: int = 1
    special_effects: Dict = field(default_factory=dict)
    description: str = ""
    
    def get_damage_reduction(self, damage_type: DamageType) -> float:
        base_reduction = self.defense / (self.defense + 100)
        type_resistance = self.resistance.get(damage_type.value, 0)
        
        return min(0.9, base_reduction + type_resistance * 0.01)
    
    def absorb_damage(self, damage: int, damage_type: DamageType) -> int:
        reduction = self.get_damage_reduction(damage_type)
        absorbed = int(damage * reduction)
        
        durability_loss = max(1, absorbed // 20)
        self.durability = max(0, self.durability - durability_loss)
        
        return damage - absorbed


@dataclass
class Skill:
    skill_id: str
    name: str
    skill_type: SkillType
    description: str
    max_level: int = 10
    current_level: int = 0
    exp: int = 0
    exp_to_next: int = 100
    effects_per_level: Dict = field(default_factory=dict)
    unlocked_abilities: List[str] = field(default_factory=list)
    
    def add_exp(self, amount: int) -> Tuple[bool, int]:
        self.exp += amount
        leveled_up = False
        levels_gained = 0
        
        while self.exp >= self.exp_to_next and self.current_level < self.max_level:
            self.exp -= self.exp_to_next
            self.current_level += 1
            self.exp_to_next = int(self.exp_to_next * 1.5)
            leveled_up = True
            levels_gained += 1
        
        return leveled_up, levels_gained
    
    def get_effect(self, effect_name: str) -> float:
        base = self.effects_per_level.get(effect_name, 0)
        return base * self.current_level


@dataclass
class Enemy:
    enemy_id: str
    name: str
    enemy_type: EnemyType
    level: int
    health: int
    max_health: int
    damage: int
    damage_type: DamageType
    armor: int
    speed: float
    detection_range: int
    attack_range: int
    special_abilities: List[str] = field(default_factory=list)
    loot_table: Dict = field(default_factory=dict)
    exp_reward: int = 0
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def take_damage(self, damage: int, damage_type: DamageType) -> int:
        effective_damage = max(1, damage - self.armor)
        
        if damage_type == DamageType.FIRE and "fire_weakness" in self.special_abilities:
            effective_damage = int(effective_damage * 1.5)
        
        self.health = max(0, self.health - effective_damage)
        return effective_damage
    
    def attack(self) -> Tuple[int, DamageType]:
        damage_variance = random.uniform(0.8, 1.2)
        return int(self.damage * damage_variance), self.damage_type


WEAPONS = {
    "pipe": Weapon(
        weapon_id="pipe",
        name="铁管",
        weapon_type=WeaponType.MELEE,
        damage=15,
        damage_type=DamageType.PHYSICAL,
        range=1,
        accuracy=0.9,
        fire_rate=1.0,
        ammo_type="",
        magazine_size=0,
        durability=50,
        max_durability=50,
        description="一根生锈的铁管，聊胜于无。"
    ),
    "pistol": Weapon(
        weapon_id="pistol",
        name="手枪",
        weapon_type=WeaponType.PISTOL,
        damage=25,
        damage_type=DamageType.PHYSICAL,
        range=15,
        accuracy=0.8,
        fire_rate=2.0,
        ammo_type="pistol_ammo",
        magazine_size=12,
        durability=100,
        max_durability=100,
        level_requirement=2,
        description="标准9mm手枪，可靠的自卫武器。"
    ),
    "shotgun": Weapon(
        weapon_id="shotgun",
        name="霰弹枪",
        weapon_type=WeaponType.SHOTGUN,
        damage=60,
        damage_type=DamageType.PHYSICAL,
        range=8,
        accuracy=0.6,
        fire_rate=0.8,
        ammo_type="shotgun_ammo",
        magazine_size=6,
        durability=80,
        max_durability=80,
        level_requirement=5,
        special_effects={"spread": 0.3, "knockback": 0.5},
        description="近距离毁灭性武器，对付感染者非常有效。"
    ),
    "assault_rifle": Weapon(
        weapon_id="assault_rifle",
        name="突击步枪",
        weapon_type=WeaponType.RIFLE,
        damage=35,
        damage_type=DamageType.PHYSICAL,
        range=30,
        accuracy=0.75,
        fire_rate=5.0,
        ammo_type="rifle_ammo",
        magazine_size=30,
        durability=120,
        max_durability=120,
        level_requirement=8,
        special_effects={"full_auto": True},
        description="军用突击步枪，火力强大。"
    ),
    "flamethrower": Weapon(
        weapon_id="flamethrower",
        name="火焰喷射器",
        weapon_type=WeaponType.SPECIAL,
        damage=40,
        damage_type=DamageType.FIRE,
        range=10,
        accuracy=0.9,
        fire_rate=3.0,
        ammo_type="fuel",
        magazine_size=50,
        durability=60,
        max_durability=60,
        level_requirement=12,
        special_effects={"burning": 3, "area_damage": True},
        description="对付感染者群的终极武器。"
    ),
    "sniper_rifle": Weapon(
        weapon_id="sniper_rifle",
        name="狙击步枪",
        weapon_type=WeaponType.RIFLE,
        damage=120,
        damage_type=DamageType.PHYSICAL,
        range=100,
        accuracy=0.95,
        fire_rate=0.5,
        ammo_type="rifle_ammo",
        magazine_size=5,
        durability=100,
        max_durability=100,
        level_requirement=10,
        special_effects={"headshot_bonus": 2.0, "armor_pierce": 0.5},
        description="远程精确打击武器，一击致命。"
    ),
}

ARMORS = {
    "civilian_clothes": Armor(
        armor_id="civilian_clothes",
        name="平民服装",
        armor_type=ArmorType.LIGHT,
        defense=5,
        description="普通的衣服，几乎没有防护作用。"
    ),
    "leather_jacket": Armor(
        armor_id="leather_jacket",
        name="皮夹克",
        armor_type=ArmorType.LIGHT,
        defense=15,
        resistance={"physical": 5},
        level_requirement=1,
        description="提供基本防护的皮夹克。"
    ),
    "tactical_vest": Armor(
        armor_id="tactical_vest",
        name="战术背心",
        armor_type=ArmorType.MEDIUM,
        defense=35,
        resistance={"physical": 15, "viral": 10},
        movement_penalty=0.05,
        level_requirement=5,
        description="军规战术背心，提供良好的防护。"
    ),
    "hazmat_suit": Armor(
        armor_id="hazmat_suit",
        name="防化服",
        armor_type=ArmorType.HAZMAT,
        defense=20,
        resistance={"toxic": 80, "viral": 60, "fire": 20},
        movement_penalty=0.15,
        stealth_penalty=0.3,
        level_requirement=8,
        special_effects={"infection_immunity": 0.8},
        description="完全密封的防护服，抵御病毒和毒素。"
    ),
    "heavy_armor": Armor(
        armor_id="heavy_armor",
        name="重型护甲",
        armor_type=ArmorType.HEAVY,
        defense=60,
        resistance={"physical": 40, "fire": 20, "toxic": 10},
        movement_penalty=0.25,
        stealth_penalty=0.5,
        level_requirement=12,
        description="重型军用护甲，提供最大防护但影响机动性。"
    ),
}

ENEMIES = {
    "zombie": Enemy(
        enemy_id="zombie",
        name="感染者",
        enemy_type=EnemyType.ZOMBIE,
        level=1,
        health=50,
        max_health=50,
        damage=10,
        damage_type=DamageType.PHYSICAL,
        armor=0,
        speed=0.5,
        detection_range=10,
        attack_range=1,
        loot_table={"rotten_flesh": 0.5, "coin": 0.3},
        exp_reward=10
    ),
    "runner": Enemy(
        enemy_id="runner",
        name="疾行者",
        enemy_type=EnemyType.RUNNER,
        level=3,
        health=40,
        max_health=40,
        damage=15,
        damage_type=DamageType.PHYSICAL,
        armor=0,
        speed=1.5,
        detection_range=15,
        attack_range=1,
        special_abilities=["sprint", "pack_tactics"],
        loot_table={"runner_claw": 0.3, "coin": 0.4},
        exp_reward=25
    ),
    "tank": Enemy(
        enemy_id="tank",
        name="坦克",
        enemy_type=EnemyType.TANK,
        level=8,
        health=300,
        max_health=300,
        damage=40,
        damage_type=DamageType.PHYSICAL,
        armor=30,
        speed=0.3,
        detection_range=8,
        attack_range=2,
        special_abilities=["charge", "stomp", "fire_weakness"],
        loot_table={"tank_plate": 0.2, "rare_material": 0.1},
        exp_reward=100
    ),
    "spitter": Enemy(
        enemy_id="spitter",
        name="喷射者",
        enemy_type=EnemyType.SPITTER,
        level=5,
        health=60,
        max_health=60,
        damage=25,
        damage_type=DamageType.TOXIC,
        armor=0,
        speed=0.7,
        detection_range=20,
        attack_range=15,
        special_abilities=["ranged_attack", "acid_pool"],
        loot_table={"acid_gland": 0.3, "toxin": 0.2},
        exp_reward=40
    ),
    "stalker": Enemy(
        enemy_id="stalker",
        name="潜行者",
        enemy_type=EnemyType.STALKER,
        level=6,
        health=80,
        max_health=80,
        damage=35,
        damage_type=DamageType.PHYSICAL,
        armor=10,
        speed=1.2,
        detection_range=25,
        attack_range=1,
        special_abilities=["stealth", "backstab", "fear"],
        loot_table={"stalker_claw": 0.25, "stealth_cloak": 0.05},
        exp_reward=60
    ),
    "mutant_boss": Enemy(
        enemy_id="mutant_boss",
        name="变异首领",
        enemy_type=EnemyType.BOSS,
        level=15,
        health=1000,
        max_health=1000,
        damage=80,
        damage_type=DamageType.VIRAL,
        armor=50,
        speed=0.8,
        detection_range=30,
        attack_range=3,
        special_abilities=["regeneration", "summon", "rage", "fire_weakness"],
        loot_table={"boss_core": 1.0, "legendary_weapon_part": 0.3},
        exp_reward=500
    ),
}


class CombatSystem:
    
    def __init__(self):
        self.weapons = WEAPONS.copy()
        self.armors = ARMORS.copy()
        self.enemies = ENEMIES.copy()
        self.active_combat: Optional[Dict] = None
        self.combat_log: List[str] = []
        self.on_combat_end: Optional[Callable] = None
    
    def start_combat(self, player_stats: Dict, enemy_ids: List[str]) -> Dict:
        enemies = []
        for eid in enemy_ids:
            if eid in self.enemies:
                enemy = self.enemies[eid]
                enemies.append(Enemy(
                    enemy_id=enemy.enemy_id,
                    name=enemy.name,
                    enemy_type=enemy.enemy_type,
                    level=enemy.level,
                    health=enemy.max_health,
                    max_health=enemy.max_health,
                    damage=enemy.damage,
                    damage_type=enemy.damage_type,
                    armor=enemy.armor,
                    speed=enemy.speed,
                    detection_range=enemy.detection_range,
                    attack_range=enemy.attack_range,
                    special_abilities=enemy.special_abilities.copy(),
                    loot_table=enemy.loot_table.copy(),
                    exp_reward=enemy.exp_reward
                ))
        
        self.active_combat = {
            "player": player_stats,
            "enemies": enemies,
            "turn": 0,
            "log": []
        }
        
        return {
            "started": True,
            "enemies": [{"name": e.name, "level": e.level, "health": e.health} for e in enemies],
            "message": f"战斗开始！遭遇 {len(enemies)} 个敌人！"
        }
    
    def player_attack(self, weapon_id: str, target_index: int) -> Dict:
        if not self.active_combat:
            return {"success": False, "message": "没有进行中的战斗"}
        
        weapon = self.weapons.get(weapon_id)
        if not weapon:
            return {"success": False, "message": "未知武器"}
        
        enemies = self.active_combat["enemies"]
        if target_index >= len(enemies):
            return {"success": False, "message": "无效目标"}
        
        target = enemies[target_index]
        if not target.is_alive():
            return {"success": False, "message": "目标已死亡"}
        
        hit_chance = weapon.accuracy
        if random.random() > hit_chance:
            self.active_combat["log"].append(f"攻击 {target.name} 未命中！")
            return {"success": True, "hit": False, "message": "未命中！"}
        
        damage = weapon.get_effective_damage(self.active_combat["player"])
        
        if "headshot_bonus" in weapon.special_effects and random.random() < 0.1:
            damage = int(damage * weapon.special_effects["headshot_bonus"])
            self.active_combat["log"].append("💥 暴击！")
        
        actual_damage = target.take_damage(damage, weapon.damage_type)
        
        weapon.use()
        
        self.active_combat["log"].append(f"对 {target.name} 造成 {actual_damage} 点伤害！")
        
        result = {
            "success": True,
            "hit": True,
            "damage": actual_damage,
            "target": target.name,
            "target_remaining_health": target.health,
            "target_alive": target.is_alive()
        }
        
        if not target.is_alive():
            result["kill"] = True
            result["exp_reward"] = target.exp_reward
            result["loot"] = self._generate_loot(target)
            self.active_combat["log"].append(f"💀 {target.name} 被消灭！")
        
        return result
    
    def enemy_turn(self) -> Dict:
        if not self.active_combat:
            return {"success": False, "message": "没有进行中的战斗"}
        
        results = []
        total_damage = 0
        
        for enemy in self.active_combat["enemies"]:
            if not enemy.is_alive():
                continue
            
            if random.random() < 0.1:
                self.active_combat["log"].append(f"{enemy.name} 的攻击落空！")
                continue
            
            damage, damage_type = enemy.attack()
            
            player_armor_id = self.active_combat["player"].get("armor_id")
            if player_armor_id and player_armor_id in self.armors:
                armor = self.armors[player_armor_id]
                damage = armor.absorb_damage(damage, damage_type)
            
            total_damage += damage
            results.append({
                "attacker": enemy.name,
                "damage": damage,
                "damage_type": damage_type.value
            })
            self.active_combat["log"].append(f"{enemy.name} 对你造成 {damage} 点伤害！")
        
        self.active_combat["turn"] += 1
        
        return {
            "success": True,
            "attacks": results,
            "total_damage": total_damage,
            "turn": self.active_combat["turn"]
        }
    
    def _generate_loot(self, enemy: Enemy) -> Dict:
        loot = {}
        for item_id, chance in enemy.loot_table.items():
            if random.random() < chance:
                loot[item_id] = random.randint(1, 3)
        return loot
    
    def check_combat_end(self) -> Dict:
        if not self.active_combat:
            return {"ended": True, "result": "no_combat"}
        
        enemies_alive = any(e.is_alive() for e in self.active_combat["enemies"])
        player_alive = self.active_combat["player"].get("health", 0) > 0
        
        if not enemies_alive:
            total_exp = sum(e.exp_reward for e in self.active_combat["enemies"])
            all_loot = {}
            for e in self.active_combat["enemies"]:
                for item, count in self._generate_loot(e).items():
                    all_loot[item] = all_loot.get(item, 0) + count
            
            result = {
                "ended": True,
                "result": "victory",
                "exp_gained": total_exp,
                "loot": all_loot,
                "turns": self.active_combat["turn"],
                "log": self.active_combat["log"]
            }
            
            if self.on_combat_end:
                self.on_combat_end(result)
            
            self.active_combat = None
            return result
        
        if not player_alive:
            result = {
                "ended": True,
                "result": "defeat",
                "turns": self.active_combat["turn"],
                "log": self.active_combat["log"]
            }
            
            if self.on_combat_end:
                self.on_combat_end(result)
            
            self.active_combat = None
            return result
        
        return {"ended": False}
    
    def try_escape(self) -> Dict:
        if not self.active_combat:
            return {"success": False, "message": "没有进行中的战斗"}
        
        player_speed = self.active_combat["player"].get("speed", 1.0)
        enemy_speeds = [e.speed for e in self.active_combat["enemies"] if e.is_alive()]
        avg_enemy_speed = sum(enemy_speeds) / len(enemy_speeds) if enemy_speeds else 0
        
        escape_chance = 0.3 + (player_speed - avg_enemy_speed) * 0.2
        escape_chance = max(0.1, min(0.8, escape_chance))
        
        if random.random() < escape_chance:
            self.active_combat = None
            return {"success": True, "message": "成功逃脱！"}
        else:
            return {"success": False, "message": "逃脱失败！"}


class CharacterGrowthSystem:
    
    SKILL_TEMPLATES = {
        "combat": Skill(
            skill_id="combat",
            name="⚔️ 战斗技巧",
            skill_type=SkillType.COMBAT,
            description="提升战斗能力和武器伤害",
            effects_per_level={"damage_bonus": 3, "accuracy_bonus": 0.02}
        ),
        "survival": Skill(
            skill_id="survival",
            name="🏕️ 生存技能",
            skill_type=SkillType.SURVIVAL,
            description="提升资源收集效率和生存能力",
            effects_per_level={"scavenge_bonus": 0.1, "stamina_regen": 0.05}
        ),
        "medical": Skill(
            skill_id="medical",
            name="💊 医疗知识",
            skill_type=SkillType.MEDICAL,
            description="提升治疗效果和抗感染能力",
            effects_per_level={"heal_bonus": 5, "infection_resist": 0.05}
        ),
        "engineering": Skill(
            skill_id="engineering",
            name="🔧 工程技术",
            skill_type=SkillType.ENGINEERING,
            description="提升制造和修理能力",
            effects_per_level={"craft_bonus": 0.1, "repair_bonus": 0.1}
        ),
        "leadership": Skill(
            skill_id="leadership",
            name="👥 领导能力",
            skill_type=SkillType.LEADERSHIP,
            description="提升团队效率和士气",
            effects_per_level={"team_bonus": 0.05, "morale_bonus": 0.1}
        ),
        "stealth": Skill(
            skill_id="stealth",
            name="🥷 潜行技巧",
            skill_type=SkillType.STEALTH,
            description="提升潜行和闪避能力",
            effects_per_level={"stealth_bonus": 0.08, "dodge_bonus": 0.03}
        ),
    }
    
    def __init__(self):
        self.level: int = 1
        self.exp: int = 0
        self.exp_to_next: int = 100
        self.skill_points: int = 0
        self.skills: Dict[str, Skill] = {}
        self.stats: Dict = {
            "health": 100,
            "max_health": 100,
            "stamina": 100,
            "max_stamina": 100,
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "endurance": 10,
            "luck": 5
        }
        self.stat_points: int = 0
        
        self._init_skills()
    
    def _init_skills(self):
        for skill_id, template in self.SKILL_TEMPLATES.items():
            self.skills[skill_id] = Skill(
                skill_id=template.skill_id,
                name=template.name,
                skill_type=template.skill_type,
                description=template.description,
                effects_per_level=template.effects_per_level.copy()
            )
    
    def add_exp(self, amount: int) -> Dict:
        self.exp += amount
        levels_gained = 0
        
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            levels_gained += 1
            self.exp_to_next = int(self.exp_to_next * 1.3)
            self.skill_points += 1
            self.stat_points += 2
            
            self.stats["max_health"] += 10
            self.stats["max_stamina"] += 5
        
        return {
            "levels_gained": levels_gained,
            "new_level": self.level,
            "skill_points": self.skill_points,
            "stat_points": self.stat_points
        }
    
    def upgrade_skill(self, skill_id: str) -> Tuple[bool, str]:
        if skill_id not in self.skills:
            return False, "未知技能"
        
        if self.skill_points <= 0:
            return False, "技能点不足"
        
        skill = self.skills[skill_id]
        if skill.current_level >= skill.max_level:
            return False, "技能已满级"
        
        skill.current_level += 1
        self.skill_points -= 1
        
        return True, f"{skill.name} 提升到 {skill.current_level} 级！"
    
    def upgrade_stat(self, stat_name: str) -> Tuple[bool, str]:
        if stat_name not in self.stats:
            return False, "未知属性"
        
        if self.stat_points <= 0:
            return False, "属性点不足"
        
        self.stats[stat_name] += 1
        self.stat_points -= 1
        
        return True, f"{stat_name} 提升到 {self.stats[stat_name]}！"
    
    def get_skill_effect(self, skill_id: str, effect_name: str) -> float:
        if skill_id not in self.skills:
            return 0
        return self.skills[skill_id].get_effect(effect_name)
    
    def get_total_power(self) -> int:
        base = self.level * 10
        stats_power = sum(self.stats.values()) // 5
        skills_power = sum(s.current_level * 5 for s in self.skills.values())
        
        return base + stats_power + skills_power
    
    def get_level_info(self) -> Dict:
        return {
            "level": self.level,
            "exp": self.exp,
            "exp_to_next": self.exp_to_next,
            "exp_progress": self.exp / self.exp_to_next if self.exp_to_next > 0 else 1.0,
            "skill_points": self.skill_points,
            "stat_points": self.stat_points,
            "total_power": self.get_total_power()
        }
    
    def get_save_data(self) -> Dict:
        return {
            "level": self.level,
            "exp": self.exp,
            "exp_to_next": self.exp_to_next,
            "skill_points": self.skill_points,
            "stat_points": self.stat_points,
            "stats": self.stats.copy(),
            "skills": {
                skill_id: {
                    "level": skill.current_level,
                    "exp": skill.exp
                }
                for skill_id, skill in self.skills.items()
            }
        }
    
    def load_save_data(self, data: Dict):
        self.level = data.get("level", 1)
        self.exp = data.get("exp", 0)
        self.exp_to_next = data.get("exp_to_next", 100)
        self.skill_points = data.get("skill_points", 0)
        self.stat_points = data.get("stat_points", 0)
        
        for stat, value in data.get("stats", {}).items():
            if stat in self.stats:
                self.stats[stat] = value
        
        for skill_id, skill_data in data.get("skills", {}).items():
            if skill_id in self.skills:
                self.skills[skill_id].current_level = skill_data.get("level", 0)
                self.skills[skill_id].exp = skill_data.get("exp", 0)
