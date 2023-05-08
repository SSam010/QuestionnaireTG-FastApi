import uuid
from typing import Optional

from fastapi_users import schemas
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import UUID


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: UUID_ID
    username: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
