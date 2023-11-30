import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv


from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    await message.answer("Выбери с помощью кнопок внизу, какую еду ты хочешь"
                         " заказать на сегодня!")

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types
    (like a text, photo, sticker etc.)
    """
    await message.answer("Писать мне текст бесполезно, я не отвечу =( "
                         "Пожалуйста, для выбора еды пользуйся кнопками")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
