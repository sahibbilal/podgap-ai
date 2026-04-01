from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models import User
from app.core.security import decode_access_token

security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User | None:
    if not credentials:
        return None
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        return None
    result = await db.execute(select(User).where(User.id == int(user_id), User.is_active == True))
    return result.scalar_one_or_none()


async def get_current_user(
    current_user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return current_user
