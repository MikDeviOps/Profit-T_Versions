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

# Настройки
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'TOKEN')
CHAT_ID = os.getenv('CHAT_ID', 'CHAT_ID')
WEB_VERSION_URL = os.getenv('WEB_VERSION_URL', 'https://your-site.com/history')
LOG_FOLDER = Path(os.getenv('LOG_FOLDER', 'G:/'))
MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4000'))
MAX_FILES_IN_SUMMARY = int(os.getenv('MAX_FILES_IN_SUMMARY', '100'))

# Создаем папку для логов если не существует
LOG_FOLDER.mkdir(parents=True, exist_ok=True)