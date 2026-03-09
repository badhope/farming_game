"""
启动 FastAPI 后端服务器
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 启动 FastAPI 后端服务器...")
    print("=" * 50)
    print("\n📡 API 文档地址:")
    print("   - Swagger UI: http://localhost:8000/api/docs")
    print("   - ReDoc: http://localhost:8000/api/redoc")
    print("\n💡 提示:")
    print("   - 按 Ctrl+C 停止服务器")
    print("   - 确保前端已配置 CORS")
    print("\n" + "=" * 50)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式自动重载
    )
