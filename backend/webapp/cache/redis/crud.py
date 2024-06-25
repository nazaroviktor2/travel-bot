from typing import Any

import orjson
from conf.config import settings

from webapp.cache.redis.key_builder import get_model_cache
from webapp.db.redis import get_redis
from webapp.metrics import async_integrations_timer


@async_integrations_timer
async def redis_set_model(model: str, model_id: int, payload: Any) -> None:
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    await redis.set(redis_key, orjson.dumps(payload), ex=settings.FILE_EXPIRE_TIME)


@async_integrations_timer
async def redis_get_model(model: str, model_id: int) -> dict[str, str]:
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return orjson.loads(cache)


@async_integrations_timer
async def redis_drop_model_key(model: str, model_id: int) -> None:
    redis = get_redis()
    redis_key = await get_model_cache(model, model_id)
    await redis.delete(redis_key)
