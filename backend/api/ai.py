"""
AI 功能 API
提供 AI 助手、种植建议、农场分析等功能
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os
import json

from backend.services.game_session import game_service

router = APIRouter()

AI_CONFIG_FILE = "data/ai_config.json"

def load_ai_config() -> Dict[str, Any]:
    """加载AI配置"""
    os.makedirs("data", exist_ok=True)
    if os.path.exists(AI_CONFIG_FILE):
        with open(AI_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "provider": "built-in",
        "api_key": "",
        "model": "gpt-3.5-turbo",
        "base_url": "https://api.openai.com/v1",
        "temperature": 0.7,
    }

def save_ai_config(config: Dict[str, Any]) -> None:
    """保存AI配置"""
    os.makedirs("data", exist_ok=True)
    with open(AI_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_ai_config() -> Dict[str, Any]:
    """获取AI配置（不返回API密钥）"""
    config = load_ai_config()
    return {
        "provider": config.get("provider", "built-in"),
        "model": config.get("model", "gpt-3.5-turbo"),
        "base_url": config.get("base_url", "https://api.openai.com/v1"),
        "temperature": config.get("temperature", 0.7),
        "has_api_key": bool(config.get("api_key", "")),
    }

def call_external_ai(prompt: str, system_prompt: str = "") -> Optional[str]:
    """调用外部AI API"""
    config = load_ai_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        return None
    
    try:
        import requests
        model = config.get("model", "gpt-3.5-turbo")
        base_url = config.get("base_url", "https://api.openai.com/v1")
        temperature = config.get("temperature", 0.7)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
            },
            timeout=30,
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return None
    except Exception as e:
        print(f"AI API调用失败: {e}")
        return None


# ============ Schema 定义 ============

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    suggestions: List[str] = []


# ============ API 端点 ============

@router.post("/chat")
async def chat_with_ai(request: ChatRequest) -> Dict[str, Any]:
    """与 AI 助手对话"""
    if not game_service.has_active_game():
        return {
            "response": "没有进行中的游戏，请先创建新游戏！",
            "suggestions": ["创建一个新游戏"],
        }
    
    result = game_service.chat_with_ai(request.message)
    return {
        "response": result.get("response", "..."),
        "suggestions": [
            "现在种什么最赚钱？",
            "我的农场怎么样？",
            "给我一些种植建议",
        ],
    }


@router.get("/advice/planting")
async def get_planting_advice() -> Dict[str, Any]:
    """获取种植建议"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    advice = game_service.get_planting_advice()
    
    if not advice:
        return {
            "message": "当前季节没有适合种植的作物",
            "advice": [],
        }
    
    return {
        "message": "以下是推荐种植的作物：",
        "advice": advice,
    }


@router.get("/analysis/farm")
async def analyze_farm() -> Dict[str, Any]:
    """分析农场状况"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    analysis = game_service.analyze_farm()
    return analysis


@router.get("/knowledge/{topic}")
async def get_knowledge(topic: str) -> Dict[str, Any]:
    """获取农业知识"""
    if not game_service.has_active_game():
        raise HTTPException(status_code=400, detail="没有进行中的游戏")
    
    knowledge_base = {
        "watering": {
            "title": "浇水知识",
            "content": "作物需要每天浇水才能健康生长，下雨天可以免除浇水。不同作物需水量不同，夏季高温时需水量会增加。",
        },
        "fertilizer": {
            "title": "肥料知识",
            "content": "肥料可以加速作物生长，提高作物品质。合理使用肥料能让作物更快成熟。",
        },
        "seasons": {
            "title": "季节知识",
            "content": "不同季节适合种植不同作物：春季适合土豆、胡萝卜；夏季适合番茄、玉米；秋季适合南瓜、葡萄；冬季适合萝卜、白菜。",
        },
        "weather": {
            "title": "天气知识",
            "content": "晴天适合所有农活；雨天可以免除浇水；暴风雨可能损坏作物；干旱时需水量加倍。",
        },
    }
    
    topic_lower = topic.lower()
    if topic_lower in knowledge_base:
        return knowledge_base[topic_lower]
    else:
        return {
            "title": "未知主题",
            "content": f"未找到关于 '{topic}' 的知识，请尝试其他主题：watering, fertilizer, seasons, weather",
        }


class AIConfigRequest(BaseModel):
    """AI配置请求"""
    provider: str = "openai"
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    base_url: str = "https://api.openai.com/v1"
    temperature: float = 0.7


@router.get("/config")
async def get_ai_config_endpoint() -> Dict[str, Any]:
    """获取AI配置"""
    return get_ai_config()


@router.post("/config")
async def set_ai_config_endpoint(request: AIConfigRequest) -> Dict[str, Any]:
    """设置AI配置"""
    config = load_ai_config()
    
    config["provider"] = request.provider
    config["model"] = request.model
    config["base_url"] = request.base_url
    config["temperature"] = request.temperature
    
    if request.api_key:
        config["api_key"] = request.api_key
    
    save_ai_config(config)
    
    return {
        "success": True,
        "message": "AI配置已保存",
        "config": get_ai_config(),
    }


@router.post("/config/test")
async def test_ai_connection() -> Dict[str, Any]:
    """测试AI连接"""
    config = load_ai_config()
    api_key = config.get("api_key", "")
    
    if not api_key:
        return {
            "success": False,
            "message": "请先配置API密钥",
        }
    
    result = call_external_ai("你好，请回复'连接成功'")
    
    if result:
        return {
            "success": True,
            "message": "AI连接成功！",
            "response": result,
        }
    else:
        return {
            "success": False,
            "message": "AI连接失败，请检查配置",
        }
