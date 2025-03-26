import asyncio
from datetime import datetime, time, timedelta, timezone
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from bot.config import TELEGRAM_TOKEN, CHAT_ID
from bot.routers import router
from aiogram.utils.formatting import Text, Bold, Italic

# Конфигурация
CHECK_TIME = time(22, 30)  # Время ежедневной проверки
MOSCOW_TZ = timezone(timedelta(hours=3))  # Часовой пояс Москвы
UPDATE_INTERVAL = 3600  # Интервал обновления статуса (1 час)
MAX_RETRIES = 5  # Максимальное количество попыток переподключения
RETRY_DELAY = 5  # Задержка между попытками (в секундах)


class StatusMessage:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.message_id = None
        self.last_check_time = None

    async def update_status(self, retry_count=0):
        """Обновляет статусное сообщение с обработкой ошибок"""
        try:
            now = datetime.now(MOSCOW_TZ)

            if now.time() > CHECK_TIME:
                next_check = datetime.combine(now.date() + timedelta(days=1), CHECK_TIME, tzinfo=MOSCOW_TZ)
            else:
                next_check = datetime.combine(now.date(), CHECK_TIME, tzinfo=MOSCOW_TZ)

            time_left = next_check - now
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes = remainder // 60

            text = Text(
                Bold("🤖 Бот мониторинга изменений Профи-Т\n"),
                f"🔄 Последняя проверка: {self.last_check_time or 'еще не выполнялась'}\n",
                f"⏳ Следующая проверка через: ",
                Bold(f"{time_left.days}д {hours}ч {minutes}м\n"),
                f"🕒 Будет выполнена: ",
                Italic(next_check.strftime('%d.%m.%Y в %H:%M')),
                "\n\n",
                Italic("(сообщение обновляется автоматически)")
            )

            if self.message_id:
                await self.bot.edit_message_text(
                    chat_id=CHAT_ID,
                    message_id=self.message_id,
                    text=text.as_markdown(),
                    parse_mode="Markdown"
                )
            else:
                msg = await self.bot.send_message(
                    CHAT_ID,
                    text.as_markdown(),
                    parse_mode="Markdown"
                )
                self.message_id = msg.message_id

        except TelegramNetworkError as e:
            if retry_count < MAX_RETRIES:
                print(f"⚠️ Ошибка сети (попытка {retry_count + 1}/{MAX_RETRIES}): {e}")
                await asyncio.sleep(RETRY_DELAY)
                return await self.update_status(retry_count + 1)
            raise
        except Exception as e:
            print(f"❌ Ошибка обновления статуса: {e}")


async def safe_check_updates(bot: Bot):
    """Безопасное выполнение проверки обновлений"""
    for attempt in range(MAX_RETRIES):
        try:
            from bot.check_updates import check_updates
            await check_updates(bot)
            return True
        except TelegramNetworkError as e:
            wait_time = (attempt + 1) * RETRY_DELAY
            print(f"⚠️ Ошибка сети при проверке (попытка {attempt + 1}/{MAX_RETRIES}): {e}")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"❌ Ошибка при проверке: {e}")
            await bot.send_message(CHAT_ID, f"❌ Ошибка проверки: {str(e)[:1000]}")
            return False
    return False


async def scheduled_evening_check(bot: Bot, status_msg: StatusMessage):
    """Ежедневная проверка с улучшенной обработкой ошибок"""
    while True:
        try:
            now = datetime.now(MOSCOW_TZ)

            if now.time() > CHECK_TIME:
                next_check = datetime.combine(now.date() + timedelta(days=1), CHECK_TIME, tzinfo=MOSCOW_TZ)
            else:
                next_check = datetime.combine(now.date(), CHECK_TIME, tzinfo=MOSCOW_TZ)

            wait_seconds = (next_check - now).total_seconds()

            # Динамическое обновление статуса
            while wait_seconds > 0:
                await status_msg.update_status()
                sleep_time = min(UPDATE_INTERVAL, wait_seconds)
                await asyncio.sleep(sleep_time)
                wait_seconds -= sleep_time

            # Выполнение проверки
            status_msg.last_check_time = datetime.now(MOSCOW_TZ).strftime('%d.%m.%Y %H:%M')
            if await safe_check_updates(bot):
                print(f"✅ Проверка выполнена в {status_msg.last_check_time}")
            await status_msg.update_status()

        except Exception as e:
            print(f"🔴 Критическая ошибка в scheduled_evening_check: {e}")
            await asyncio.sleep(RETRY_DELAY * 2)


async def main():
    """Точка входа с обработкой ошибок запуска"""
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            bot = Bot(token=TELEGRAM_TOKEN)
            dp = Dispatcher()
            dp.include_router(router)

            status_msg = StatusMessage(bot)
            await status_msg.update_status()

            asyncio.create_task(scheduled_evening_check(bot, status_msg))

            await dp.start_polling(bot)
            break

        except TelegramNetworkError as e:
            retry_count += 1
            print(f"⚠️ Ошибка сети при запуске (попытка {retry_count}/{MAX_RETRIES}): {e}")
            await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"🔴 Критическая ошибка: {e}")
            break
        finally:
            if 'bot' in locals():
                await bot.session.close()


if __name__ == "__main__":
    print("🤖 Бот запущен с улучшенной обработкой ошибок...")
    asyncio.run(main())