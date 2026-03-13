from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import logging
import json
from datetime import datetime
from typing import Callable
from functools import wraps

logger = logging.getLogger("farming_game.performance")


class PerformanceMonitorMiddleware(BaseHTTPMiddleware):
    """性能监控中间件"""
    
    def __init__(self, app: ASGIApp, slow_request_threshold: float = 1.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        request_id = request.headers.get("X-Request-ID", f"req_{int(time.time() * 1000)}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            log_data = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": round(process_time, 3),
                "client_ip": request.client.host if request.client else "unknown",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if process_time > self.slow_request_threshold:
                logger.warning(f"慢请求警告: {json.dumps(log_data)}")
            else:
                logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
            
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time, 3))
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"请求异常: {request.method} {request.url.path} - {str(e)} - {process_time:.3f}s")
            raise


def log_api_call(func: Callable) -> Callable:
    """API调用日志装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
        
        try:
            result = await func(*args, **kwargs)
            process_time = time.time() - start_time
            
            logger.info(f"API调用: {func_name} - 耗时: {process_time:.3f}s")
            
            return result
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"API异常: {func_name} - 耗时: {process_time:.3f}s - 错误: {str(e)}")
            raise
    
    return wrapper


class RequestMetrics:
    """请求指标收集器"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.slow_requests = 0
        self.start_time = time.time()
    
    def record_request(self, response_time: float, is_error: bool = False, is_slow: bool = False):
        self.request_count += 1
        if is_error:
            self.error_count += 1
        if is_slow:
            self.slow_requests += 1
        self.total_response_time += response_time
    
    def get_metrics(self) -> dict:
        uptime = time.time() - self.start_time
        avg_response_time = self.total_response_time / self.request_count if self.request_count > 0 else 0
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "slow_requests": self.slow_requests,
            "average_response_time": round(avg_response_time, 3),
            "error_rate_percent": round(error_rate, 2),
            "requests_per_second": round(self.request_count / uptime, 2) if uptime > 0 else 0
        }
    
    def reset(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.slow_requests = 0
        self.start_time = time.time()


request_metrics = RequestMetrics()
