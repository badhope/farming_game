#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
情报系统
管理市场情报、谣言、信息精度
"""

import random


class IntelligenceSystem:
    """
    情报系统 - 管理信息获取
    
    核心机制:
    - 低身份：情报模糊、真假难辨、信息滞后
    - 高身份：情报准确、第一时间、内幕消息
    """
    
    def __init__(self):
        self.intelligence_levels = {
            1: "模糊传闻",      # 听说有个商机，但不确定
            2: "街头传闻",      # 大概知道方向
            3: "市场情报",      # 基本准确
            4: "行业数据",      # 有数据支持
            5: "内幕消息",      # 准确情报
            6: "高层决策",      # 提前知道政策
            7: "国家机密",      # 核心机密
            8: "全知视角"       # 上帝视角
        }
        
    def get_market_info(self, market_type, player_level):
        """
        获取市场情报（随身份变化）
        
        Args:
            market_type: 市场类型（房地产、股票等）
            player_level: 玩家阶层等级（1-8）
            
        Returns:
            情报信息（精度随身份变化）
        """
        # 真实数据（玩家看不到）
        true_data = {
            "房地产": {
                "trend": "上涨",
                "change": "+30%",
                "risk": "低"
            },
            "股票": {
                "trend": "下跌",
                "change": "-20%",
                "risk": "高"
            },
            "大宗商品": {
                "trend": "震荡",
                "change": "±10%",
                "risk": "中"
            }
        }
        
        # 根据身份返回不同精度的情报
        if player_level <= 2:
            # 低身份：模糊情报
            return {
                "房地产": "听说房子能赚钱？（模糊）",
                "股票": "股市好像有风险？（传闻）",
                "大宗商品": "什么东西在涨价？（不清楚）"
            }
        elif player_level <= 4:
            # 中等身份：基本准确
            return {
                "房地产": "房价可能在涨（+10~40%）",
                "股票": "股市不太乐观（-10~-30%）",
                "大宗商品": "价格波动较大（±15%）"
            }
        elif player_level <= 6:
            # 高身份：准确情报
            return {
                "房地产": "准确数据：房价将涨 +25~35%",
                "股票": "内部消息：股市将跌 -15~-25%",
                "大宗商品": "精确数据：震荡±8-12%"
            }
        else:
            # 顶级身份：内幕消息
            return {
                "房地产": "内幕：某新区规划即将公布，房价将涨 30%",
                "股票": "高层决策：某政策即将出台，某股将跌 20%",
                "大宗商品": "机密：国家储备计划，价格将上涨 15%"
            }
            
    def generate_rumors(self, player_level):
        """
        生成谣言（低身份更容易听到假消息）
        
        Args:
            player_level: 玩家阶层等级
            
        Returns:
            谣言列表（真假混合）
        """
        all_rumors = [
            ("听说某地要建开发区", True),
            ("某股票有内幕，马上要涨", False),
            ("某老板要跑路了", False),
            ("政府要发补贴", True),
            ("某行业要整顿", True),
            ("某大佬要投资", False)
        ]
        
        # 根据身份决定真假比例
        if player_level <= 3:
            # 30% 真消息，70% 假消息
            truth_rate = 0.3
        elif player_level <= 5:
            # 60% 真消息
            truth_rate = 0.6
        else:
            # 90% 真消息
            truth_rate = 0.9
            
        # 选择 3 个谣言
        selected = random.sample(all_rumors, 3)
        rumors = []
        
        for rumor, is_true in selected:
            # 根据真假率决定是否反转
            if random.random() > truth_rate:
                is_true = not is_true
                
            # 添加真假标记（但玩家不知道）
            if is_true:
                rumors.append(f"{rumor}（✓）")
            else:
                rumors.append(f"{rumor}（？）")
                
        return rumors
        
    def get_investment_tip(self, player_level):
        """
        获取投资建议
        
        Args:
            player_level: 玩家阶层等级
            
        Returns:
            投资建议（精度随身份变化）
        """
        if player_level <= 2:
            return "听说投资房子比较稳？（不确定）"
        elif player_level <= 4:
            return "建议投资房地产，预计年化收益 10-15%"
        elif player_level <= 6:
            return "内幕：某区域即将开发，提前买入，收益 30%+"
        else:
            return "机密：国家政策将支持某行业，提前布局，收益 50%+"
