from sqlalchemy.ext.asyncio import AsyncSession

from webapp.logger import logger
from webapp.metrics import async_integrations_timer
from webapp.models.travel.user import User
from webapp.schema.auth.register.user import UserRegister


@async_integrations_timer
async def db_get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


@async_integrations_timer
async def create_user(session: AsyncSession, user_info: UserRegister) -> User | None:
    try:
        user = User(id=user_info.id, username=user_info.username)

        session.add(user)
        await session.commit()
        return user
    except Exception as err:
        logger.error(f"An error occurred while creating a user: {err}")
        await session.rollback()
        return None
