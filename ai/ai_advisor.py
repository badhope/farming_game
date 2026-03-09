"""
AI 种植顾问模块
提供智能种植建议和收益分析
"""

from typing import Dict, List, Optional, Tuple
from config.settings import CropData, Season, GameConfig


class AIPlantingAdvisor:
    """
    AI 种植顾问
    
    基于数据分析提供最优种植策略
    """
    
    def __init__(self):
        self.crop_data = CropData.CROPS
        self.season_days = GameConfig.DAYS_PER_SEASON
    
    def get_best_crop(self, season: str, days_remaining: int, budget: float) -> Dict:
        """
        根据当前情况推荐最优作物
        
        Args:
            season: 当前季节
            days_remaining: 剩余天数
            budget: 可用资金
            
        Returns:
            Dict: 推荐结果
        """
        suitable_crops = self._get_suitable_crops(season)
        
        if not suitable_crops:
            return {
                "success": False,
                "message": f"{season}没有适合种植的作物。",
            }
        
        # 计算每种作物的收益
        crop_analysis = []
        for crop_name, data in suitable_crops.items():
            analysis = self._analyze_crop(crop_name, data, days_remaining, budget)
            if analysis["can_plant"]:
                crop_analysis.append(analysis)
        
        if not crop_analysis:
            return {
                "success": False,
                "message": "当前资金不足或时间不够，无法种植任何作物。",
            }
        
        # 按利润率排序
        crop_analysis.sort(key=lambda x: x["profit_per_day"], reverse=True)
        
        best = crop_analysis[0]
        
        return {
            "success": True,
            "recommended_crop": best["name"],
            "reason": self._generate_recommendation_reason(best),
            "analysis": crop_analysis[:3],  # 返回前 3 个选择
        }
    
    def _get_suitable_crops(self, season: str) -> Dict:
        """获取适合当前季节的作物"""
        season_map = {
            "春天": Season.SPRING,
            "夏天": Season.SUMMER,
            "秋天": Season.AUTUMN,
            "冬天": Season.WINTER,
        }
        
        season_enum = season_map.get(season)
        if not season_enum:
            return {}
        
        suitable = {}
        for name, data in self.crop_data.items():
            if season_enum in data["seasons"]:
                suitable[name] = data
        
        return suitable
    
    def _analyze_crop(self, crop_name: str, data: Dict, days_remaining: int, budget: float) -> Dict:
        """分析单个作物的种植可行性"""
        grow_days = data["grow_days"]
        seed_price = data["seed_price"]
        sell_price = data["sell_price"]
        water_needed = data.get("water_needed", 1)
        
        # 计算可种植数量
        max_seeds = int(budget / seed_price) if seed_price > 0 else 0
        
        # 判断时间是否足够
        can_plant = days_remaining >= grow_days
        
        # 计算利润率
        profit_per_crop = sell_price - seed_price
        profit_rate = (profit_per_crop / seed_price * 100) if seed_price > 0 else 0
        
        # 计算日均收益
        profit_per_day = profit_per_crop / grow_days if grow_days > 0 else 0
        
        # 总收益（假设全部种植）
        total_profit = profit_per_crop * max_seeds
        
        return {
            "name": crop_name,
            "seed_price": seed_price,
            "sell_price": sell_price,
            "grow_days": grow_days,
            "water_needed": water_needed,
            "can_plant": can_plant,
            "max_seeds": max_seeds,
            "profit_per_crop": profit_per_crop,
            "profit_rate": profit_rate,
            "profit_per_day": profit_per_day,
            "total_profit": total_profit,
        }
    
    def _generate_recommendation_reason(self, crop_analysis: Dict) -> str:
        """生成推荐理由"""
        name = crop_analysis["name"]
        profit_rate = crop_analysis["profit_rate"]
        grow_days = crop_analysis["grow_days"]
        profit_per_day = crop_analysis["profit_per_day"]
        
        reasons = []
        
        if profit_rate > 150:
            reasons.append(f"利润率高达{profit_rate:.0f}%")
        elif profit_rate > 100:
            reasons.append(f"利润率不错，为{profit_rate:.0f}%")
        
        if grow_days <= 3:
            reasons.append(f"生长周期短（{grow_days}天）")
        elif grow_days <= 7:
            reasons.append(f"生长周期适中（{grow_days}天）")
        
        if profit_per_day > 30:
            reasons.append(f"日均收益高（{profit_per_day:.1f}金币/天）")
        
        if reasons:
            return f"推荐种植{name}：{'，'.join(reasons)}"
        else:
            return f"推荐种植{name}"
    
    def get_crop_comparison(self, crop_names: List[str], days_remaining: int) -> str:
        """
        对比多种作物
        
        Args:
            crop_names: 作物名称列表
            days_remaining: 剩余天数
            
        Returns:
            str: 对比分析
        """
        comparisons = []
        
        for name in crop_names:
            if name in self.crop_data:
                data = self.crop_data[name]
                analysis = self._analyze_crop(name, data, days_remaining, float('inf'))
                
                comparisons.append(
                    f"{name}: 种子{analysis['seed_price']}金币，"
                    f"售价{analysis['sell_price']}金币，"
                    f"生长{analysis['grow_days']}天，"
                    f"利润率{analysis['profit_rate']:.0f}%"
                )
        
        return "\n".join(comparisons)
    
    def calculate_optimal_strategy(self, season: str, total_days: int, initial_budget: float) -> Dict:
        """
        计算整个季节的最优种植策略
        
        Args:
            season: 季节
            total_days: 总天数（通常 28 天）
            initial_budget: 初始资金
            
        Returns:
            Dict: 策略建议
        """
        # 简化版本：推荐 3 个阶段的种植计划
        phase_days = total_days // 3
        
        strategy = {
            "early_phase": {
                "days": f"1-{phase_days}",
                "suggestion": "种植短期作物快速回笼资金",
                "recommended_crops": ["胡萝卜", "土豆"],
            },
            "mid_phase": {
                "days": f"{phase_days+1}-{phase_days*2}",
                "suggestion": "种植中等周期的高价值作物",
                "recommended_crops": ["番茄", "玉米"],
            },
            "late_phase": {
                "days": f"{phase_days*2+1}-{total_days}",
                "suggestion": "确保在季节结束前收获",
                "recommended_crops": ["南瓜", "萝卜"],
            },
        }
        
        return strategy
    
    def get_risk_assessment(self, crop_name: str, weather: str, days_remaining: int) -> Dict:
        """
        风险评估
        
        Args:
            crop_name: 作物名称
            weather: 天气状况
            days_remaining: 剩余天数
            
        Returns:
            Dict: 风险评估结果
        """
        if crop_name not in self.crop_data:
            return {"risk": "unknown", "message": "未知作物"}
        
        data = self.crop_data[crop_name]
        grow_days = data["grow_days"]
        
        risks = []
        risk_level = "low"
        
        # 时间风险
        if days_remaining < grow_days + 3:
            risks.append("⚠️ 时间紧张，可能无法在季节结束前收获")
            risk_level = "high"
        elif days_remaining < grow_days + 7:
            risks.append("⚠️ 时间较紧，建议尽快种植")
            if risk_level != "high":
                risk_level = "medium"
        
        # 天气风险
        if weather == "暴风雨":
            risks.append("⛈️ 暴风雨可能损坏作物")
            risk_level = "high"
        elif weather == "干旱":
            risks.append("🏜️ 干旱天气需水量增加")
            if risk_level != "high":
                risk_level = "medium"
        
        # 市场风险（简化）
        if data["sell_price"] > 500:
            risks.append("💰 高价值作物，建议及时出售")
        
        if not risks:
            risks.append("✅ 风险较低，可以放心种植")
        
        return {
            "risk_level": risk_level,
            "risks": risks,
        }
