from pathlib import Path
from aiogram import Bot
from bot.config import LOG_FOLDER, CHAT_ID
from bot.keyboards import create_main_keyboard
from bot.services.parser import ChangeLogParser
from bot.services.reporter import send_report
from bot.services.utils import get_latest_history_file
import logging

logger = logging.getLogger(__name__)

async def check_updates(bot: Bot):
    """Проверка и отправка обновлений"""
    try:
        latest_file = get_latest_history_file(LOG_FOLDER)
        if not latest_file:
            await bot.send_message(
                CHAT_ID,
                "⚠️ Файл изменений не найден",
                reply_markup=create_main_keyboard()
            )
            return

        parser = ChangeLogParser()
        changes = parser.parse_file(latest_file)
        await send_report(bot, changes, latest_file.name)

    except Exception as e:
        logger.error(f"Ошибка при проверке обновлений: {e}")
        await bot.send_message(
            CHAT_ID,
            f"❌ Ошибка при проверке обновлений: {str(e)}",
            reply_markup=create_main_keyboard()
        )