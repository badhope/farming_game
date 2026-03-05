"""
动态数值体系模块
提供概率公式、动态平衡算法等数学模型
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import math
import random


class DistributionType(Enum):
    UNIFORM = "uniform"
    NORMAL = "normal"
    LOG_NORMAL = "log_normal"
    EXPONENTIAL = "exponential"
    TRIANGULAR = "triangular"
    BETA = "beta"


@dataclass
class StatModifier:
    name: str
    value: float
    is_percentage: bool = False
    duration: float = -1
    source: str = ""
    
    def is_expired(self, current_time: float) -> bool:
        return self.duration > 0 and current_time > self.duration


@dataclass
class DynamicStat:
    base_value: float
    current_value: float = None
    min_value: float = 0
    max_value: float = float('inf')
    modifiers: List[StatModifier] = field(default_factory=list)
    
    def __post_init__(self):
        if self.current_value is None:
            self.current_value = self.base_value
    
    def get_final_value(self, current_time: float = 0) -> float:
        self.modifiers = [m for m in self.modifiers if not m.is_expired(current_time)]
        
        flat_bonus = 0
        percent_bonus = 0
        
        for mod in self.modifiers:
            if mod.is_percentage:
                percent_bonus += mod.value
            else:
                flat_bonus += mod.value
        
        result = (self.base_value + flat_bonus) * (1 + percent_bonus / 100)
        return max(self.min_value, min(self.max_value, result))
    
    def add_modifier(self, modifier: StatModifier):
        self.modifiers.append(modifier)
    
    def remove_modifier(self, name: str):
        self.modifiers = [m for m in self.modifiers if m.name != name]
    
    def clear_modifiers(self):
        self.modifiers.clear()


class ProbabilityEngine:
    
    @staticmethod
    def uniform_random(min_val: float, max_val: float) -> float:
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def normal_random(mean: float, std_dev: float) -> float:
        return random.gauss(mean, std_dev)
    
    @staticmethod
    def log_normal_random(mean: float, std_dev: float) -> float:
        return random.lognormvariate(mean, std_dev)
    
    @staticmethod
    def exponential_random(lambda_param: float) -> float:
        return random.expovariate(lambda_param)
    
    @staticmethod
    def triangular_random(min_val: float, mode: float, max_val: float) -> float:
        return random.triangular(min_val, max_val, mode)
    
    @staticmethod
    def beta_random(alpha: float, beta: float) -> float:
        return random.betavariate(alpha, beta)
    
    @staticmethod
    def weighted_choice(choices: List[Tuple[any, float]]) -> any:
        total_weight = sum(w for _, w in choices)
        r = random.uniform(0, total_weight)
        
        cumulative = 0
        for choice, weight in choices:
            cumulative += weight
            if r <= cumulative:
                return choice
        
        return choices[-1][0]
    
    @staticmethod
    def chance(probability: float) -> bool:
        return random.random() < probability
    
    @staticmethod
    def critical_hit(base_chance: float, luck_bonus: float = 0) -> Tuple[bool, float]:
        final_chance = min(1.0, base_chance + luck_bonus)
        is_crit = random.random() < final_chance
        
        if is_crit:
            multiplier = 1.5 + random.uniform(0, 0.5)
            return True, multiplier
        return False, 1.0
    
    @staticmethod
    def drop_rate(base_rate: float, luck: float = 0, rarity_modifier: float = 1.0) -> bool:
        adjusted_rate = base_rate * (1 + luck * 0.01) * rarity_modifier
        return random.random() < min(1.0, adjusted_rate)


class DamageCalculator:
    
    @staticmethod
    def physical_damage(attack: float, defense: float, level_diff: int = 0) -> float:
        base_damage = max(1, attack - defense * 0.5)
        
        level_factor = 1 + level_diff * 0.05
        level_factor = max(0.5, min(2.0, level_factor))
        
        variance = random.uniform(0.9, 1.1)
        
        return base_damage * level_factor * variance
    
    @staticmethod
    def magical_damage(spell_power: float, magic_defense: float, element_bonus: float = 1.0) -> float:
        base_damage = spell_power * (100 / (100 + magic_defense))
        
        variance = random.uniform(0.85, 1.15)
        
        return base_damage * element_bonus * variance
    
    @staticmethod
    def true_damage(base_damage: float, variance: float = 0.1) -> float:
        multiplier = random.uniform(1 - variance, 1 + variance)
        return base_damage * multiplier
    
    @staticmethod
    def damage_reduction(armor: float) -> float:
        return armor / (armor + 100)
    
    @staticmethod
    def effective_health(health: float, armor: float) -> float:
        reduction = DamageCalculator.damage_reduction(armor)
        return health / (1 - reduction)


class GrowthCalculator:
    
    @staticmethod
    def linear_growth(base: float, rate: float, level: int) -> float:
        return base + rate * level
    
    @staticmethod
    def exponential_growth(base: float, rate: float, level: int) -> float:
        return base * (rate ** level)
    
    @staticmethod
    def logarithmic_growth(base: float, rate: float, level: int) -> float:
        return base + rate * math.log(level + 1)
    
    @staticmethod
    def sigmoid_growth(base: float, max_val: float, rate: float, level: int) -> float:
        return base + (max_val - base) / (1 + math.exp(-rate * (level - 10)))
    
    @staticmethod
    def diminishing_returns(base: float, rate: float, decay: float, level: int) -> float:
        return base + rate * (1 - math.exp(-decay * level)) / decay
    
    @staticmethod
    def experience_to_level(level: int, base_exp: int = 100, growth_rate: float = 1.5) -> int:
        return int(base_exp * (level ** growth_rate))
    
    @staticmethod
    def crop_growth(base_days: int, fertility: float, weather_bonus: float, 
                    fertilizer_bonus: float) -> int:
        total_bonus = fertility * weather_bonus * fertilizer_bonus
        return max(1, int(base_days / total_bonus))


class EconomyCalculator:
    
    @staticmethod
    def item_price(base_price: float, demand: float, supply: float, 
                   reputation: float = 0) -> float:
        demand_factor = 1 + (demand - 50) / 100
        supply_factor = 1 - (supply - 50) / 100
        reputation_factor = 1 - reputation * 0.001
        
        return base_price * demand_factor * supply_factor * reputation_factor
    
    @staticmethod
    def selling_price(base_price: float, quality: float, market_trend: float = 1.0) -> float:
        quality_multiplier = 0.5 + quality * 0.5
        return base_price * quality_multiplier * market_trend
    
    @staticmethod
    def inflation_adjustment(value: float, days_passed: int, inflation_rate: float = 0.001) -> float:
        return value * (1 + inflation_rate) ** days_passed
    
    @staticmethod
    def compound_interest(principal: float, rate: float, periods: int) -> float:
        return principal * (1 + rate) ** periods
    
    @staticmethod
    def depreciation(base_value: float, age: int, decay_rate: float = 0.1) -> float:
        return base_value * math.exp(-decay_rate * age)


class BalanceSystem:
    
    def __init__(self):
        self.base_values: Dict[str, float] = {}
        self.multipliers: Dict[str, float] = {}
        self.thresholds: Dict[str, Tuple[float, float]] = {}
        self.scaling_factors: Dict[str, float] = {}
    
    def set_base_value(self, name: str, value: float):
        self.base_values[name] = value
    
    def set_multiplier(self, name: str, value: float):
        self.multipliers[name] = value
    
    def set_threshold(self, name: str, min_val: float, max_val: float):
        self.thresholds[name] = (min_val, max_val)
    
    def calculate_scaled_value(self, name: str, level: int) -> float:
        base = self.base_values.get(name, 1)
        multiplier = self.multipliers.get(name, 1)
        scaling = self.scaling_factors.get(name, 1)
        
        return base * (multiplier ** level) * scaling
    
    def clamp_value(self, name: str, value: float) -> float:
        if name in self.thresholds:
            min_val, max_val = self.thresholds[name]
            return max(min_val, min(max_val, value))
        return value
    
    def dynamic_difficulty(self, player_level: int, player_power: float, 
                           base_difficulty: float) -> float:
        expected_power = self.calculate_scaled_value("player_power", player_level)
        power_ratio = player_power / expected_power if expected_power > 0 else 1
        
        difficulty = base_difficulty * power_ratio
        
        return self.clamp_value("difficulty", difficulty)
    
    def reward_scaling(self, base_reward: float, level: int, difficulty: float) -> float:
        level_scale = 1 + level * 0.1
        difficulty_scale = 0.5 + difficulty * 0.5
        
        return base_reward * level_scale * difficulty_scale


class RandomGenerator:
    
    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 999999)
        self.state = self.seed
    
    def next(self) -> float:
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        return self.state / 0x7FFFFFFF
    
    def next_int(self, min_val: int, max_val: int) -> int:
        return min_val + int(self.next() * (max_val - min_val + 1))
    
    def next_float(self, min_val: float, max_val: float) -> float:
        return min_val + self.next() * (max_val - min_val)
    
    def next_bool(self, probability: float = 0.5) -> bool:
        return self.next() < probability
    
    def shuffle(self, items: List) -> List:
        result = items.copy()
        for i in range(len(result) - 1, 0, -1):
            j = self.next_int(0, i)
            result[i], result[j] = result[j], result[i]
        return result
    
    def sample(self, items: List, k: int) -> List:
        shuffled = self.shuffle(items)
        return shuffled[:k]


class DynamicFormula:
    
    @staticmethod
    def evaluate(formula: str, variables: Dict[str, float]) -> float:
        safe_vars = {k: v for k, v in variables.items() if isinstance(v, (int, float))}
        safe_vars.update({
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,
            'exp': math.exp,
            'abs': abs,
            'min': min,
            'max': max,
            'pi': math.pi,
            'e': math.e
        })
        
        try:
            return eval(formula, {"__builtins__": {}}, safe_vars)
        except:
            return 0
    
    @staticmethod
    def create_growth_formula(base: float, rate: float, formula_type: str = "linear") -> str:
        if formula_type == "linear":
            return f"{base} + {rate} * level"
        elif formula_type == "exponential":
            return f"{base} * ({rate} ** level)"
        elif formula_type == "logarithmic":
            return f"{base} + {rate} * log(level + 1)"
        else:
            return f"{base}"
    
    @staticmethod
    def interpolate(start: float, end: float, t: float, easing: str = "linear") -> float:
        t = max(0, min(1, t))
        
        if easing == "linear":
            return start + (end - start) * t
        elif easing == "ease_in":
            return start + (end - start) * t * t
        elif easing == "ease_out":
            return start + (end - start) * (1 - (1 - t) * (1 - t))
        elif easing == "ease_in_out":
            if t < 0.5:
                return start + (end - start) * (2 * t * t)
            else:
                return start + (end - start) * (1 - 2 * (1 - t) * (1 - t))
        elif easing == "bounce":
            if t < 1/2.75:
                return start + (end - start) * (7.5625 * t * t)
            elif t < 2/2.75:
                t -= 1.5/2.75
                return start + (end - start) * (7.5625 * t * t + 0.75)
            elif t < 2.5/2.75:
                t -= 2.25/2.75
                return start + (end - start) * (7.5625 * t * t + 0.9375)
            else:
                t -= 2.625/2.75
                return start + (end - start) * (7.5625 * t * t + 0.984375)
        elif easing == "elastic":
            if t == 0:
                return start
            elif t == 1:
                return end
            else:
                p = 0.3
                s = p / 4
                return start + (end - start) * (math.pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1)
        
        return start + (end - start) * t


class StatSystem:
    
    def __init__(self):
        self.stats: Dict[str, DynamicStat] = {}
        self.formulas: Dict[str, str] = {}
        self.dependencies: Dict[str, List[str]] = {}
    
    def add_stat(self, name: str, base_value: float, min_val: float = 0, 
                 max_val: float = float('inf')):
        self.stats[name] = DynamicStat(
            base_value=base_value,
            min_value=min_val,
            max_value=max_val
        )
    
    def get_stat(self, name: str, current_time: float = 0) -> float:
        if name not in self.stats:
            return 0
        
        stat = self.stats[name]
        base = stat.get_final_value(current_time)
        
        if name in self.formulas:
            variables = {n: self.get_stat(n, current_time) for n in self.dependencies.get(name, [])}
            variables[name] = base
            return DynamicFormula.evaluate(self.formulas[name], variables)
        
        return base
    
    def set_formula(self, name: str, formula: str, dependencies: List[str] = None):
        self.formulas[name] = formula
        self.dependencies[name] = dependencies or []
    
    def modify_stat(self, name: str, modifier: StatModifier):
        if name in self.stats:
            self.stats[name].add_modifier(modifier)
    
    def remove_modifier(self, stat_name: str, modifier_name: str):
        if stat_name in self.stats:
            self.stats[stat_name].remove_modifier(modifier_name)
    
    def update(self, current_time: float):
        for stat in self.stats.values():
            stat.modifiers = [m for m in stat.modifiers if not m.is_expired(current_time)]
    
    def get_all_stats(self, current_time: float = 0) -> Dict[str, float]:
        return {name: self.get_stat(name, current_time) for name in self.stats}
    
    def get_save_data(self) -> Dict:
        return {
            "stats": {
                name: {
                    "base_value": stat.base_value,
                    "current_value": stat.current_value,
                    "min_value": stat.min_value,
                    "max_value": stat.max_value
                }
                for name, stat in self.stats.items()
            },
            "formulas": self.formulas
        }
    
    def load_save_data(self, data: Dict):
        for name, stat_data in data.get("stats", {}).items():
            self.stats[name] = DynamicStat(
                base_value=stat_data.get("base_value", 0),
                current_value=stat_data.get("current_value"),
                min_value=stat_data.get("min_value", 0),
                max_value=stat_data.get("max_value", float('inf'))
            )
        
        self.formulas = data.get("formulas", {})
