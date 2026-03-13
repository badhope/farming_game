from fastapi import APIRouter, Depends
from datetime import datetime
import psutil
import os

from backend.schemas.api_response import ApiResponse
from backend.middleware.performance import request_metrics

router = APIRouter(prefix="/health", tags=["健康检查"])


@router.get("")
async def health_check():
    """基础健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "farming_game",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check():
    """详细健康检查"""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        metrics = request_metrics.get_metrics()
        
        health_status = "healthy"
        if cpu_percent > 80 or memory_percent > 80:
            health_status = "degraded"
        if cpu_percent > 95 or memory_percent > 95:
            health_status = "unhealthy"
        
        return ApiResponse(
            success=True,
            message="系统健康检查完成",
            data={
                "status": health_status,
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_percent": round(cpu_percent, 1),
                    "memory_percent": round(memory_percent, 1),
                    "disk_percent": round(psutil.disk_usage('/').percent, 1)
                },
                "process": {
                    "memory_mb": round(memory_info.rss / 1024 / 1024, 1),
                    "cpu_percent": round(process.cpu_percent(), 1),
                    "threads": process.num_threads()
                },
                "metrics": metrics
            }
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            message=f"健康检查失败: {str(e)}",
            data={"status": "unhealthy"}
        )


@router.get("/metrics")
async def get_metrics():
    """获取性能指标"""
    return ApiResponse(
        success=True,
        message="性能指标获取成功",
        data=request_metrics.get_metrics()
    )
