from aiogram.types import InlineKeyboardButton

from src.buttons.menu.config import MenuCallback, MenuCallbackActions

TO_MAIN_MENU_BUTTON = InlineKeyboardButton(
    text="Назад", callback_data=MenuCallback(action=MenuCallbackActions.HOME).pack()
)
