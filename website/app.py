import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from starlette.staticfiles import StaticFiles

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate
from clients.router import router as router_clients
from logger import logger
from pages.router import router as router_pages

app = FastAPI(title="Финансовый финанс")

app.include_router(router_clients)
app.include_router(router_pages)

app.mount("/static", StaticFiles(directory="static"), name="static")


# сохранение логов при валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    logger.error(f"При валидации запроса возникла ошибка: {errors}")
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"detail": {"validation_error": errors}})


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
# мар
# шрут для регистрации пользователя
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# маршрут для получения аутентификации
app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

