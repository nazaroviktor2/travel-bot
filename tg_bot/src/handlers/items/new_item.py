from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.buttons.items.config import ItemsCallback, ItemsCallbackActions
from src.buttons.items.getter import get_cancel_keyboad, get_cancel_or_skip_keyboad
from src.handlers.items.router import items_router
from src.handlers.menu.home import get_menu_from_command
from src.requests.items.items import create_new_item_request
from src.state.item import AddItemStates


@items_router.message(AddItemStates.cancel)
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("Добавление предмета отменено.", reply_markup=ReplyKeyboardRemove())
        await get_menu_from_command(message, state)
    else:
        await message.answer("Нет активного процесса для отмены.")


@items_router.callback_query(ItemsCallback.filter(F.action == ItemsCallbackActions.ADD_ITEM))
async def get_items_home(callback: CallbackQuery, callback_data: ItemsCallback, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer(
        "Давайте добавил новую вещь!\nВведите название нового предмета:", reply_markup=get_cancel_keyboad()
    )

    await state.set_state(AddItemStates.waiting_for_item_name)

    await callback.answer()


@items_router.message(AddItemStates.waiting_for_item_name)
async def process_item_name(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await cancel_handler(message, state)
        return

    await state.update_data(item_name=message.text)
    await message.answer(
        "Введите количество дней, после которого надо брать предмет в поездку:",
        reply_markup=get_cancel_keyboad(),
    )

    await state.set_state(AddItemStates.waiting_for_item_days_needed)


@items_router.message(AddItemStates.waiting_for_item_days_needed)
async def process_item_days_needed(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await cancel_handler(message, state)
        return

    try:
        days_needed = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    if days_needed <= 0:
        await message.answer("Пожалуйста, введите число больше или равное 0.")
        return

    await state.update_data(days_needed=days_needed)

    await message.answer(
        'Введите заметку для предмета (или нажмите "нет", если заметка не нужна):',
        reply_markup=get_cancel_or_skip_keyboad(),
    )

    await state.set_state(AddItemStates.waiting_for_item_note)


@items_router.message(AddItemStates.waiting_for_item_note)
async def process_item_note(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await cancel_handler(message, state)
        return

    item_note = message.text if message.text.lower() != "нет" else None
    await state.update_data(item_note=item_note)

    user_data = await state.get_data()
    item_name = user_data["item_name"]
    days_needed = user_data["days_needed"]

    item = await create_new_item_request(name=item_name, days_needed=days_needed, note=item_note)
    await message.answer(
        f'Предмет "{item.get("name")}" успешно добавлен!', reply_markup=ReplyKeyboardRemove()
    )
    await get_menu_from_command(message, state)
    await state.clear()
