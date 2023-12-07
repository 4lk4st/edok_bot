from aiogram import types, Router, F

from create_bot import dp


router = Router()

@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    await message.answer("Писать мне текст бесполезно, я не отвечу =( "
                         "Пожалуйста, для выбора еды пользуйся кнопками")
