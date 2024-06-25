from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists

from webapp.metrics import async_integrations_timer
from webapp.models.travel.api_key import ApiKey


@async_integrations_timer
async def check_api_key(session: AsyncSession, api_key: str) -> bool:
    query = select(exists().where(ApiKey.key == api_key))
    return bool(await session.scalar(query))
