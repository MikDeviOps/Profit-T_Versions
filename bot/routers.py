from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from bot.config import BotData, MAX_MESSAGE_LENGTH
from bot.keyboards import (
    create_main_keyboard,
    create_authors_keyboard,
    create_back_to_authors_keyboard
)
from bot.services.reporter import create_author_report
from bot.check_updates import check_updates
from aiogram.utils.markdown import hbold

router = Router()

def get_start_keyboard():
    """Reply-клавиатура для команды /start"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Запрос обновления")],
            [KeyboardButton(text="Показать меню")]
        ],
        resize_keyboard=True,
        selective=True
    )

@router.message(Command("start"))
async def cmd_start(message: Message):
    info_text = f"""
{hbold('🤖 Бот мониторинга изменений «Профи-Т»')}

{hbold('Проект:')} Кассовая программа «Профи-Т»
{hbold('Автор:')} Михаил Горчаков (@Mikdevops)
{hbold('Версия:')} 1.1 - 28.03.2025
{hbold('GitHub:')} https://github.com/MikDeviOps
{hbold('GitHub-Project:')} https://github.com/MikDeviOps/Profit-T_Versions
    """
    await message.answer(
        info_text,
        parse_mode='HTML',
        reply_markup=get_start_keyboard()
    )

@router.message(F.text == "Запрос обновления")
async def request_update(message: Message, bot: Bot):
    await message.answer(
        "🔄 Проверяю изменения...",
        reply_markup=ReplyKeyboardRemove()
    )
    await check_updates(bot)
    await message.answer(
        "Главное меню:",
        reply_markup=create_main_keyboard()
    )

@router.message(F.text == "Показать меню")
async def show_menu(message: Message):
    await message.answer(
        "Скрываю клавиатуру...",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Главное меню:",
        reply_markup=create_main_keyboard()
    )

@router.message(Command("check"))
async def cmd_check(message: Message, bot: Bot):
    await message.answer(
        "🔄 Проверяю изменения...",
        reply_markup=ReplyKeyboardRemove()
    )
    await check_updates(bot)
    await message.answer(
        "Главное меню:",
        reply_markup=create_main_keyboard()
    )

@router.callback_query(F.data == "refresh")
async def callback_refresh(callback: CallbackQuery, bot: Bot):
    await callback.answer("Обновление данных...")
    await check_updates(bot)

@router.callback_query(F.data == "show_authors")
async def callback_show_authors(callback: CallbackQuery):
    if not BotData.current_authors_data:
        await callback.answer("Нет данных об авторах", show_alert=True)
        return
    await callback.answer()
    await callback.message.edit_text(
        "👥 Выберите автора:",
        reply_markup=create_authors_keyboard(BotData.current_authors_data.keys())
    )

@router.callback_query(F.data.startswith("author_"))
async def callback_show_author(callback: CallbackQuery):
    author = callback.data.split("_")[1]
    report = await create_author_report(author)

    if len(report) > MAX_MESSAGE_LENGTH:
        parts = [report[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(report), MAX_MESSAGE_LENGTH)]
        await callback.message.edit_text(
            parts[0],
            parse_mode='HTML',
            reply_markup=create_back_to_authors_keyboard()
        )
        for part in parts[1:]:
            await callback.message.answer(part, parse_mode='HTML')
    else:
        await callback.message.edit_text(
            report,
            parse_mode='HTML',
            reply_markup=create_back_to_authors_keyboard()
        )
    await callback.answer()

@router.callback_query(F.data == "back_to_authors")
async def callback_back_to_authors(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "👥 Выберите автора:",
        reply_markup=create_authors_keyboard(BotData.current_authors_data.keys())
    )

@router.callback_query(F.data == "back_to_main")
async def callback_back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Главное меню:",

        reply_markup=create_main_keyboard()
    )