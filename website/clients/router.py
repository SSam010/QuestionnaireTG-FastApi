from math import ceil

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, insert, asc
from sqlalchemy.ext.asyncio import AsyncSession

from clients.models import Client
from clients.schemas import ClientCreate, ClientUpdate, ClientUpdateProcessed
from database import get_async_session
from logger import logger

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"]
)


def paginator(result_execute: sqlalchemy.engine.result.ChunkedIteratorResult, page: int, limit: int):
    # Получаем список записей из запроса
    data = list(result_execute.mappings())
    # Отдаем записи с соответствующим смещением и лимитом
    clients = data[(page - 1) * limit:][:limit]
    # Проверяем, есть ли еще записи
    has_more = len(data[(page - 1) * limit:]) > limit
    # Определяем логическое выражение для пагинации
    down_page = (page - 1) > 0
    # Определяем макс число страниц
    max_page = ceil(len(data) / limit)
    return {"clients": clients, "has_more": has_more, "page": page, "down_page": down_page, "max_page": max_page}


@router.get("")
async def get_all_clients(
        page: int = 1,
        limit: int = 5,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Client).order_by(asc(Client.id))
        result = await session.execute(query)

        data = paginator(result, page, limit)

        return {"status": "success",
                "data": data["clients"],
                "page": data["page"],
                "down_page": data["down_page"],
                "has_more": data["has_more"],
                "max_page": data["max_page"]
                }

    except Exception as e:
        logger.error(e)
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": "error"
        })


@router.get("/not_processed")
async def get_not_processed_clients(
        page: int = 1,
        limit: int = 5,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Client).where(Client.is_processed == False).order_by(asc(Client.id))
        result = await session.execute(query)
        data = paginator(result, page, limit)

        return {"status": "success",
                "data": data["clients"],
                "page": data["page"],
                "down_page": data["down_page"],
                "has_more": data["has_more"],
                "max_page": data["max_page"]
                }

    except Exception as e:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": "error"
        })


@router.post("/add_new_client")
async def add_new_client(new_client: ClientCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Client).values(**new_client.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "New client added",
            "data": None,
            "details": None
        }

    except Exception as e:
        logger.error(f"При создании новой записи произошла ошибка\n{e}")
        return HTTPException(status_code=500, detail={
            "status": "error",
            "data": "error",
            "details": None
        })


# Change client's data
@router.put("/{client_id}")
async def update_client(client_id: int, change_client: ClientUpdate,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(Client).where(Client.id == client_id).values(**change_client.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "changes completed",
            "data": None,
            "details": None
        }

    except Exception as e:
        logger.error(f"При изменении записи клиента id{client_id} произошла ошибка\n{e}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.put("/{client_id}/processed")
async def update_client_processed(client_id: int, is_processed: ClientUpdateProcessed,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(Client).where(Client.id == client_id).values(**is_processed.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }

    except Exception as e:
        logger.error(f"Failed to update 'is_processed' for client id {client_id}\n{e}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
