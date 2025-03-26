from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.config import BotData, MAX_MESSAGE_LENGTH
from bot.keyboards import (
    create_main_keyboard,
    create_authors_keyboard,
    create_reply_keyboard,
    create_back_to_authors_keyboard, create_welcome_keyboard
)
from bot.services.reporter import create_author_report
from bot.check_updates import check_updates
from aiogram.utils.markdown import hbold, hitalic
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    info_text = f"""
{hbold('🤖 Бот мониторинга изменений «Профи-Т»')}

{hbold('Проект:')} Кассовая программа «Профи-Т»
{hbold('Автор:')} Михаил Горчаков (@Mikdevops)
{hbold('Версия:')} 1.0
{hbold('GitHub:')} https://github.com/MikDeviOps
{hbold('GitHub-Project:')} https://github.com/MikDeviOps/Profit-T_Versions

{hbold('Основные возможности:')}
🔹 Автоматический мониторинг изменений
🔹 Отслеживание версий файлов конфигурации
🔹 История изменений по разработчикам

{hbold('Команды:')}
/start - Главное меню
/check - Проверить изменения
    """
    await message.answer(
        info_text,
        parse_mode='HTML',
        reply_markup=create_reply_keyboard()
    )


@router.message(Command("check"))
async def cmd_check(message: Message, bot: Bot):
    await message.answer("🔄 Проверяю изменения...", reply_markup=create_reply_keyboard())
    await check_updates(bot)


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


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def welcome_new_member(event: ChatMemberUpdated, bot: Bot):
    """Приветствие нового участника с большой кнопкой"""
    # Игнорируем, если это сам бот
    if event.new_chat_member.user.id == bot.id:
        return

    welcome_text = """
🎉 Добро пожаловать в группу мониторинга изменений «Профи-Т»!

Нажмите кнопку 🚀 СТАРТ ниже, чтобы начать работу.
    """

    await bot.send_message(
        chat_id=event.chat.id,
        text=welcome_text,
        reply_markup=create_welcome_keyboard()
    )


@router.message(F.text.in_(["🚀 СТАРТ", "/start"]))
async def cmd_start(message: Message, bot: Bot):
    """Обработчик большой кнопки СТАРТ и команды /start"""
    info_text = f"""
{hbold('🤖 Бот мониторинга изменений «Профи-Т»')}

{hbold('Проект:')} Кассовая программа «Профи-Т»
{hbold('Автор:')} Михаил Горчаков (@Mikdevops)
    """

    await message.answer(
        info_text,
        parse_mode='HTML',
        reply_markup=create_reply_keyboard()
    )

    # Показываем последние изменения
    await check_updates(bot)