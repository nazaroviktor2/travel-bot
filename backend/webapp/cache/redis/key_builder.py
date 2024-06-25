from conf.config import settings


async def get_model_cache(model: str, user_id: int) -> str:
    return f"{settings.REDIS_CACHE_PREFIX}:{model}:{user_id}"


async def get_rate_limit_cache(func: str, user_id: int) -> str:
    return f"{settings.REDIS_CACHE_PREFIX}:rate_limit:{func}:{user_id}"
