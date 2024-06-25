from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.auth.login.login import get_user
from webapp.api.v1.items.router import items_router
from webapp.crud.item import count_items_for_user
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.models.travel.user import User


@items_router.get(
    "/user/count",
)
async def count_user_items(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        count = await count_items_for_user(
            user_id=user.id,
            session=session,
        )
        return ORJSONResponse(content={"count": count}, status_code=status.HTTP_200_OK)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"An error occurred while verifying login information: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
