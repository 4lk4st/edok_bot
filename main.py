import asyncio
import logging
import sys

from aiogram import types

from create_bot import dp, bot
from handlers import food, other


food.register_handlers_food(dp)
# other.register_handlers_other(dp)


async def main() -> None:
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
