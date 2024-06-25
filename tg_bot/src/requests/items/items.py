from conf.config import settings
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from src.logger import logger
from src.requests import do_request

BASE_URL = f"{settings.BACKEND_HOST}/api/v1/items"


async def count_user_items() -> int:
    response, status = await do_request(url=BASE_URL + "/user/count", method="GET")
    if status != HTTP_200_OK:
        logger.error(response)

    return response.get("count")


async def create_new_item_request(
    name: str,
    days_needed: int,
    note: str = None,
):
    response, status = await do_request(
        url=BASE_URL,
        method="POST",
        params={
            "name": name,
            "days_needed": days_needed,
            "note": note,
        },
    )
    logger.info(response)
    if status != HTTP_201_CREATED:
        logger.error(response)

    return response["item"]


async def get_items_for_trip_request(
    trip_days: int,
):
    response, status = await do_request(
        url=BASE_URL + f"/trip?trip_days={trip_days}",
        method="GET",
    )
    logger.info(response)
    if status != HTTP_200_OK:
        logger.error(response)

    return response["items"]


async def get_user_items_request(offset: int, limit: int):
    response, status = await do_request(
        url=BASE_URL + f"?offset={offset}&limit={limit}",
        method="GET",
    )
    logger.info(response)
    if status != HTTP_200_OK:
        logger.error(response)

    return response["items"]


async def get_item_by_id_request(
    item_id: int,
):
    response, status = await do_request(
        url=BASE_URL + f"/{item_id}",
        method="GET",
    )
    logger.info(response)
    if status == HTTP_404_NOT_FOUND:
        return None

    if status != HTTP_200_OK:
        logger.error(response)
    return response["item"]


async def delete_item_by_id_request(
    item_id: int,
):
    response, status = await do_request(
        url=BASE_URL + f"/{item_id}",
        method="DELETE",
    )
    logger.info(response)
    if status != HTTP_200_OK:
        logger.error(response)
