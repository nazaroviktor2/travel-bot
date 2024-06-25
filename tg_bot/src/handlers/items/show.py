from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.buttons.items.config import ItemsCallback, ItemsCallbackActions
from src.buttons.menu.getter import get_main_menu
from src.handlers.items.router import items_router
from src.requests.items.items import (
    delete_item_by_id_request,
    get_item_by_id_request,
    get_user_items_request,
)


@items_router.callback_query(ItemsCallback.filter(F.action == ItemsCallbackActions.MY_ITEMS))
async def get_my_items(callback: CallbackQuery, callback_data: ItemsCallback, state: FSMContext) -> None:
    await callback.answer()

    items = await get_user_items_request(offset=callback_data.offset, limit=callback_data.limit)

    buttons = [
        [
            InlineKeyboardButton(
                text=item["name"],
                callback_data=ItemsCallback(
                    action=ItemsCallbackActions.SHOW,
                    offset=callback_data.offset,
                    limit=callback_data.limit,
                    item_id=item["id"],
                ).pack(),
            )
        ]
        for item in items
    ]
    if len(items) == callback_data.limit:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперед",
                    callback_data=ItemsCallback(
                        action=ItemsCallbackActions.MY_ITEMS,
                        offset=callback_data.offset + callback_data.limit,
                        limit=callback_data.limit,
                    ).pack(),
                )
            ]
        )
    if callback_data.offset > 0:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=ItemsCallback(
                        action=ItemsCallbackActions.MY_ITEMS,
                        offset=max(0, callback_data.offset - callback_data.limit),
                        limit=callback_data.limit,
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="Домой",
                callback_data=ItemsCallback(
                    action=ItemsCallbackActions.HOME, offset=callback_data.offset, limit=callback_data.limit
                ).pack(),
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Ваши вещи:", reply_markup=reply_markup)


@items_router.callback_query(ItemsCallback.filter(F.action == ItemsCallbackActions.SHOW))
async def process_view_item(
    callback: types.CallbackQuery, callback_data: ItemsCallback, state: FSMContext
) -> None:
    await callback.answer()

    item = await get_item_by_id_request(item_id=callback_data.item_id)
    buttons = []
    if item:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=ItemsCallback(
                        action=ItemsCallbackActions.DELETE,
                        offset=callback_data.offset,
                        limit=callback_data.limit,
                        item_id=callback_data.item_id,
                    ).pack(),
                )
            ],
        )
        text = (
            f"Название: {item['name']}\n"
            f"Количество дней: {item['days_needed']}\n"
            f"Заметка: {item['note'] or 'Нет'}"
        )
    else:
        text = "Предмет не найден"
    buttons.append(
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data=ItemsCallback(
                    action=ItemsCallbackActions.MY_ITEMS,
                    offset=callback_data.offset,
                    limit=callback_data.limit,
                ).pack(),
            )
        ]
    )
    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@items_router.callback_query(ItemsCallback.filter(F.action == ItemsCallbackActions.DELETE))
async def process_main_menu(
    callback_query: types.CallbackQuery, callback_data: ItemsCallback, state: FSMContext
) -> None:
    await callback_query.answer()
    await delete_item_by_id_request(item_id=callback_data.item_id)
    await callback_query.message.edit_text("Главное меню:", reply_markup=get_main_menu())
