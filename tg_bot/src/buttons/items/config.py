from enum import Enum

from aiogram.filters.callback_data import CallbackData

_prefix = "items"


class ItemsCallbackActions(str, Enum):
    MY_ITEMS = "my"
    HOME = "home"
    ADD_ITEM = "add"
    SHOW = "show"
    DELETE = "delete"


class ItemsCallback(CallbackData, prefix=_prefix):
    action: ItemsCallbackActions
    offset: int = 0
    limit: int = 5
    item_id: int | None = None
