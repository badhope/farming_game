#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本格式化器
提供美观的文本输出格式
"""


class TableFormatter:
    """
    表格格式化器
    用于显示美观的表格
    """
    
    @staticmethod
    def create_table(headers, rows):
        """
        创建表格
        
        Args:
            headers: 表头列表 ["列 1", "列 2", "列 3"]
            rows: 数据行列表 [["值 1", "值 2", "值 3"], ...]
            
        Returns:
            格式化后的表格字符串
        """
        # 计算每列宽度
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
                
        # 创建表格
        lines = []
        
        # 表头
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        lines.append(header_line)
        
        # 分隔线
        separator = "-+-".join("-" * w for w in col_widths)
        lines.append(separator)
        
        # 数据行
        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            lines.append(row_line)
            
        return "\n".join(lines)
        
    @staticmethod
    def create_box(title, content):
        """
        创建带边框的文本框
        
        Args:
            title: 标题
            content: 内容
            
        Returns:
            格式化后的文本框
        """
        width = max(len(title), len(content), 40)
        
        lines = []
        lines.append("╔" + "═" * width + "╗")
        lines.append("║ " + title.ljust(width - 1) + " ║")
        lines.append("╠" + "═" * width + "╣")
        
        for line in content.split('\n'):
            lines.append("║ " + line.ljust(width - 1) + " ║")
            
        lines.append("╚" + "═" * width + "╝")
        
        return "\n".join(lines)
