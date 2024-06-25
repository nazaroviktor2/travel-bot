from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.auth.login.login import get_user
from webapp.api.v1.items.router import items_router
from webapp.cache.redis.crud import redis_drop_model_key, redis_get_model, redis_set_model
from webapp.crud.item import (
    create_item,
    delete_user_item,
    get_item_by_id,
    get_items_for_trip,
    get_user_items,
)
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.models.travel.item import Item
from webapp.models.travel.user import User
from webapp.schema.item.item import CreateItemRequest, ItemDTO


@items_router.get(
    "/trip",
    response_model=list[ItemDTO],
)
async def get_to_trip(
    trip_days: int,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        items = await get_items_for_trip(
            session=session,
            user_id=user.id,
            trip_days=trip_days,
        )
        return ORJSONResponse(
            content={"items": [ItemDTO.model_validate(item).model_dump() for item in items]},
            status_code=status.HTTP_200_OK,
        )
    except Exception as er:
        logger.error(f"An error in get items for trip: {er}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@items_router.get(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
)
async def get_item(
    item_id: int,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        cached_item = await redis_get_model(Item.__tablename__, item_id)

        if cached_item:
            return ORJSONResponse(
                content={"item": cached_item},
                status_code=status.HTTP_200_OK,
            )

        item = await get_item_by_id(session=session, item_id=item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item not found {item_id}")

        itemDTO = ItemDTO.model_validate(item).model_dump()
        await redis_set_model(Item.__tablename__, item_id, itemDTO)

        return ORJSONResponse(
            content={"item": itemDTO},
            status_code=status.HTTP_200_OK,
        )
    except Exception as er:
        logger.error(f"An error in delete items: {er}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@items_router.get("", response_model=list[ItemDTO])
async def get_items(
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        items = await get_user_items(
            session=session,
            user_id=user.id,
            offset=offset,
            limit=limit,
        )
        dto_items = [ItemDTO.model_validate(item).model_dump() for item in items]
        return ORJSONResponse(
            content={"items": dto_items, "count": len(dto_items)},
            status_code=status.HTTP_200_OK,
        )
    except Exception as er:
        logger.error(f"An error in get items: {er}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@items_router.post(
    "",
    response_model=ItemDTO,
)
async def new_item(
    payload: CreateItemRequest,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        item = await create_item(
            session=session,
            user_id=user.id,
            name=payload.name,
            days_needed=payload.days_needed,
            note=payload.note,
        )
        logger.info(item)
        return ORJSONResponse(
            content={"item": ItemDTO.model_validate(item).model_dump()},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as er:
        logger.error(f"An error in create items: {er}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@items_router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(
    item_id: int,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    try:
        await delete_user_item(session=session, user_id=user.id, item_id=item_id)
        redis_drop_model_key(Item.__tablename__, item_id)

        return
    except Exception as er:
        logger.error(f"An error in delete items: {er}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
