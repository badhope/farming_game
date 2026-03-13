#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
策略系统
管理多种策略选择和组合
"""


class StrategySystem:
    """
    策略系统 - 管理玩家的策略选择
    
    策略类型:
    1. 商业策略（如何赚钱）
    2. 投资策略（如何钱生钱）
    3. 社交策略（如何经营人脉）
    4. 政治策略（如何获取权力）
    5. 灰色策略（高风险高回报）
    """
    
    STRATEGIES = {
        # === 商业策略 ===
        "稳扎稳打": {
            "type": "商业",
            "effect": "利润稳定，风险低，增长慢",
            "bonus": {"profit": 1.0, "risk": 0.5, "growth": 0.8},
            "unlock_requirement": "无",
            "description": "老老实实做生意，薄利多销"
        },
        
        "薄利多销": {
            "type": "商业",
            "effect": "销量增加，利润率降低",
            "bonus": {"sales": 1.5, "profit_margin": 0.7},
            "unlock_requirement": "小老板",
            "description": "以价换量，占领市场"
        },
        
        "高端定位": {
            "type": "商业",
            "effect": "利润率提高，销量降低",
            "bonus": {"profit_margin": 1.5, "sales": 0.7},
            "unlock_requirement": "中产阶层",
            "description": "做高端客户，三年不开张，开张吃三年"
        },
        
        "垄断经营": {
            "type": "商业",
            "effect": "超高利润，高风险",
            "bonus": {"profit": 2.0, "risk": 1.5, "reputation": 0.5},
            "unlock_requirement": "富豪阶层",
            "description": "垄断市场，操控价格"
        },
        
        # === 投资策略 ===
        "保守理财": {
            "type": "投资",
            "effect": "稳定收益，低风险",
            "bonus": {"return": 0.05, "risk": 0.2},
            "unlock_requirement": "无",
            "description": "存银行，买国债，稳稳当当"
        },
        
        "股票投机": {
            "type": "投资",
            "effect": "高回报，高风险",
            "bonus": {"return": 0.3, "risk": 0.8},
            "unlock_requirement": "中产阶层",
            "description": "炒股，可能暴富也可能破产"
        },
        
        "房地产投资": {
            "type": "投资",
            "effect": "稳定增值，需要大量资金",
            "bonus": {"return": 0.15, "risk": 0.4},
            "unlock_requirement": "小老板",
            "description": "买房收租，坐等升值"
        },
        
        "风险投资": {
            "type": "投资",
            "effect": "极高回报，极高失败率",
            "bonus": {"return": 2.0, "risk": 0.9},
            "unlock_requirement": "富豪阶层",
            "description": "投资创业公司，十个死九个，成一个就赚翻"
        },
        
        # === 社交策略 ===
        "低调做人": {
            "type": "社交",
            "effect": "减少麻烦，错失机会",
            "bonus": {"trouble": 0.5, "opportunity": 0.7},
            "unlock_requirement": "无",
            "description": "闷声发大财，不惹事"
        },
        
        "高调炫富": {
            "type": "社交",
            "effect": "吸引机会，也吸引麻烦",
            "bonus": {"opportunity": 1.5, "trouble": 1.5, "envy": 0.8},
            "unlock_requirement": "中产阶层",
            "description": "买豪车豪宅，吸引眼球"
        },
        
        "广结善缘": {
            "type": "社交",
            "effect": "人脉增长快，开销大",
            "bonus": {"connections": 1.5, "expense": 1.3},
            "unlock_requirement": "小老板",
            "description": "到处请客送礼，朋友多"
        },
        
        "攀附权贵": {
            "type": "社交",
            "effect": "快速提升阶层，风险高",
            "bonus": {"class_jump": 0.3, "risk": 0.7},
            "unlock_requirement": "富豪阶层",
            "description": "巴结大官大富豪，鸡犬升天"
        },
        
        # === 政治策略 ===
        "合法经营": {
            "type": "政治",
            "effect": "安全，发展慢",
            "bonus": {"safety": 1.0, "growth": 0.8},
            "unlock_requirement": "无",
            "description": "遵纪守法，安心做生意"
        },
        
        "官商勾结": {
            "type": "政治",
            "effect": "快速发展，高风险",
            "bonus": {"growth": 2.0, "corruption_risk": 0.8},
            "unlock_requirement": "小老板",
            "description": "给官员好处，拿项目拿政策"
        },
        
        "政商旋转门": {
            "type": "政治",
            "effect": "左右逢源，极高回报",
            "bonus": {"profit": 3.0, "jail_risk": 0.5},
            "unlock_requirement": "富豪阶层",
            "description": "自己当官，家人经商，权钱交易"
        },
        
        # === 灰色策略 ===
        "偷税漏税": {
            "type": "灰色",
            "effect": "短期暴利，被抓就完蛋",
            "bonus": {"tax_save": 0.5, "jail_risk": 0.3},
            "unlock_requirement": "小老板",
            "description": "做假账，少交税"
        },
        
        "假冒伪劣": {
            "type": "灰色",
            "effect": "成本大降，声誉风险",
            "bonus": {"cost": 0.6, "reputation_risk": 0.7},
            "unlock_requirement": "小商贩",
            "description": "卖假货，成本低利润高"
        },
        
        "内幕交易": {
            "type": "灰色",
            "effect": "稳赚不赔，发现就坐牢",
            "bonus": {"profit": 5.0, "jail_risk": 0.8},
            "unlock_requirement": "大资本家",
            "description": "利用内幕消息炒股"
        }
    }
    
    def get_available_strategies(self, player_class_level):
        """获取可用策略"""
        available = []
        
        for name, strategy in self.STRATEGIES.items():
            if self._is_unlocked(strategy, player_class_level):
                available.append({
                    'name': name,
                    'type': strategy['type'],
                    'description': strategy['description']
                })
                
        return available
        
    def _is_unlocked(self, strategy, class_level):
        """检查策略是否解锁"""
        req = strategy['unlock_requirement']
        
        if req == "无":
            return True
            
        # 简化版：根据阶层等级判断
        class_requirements = {
            "小商贩": 3,
            "小老板": 4,
            "中产阶层": 5,
            "富豪阶层": 6,
            "大资本家": 7
        }
        
        required_level = class_requirements.get(req, 99)
        return class_level >= required_level
        
    def apply_strategy(self, strategy_name, base_value):
        """应用策略加成"""
        if strategy_name not in self.STRATEGIES:
            return base_value
            
        strategy = self.STRATEGIES[strategy_name]
        # 简化版：直接返回加成后的值
        return base_value * strategy['bonus'].get('profit', 1.0)
