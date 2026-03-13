#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
经济系统
管理宏观经济环境、市场波动、随机事件
"""

import random


class EconomySystem:
    """
    经济系统 - 管理宏观经济状态
    """
    
    def __init__(self):
        self.day = 1
        self.gdp_growth = 0.05  # GDP 增长率 5%
        self.inflation_rate = 0.02  # 通胀率 2%
        self.unemployment_rate = 0.04  # 失业率 4%
        
        # 市场状态
        self.market_conditions = {
            "房地产": {
                "base_price": 20000,  # 基础价格（元/平）
                "trend": "stable",  # stable/up/down
                "volatility": 0.1  # 波动率 10%
            },
            "股票": {
                "base_index": 3000,  # 上证指数
                "trend": "stable",
                "volatility": 0.2
            },
            "大宗商品": {
                "base_price": 100,
                "trend": "stable",
                "volatility": 0.15
            }
        }
        
    def update_daily(self):
        """每日更新经济状态"""
        self.day += 1
        
        # 随机波动
        for market in self.market_conditions.values():
            change = random.uniform(-market['volatility'], market['volatility'])
            # 应用变化（简化版）
            
    def get_market_price(self, market_name):
        """获取市场价格"""
        market = self.market_conditions.get(market_name)
        if market:
            return market['base_price']
        return 0
        
    def get_economic_report(self):
        """获取经济报告"""
        report = f"""
╔════════════════════════════════════╗
║        宏观经济报告                ║
╠════════════════════════════════════╣
║ GDP 增长率：{self.gdp_growth:.2%}              ║
║ 通胀率：{self.inflation_rate:.2%}                    ║
║ 失业率：{self.unemployment_rate:.2%}                  ║
╚════════════════════════════════════╝
        """
        return report
