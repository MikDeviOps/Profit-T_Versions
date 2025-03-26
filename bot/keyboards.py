from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
from bot.config import WEB_VERSION_URL

def create_main_keyboard():
    """Основная inline-клавиатура"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
        InlineKeyboardButton(text="👤 По авторам", callback_data="show_authors"),
        InlineKeyboardButton(text="🌐 Веб-версия", url=WEB_VERSION_URL)
    )
    builder.adjust(2, 1)
    return builder.as_markup()

def create_authors_keyboard(authors: list):
    """Клавиатура со списком авторов"""
    builder = InlineKeyboardBuilder()
    for author in sorted(authors):
        builder.add(InlineKeyboardButton(
            text=author,
            callback_data=f"author_{author}"
        ))
    builder.add(InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="back_to_main"
    ))
    builder.adjust(2)
    return builder.as_markup()

def create_reply_keyboard():
    """Обычная reply-клавиатура"""
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="/start"),
        KeyboardButton(text="/check")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def create_back_to_authors_keyboard():
    """Клавиатура для возврата к авторам"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="⬅️ К списку авторов",
            callback_data="back_to_authors"
        ),
        InlineKeyboardButton(
            text="↩️ В главное меню",
            callback_data="back_to_main"
        )
    )
    builder.adjust(1)
    return builder.as_markup()