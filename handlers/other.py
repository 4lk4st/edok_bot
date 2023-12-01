from aiogram import types, Dispatcher

from create_bot import dp


async def echo_handler(message: types.Message) -> None:
    await message.answer("Писать мне текст бесполезно, я не отвечу =( "
                         "Пожалуйста, для выбора еды пользуйся кнопками")
    

def register_handlers_other(dp: Dispatcher) -> None:
    dp.register_message_handler(echo_handler)
