import asyncio
from aiogram import Bot, Dispatcher
from bot.config import TELEGRAM_TOKEN
from bot.routers import router


async def scheduled_checker(bot: Bot):
    """Фоновая проверка изменений"""
    while True:
        try:
            from bot.check_updates import check_updates
            await check_updates(bot)
        except Exception as e:
            print(f"Ошибка проверки: {e}")
        await asyncio.sleep(3600)


async def main():
    """Точка входа"""
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(scheduled_checker(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    print("🤖 Бот запущен...")
    asyncio.run(main())