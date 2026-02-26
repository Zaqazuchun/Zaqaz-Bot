import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db

import handlers.admin
import handlers.products
import handlers.orders

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

handlers.admin.register(dp)
handlers.products.register(dp)
handlers.orders.register(dp)

async def main():
    await init_db()
    print("🚀 BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())