from enum import Enum

from aiogram.filters.callback_data import CallbackData

_prefix = "menu"


class MenuCallbackActions(str, Enum):
    HOME = "home"


class MenuCallback(CallbackData, prefix=_prefix):
    action: MenuCallbackActions
