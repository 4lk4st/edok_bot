import asyncio
import logging
import sys

from time import sleep

from create_bot import dp, bot
from handlers import food, other


async def main() -> None:
    try:
        dp.include_routers(food.router, other.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
