from aiogram.fsm.state import State, StatesGroup


class AddItemStates(StatesGroup):
    waiting_for_item_name = State()
    waiting_for_item_days_needed = State()
    waiting_for_item_note = State()
    cancel = State()
