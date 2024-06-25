from enum import Enum

from aiogram.filters.callback_data import CallbackData

_prefix = "travel"


class TravelCallbackActions(str, Enum):
    GO_TRAVEL = "go"
    START = "start"


class TravelCallback(CallbackData, prefix=_prefix):
    action: TravelCallbackActions
