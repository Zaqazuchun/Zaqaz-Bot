import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db


# handlers import
from handlers import admin, products, orders
from handlers import admin, products, orders


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# register handlers
admin.register(dp)
products.register(dp)
orders.register(dp)
products.register(dp)
orders.register(dp)

async def main():
    await init_db()
    print("🚀 BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())