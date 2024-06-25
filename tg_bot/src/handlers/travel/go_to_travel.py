from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from src.buttons.items.getter import get_cancel_keyboad
from src.buttons.travel.config import TravelCallback, TravelCallbackActions
from src.buttons.travel.getter import get_main_menu
from src.handlers.menu.home import get_menu_from_command
from src.handlers.travel.router import travel_router
from src.requests.items.items import get_items_for_trip_request
from src.state.travel import NewTripStates


@travel_router.callback_query(TravelCallback.filter(F.action == TravelCallbackActions.GO_TRAVEL))
async def start_travel(callback: CallbackQuery, callback_data: TravelCallback, state: FSMContext) -> None:
    await callback.message.edit_text(
        text="Хотите отправиться в новую поездку?",
        reply_markup=get_main_menu(),
    )

    await callback.answer()


@travel_router.callback_query(TravelCallback.filter(F.action == TravelCallbackActions.START))
async def start_travel(callback: CallbackQuery, callback_data: TravelCallback, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text="На сколько дней планируете поездку?", reply_markup=get_cancel_keyboad()
    )

    await state.set_state(NewTripStates.waiting_for_trip_days)


@travel_router.message(NewTripStates.waiting_for_trip_days)
async def process_trip_days(message: types.Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await cancel_handler(message, state)
        return

    try:
        trip_days = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return
    items_for_trip = await get_items_for_trip_request(trip_days=trip_days)

    if items_for_trip:
        response = "Вам нужно взять в поездку следующие предметы:\n"
        for item in items_for_trip:
            st = f"-<b>{item['name']}</b> (на {item['days_needed']})\n"

            st += f"        {item['note']}\n" if item["note"] else ""
            response += st
    else:
        response = "У вас нет предметов, которые нужно взять в эту поездку."

    await message.answer(response, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    await state.clear()
    await get_menu_from_command(message, state)


@travel_router.message(NewTripStates.cancel)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("Поездки не будет.", reply_markup=ReplyKeyboardRemove())
        await get_menu_from_command(message, state)
    else:
        await message.answer("Нет активного процесса для отмены.")
