import asyncio
from datetime import datetime, time, timedelta
from aiogram import Bot, Dispatcher
import pytz
from bot.config import TELEGRAM_TOKEN
from bot.routers import router


async def scheduled_evening_check(bot: Bot):
    """Ежедневная проверка в 22:30 по московскому времени"""
    timezone = pytz.timezone('Europe/Moscow')
    while True:
        now = datetime.now(timezone)
        target_time = time(22, 30)

        # Вычисляем время до следующей 22:30
        if now.time() > target_time:
            next_day = now.date() + timedelta(days=1)
            next_target = datetime.combine(next_day, target_time)
        else:
            next_target = datetime.combine(now.date(), target_time)

        wait_seconds = (next_target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        try:
            from bot.check_updates import check_updates
            await check_updates(bot)
            print(f"✅ Ежедневная проверка выполнена в {datetime.now(timezone).strftime('%d.%m.%Y %H:%M')}")
        except Exception as e:
            print(f"❌ Ошибка при ежедневной проверке: {e}")


async def main():
    """Точка входа"""
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Запускаем задачу для вечерней проверки
    asyncio.create_task(scheduled_evening_check(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    print("🤖 Бот запущен (проверка в 22:30)...")
    asyncio.run(main())