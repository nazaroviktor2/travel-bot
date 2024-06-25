from aiogram.fsm.state import State, StatesGroup


class NewTripStates(StatesGroup):
    waiting_for_trip_days = State()
    cancel = State()
