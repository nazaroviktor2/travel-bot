from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from src.handlers.main.router import main_router
from src.handlers.menu.home import get_menu_from_command
from src.logger import logger
from src.requests.user import create_user_request


@main_router.message(
    Command(
        "start",
    )
)
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    logger.info("Start cmd")
    user = await create_user_request(user_id=message.from_user.id, username=message.from_user.username)
    await message.answer("Спасибо что пришли!")
    await get_menu_from_command(message, state)
    return
