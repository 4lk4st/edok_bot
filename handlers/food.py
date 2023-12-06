from aiogram import types, Dispatcher, Bot
from aiogram.utils.markdown import hbold

from keyboards import user_keyboard


async def command_start(
    message: types.Message,
) -> None:
    """
    Обработчик команды `/start`
    """
    await message.answer("Чтобы сделать заказ, выбери блюдо!",
                         reply_markup=user_keyboard)


def register_handlers_food(dp: Dispatcher) -> None:
    dp.message.register(command_start)
