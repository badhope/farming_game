#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公司系统
管理公司的创建、经营、扩张
"""


class Company:
    """
    公司类 - 管理单个公司
    """
    
    def __init__(self, name, company_type, level=1):
        self.name = name
        self.type = company_type  # "农业", "零售", "科技", "贸易", "制造"
        self.level = level
        self.employees = 0
        self.monthly_revenue = 0
        self.monthly_cost = 0
        self.monthly_profit = 0
        
    def daily_operation(self):
        """
        每日经营
        返回利润
        """
        # 简化版：根据等级计算收入
        base_revenue = self.level * 1000
        
        # 根据类型有不同加成
        if self.type == "农业":
            base_revenue *= 1.0
        elif self.type == "零售":
            base_revenue *= 1.2
        elif self.type == "科技":
            base_revenue *= 1.5
        elif self.type == "贸易":
            base_revenue *= 1.3
        elif self.type == "制造":
            base_revenue *= 1.1
            
        # 成本
        base_cost = self.level * 500
        
        # 计算利润
        daily_revenue = base_revenue / 30  # 日均收入
        daily_cost = base_cost / 30  # 日均成本
        profit = daily_revenue - daily_cost
        
        self.monthly_revenue = base_revenue
        self.monthly_cost = base_cost
        self.monthly_profit = base_revenue - base_cost
        
        return int(profit)
        
    def update_daily(self):
        """每日更新"""
        # 可以在这里添加更多逻辑
        pass


class CompanySystem:
    """
    公司系统 - 管理公司相关操作
    """
    
    COMPANY_TYPES = ["农业", "零售", "科技", "贸易", "制造"]
    
    def create_company(self, name, company_type, owner):
        """创建公司"""
        if company_type not in self.COMPANY_TYPES:
            return None
            
        company = Company(name, company_type)
        return company
        
    def get_company_types(self):
        """获取所有公司类型"""
        return self.COMPANY_TYPES.copy()
