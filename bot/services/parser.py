import re
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ChangeLogParser:
    def __init__(self):
        self.changes: List[Dict] = []
        self._pattern = re.compile(
            r'^(\d{2}\.\d{2}\.\d{4})\s+'  # Дата
            r'(\d{2}:\d{2}:\d{2})\s+'  # Время
            r'\$/(.+?)\s+'  # Путь к файлу
            r'v\.(\d+)\s+'  # Версия
            r'\[([^]]+)\]'  # Автор
        )

    def parse_file(self, file_path: Path) -> List[Dict]:
        """Парсит файл истории изменений"""
        if not file_path.exists():
            logger.error(f"Файл не найден: {file_path}")
            return []

        encoding = self._detect_encoding(file_path)
        try:
            with file_path.open('r', encoding=encoding) as f:
                content = f.read()
                return self._parse_content(content)
        except Exception as e:
            logger.error(f"Ошибка чтения файла {file_path}: {e}")
            return []

    @staticmethod
    def _detect_encoding(file_path: Path) -> str:
        """Определяет кодировку файла"""
        encodings = ['utf-8', 'cp1251', 'windows-1251', 'iso-8859-1']
        for encoding in encodings:
            try:
                with file_path.open('r', encoding=encoding) as f:
                    f.read(1024)
                return encoding
            except UnicodeDecodeError:
                continue
        return 'utf-8'

    def _parse_content(self, content: str) -> List[Dict]: # Анализирует содержимое файла
        self.changes = []

        for line in content.splitlines():
            if cleaned_line := line.strip():
                self._process_line(cleaned_line)

        return self.changes

    def _process_line(self, line: str) -> None: # Обрабатывает строку лога
        if self._is_change_entry(line):
            self._parse_change_entry(line)
        elif self.changes and (desc := self._clean_description_line(line)):
            self.changes[-1]['description'].append(desc)

    def _is_change_entry(self, line: str) -> bool: # Проверяет, является ли строка записью об изменении
        return bool(self._pattern.match(line))

    def _parse_change_entry(self, line: str) -> None: # Извлекает данные об изменении
        if match := self._pattern.match(line):
            self.changes.append({
                'date': match.group(1),
                'time': match.group(2),
                'file': match.group(3),
                'version': match.group(4),
                'author': match.group(5),
                'description': []
            })

    @staticmethod
    def _clean_description_line(line: str) -> Optional[str]: # Очищает строку описания
        line = line.strip()
        if line.startswith('!--'):
            line = line[3:].strip()
        return line if line else None
