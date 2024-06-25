from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.buttons.items.config import ItemsCallback, ItemsCallbackActions
from src.buttons.travel.config import TravelCallback, TravelCallbackActions


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Путешествие", callback_data=TravelCallback(action=TravelCallbackActions.GO_TRAVEL).pack()
        ),
        InlineKeyboardButton(
            text="Мои вещи", callback_data=ItemsCallback(action=ItemsCallbackActions.HOME).pack()
        ),
    )
    return builder.as_markup()
