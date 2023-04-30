from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

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
