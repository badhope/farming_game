from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional

from backend.database.db_config import get_db
from backend.schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token,
    RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm
)
from backend.schemas.api_response import ApiResponse

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = secrets.token_hex(32)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

refresh_tokens_store = {}
password_reset_tokens = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp(), "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire.timestamp(), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    from backend.models.db_models import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        last_login=user.last_login,
        total_playtime=user.total_playtime,
        level=user.level
    )


@router.post("/register", response_model=ApiResponse[UserResponse])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    from backend.models.db_models import User
    
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    import uuid
    new_user = User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role="player",
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_response = UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=new_user.role,
        created_at=new_user.created_at,
        last_login=new_user.last_login,
        total_playtime=new_user.total_playtime,
        level=new_user.level
    )
    
    return ApiResponse(
        success=True,
        message="注册成功",
        data=user_response
    )


@router.post("/login", response_model=ApiResponse[Token])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    from backend.models.db_models import User
    
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token({"sub": user.id, "username": user.username, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.id})
    
    refresh_tokens_store[refresh_token] = user.id
    
    token_data = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return ApiResponse(
        success=True,
        message="登录成功",
        data=token_data
    )


@router.post("/refresh", response_model=ApiResponse[Token])
async def refresh_token(request: RefreshTokenRequest):
    payload = decode_token(request.refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    user_id = payload.get("sub")
    if user_id not in refresh_tokens_store.values():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌已失效"
        )
    
    from backend.database.db_config import get_db_session
    db = next(get_db_session())
    from backend.models.db_models import User
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    access_token = create_access_token({"sub": user.id, "username": user.username, "role": user.role})
    new_refresh_token = create_refresh_token({"sub": user.id})
    
    return ApiResponse(
        success=True,
        message="令牌刷新成功",
        data=Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )


@router.post("/logout")
async def logout(current_user: UserResponse = Depends(get_current_user)):
    return ApiResponse(
        success=True,
        message="登出成功"
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return ApiResponse(
        success=True,
        message="获取用户信息成功",
        data=current_user
    )


@router.post("/password/reset", response_model=ApiResponse)
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    from backend.models.db_models import User
    
    user = db.query(User).filter(User.email == request.email).first()
    
    if user:
        reset_token = secrets.token_urlsafe(32)
        password_reset_tokens[reset_token] = user.id
        
        return ApiResponse(
            success=True,
            message="如果邮箱存在，将收到密码重置链接"
        )
    
    return ApiResponse(
        success=True,
        message="如果邮箱存在，将收到密码重置链接"
    )


@router.post("/password/reset/confirm", response_model=ApiResponse)
async def confirm_password_reset(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    from backend.models.db_models import User
    
    user_id = password_reset_tokens.get(request.token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效或已过期的重置令牌"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.password_hash = get_password_hash(request.new_password)
        db.commit()
        
        del password_reset_tokens[request.token]
        
        return ApiResponse(
            success=True,
            message="密码重置成功"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="用户不存在"
    )
