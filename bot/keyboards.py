from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
from bot.config import WEB_VERSION_URL
from typing import List

def create_main_keyboard() -> InlineKeyboardBuilder.as_markup:
    """Основная inline-клавиатура"""
    buttons = [
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
        InlineKeyboardButton(text="👤 По авторам", callback_data="show_authors"),
        InlineKeyboardButton(text="🌐 Веб-версия", url=WEB_VERSION_URL)
    ]
    return InlineKeyboardBuilder().add(*buttons).adjust(2, 1).as_markup()

def create_authors_keyboard(authors: List[str]) -> InlineKeyboardBuilder.as_markup:
    """Клавиатура со списком авторов"""
    builder = InlineKeyboardBuilder()
    builder.add(*[
        InlineKeyboardButton(text=author, callback_data=f"author_{author}")
        for author in sorted(authors)
    ])
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    return builder.adjust(2).as_markup()

def create_reply_keyboard() -> ReplyKeyboardBuilder.as_markup:
    """Обычная reply-клавиатура"""
    buttons = [
        KeyboardButton(text="/start"),
        KeyboardButton(text="/check")
    ]
    return ReplyKeyboardBuilder().add(*buttons).adjust(2).as_markup(resize_keyboard=True)

def create_back_to_authors_keyboard() -> InlineKeyboardBuilder.as_markup:
    """Клавиатура для возврата к авторам"""
    buttons = [
        InlineKeyboardButton(text="⬅️ К списку авторов", callback_data="back_to_authors"),
        InlineKeyboardButton(text="↩️ В главное меню", callback_data="back_to_main")
    ]
    return InlineKeyboardBuilder().add(*buttons).adjust(1).as_markup()