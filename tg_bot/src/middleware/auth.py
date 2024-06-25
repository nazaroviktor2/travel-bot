from collections.abc import Awaitable, Callable, Coroutine
from contextvars import ContextVar
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

from src.requests.user import get_user_token_request

access_token_cxt: ContextVar[str] = ContextVar("access_token_cxt")


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Coroutine[Any, Any, Any]]:
        state: FSMContext = data["state"]
        access_token = (await state.get_data()).get("access_token")

        if access_token is None:
            bot: Bot = data["bot"]

            access_token = await get_user_token_request(user_id=data["event_from_user"].id)
            if access_token:
                await state.update_data({"access_token": access_token})
                await state.set_state(None)
            else:
                if data.get("command") and data["command"].command not in {"start"}:
                    await bot.send_message(text="Что-то пошло не так", chat_id=data["event_chat"].id)
                    raise SkipHandler("Unauthorized")

        if access_token is not None:
            access_token_cxt.set(access_token)

        return await handler(event, data)
