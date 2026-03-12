"""
统一 API 响应模型
为所有 API 提供统一的响应格式
"""

from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一 API 响应格式
    
    所有 API 响应都应遵循此格式，以便前端统一处理
    """
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None
    
    @classmethod
    def ok(cls, data: T = None, message: str = None):
        """成功响应"""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def fail(cls, message: str, error: str = None):
        """失败响应"""
        return cls(success=False, message=message, error=error)


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    success: bool = True
    data: list[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 20
    message: Optional[str] = None
