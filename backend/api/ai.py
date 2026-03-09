"""
AI 功能 API
提供 AI 助手、种植建议、农场分析等功能
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()


# ============ Schema 定义 ============

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    suggestions: List[str] = []


class PlantingAdvice(BaseModel):
    """种植建议"""
    crop_id: str
    crop_name: str
    reason: str
    expected_profit: float
    growth_days: int
    risk_level: str  # "low", "medium", "high"


class FarmAnalysis(BaseModel):
    """农场分析报告"""
    score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


# ============ API 端点 ============

@router.post("/chat")
async def chat_with_ai(request: ChatRequest) -> ChatResponse:
    """与 AI 助手对话"""
    # TODO: 实现 AI 聊天逻辑
    return ChatResponse(
        response="你好！我是你的 AI 农场助手，有什么问题尽管问我！",
        suggestions=[
            "现在种什么最赚钱？",
            "怎么快速升级？",
            "我的农场怎么样？",
        ],
    )


@router.get("/advice/planting")
async def get_planting_advice() -> List[PlantingAdvice]:
    """获取种植建议"""
    # TODO: 实现种植建议逻辑
    return [
        PlantingAdvice(
            crop_id="turnip",
            crop_name="萝卜",
            reason="当前季节最适合种植，生长周期短，收益稳定",
            expected_profit=150.0,
            growth_days=4,
            risk_level="low",
        )
    ]


@router.get("/analysis/farm")
async def analyze_farm() -> FarmAnalysis:
    """分析农场状况"""
    # TODO: 实现农场分析逻辑
    return FarmAnalysis(
        score=75,
        strengths=[
            "土地利用率高",
            "作物多样性好",
        ],
        weaknesses=[
            "浇水不够及时",
            "缺少高价值作物",
        ],
        suggestions=[
            "建议种植更多夏季高价值作物",
            "定时浇水提高产量",
        ],
    )


@router.get("/knowledge/{topic}")
async def get_knowledge(topic: str):
    """获取农业知识"""
    # TODO: 实现农业知识库查询
    knowledge_base = {
        "watering": "作物需要每天浇水才能健康生长，下雨天可以免除浇水。",
        "fertilizer": "肥料可以加速作物生长，提高作物品质。",
        "seasons": "不同季节适合种植不同作物，请根据季节选择合适的作物。",
    }
    
    if topic in knowledge_base:
        return {"topic": topic, "content": knowledge_base[topic]}
    else:
        raise HTTPException(status_code=404, detail="知识主题不存在")
