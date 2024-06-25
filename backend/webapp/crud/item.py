from collections.abc import Sequence
from datetime import datetime

import pytz
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.travel.item import Item


@async_integrations_timer
async def create_item(
    session: AsyncSession,
    user_id: int,
    name: str,
    days_needed: int,
    note: str = "",
) -> Item:
    new_item = Item(name=name, days_needed=days_needed, user_id=user_id, note=note)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


@async_integrations_timer
async def get_user_items(
    session: AsyncSession, user_id: int, offset: int = 0, limit: int = 0, is_deleted: bool = False
) -> Sequence[Item]:
    query = (
        select(Item)
        .where(Item.user_id == user_id, Item.is_deleted == is_deleted)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalars().all()


@async_integrations_timer
async def get_item_by_id(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


@async_integrations_timer
async def delete_user_item(session: AsyncSession, item_id: int, user_id: int) -> bool:
    item = await session.get(Item, item_id)

    if not item:
        return False

    if item.user_id != user_id:
        return False

    item.deleted_at = datetime.now(tz=pytz.UTC)
    item.is_deleted = True
    await session.commit()
    return True


@async_integrations_timer
async def admin_delete_item(session: AsyncSession, item_id: int, force: bool = False) -> bool:
    item = await session.get(Item, item_id)

    if not item:
        return False

    item.deleted_at = datetime.now(tz=pytz.UTC)
    item.is_deleted = True

    if force:
        await session.delete(item)

    await session.commit()
    return False


@async_integrations_timer
async def get_items_for_trip(session: AsyncSession, user_id: int, trip_days: int) -> Sequence[Item]:
    query = select(Item).where(
        Item.user_id == user_id, Item.is_deleted == False, Item.days_needed <= trip_days
    )
    result = await session.execute(query)
    return result.scalars().all()


@async_integrations_timer
async def count_items_for_user(session: AsyncSession, user_id: int) -> int:
    query = select(func.count(Item.id)).where(
        Item.user_id == user_id,
        Item.is_deleted == False,
    )

    result = await session.execute(query)
    return result.fetchone()[0]
