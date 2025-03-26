from datetime import datetime
from pathlib import Path
from bot.config import BotData, CHAT_ID, MAX_FILES_IN_SUMMARY
from bot.keyboards import create_main_keyboard


async def prepare_data(changes: list):
    """Подготавливает данные для отчетов"""
    BotData.current_authors_data = {}
    BotData.latest_changes = changes[-MAX_FILES_IN_SUMMARY:]

    for change in changes:
        author = change['author']
        if author not in BotData.current_authors_data:
            BotData.current_authors_data[author] = []
        BotData.current_authors_data[author].append(change)


async def create_author_report(author: str) -> str:
    """Генерирует отчет по конкретному автору"""
    if author not in BotData.current_authors_data:
        return f"Нет данных об авторе {author}"

    changes = BotData.current_authors_data[author]
    report_lines = [
        f"👤 <b>Автор:</b> {author}",
        f"📌 <b>Всего изменений:</b> {len(changes)}",
        f"🕒 <b>Последняя активность:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        ""
    ]

    for change in sorted(changes, key=lambda x: (x['date'], x['time']), reverse=True):
        file_path = Path(change['file'])
        report_lines.extend([
            f"📅 {change['date']} {change['time']}",
            f"📁 {file_path.parent}/<code>{file_path.name}</code> (v.{change['version']})",
            *[f"• {desc}" for desc in change['description'] if desc.strip()],
            ""
        ])

    return "\n".join(report_lines)


async def send_report(bot, changes: list, filename: str):
    """Отправляет отчет об изменениях"""
    await prepare_data(changes)

    if not changes:
        await bot.send_message(
            CHAT_ID,
            "ℹ️ Нет данных об изменениях",
            reply_markup=create_main_keyboard()
        )
        return

    unique_files = list({
        f"{Path(change['file']).parent}/<code>{Path(change['file']).name}</code> (v.{change['version']})"
        for change in BotData.latest_changes
    })

    message = [
        f"📅 <b>Последние изменения</b> ({filename})",
        f"🕒 <b>Актуально на:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        "",
        "<b>Доработки:</b>",
        *unique_files[:MAX_FILES_IN_SUMMARY],
        "",
        f"👥 <b>Разработчиков:</b> {len(BotData.current_authors_data)}"
    ]

    if len(unique_files) > MAX_FILES_IN_SUMMARY:
        message.insert(-2, f"\n...и ещё {len(unique_files) - MAX_FILES_IN_SUMMARY} изменений")

    await bot.send_message(
        CHAT_ID,
        "\n".join(message),
        parse_mode='HTML',
        reply_markup=create_main_keyboard()
    )