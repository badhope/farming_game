"""
AI 农场分析器模块
分析农场经营状况并提供优化建议
"""

from typing import Dict, List, Optional


class AIFarmAnalyzer:
    """
    AI 农场分析器
    
    分析农场整体经营状况，提供优化建议
    """
    
    def __init__(self):
        self.analysis_templates = {
            "money_low": "💰 资金紧张（{money}金币），建议：\n- 尽快收获成熟作物\n- 优先种植短期作物（胡萝卜、土豆）\n- 减少非必要支出",
            "money_good": "💰 资金充足（{money}金币），建议：\n- 可以扩大种植规模\n- 考虑种植高价值作物\n- 预留升级农场的资金",
            "land_inefficient": "📊 土地利用率低（{usage}%），建议：\n- 开垦更多空地\n- 及时收获成熟作物\n- 合理规划种植区域",
            "land_good": "📊 土地利用率高（{usage}%），继续保持！",
            "crop_diversity_low": "🌱 作物种类单一，建议：\n- 尝试种植不同作物\n- 分散风险\n- 探索新作物的收益",
            "crop_diversity_good": "🌱 作物种类丰富，风险分散良好！",
        }
    
    def analyze_farm(self, game_state: Dict) -> Dict:
        """
        全面分析农场状况
        
        Args:
            game_state: 游戏状态字典，包含：
                - money: 金币
                - plots: 地块信息
                - harvested_crops: 已收获作物种类
                - season: 季节
                - day: 天数
                
        Returns:
            Dict: 分析报告
        """
        analysis = {
            "overall_score": 0,
            "aspects": {},
            "suggestions": [],
            "summary": "",
        }
        
        # 资金分析
        money_analysis = self._analyze_money(game_state.get("money", 0))
        analysis["aspects"]["economy"] = money_analysis
        
        # 土地利用分析
        land_analysis = self._analyze_land_usage(game_state.get("plots", []))
        analysis["aspects"]["land_usage"] = land_analysis
        
        # 作物多样性分析
        diversity_analysis = self._analyze_crop_diversity(
            game_state.get("harvested_crops", [])
        )
        analysis["aspects"]["diversity"] = diversity_analysis
        
        # 季节进度分析
        season_analysis = self._analyze_season_progress(
            game_state.get("day", 1),
            game_state.get("season", "春天")
        )
        analysis["aspects"]["season_progress"] = season_analysis
        
        # 计算总分
        analysis["overall_score"] = self._calculate_overall_score(analysis["aspects"])
        
        # 生成建议
        analysis["suggestions"] = self._generate_suggestions(analysis["aspects"])
        
        # 生成总结
        analysis["summary"] = self._generate_summary(analysis)
        
        return analysis
    
    def _analyze_money(self, money: int) -> Dict:
        """资金分析"""
        if money < 200:
            return {
                "status": "poor",
                "score": 30,
                "message": self.analysis_templates["money_low"].format(money=money),
            }
        elif money < 1000:
            return {
                "status": "fair",
                "score": 60,
                "message": f"💰 资金一般（{money}金币），保持稳定发展。",
            }
        else:
            return {
                "status": "good",
                "score": 90,
                "message": self.analysis_templates["money_good"].format(money=money),
            }
    
    def _analyze_land_usage(self, plots: List) -> Dict:
        """土地利用分析"""
        if not plots:
            return {
                "status": "unknown",
                "score": 50,
                "message": "📊 无法评估土地利用情况。",
            }
        
        total_plots = len(plots) * len(plots[0]) if isinstance(plots[0], list) else len(plots)
        
        # 计算已使用地块
        used_plots = 0
        for row in plots:
            for plot in row:
                if hasattr(plot, 'is_empty'):
                    if not plot.is_empty():
                        used_plots += 1
                elif isinstance(plot, dict) and not plot.get("is_empty", True):
                    used_plots += 1
        
        usage_rate = (used_plots / total_plots * 100) if total_plots > 0 else 0
        
        if usage_rate < 50:
            return {
                "status": "poor",
                "score": 40,
                "message": self.analysis_templates["land_inefficient"].format(usage=usage_rate),
            }
        elif usage_rate < 80:
            return {
                "status": "fair",
                "score": 70,
                "message": f"📊 土地利用率中等（{usage_rate:.0f}%），还有提升空间。",
            }
        else:
            return {
                "status": "good",
                "score": 95,
                "message": self.analysis_templates["land_good"].format(usage=usage_rate),
            }
    
    def _analyze_crop_diversity(self, harvested_crops: List[str]) -> Dict:
        """作物多样性分析"""
        unique_crops = len(set(harvested_crops)) if harvested_crops else 0
        
        if unique_crops < 3:
            return {
                "status": "poor",
                "score": 40,
                "message": self.analysis_templates["crop_diversity_low"],
            }
        elif unique_crops < 6:
            return {
                "status": "fair",
                "score": 70,
                "message": f"🌱 已种植{unique_crops}种作物，还可以尝试更多种类。",
            }
        else:
            return {
                "status": "good",
                "score": 90,
                "message": self.analysis_templates["crop_diversity_good"],
            }
    
    def _analyze_season_progress(self, day: int, season: str) -> Dict:
        """季节进度分析"""
        progress = day / 28  # 假设每季 28 天
        
        if progress < 0.3:
            return {
                "status": "early",
                "score": 80,
                "message": f"📅 {season}初期（第{day}天），时间充裕，可以规划长期作物。",
            }
        elif progress < 0.7:
            return {
                "status": "mid",
                "score": 70,
                "message": f"📅 {season}中期（第{day}天），注意平衡短期和长期作物。",
            }
        else:
            return {
                "status": "late",
                "score": 50,
                "message": f"📅 {season}末期（第{day}天），建议种植短期作物确保收获。",
            }
    
    def _calculate_overall_score(self, aspects: Dict) -> int:
        """计算总体评分"""
        scores = [aspect["score"] for aspect in aspects.values()]
        return int(sum(scores) / len(scores)) if scores else 0
    
    def _generate_suggestions(self, aspects: Dict) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 根据各方面状态生成建议
        if aspects.get("economy", {}).get("status") == "poor":
            suggestions.append("优先解决资金问题")
        
        if aspects.get("land_usage", {}).get("status") in ["poor", "fair"]:
            suggestions.append("提高土地利用率")
        
        if aspects.get("diversity", {}).get("status") == "poor":
            suggestions.append("增加作物种类")
        
        if aspects.get("season_progress", {}).get("status") == "late":
            suggestions.append("注意季节即将结束")
        
        if not suggestions:
            suggestions.append("农场运营良好，继续保持！")
        
        return suggestions
    
    def _generate_summary(self, analysis: Dict) -> str:
        """生成总结"""
        score = analysis["overall_score"]
        
        if score >= 80:
            level = "优秀"
            emoji = "🌟"
        elif score >= 60:
            level = "良好"
            emoji = "👍"
        elif score >= 40:
            level = "一般"
            emoji = "📈"
        else:
            level = "需要改进"
            emoji = "💪"
        
        return f"{emoji} 农场综合评分：{score}分（{level}）"
    
    def get_detailed_report(self, game_state: Dict) -> str:
        """
        获取详细分析报告
        
        Args:
            game_state: 游戏状态
            
        Returns:
            str: 格式化报告
        """
        analysis = self.analyze_farm(game_state)
        
        report_lines = [
            "=" * 50,
            "🤖 AI 农场分析报告",
            "=" * 50,
            "",
            analysis["summary"],
            "",
            "📊 各方面评估:",
            "-" * 30,
        ]
        
        aspect_names = {
            "economy": "💰 经济状况",
            "land_usage": "📊 土地利用",
            "diversity": "🌱 作物多样性",
            "season_progress": "📅 季节进度",
        }
        
        for key, aspect in analysis["aspects"].items():
            name = aspect_names.get(key, key)
            report_lines.append(f"{name}: {aspect['message']}")
        
        report_lines.extend([
            "",
            "💡 优化建议:",
            "-" * 30,
        ])
        
        for i, suggestion in enumerate(analysis["suggestions"], 1):
            report_lines.append(f"{i}. {suggestion}")
        
        report_lines.extend([
            "",
            "=" * 50,
        ])
        
        return "\n".join(report_lines)
