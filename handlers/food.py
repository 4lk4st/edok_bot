from aiogram import types, Dispatcher, Router
from aiogram.utils.markdown import hbold
from aiogram.filters.command import Command

from keyboards import user_keyboard


router = Router()

@router.message(Command("start"))
async def command_start(
    message: types.Message,
) -> None:
    await message.answer("Чтобы сделать заказ, выбери блюдо!",
                         reply_markup=user_keyboard)
