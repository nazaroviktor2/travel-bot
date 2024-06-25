from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.buttons.base import TO_MAIN_MENU_BUTTON
from src.buttons.items.config import ItemsCallback, ItemsCallbackActions


def get_items_menu():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Посмотреть",
            callback_data=ItemsCallback(action=ItemsCallbackActions.MY_ITEMS).pack(),
        ),
        InlineKeyboardButton(
            text="Новая вещь",
            callback_data=ItemsCallback(action=ItemsCallbackActions.ADD_ITEM).pack(),
        ),
    )
    builder.row(TO_MAIN_MENU_BUTTON)
    return builder.as_markup()


def get_cancel_keyboad():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/cancel"),
            ]
        ],
        resize_keyboard=True,
    )


def get_cancel_or_skip_keyboad():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="нет"),
            ],
            [
                KeyboardButton(text="/cancel"),
            ],
        ],
        resize_keyboard=True,
    )
