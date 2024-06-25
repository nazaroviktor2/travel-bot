from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.buttons.menu.config import MenuCallback, MenuCallbackActions
from src.buttons.menu.getter import get_main_menu
from src.handlers.menu.router import menu_router
from src.logger import logger


@menu_router.callback_query(MenuCallback.filter(F.action == MenuCallbackActions.HOME))
async def get_menu(callback: CallbackQuery, callback_data: MenuCallback, state: FSMContext) -> None:
    logger.info("Menu callback")
    await callback.answer()
    await callback.message.edit_text("Что хотите сделать?", reply_markup=get_main_menu())


@menu_router.message(Command("menu"))
async def get_menu_from_command(message: types.Message, state: FSMContext) -> None:
    logger.info("Menu cmd")
    await message.answer("Что хотите сделать?", reply_markup=get_main_menu())
