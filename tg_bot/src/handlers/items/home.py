from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.buttons.items.config import ItemsCallback, ItemsCallbackActions
from src.buttons.items.getter import get_items_menu
from src.handlers.items.router import items_router
from src.requests.items.items import count_user_items


@items_router.callback_query(ItemsCallback.filter(F.action == ItemsCallbackActions.HOME))
async def get_items_home(callback: CallbackQuery, callback_data: ItemsCallback, state: FSMContext) -> None:
    count = await count_user_items()
    await callback.message.edit_text(text=f"У вас есть {count} вещей!", reply_markup=get_items_menu())

    await callback.answer()
