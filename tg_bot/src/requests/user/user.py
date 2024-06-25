from conf.config import settings
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.requests import do_request


async def create_user_request(user_id: int, username: str) -> bool:
    _, status = await do_request(
        f"{settings.BACKEND_HOST}/api/v1/auth/register",
        headers={"Authorization": f"Bearer {settings.BACKEND_API_KEY}"},
        params={"id": user_id, "username": username},
    )
    if status != HTTP_201_CREATED:
        return False

    return True


async def get_user_token_request(user_id: int) -> str | None:
    response, status = await do_request(
        f"{settings.BACKEND_HOST}/api/v1/auth/login",
        headers={"Authorization": f"Bearer {settings.BACKEND_API_KEY}"},
        params={"id": user_id},
    )
    if status != HTTP_200_OK:
        return None

    return response["access_token"]
