from typing import Optional
from fastapi import Header

from api.core.config import settings
from api.core.exceptions import (
    UnauthorizedException,
    ForbiddenException,
)

async def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> bool:
    if not x_api_key:
        raise UnauthorizedException(detail="X-API-Key header required")
    if x_api_key != settings.SECRET_KEY:
        raise ForbiddenException(detail="Invalid API key")
    return True
