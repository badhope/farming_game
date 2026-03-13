#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
身份系统
定义 6 个不同的起始身份及其特性
"""


class Identity:
    """身份类"""
    
    def __init__(self, name, description, start_money, connections, education, skills, bonus, bonus_description):
        self.name = name
        self.description = description
        self.start_money = start_money
        self.connections = connections
        self.education = education
        self.skills = skills
        self.bonus = bonus
        self.bonus_description = bonus_description


class IdentitySystem:
    """
    身份系统 - 管理所有身份数据
    """
    
    def __init__(self):
        self.identities = [
            Identity(
                name="农民",
                description="农村起家，农业相关加成",
                start_money=8000,
                connections=20,
                education="初中",
                skills=["精通农业", "吃苦耐劳"],
                bonus={
                    "agriculture_cost": 0.7,  # 农业成本 -30%
                    "crop_yield": 1.25  # 产量 +25%
                },
                bonus_description="农业成本 -30%，产量 +25%"
            ),
            
            Identity(
                name="小镇青年",
                description="县城创业，零售业优势",
                start_money=25000,
                connections=35,
                education="高中",
                skills=["精打细算", "人情世故"],
                bonus={
                    "rent_cost": 0.6,  # 租金 -40%
                    "loan_rate": 1.1  # 贷款利率 +10%
                },
                bonus_description="租金 -40%，小额贷款更容易"
            ),
            
            Identity(
                name="大学生",
                description="科技创业，互联网行业",
                start_money=50000,
                connections=25,
                education="本科",
                skills=["创新思维", "学习能力"],
                bonus={
                    "tech_unlock": 0.5,  # 科技行业门槛 -50%
                    "vc_success": 1.4  # 融资成功率 +40%
                },
                bonus_description="科技创业门槛 -50%，融资成功率 +40%"
            ),
            
            Identity(
                name="海归",
                description="国际贸易，金融投资",
                start_money=200000,
                connections=15,
                education="海外硕士",
                skills=["国际视野", "英语流利"],
                bonus={
                    "trade_tariff": 0.7,  # 关税 -30%
                    "forex_fee": 0.5  # 外汇手续费 -50%
                },
                bonus_description="国际贸易关税 -30%，外汇手续费 -50%"
            ),
            
            Identity(
                name="个体户",
                description="批发市场，制造业",
                start_money=80000,
                connections=50,
                education="初中",
                skills=["生意头脑", "供应链"],
                bonus={
                    "wholesale_price": 0.75,  # 批发价 -25%
                    "cash_flow": 1.3  # 现金流 +30%
                },
                bonus_description="批发价 -25%，现金流 +30%"
            ),
            
            Identity(
                name="官二代",
                description="人脉优势，政策敏感",
                start_money=150000,
                connections=80,
                education="本科",
                skills=["人脉通天", "政策敏感"],
                bonus={
                    "gov_project": 1.6,  # 政府项目成功率 +60%
                    "loan_approve": 1.4  # 贷款审批 +40%
                },
                bonus_description="政府项目优势，贷款审批更容易（但有腐败风险）"
            )
        ]
        
    def get_all_identities(self):
        """获取所有身份数据"""
        return [
            {
                'name': identity.name,
                'description': identity.description,
                'start_money': identity.start_money,
                'connections': identity.connections,
                'education': identity.education,
                'skills': identity.skills,
                'bonus': identity.bonus,
                'bonus_description': identity.bonus_description
            }
            for identity in self.identities
        ]
        
    def get_identity_by_name(self, name):
        """根据名称获取身份"""
        for identity in self.identities:
            if identity.name == name:
                return identity
        return None
