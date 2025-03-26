import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class BotData:
    """Класс для хранения состояния бота"""
    current_authors_data = {}
    latest_changes = []
    WELCOME_MESSAGE = """
🎉 Добро пожаловать в группу мониторинга изменений «Профи-Т»!

Нажмите кнопку 🚀 СТАРТ ниже, чтобы начать работу.
    """

# Основные настройки
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("Токен бота не указан в .env файле")

CHAT_ID = os.getenv('CHAT_ID')
if not CHAT_ID:
    raise ValueError("Chat ID не указан в .env файле")

LOG_FOLDER = Path(os.getenv('LOG_FOLDER'))
if not LOG_FOLDER.exists():
    try:
        LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Не удалось создать/достучаться до папки логов: {e}")

WEB_VERSION_URL = os.getenv('WEB_VERSION_URL', '')
MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4000'))
MAX_FILES_IN_SUMMARY = int(os.getenv('MAX_FILES_IN_SUMMARY', '100'))