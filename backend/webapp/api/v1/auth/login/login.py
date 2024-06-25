from typing import Annotated

from fastapi import Depends, Header, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.auth.router import auth_router
from webapp.crud.user import db_get_user
from webapp.db.postgres import get_session
from webapp.logger import logger
from webapp.models.travel.user import User
from webapp.schema.auth.login.user import UserLogin, UserLoginResponse
from webapp.utils.auth.api_key import validate_and_check_api_key
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
)
async def auth_login_handler(
    body: UserLogin,
    authorization: Annotated[str, Header()],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        valid_token = await validate_and_check_api_key(session, authorization)
        if not valid_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        user = await db_get_user(session, body.id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return ORJSONResponse(
            {
                "access_token": jwt_auth.create_token(user),
            }
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"An error occurred during login: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


async def get_user(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> User:
    user_id = access_token.get("user_id")

    user = await db_get_user(session, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
