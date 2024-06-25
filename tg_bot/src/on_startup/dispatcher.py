from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.handlers.items.router import items_router
from src.handlers.main.router import main_router
from src.handlers.menu.router import menu_router
from src.handlers.travel.router import travel_router
from src.integrations.redis import redis
from src.middleware.auth import AuthMiddleware
from src.middleware.logger import LogMessageMiddleware
from src.middleware.throttling import ThrottlingMiddleware


def setup_dispatcher(bot: Bot) -> Dispatcher:
    storage = RedisStorage(redis)
    dp = Dispatcher(storage=storage, bot=bot)

    dp.include_routers(main_router)
    dp.include_routers(travel_router)
    dp.include_routers(items_router)
    dp.include_routers(menu_router)

    dp.message.middleware(LogMessageMiddleware())
    dp.callback_query.middleware(LogMessageMiddleware())

    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    dp.message.middleware(ThrottlingMiddleware(redis))
    dp.callback_query.middleware(ThrottlingMiddleware(redis))

    return dp
