from pathlib import Path
from typing import Optional
from bot.config import LOG_FOLDER
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache(maxsize=10)
def get_latest_history_file(folder_path: Path = None) -> Optional[Path]:
    """Находит самый свежий файл истории с кэшированием"""
    search_folder = folder_path or LOG_FOLDER
    try:
        history_files = list(search_folder.glob('history*.txt'))
        if not history_files:
            logger.warning(f"Не найдено файлов истории в {search_folder}")
            return None
        return max(history_files, key=lambda f: f.stat().st_mtime)
    except Exception as e:
        logger.error(f"Ошибка поиска файла: {e}")
        return None