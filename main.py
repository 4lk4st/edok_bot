import asyncio
import logging
import sys

from aiogram import types
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from create_bot import dp, bot



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


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
