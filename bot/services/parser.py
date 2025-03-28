import re
from pathlib import Path
from typing import List, Dict, Optional, Union
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class ChangeLogParser:
    _CHANGE_ENTRY_PATTERN = re.compile(
        r'^(\d{2}\.\d{2}\.\d{4})\s+'  # Дата
        r'(\d{2}:\d{2}:\d{2})\s+'  # Время
        r'\$/(.+?)\s+'  # Путь к файлу
        r'v\.(\d+)\s+'  # Версия
        r'\[([^]]+)]'  # Автор
    )

    def __init__(self):
        self.changes: List[Dict[str, Union[str, List[str]]]] = []

    def parse_file(self, file_path: Path) -> List[Dict[str, Union[str, List[str]]]]:
        """Парсит файл истории изменений"""
        if not file_path.exists():
            logger.error(f"Файл не найден: {file_path}")
            return []

        try:
            with file_path.open('r', encoding=self._detect_encoding(file_path)) as f:
                return self._parse_content(f.read())
        except Exception as e:
            logger.error(f"Ошибка чтения файла {file_path}: {e}")
            return []

    @staticmethod
    @lru_cache(maxsize=10)
    def _detect_encoding(file_path: Path) -> str:
        """Определяет кодировку файла с кэшированием"""
        encodings = ['utf-8', 'cp1251', 'windows-1251', 'iso-8859-1']
        for encoding in encodings:
            try:
                with file_path.open('r', encoding=encoding) as f:
                    f.read(1024)
                return encoding
            except UnicodeDecodeError:
                continue
        return 'utf-8'

    def _parse_content(self, content: str) -> List[Dict[str, Union[str, List[str]]]]:
        """Анализирует содержимое файла"""
        self.changes = []
        for line in content.splitlines():
            if line := line.strip():
                self._process_line(line)
        return self.changes

    def _process_line(self, line: str) -> None:
        """Обрабатывает строку лога"""
        if match := self._CHANGE_ENTRY_PATTERN.match(line):
            self._add_change_entry(match)
        elif self.changes:
            if desc := self._clean_description_line(line):
                # Безопасное добавление описания
                last_change = self.changes[-1]
                if isinstance(last_change['description'], list):
                    last_change['description'].append(desc)
                else:
                    last_change['description'] = [desc]

    def _add_change_entry(self, match: re.Match) -> None:
        """Добавляет запись об изменении"""
        self.changes.append({
            'date': match.group(1),
            'time': match.group(2),
            'file': match.group(3),
            'version': match.group(4),
            'author': match.group(5),
            'description': []  # Гарантированно список
        })

    @staticmethod
    def _clean_description_line(line: str) -> Optional[str]:
        """Очищает строку описания"""
        if line.startswith('!--'):
            line = line[3:].strip()
        return line if line else None