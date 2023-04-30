import asyncio

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select, update, insert, asc
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from clients.models import Client
from clients.schemas import ClientCreate, ClientUpdate, ClientUpdateProcessed
from database import get_async_session


router = APIRouter(
     prefix="/api/v1/clients",
     tags=["Clients"]
)


@router.get("")
async def get_all_clients(
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Client).order_by(asc(Client.id))
        result = await session.execute(query)
        return {
            "status": "success",
            "data": list(result.mappings()),
            "details": None
        }

    except Exception as e:
        logger.error(e)
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": "error",
            "details": None
        })


@router.get("/not_processed")
async def get_not_processed_clients(
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Client).where(Client.is_processed == False)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": list(result.mappings()),
            "details": None
        }
    except Exception as e:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": "error",
            "details": None
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
async def update_client(client_id: int, change_client: ClientUpdate, session: AsyncSession = Depends(get_async_session)):
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
async def update_client_processed(client_id: int, is_processed: ClientUpdateProcessed, session: AsyncSession = Depends(get_async_session)):
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
