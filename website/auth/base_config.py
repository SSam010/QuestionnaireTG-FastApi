import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy
from fastapi_users.authentication import CookieTransport

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_KEY

SECRET = SECRET_KEY

cookie_transport = CookieTransport(cookie_name="fin-cook", cookie_max_age=60*60*24*31)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=60*60*24*31)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)
