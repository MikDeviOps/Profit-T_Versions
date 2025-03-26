from pathlib import Path
from typing import Optional
from bot.config import LOG_FOLDER

def get_latest_history_file(folder_path: Path = None) -> Optional[Path]:
    """Находит самый свежий файл истории"""
    search_folder = folder_path or LOG_FOLDER
    try:
        return max(
            search_folder.glob('history*.txt'),
            key=lambda f: f.stat().st_mtime,
            default=None
        )
    except Exception as e:
        print(f"Ошибка поиска файла: {e}")
        return None