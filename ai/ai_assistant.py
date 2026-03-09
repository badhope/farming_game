"""
AI 农场助手模块
提供智能对话、农场建议和问题解答功能
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class AIFarmAssistant:
    """
    AI 农场助手
    
    基于规则的智能助手（简化版本，可后续接入 LLM）
    提供农场相关的问答和建议
    """
    
    def __init__(self):
        self.conversation_history = []
        self.player_preference = {}
        
        # 农业知识库
        self.knowledge_base = {
            "greeting": [
                "你好！我是你的 AI 农场助手，有什么问题尽管问我！",
                "欢迎来到农场！我是你的智能助手，随时为你服务！",
                "嗨！今天想了解什么农业知识呢？",
            ],
            "planting_tips": {
                "春天": [
                    "春天适合种植土豆、胡萝卜、草莓。",
                    "春季作物生长快，建议多种植短期作物快速回笼资金。",
                    "春天雨水较多，注意合理安排浇水时间。",
                ],
                "夏天": [
                    "夏天可以种植番茄、玉米、西瓜等高价值作物。",
                    "夏季炎热，作物需水量大，记得及时浇水。",
                    "注意防范暴风雨对作物的损害。",
                ],
                "秋天": [
                    "秋天是收获的季节，适合种植南瓜、葡萄。",
                    "秋季天气稳定，是扩大种植规模的好时机。",
                    "记得在冬天来临前收获所有作物。",
                ],
                "冬天": [
                    "冬天可以种植萝卜、白菜等耐寒作物。",
                    "冬季作物生长缓慢，建议规划来年种植计划。",
                    "利用冬季升级农场设施，为来年做准备。",
                ],
            },
            "money_tips": [
                "初期建议种植土豆，投资小回报快。",
                "有钱后可以种植草莓，利润率高。",
                "不要把所有钱都用来买种子，留一些备用。",
                "成熟作物及时收获出售，资金流转很重要。",
            ],
            "weather_tips": {
                "晴天": "晴天适合所有农活，记得给作物浇水！",
                "雨天": "下雨天不用浇水，可以休息或规划农场。",
                "暴风雨": "暴风雨可能损坏作物，提前收获成熟作物！",
                "干旱": "干旱天气作物需水量加倍，注意及时浇水！",
            },
        }
    
    def chat(self, user_input: str, game_state: Dict) -> str:
        """
        与用户对话
        
        Args:
            user_input: 用户输入
            game_state: 当前游戏状态
            
        Returns:
            str: AI 回复
        """
        self.conversation_history.append({
            "time": datetime.now().isoformat(),
            "user": user_input,
        })
        
        # 简单关键词匹配（后续可接入 LLM）
        user_input_lower = user_input.lower()
        
        # 问候
        if any(word in user_input_lower for word in ["你好", "嗨", "hello", "hi"]):
            response = random.choice(self.knowledge_base["greeting"])
        
        # 种植建议
        elif any(word in user_input_lower for word in ["种植", "种什么", "作物"]):
            season = game_state.get("season", "春天")
            tips = self.knowledge_base["planting_tips"].get(season, [])
            response = random.choice(tips) if tips else "每个季节都有适合的作物，请查看作物图鉴。"
        
        # 赚钱建议
        elif any(word in user_input_lower for word in ["赚钱", "钱不够", "资金"]):
            response = random.choice(self.knowledge_base["money_tips"])
        
        # 天气相关
        elif any(word in user_input_lower for word in ["天气", "下雨", "晴天"]):
            weather = game_state.get("weather", "晴天")
            response = self.knowledge_base["weather_tips"].get(weather, "天气多变，注意关注天气预报。")
        
        # 农场状态
        elif any(word in user_input_lower for word in ["农场", "状态", "情况"]):
            response = self._analyze_farm_state(game_state)
        
        # 帮助
        elif any(word in user_input_lower for word in ["帮助", "help", "怎么办"]):
            response = self._get_help_info()
        
        # 默认回复
        else:
            response = self._get_default_response(user_input)
        
        self.conversation_history.append({
            "time": datetime.now().isoformat(),
            "ai": response,
        })
        
        return response
    
    def _analyze_farm_state(self, game_state: Dict) -> str:
        """分析农场状态并给出建议"""
        money = game_state.get("money", 0)
        day = game_state.get("day", 1)
        season = game_state.get("season", "春天")
        
        analysis = []
        
        # 资金分析
        if money < 100:
            analysis.append("💰 资金紧张，建议尽快收获作物出售。")
        elif money > 1000:
            analysis.append("💰 资金充足，可以考虑扩大种植规模。")
        
        # 季节分析
        if day > 25:
            analysis.append(f"📅 {season}即将结束，请提前规划下季作物。")
        
        # 综合建议
        if not analysis:
            analysis.append("✅ 农场运营正常，继续保持！")
        
        return "\n".join(analysis)
    
    def _get_help_info(self) -> str:
        """获取帮助信息"""
        return """
🤖 AI 农场助手可以帮助你：

1. 种植建议 - 询问"种什么"
2. 赚钱攻略 - 询问"怎么赚钱"
3. 天气提示 - 询问"天气怎么样"
4. 农场分析 - 询问"农场情况"
5. 农业知识 - 询问相关问题

试试问我这些问题吧！
"""
    
    def _get_default_response(self, user_input: str) -> str:
        """默认回复"""
        default_responses = [
            "这个问题很有意思，但我还在学习中。你可以问我种植建议、赚钱方法等。",
            "我暂时不太理解你的问题。试试问我'怎么赚钱'或'种什么作物'？",
            "作为 AI 助手，我主要擅长农业相关的问题。其他问题我可能不太了解。",
        ]
        return random.choice(default_responses)
    
    def get_suggestion(self, suggestion_type: str, game_state: Dict) -> str:
        """
        获取特定类型的建议
        
        Args:
            suggestion_type: 建议类型 (planting/money/weather)
            game_state: 游戏状态
            
        Returns:
            str: 建议内容
        """
        if suggestion_type == "planting":
            season = game_state.get("season", "春天")
            tips = self.knowledge_base["planting_tips"].get(season, [])
            return random.choice(tips) if tips else "请查看作物图鉴选择适合的作物。"
        
        elif suggestion_type == "money":
            return random.choice(self.knowledge_base["money_tips"])
        
        elif suggestion_type == "weather":
            weather = game_state.get("weather", "晴天")
            return self.knowledge_base["weather_tips"].get(weather, "注意关注天气预报。")
        
        else:
            return "我可以提供种植、赚钱、天气等方面的建议。"
    
    def get_conversation_history(self) -> List[Dict]:
        """获取对话历史"""
        return self.conversation_history[-10:]  # 返回最近 10 条
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
