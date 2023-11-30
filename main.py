import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv


from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    Обработчик команды `/start`
    """
    kb = [
        [
            types.KeyboardButton(text="Салаты"),
            types.KeyboardButton(text="Каши")
        ],
        [
            types.KeyboardButton(text="Вторые блюда"),
            types.KeyboardButton(text="Выпечка")
        ],
        [
            types.KeyboardButton(text="Напитки и десерты")
        ],
    ]
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел меню"
    )

    await message.answer(f"Добрый день, {hbold(message.from_user.full_name)}!")
    await message.answer("Чтобы сделать заказ, сначала выберите раздел меню, "
                         "а затем выберите нужное Вам блюдо!",
                         reply_markup=keyboard)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer("Писать мне текст бесполезно, я не отвечу =( "
                         "Пожалуйста, для выбора еды пользуйся кнопками")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
