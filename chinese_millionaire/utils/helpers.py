#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具函数
提供常用辅助函数
"""


def format_money(amount):
    """
    格式化金额显示
    
    Args:
        amount: 金额数字
        
    Returns:
        格式化后的字符串，如 "¥1,234,567.89"
    """
    return f"¥{amount:,.2f}"
    
    
def format_number(num):
    """
    格式化数字显示（千分位）
    
    Args:
        num: 数字
        
    Returns:
        格式化后的字符串，如 "1,234,567"
    """
    return f"{num:,}"
    
    
def clamp(value, min_value, max_value):
    """
    限制值在指定范围内
    
    Args:
        value: 原始值
        min_value: 最小值
        max_value: 最大值
        
    Returns:
        限制后的值
    """
    return max(min_value, min(max_value, value))
    
    
def percentage_change(old_value, new_value):
    """
    计算百分比变化
    
    Args:
        old_value: 原始值
        new_value: 新值
        
    Returns:
        变化百分比，如 0.25 表示 +25%
    """
    if old_value == 0:
        return 0
    return (new_value - old_value) / old_value
