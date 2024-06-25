from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.buttons.base import TO_MAIN_MENU_BUTTON
from src.buttons.travel.config import TravelCallback, TravelCallbackActions


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Да!", callback_data=TravelCallback(action=TravelCallbackActions.START).pack()
        ),
    )
    builder.row(TO_MAIN_MENU_BUTTON)
    return builder.as_markup()
