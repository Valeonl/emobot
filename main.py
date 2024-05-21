from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.handlers.basic import get_voice, get_text
from core.settings import settings
import asyncio
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

dp = Dispatcher()

async def start_bot(bot: Bot):
    """Функция отправки сообщения админу бота о его запуске"""
    await bot.send_message(settings.bots.admin_id, text="СмайлБот запущен")


async def stop_bot(bot: Bot):
    """Функция отправки сообщения админу бота о его остановке"""
    await bot.send_message(settings.bots.admin_id, text="СмайлБот отстановлен")

@dp.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    """Функция при отправке боту сообщения /start"""
    await message.reply(f"Привет, *{message.from_user.first_name}*\!\nОтправь любое голосовое сообщение и наш бот выполнит для него эмодзи-разметку\!")

async def start():
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    # Функция бота при его старте
    dp.startup.register(start_bot)
    # Функция бота при его остановке
    dp.shutdown.register(stop_bot)
    dp.message.register(get_voice, F.voice)
    # Функция бота при отправки ему текстового сообщения
    dp.message.register(get_text, F.text)
    try:
        print("Бот запущен")
        await dp.start_polling(bot)
    finally:
        print("Бот отстановлен")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
