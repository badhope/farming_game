from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import json

from backend.database.db_config import get_db
from backend.schemas.sync import (
    SyncRequest, SyncResponse, SyncStatus, SyncStatusResponse,
    CloudSaveResponse, GameSave, Platform
)
from backend.schemas.api_response import ApiResponse
from backend.api.auth import get_current_user

router = APIRouter(prefix="/sync", tags=["数据同步"])

user_saves = {}


@router.post("/push", response_model=ApiResponse[SyncResponse])
async def push_sync_data(
    request: SyncRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id
    client_data = request.client_data
    client_data.user_id = user_id
    client_data.synced_at = datetime.utcnow()
    
    if user_id not in user_saves:
        user_saves[user_id] = []
    
    server_timestamp = datetime.utcnow().timestamp()
    client_timestamp = client_data.timestamp.timestamp() if client_data.timestamp else 0
    
    if client_timestamp < server_timestamp - 86400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="数据过于陈旧，请先拉取最新数据"
        )
    
    user_saves[user_id].append(client_data.dict())
    
    return ApiResponse(
        success=True,
        message="数据同步成功",
        data=SyncResponse(
            server_data=client_data,
            sync_status=SyncStatus.SYNCED,
            conflicts=[],
            message="数据已成功同步到服务器"
        )
    )


@router.get("/pull", response_model=ApiResponse[GameSave])
async def pull_sync_data(
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    
    if user_id not in user_saves or not user_saves[user_id]:
        default_save = GameSave(
            user_id=user_id,
            version="1.0.0",
            timestamp=datetime.utcnow(),
            platform=Platform.WEB
        )
        
        return ApiResponse(
            success=True,
            message="未找到存档，返回默认存档",
            data=default_save
        )
    
    latest_save = user_saves[user_id][-1]
    
    return ApiResponse(
        success=True,
        message="数据拉取成功",
        data=GameSave(**latest_save)
    )


@router.get("/status", response_model=ApiResponse[SyncStatusResponse])
async def get_sync_status(
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    
    pending_count = 0
    last_sync = None
    
    if user_id in user_saves and user_saves[user_id]:
        last_save = user_saves[user_id][-1]
        last_sync = datetime.fromisoformat(last_save.get("synced_at", ""))
        pending_count = len(user_saves[user_id])
    
    status = SyncStatus.SYNCED if pending_count == 0 else SyncStatus.PENDING
    
    return ApiResponse(
        success=True,
        message="同步状态获取成功",
        data=SyncStatusResponse(
            user_id=user_id,
            last_sync=last_sync,
            pending_changes=pending_count,
            status=status
        )
    )


@router.post("/resolve", response_model=ApiResponse[SyncResponse])
async def resolve_conflicts(
    resolution: dict,
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    
    if user_id not in user_saves:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="没有找到需要解决的冲突"
        )
    
    resolved_data = resolution.get("resolved_data")
    if not resolved_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少解决后的数据"
        )
    
    game_save = GameSave(**resolved_data)
    game_save.user_id = user_id
    game_save.synced_at = datetime.utcnow()
    
    user_saves[user_id].append(game_save.dict())
    
    return ApiResponse(
        success=True,
        message="冲突已解决",
        data=SyncResponse(
            server_data=game_save,
            sync_status=SyncStatus.SYNCED,
            conflicts=[],
            message="冲突已成功解决"
        )
    )


@router.get("/cloud/saves", response_model=ApiResponse[CloudSaveResponse])
async def list_cloud_saves(
    limit: int = 10,
    offset: int = 0,
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    
    if user_id not in user_saves:
        return ApiResponse(
            success=True,
            message="暂无云存档",
            data=CloudSaveResponse(saves=[], total=0)
        )
    
    saves = user_saves[user_id][offset:offset+limit]
    total = len(user_saves[user_id])
    
    game_saves = [GameSave(**s) for s in saves]
    
    return ApiResponse(
        success=True,
        message="云存档列表获取成功",
        data=CloudSaveResponse(saves=game_saves, total=total)
    )


@router.post("/cloud/save", response_model=ApiResponse)
async def create_cloud_save(
    save_data: GameSave,
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    save_data.user_id = user_id
    save_data.synced_at = datetime.utcnow()
    
    if user_id not in user_saves:
        user_saves[user_id] = []
    
    user_saves[user_id].append(save_data.dict())
    
    return ApiResponse(
        success=True,
        message="云存档创建成功"
    )


@router.delete("/cloud/save/{save_id}", response_model=ApiResponse)
async def delete_cloud_save(
    save_id: int,
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    
    if user_id not in user_saves or save_id >= len(user_saves[user_id]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="存档不存在"
        )
    
    del user_saves[user_id][save_id]
    
    return ApiResponse(
        success=True,
        message="云存档删除成功"
    )
