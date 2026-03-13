#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
玩家类
管理玩家的所有属性、状态和行为
"""


class Player:
    """
    玩家类 - 管理玩家的所有属性和行为
    """
    
    def __init__(self, name, identity_data):
        # 基础属性
        self.name = name
        self.identity = identity_data['name']
        self.class_level = 1  # 阶层等级（1-8）
        self.current_class = "赤贫阶层"
        
        # 财务属性
        self.cash = identity_data['start_money']
        self.real_estate = 0  # 房产
        self.vehicles = 0  # 车辆
        self.investments = 0  # 投资
        self.loans = 0  # 贷款
        
        # 公司（如果有）
        self.company = None
        
        # 社会属性
        self.connections = identity_data['connections']  # 人脉
        self.reputation = 50  # 声誉（0-100）
        self.health = 100  # 健康
        self.stamina = 100  # 体力
        self.happiness = 50  # 幸福感
        
        # 技能
        self.skills = identity_data['skills']
        self.skill_bonus = identity_data.get('bonus', {})
        
        # 位置
        self.city = "广州"  # 初始城市
        
        # 排名
        self.ranking = 999999
        
    @property
    def total_assets(self):
        """计算总资产"""
        return self.cash + self.real_estate + self.vehicles + self.investments
        
    @property
    def total_liabilities(self):
        """计算总负债"""
        return self.loans
        
    @property
    def net_worth(self):
        """计算净资产"""
        return self.total_assets - self.total_liabilities
        
    def work(self):
        """
        工作赚钱
        收入根据身份和技能有差异
        """
        base_income = 100  # 基础日收入
        
        # 身份加成
        if self.identity == "农民":
            base_income = 80
        elif self.identity == "小镇青年":
            base_income = 120
        elif self.identity == "大学生":
            base_income = 200
        elif self.identity == "海归":
            base_income = 400
        elif self.identity == "个体户":
            base_income = 150
        elif self.identity == "官二代":
            base_income = 300
            
        # 技能加成
        if "精打细算" in self.skills:
            base_income *= 1.1
            
        income = int(base_income)
        self.cash += income
        return income
        
    def study(self):
        """
        学习提升
        提升技能和知识
        """
        # 简化版：增加少量声誉
        self.reputation += 1
        return True
        
    def rest(self):
        """
        休息恢复
        恢复体力和健康
        """
        recovered = min(20, 100 - self.stamina)
        self.stamina += recovered
        self.health = min(100, self.health + 5)
        return recovered
        
    def operate_company(self):
        """
        经营公司
        """
        if not self.company:
            return 0
            
        profit = self.company.daily_operation()
        self.cash += profit
        return profit
        
    def expand_business(self):
        """
        拓展业务
        """
        if not self.company:
            return "没有公司"
            
        # 简化版：升级公司
        if self.cash >= 10000:
            self.cash -= 10000
            self.company.level += 1
            return "公司升级成功！"
        else:
            return "资金不足"
            
    def check_class_promotion(self):
        """
        检查阶层晋升
        根据净资产自动晋升
        """
        class_thresholds = {
            1: ("赤贫阶层", 0),
            2: ("底层劳工", 10000),
            3: ("小商贩", 50000),
            4: ("小老板", 200000),
            5: ("中产阶层", 1000000),
            6: ("富豪阶层", 5000000),
            7: ("大资本家", 50000000),
            8: ("顶级富豪", 500000000),
        }
        
        # 检查是否可以晋升
        for level, (class_name, threshold) in sorted(class_thresholds.items(), reverse=True):
            if self.net_worth >= threshold:
                if self.class_level < level:
                    self.class_level = level
                    self.current_class = class_name
                    print(f"\n🎉 恭喜你晋升为【{class_name}】！")
                    print(f"   解锁更多功能和情报！")
                break
                
    def to_dict(self):
        """转换为字典（用于存档）"""
        return {
            "name": self.name,
            "identity": self.identity,
            "class_level": self.class_level,
            "current_class": self.current_class,
            "cash": self.cash,
            "real_estate": self.real_estate,
            "vehicles": self.vehicles,
            "investments": self.investments,
            "loans": self.loans,
            "connections": self.connections,
            "reputation": self.reputation,
            "health": self.health,
            "stamina": self.stamina,
            "city": self.city,
            "ranking": self.ranking
        }
