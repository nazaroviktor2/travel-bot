from typing import Any

import aiohttp
from aiohttp.typedefs import LooseHeaders
from conf.config import settings
from multidict import CIMultiDict
from starlette import status

from src.logger import correlation_id_ctx, logger


class ClientSessionWithCorrId(aiohttp.ClientSession):
    def _prepare_headers(self, headers: LooseHeaders | None) -> CIMultiDict[str]:
        headers = super()._prepare_headers(headers)

        correlation_id = correlation_id_ctx.get()
        headers["X-Correlation-Id"] = correlation_id

        return headers


async def do_request(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    data: Any = None,
    method: str = "POST",
) -> Any:
    from src.middleware.auth import access_token_cxt

    try:
        headers_ = {"Authorization": f"Bearer {access_token_cxt.get()}"}
    except LookupError:
        headers_ = {}

    timeout = aiohttp.ClientTimeout(total=3)
    connector = aiohttp.TCPConnector()

    if headers is not None:
        headers_.update(headers)

    final_exc = None
    async with ClientSessionWithCorrId(
        connector=connector, timeout=timeout, raise_for_status=check_response_status
    ) as session:
        for _ in range(settings.RETRY_COUNT):
            try:
                async with session.request(
                    method, url, headers=headers_, json=params, data=data
                ) as response:
                    if response.content_type == "application/json":
                        return await response.json(), response.status
                    return None, response.status
            except aiohttp.ClientResponseError as exc:
                logger.exception("Http error")
                final_exc = exc

    if final_exc is not None:
        raise final_exc

    raise RuntimeError("Unsupported")


async def check_response_status(response: aiohttp.ClientResponse) -> aiohttp.ClientResponseError | None:
    if response.status >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise RuntimeError
