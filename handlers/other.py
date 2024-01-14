from aiogram import types, Router, F
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards import start_keyboard
from create_bot import bot


router = Router()

@router.message(CommandStart())
async def command_start(
    message: types.Message,
    state: FSMContext
) -> None:
    await state.clear()
    await state.update_data(
        {"current_section": "",
         "current_price": 0}
    )

    await message.answer("Привет! Ты можешь посмотреть меню или сделать заказ!",
                         reply_markup=start_keyboard)


@router.message(F.text.lower() == "выслать меню")
async def send_menu(
    message: types.Message,
) -> None:
    document = types.FSInputFile("data/menu_example.pdf", filename="menu.pdf")
    await bot.send_document(chat_id=message.chat.id, document=document)
    await message.answer("Вот актуальное меню!",
                         reply_markup=start_keyboard)


@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    await message.answer("Писать мне текст бесполезно, я не отвечу =( "
                         "Пожалуйста, для выбора еды пользуйся кнопками")
